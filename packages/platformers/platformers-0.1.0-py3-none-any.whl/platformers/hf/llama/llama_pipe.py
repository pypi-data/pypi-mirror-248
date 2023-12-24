from platform import release
from typing import Any, Dict
import torch.distributed as dist

from .llama import (
    LlamaPreTrainedModel,
    Embedding,
    gpt2_attention_mask_func,
    expand_attention_types,
    ParallelLinear,
    LlamaForCausalLM,
    LlamaForRM,
)
from optimus.model.transformer import (
    ParallelTransformerLayer,
)
import torch
import torch.nn as nn

from optimus.model.norms import get_norm
from optimus.model.init_functions import get_init_methods
from optimus.utils import release_cuda, gather_object

from optimus import mpu

# Pipeline parallelism
from deepspeed.pipe import PipelineModule, LayerSpec
import numpy
from optimus.utils.tree import broadcast_tree, send_tree, recv_tree, PipeMeta
import torch.distributed as dist
from collections import OrderedDict
from pathlib import Path
import logging

from torch.utils.checkpoint import checkpoint
from accelerate import init_empty_weights

# NOTE: Convention:
# 1. right padding
# 2. tuple input
# 3. only in first layer and last layer, attention mask is [batch_size, seq_len], other layer is upper triangle matrix
# 4. loss should be determined by a `loss layer`, when last layer is causal, return logits; rm return values

# NOTE: This version of pipeline module is trivial and does not support generation
# TODO: Add support for generation by _PipeGenerationMixin


class CheckpointMixin:
    checkpoint = False


class FlashAttentionMixin:
    flash_attention = True


