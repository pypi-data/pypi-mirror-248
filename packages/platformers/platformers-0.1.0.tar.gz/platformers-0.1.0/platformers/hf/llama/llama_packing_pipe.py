import torch
from torch import nn
from torch.utils.checkpoint import checkpoint

# from transformers.utils import logging

from optimus import mpu
from optimus.model.init_functions import get_init_methods
from optimus.model.norms import get_norm
from optimus.model.transformer import ParallelLinear, ParallelTransformerLayer
from optimus.model.word_embeddings import Embedding
from optimus.hf.llama.llama_pipe import (
    expand_attention_types,
    gpt2_attention_mask_func,
    LlamaPreTrainedModelPipe,
    CheckpointMixin,
    FlashAttentionMixin,
    LayerSpec,
    PipelineModule,
)
from flash_attn.ops.triton.cross_entropy import (
    cross_entropy_loss as triton_cross_entropy,
)


class LlamaInputLayerPacking(nn.Module):
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
            input_ids, cu_seq_lens, cu_batch_size = inputs
        else:
            raise NotImplementedError("Only support tuple input now")
        hidden_states = self.embed_in(input_ids, position_ids=None)
        return hidden_states, cu_seq_lens, cu_batch_size


class LlamaLayerPacking(nn.Module, CheckpointMixin, FlashAttentionMixin):
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
            packing=True,
        )

    def forward(self, inputs):
        # hidden_states, attention_mask = inputs[0], inputs[2]
        hidden_states, _cu_seq_lens, cu_batch_size = inputs
        cu_seq_lens = _cu_seq_lens[:cu_batch_size]
        if self.checkpoint:
            hidden_states = checkpoint(
                self.transformer_layer, hidden_states, None, cu_seq_lens
            )
        else:
            hidden_states = self.transformer_layer(hidden_states, None, cu_seq_lens)
        return hidden_states, _cu_seq_lens, cu_batch_size


class LlamaLastLayerPacking(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        norm, eps = get_norm(config)
        self.final_layer_norm = norm(config.hidden_size, eps=eps)

    def forward(self, inputs):
        hidden_states, cu_seq_lens, cu_batch_size = inputs
        hidden_states = self.final_layer_norm(hidden_states)
        return hidden_states, cu_seq_lens, cu_batch_size


# NOTE: we use parallel output here to use parallel cross_entropy


class LlamaCausalLayerPacking(nn.Module):
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
        hidden_states, _, _ = inputs
        logits, _ = self.embed_out(hidden_states)
        return logits


def create_llama_model_layer_spec(model_config):
    specs = [
        LayerSpec(LlamaInputLayerPacking, model_config),
        *[
            LayerSpec(LlamaLayerPacking, model_config, i)
            for i in range(model_config.num_hidden_layers)
        ],
        LayerSpec(LlamaLastLayerPacking, model_config),
    ]
    return specs


def create_causal_spec(model_config):
    specs = create_llama_model_layer_spec(model_config)
    specs.append(LayerSpec(LlamaCausalLayerPacking, model_config))
    return specs


def vanilla_causal_loss_packing_with_parallel_logits(
    logits, data_args, ignore_index=-100
):
    labels, loss_mask = data_args  # same
    labels = torch.where(loss_mask.bool(), labels, ignore_index)
    loss = triton_cross_entropy(
        logits,
        labels,
        process_group=mpu.get_model_parallel_group(),
        ignored_index=ignore_index,
    )
    loss = loss.sum() / loss_mask.sum()
    return loss


def vanilla_causal_loss_packing(logits, data_args):
    labels, loss_mask = data_args  # same
    loss = torch.nn.functional.cross_entropy(
        logits,
        labels,
        reduction="none",
    )
    loss = (loss * loss_mask).sum() / loss_mask.sum()
    return loss


class LlamaForCausalLMPipePacking(PipelineModule, LlamaPreTrainedModelPipe):
    def __init__(self, config, topo, loss_fn, **kwargs):
        specs = create_causal_spec(config)
        assert loss_fn is not None
        super().__init__(
            layers=specs,
            topology=topo,
            loss_fn=loss_fn,
            config=config,
            **kwargs,
        )
        self.post_init()