class LlamaPreTrainedModelPipe(LlamaPreTrainedModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pipe_meta = PipeMeta.from_mpu(mpu)
        # note that mpu is sigleton, so this is fine
        # if we change mpu by mpu(0) or mpu(1), mpu method will be changed also, so it's ok
        # just ensure that using and init using the same mpu state

    def _validate_model_class(self, *args, **kwargs):
        pass

    def _validate_model_kwargs(self, *args, **kwargs):
        pass

    def checkpoint_enabled(self, b=True):
        for layer in self.children():
            if isinstance(layer, CheckpointMixin):
                layer.checkpoint = b

    def flash_attention_enabled(self, b=True):
        for layer in self.children():
            if isinstance(layer, FlashAttentionMixin):
                layer.transformer_layer.attention.use_flash_attention = b

    @classmethod
    def from_mp_pretrained(cls, *args, **kwargs):
        cls_name = cls.__name__
        if "CausalLM" in cls_name:
            MPClass = LlamaForCausalLM
        elif "RM" in cls_name:
            MPClass = LlamaForRM
        else:
            raise NotImplementedError(
                f"Only support LlamaForCausalLMPipe and LlamaForRMPipe, got {cls}"
            )

        """
        Param Filter
        """
        save_pp_dir = kwargs.pop("save_pp_dir", None)
        topo = kwargs.pop("topo")
        loss_fn = kwargs.pop("loss_fn")
        activation_checkpoint_interval = kwargs.pop("activation_checkpoint_interval", 0)
        pipe_model = cls.from_pretrained(
            *args,
            topo=topo,
            loss_fn=loss_fn,
            activation_checkpoint_interval=activation_checkpoint_interval,
            **kwargs,
        )
        pipe_model.cpu().eval()
        release_cuda()

        model = MPClass.from_pretrained(*args, device_map="cpu", **kwargs)
        model_state_dict = model.state_dict()
        new_model_state_dict = OrderedDict()
        for k, v in model_state_dict.items():
            if "inv_freq" not in k:
                new_model_state_dict[k] = v
        parameters = list(new_model_state_dict.values())

        pipe_sd = pipe_model.state_dict()
        pipe_meta = pipe_model.pipe_meta
        length = len(pipe_sd)
        rank = mpu.get_pipe_parallel_rank()
        group_length = [0] + gather_object(length, group=pipe_meta.group)
        group_accum_length = numpy.cumsum(
            numpy.asarray(group_length, dtype=numpy.int64)
        )
        release_cuda()

        param_start = group_accum_length[rank]
        param_end = group_accum_length[rank + 1]
        pipe_sd_keys = list(pipe_sd.keys())
        new_pipe_sd = OrderedDict()
        for i, param in enumerate(parameters[param_start:param_end]):
            new_pipe_sd[pipe_sd_keys[i]] = param

        pipe_model.load_state_dict(new_pipe_sd)
        pipe_model.cuda()
        if save_pp_dir is not None:
            mp_rank = mpu.get_model_parallel_rank()
            pp_rank = mpu.get_pipe_parallel_rank()
            if mpu.get_data_parallel_rank() == 0:
                logging.warning("SAVING PIPELINE MODEL")
                save_pp_dir = Path(save_pp_dir) / f"mp_{mp_rank}_pp_{pp_rank}"
                save_pp_dir.mkdir(parents=True, exist_ok=True)
                # pipe_model.save_pretrained(save_pp_dir)
                torch.save(pipe_model.state_dict(), save_pp_dir / "pytorch_model.bin")
                pipe_model.config.save_pretrained(save_pp_dir)
        release_cuda()
        dist.barrier()
        return pipe_model

    def pipe_forward(self, *args, **kwargs):
        """
        Trivial sync method for pipeline parallelism
        Use for validating the weight
        """
        if self.pipe_meta.is_first_stage:
            hidden = self(*args, **kwargs)
            send_tree(hidden, self.pipe_meta.next_stage, self.pipe_meta.group)
            hidden = None
        elif self.pipe_meta.is_middle_stage:
            hidden = recv_tree(self.pipe_meta.prev_stage, self.pipe_meta.group)
            hidden = self(hidden)
            send_tree(hidden, self.pipe_meta.next_stage, self.pipe_meta.group)
            hidden = None
        else:
            hidden = recv_tree(self.pipe_meta.prev_stage, self.pipe_meta.group)
            hidden = self(hidden)
            hidden = mpu.mappings.gather_from_model_parallel_region(hidden)

        hidden = broadcast_tree(hidden, self.pipe_meta.last_rank, self.pipe_meta.group)
        return hidden


class LlamaInputLayer(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_method, self.output_layer_init_method = get_init_methods(config)
        config.attention_config = expand_attention_types(
            config.attention_config, config.num_hidden_layers
        )
        self.embed_in = Embedding(
            config,
            config.hidden_size,
            config.vocab_size,
            config.max_position_embeddings,
            config.hidden_dropout,
            self.init_method,
            num_tokentypes=0,
        )

    def forward(self, inputs):
        if isinstance(inputs, tuple):
            input_ids, attention_mask = inputs
        else:
            raise NotImplementedError("Only support tuple input now")

        batch_size, seq_length = input_ids.size()

        # position_ids
        position_ids = torch.arange(
            0,
            seq_length,
            dtype=torch.long,
            device=input_ids.device,
        )
        position_ids = position_ids.unsqueeze(0).view(-1, seq_length)

        # Embedding.
        attention_mask_raw = attention_mask.view(batch_size, -1).clone()
        attention_mask = attention_mask[:, None, None, :]
        tril_mask = torch.tril(
            torch.ones((1, seq_length, seq_length), device=attention_mask.device)
        ).view(1, 1, seq_length, seq_length)
        attention_mask = attention_mask * tril_mask
        attention_mask = attention_mask < 0.5
        tril_mask = attention_mask

        hidden_states = self.embed_in(input_ids, position_ids=position_ids)
        hidden_states = hidden_states.transpose(0, 1).contiguous()

        # attention_mask [b, s]
        # when use pipeline parallelism, we always use flash attention
        # so we dont need a tril attention mask
        return hidden_states, attention_mask_raw, tril_mask


class LlamaLayer(nn.Module, CheckpointMixin, FlashAttentionMixin):
    def __init__(self, config, i):
        super().__init__()
        self.config = config
        self.i = i
        self.init_method, self.output_layer_init_method = get_init_methods(config)
        is_rotary = config.pos_emb == "rotary"
        self.transformer_layer = ParallelTransformerLayer(
            config,
            attention_mask_func=gpt2_attention_mask_func,
            init_method=self.init_method,
            output_layer_init_method=self.output_layer_init_method,
            layer_number=i,
            rpe=None,
            rotary=is_rotary,
        )

    def forward(self, inputs):
        # hidden_states, attention_mask = inputs[0], inputs[2]
        hidden_states, attention_mask, tril_mask = inputs
        if self.checkpoint:
            hidden_states = checkpoint(self.transformer_layer, hidden_states, tril_mask)
        else:
            hidden_states = self.transformer_layer(hidden_states, tril_mask)
        return hidden_states, attention_mask, tril_mask


def last_pooling(hidden_states, attention_mask):
    last_index = attention_mask.cumsum(dim=1).argmax(dim=1)
    last_hidden_states = hidden_states.gather(
        1, last_index.view(-1, 1, 1).expand(-1, 1, hidden_states.size(-1))
    ).squeeze(1)
    return last_hidden_states


class LlamaLastLayer(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        norm, eps = get_norm(config)
        self.final_layer_norm = norm(config.hidden_size, eps=eps)

    def forward(self, inputs):
        hidden_states, attention_mask, _ = inputs
        hidden_states = hidden_states.transpose(0, 1).contiguous()
        hidden_states = self.final_layer_norm(hidden_states)
        return hidden_states, attention_mask  # [b, s]


class LlamaRewardLayer(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.mp_size = mpu.get_model_parallel_world_size()
        self.value_head = mpu.ColumnParallelLinear(
            config,
            config.hidden_size,
            self.mp_size,
            bias=False,
            gather_output=True,
        )

    def forward(self, inputs):
        hidden_states, attention_mask = inputs
        hidden_states = last_pooling(hidden_states, attention_mask)
        values, _ = self.value_head(hidden_states)
        values = values.mean(dim=-1)  # (b,)
        return values


class LlamaCausalLayer(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_method, self.output_layer_init_method = get_init_methods(config)
        self.embed_out = ParallelLinear(
            self.config,
            init_method=self.init_method,
            parallel_output=True,
        )

    def forward(self, inputs):
        hidden_states, _ = inputs
        logits, _ = self.embed_out(hidden_states)  # [b, s, v]
        return logits


def vanilla_causal_loss(logits, batch_args):
    # logits: [b, s, v]
    # loss_mask: [b, s] note that we can use loss mask instead of attention mask
    inputs_ids, loss_mask = batch_args
    shift_logits = logits[..., :-1, :].contiguous()
    shift_labels = inputs_ids[..., 1:].contiguous()
    loss_mask = loss_mask[..., :-1].contiguous().view(-1)
    loss = mpu.vocab_parallel_cross_entropy(
        shift_logits.view(-1, shift_logits.size(-1)),
        shift_labels.view(-1),
    )
    loss = (loss * loss_mask).sum() / loss_mask.sum()
    return loss


def create_llama_model_layer_spec(model_config):
    specs = [
        LayerSpec(LlamaInputLayer, model_config),
        *[
            LayerSpec(LlamaLayer, model_config, i)
            for i in range(model_config.num_hidden_layers)
        ],
        LayerSpec(LlamaLastLayer, model_config),
    ]
    return specs


def create_llama_rm_layer_spec(model_config):
    specs = create_llama_model_layer_spec(model_config)
    specs.append(LayerSpec(LlamaRewardLayer, model_config))
    return specs


def create_llama_causal_layer_spec(model_config):
    specs = create_llama_model_layer_spec(model_config)
    specs.append(LayerSpec(LlamaCausalLayer, model_config))
    return specs


class LlamaForRMPipe(PipelineModule, LlamaPreTrainedModelPipe):
    def __init__(self, config, topo, loss_fn, **kwargs):
        specs = create_llama_rm_layer_spec(config)
        assert loss_fn is not None
        super().__init__(
            layers=specs,
            topology=topo,
            loss_fn=loss_fn,
            config=config,
            **kwargs,
        )
        self.post_init()


class LlamaForCausalLMPipe(PipelineModule, LlamaPreTrainedModelPipe):
    def __init__(self, config, topo, loss_fn, **kwargs):
        specs = create_llama_causal_layer_spec(config)
        assert loss_fn is not None
        super().__init__(
            layers=specs,
            topology=topo,
            loss_fn=loss_fn,
            config=config,
            **kwargs,
        )
        self.post_init()
