from typing import Optional, Tuple, Union, List
import gc

import torch
from torch import nn
from torch.utils.checkpoint import checkpoint
from torch.nn import CrossEntropyLoss
from transformers.configuration_utils import PretrainedConfig
from transformers.modeling_outputs import (
    BaseModelOutputWithPast,
    CausalLMOutputWithPast,
    BaseModelOutputWithNoAttention,
)
from transformers.modeling_utils import PreTrainedModel

# from transformers.utils import logging
import logging

from optimus import mpu
from optimus.model.activations import get_activation
from optimus.model.init_functions import get_init_methods
from optimus.model.norms import get_norm
from optimus.model.utils import get_fusion_type
from optimus.model.transformer import ParallelLinear, ParallelTransformerLayer
from optimus.model.word_embeddings import Embedding
from optimus.model.fused_softmax import FusedScaleMaskSoftmax
from optimus.generator.generator import Generator
from functools import partial
from optimus.model.init_functions import (
    wang_init_method,
    small_init_init_method,
    init_method_normal,
)
from transformers.generation.utils import (
    LogitsProcessorList,
    StoppingCriteriaList,
    validate_stopping_criteria,
    # validate_torch_generate_args,
)


class UnimcConfig(PretrainedConfig):
    model_type = "unimc"

    def __init__(
        self,
        vocab_size=39424,
        hidden_size=2048,
        num_hidden_layers=24,
        num_attention_heads=16,
        intermediate_size=8192,
        pos_emb="rotary",
        hidden_act="silu",
        rotary_pct=1,
        rotary_emb_base=10000,
        max_position_embeddings=4096,
        initializer_range=0.02,
        rms_norm_epsilon=1.0e-6,
        layernorm_epsilon=1.0e-12,
        tie_word_embeddings=False,
        use_parallel_residual=True,
        torch_dtype="bfloat16",
        init_method="small_init",
        output_layer_init_method="wang_init",
        mlp_type="llama",
        hidden_dropout=0.1,
        attention_dropout=0.1,
        norm="rmsnorm",
        type_vocab_size=2,
        **kwargs,
    ):
        self.vocab_size = vocab_size
        self.max_position_embeddings = max_position_embeddings
        self.hidden_size = hidden_size
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads
        self.intermediate_size = intermediate_size
        self.hidden_act = hidden_act
        self.rotary_pct = rotary_pct
        self.rotary_emb_base = rotary_emb_base
        self.initializer_range = initializer_range
        self.rms_norm_epsilon = rms_norm_epsilon
        self.tie_word_embeddings = tie_word_embeddings
        self.use_parallel_residual = use_parallel_residual
        self.torch_dtype = torch_dtype
        self.pos_emb = pos_emb
        self.init_method = init_method
        self.mlp_type = mlp_type
        self.output_layer_init_method = output_layer_init_method
        self.hidden_dropout = hidden_dropout
        self.norm = norm
        self.type_vocab_size = type_vocab_size
        self.attention_dropout = attention_dropout
        self.layernorm_epsilon = layernorm_epsilon
        self.init_epilogue()
        super().__init__(
            tie_word_embeddings=tie_word_embeddings,
            **kwargs,
        )

    def init_epilogue(self):
        self.num_layers = self.num_hidden_layers
        self.use_mup = False
        self.use_cpu_initialization = False
        self.precision = "fp16" if self.torch_dtype == "float16" else "bfloat16"
        self.use_flash_attention = True

        self.init_method_std = self.initializer_range

        self.attention_config = ["flash"]
        self.is_causal = False  # force
        self.padded_vocab_size = self.vocab_size
        self.use_cache = False

        self.isGQA = getattr(self, "isGQA", False)
        self.activation = getattr(self, "hidden_act", "silu")
        self.opt_pos_emb_offset = getattr(self, "opt_pos_emb_offset", False)
        self.gpt_j_residual = getattr(self, "gpt_j_residual", False)
        self.gpt_j_tied = getattr(self, "gpt_j_tied", False)
        self.attention_softmax_in_fp32 = getattr(
            self, "attention_softmax_in_fp32", False
        )
        self.bias_dropout_fusion = getattr(self, "bias_dropout_fusion", False)
        self.bias_gelu_fusion = getattr(self, "bias_gelu_fusion", False)
        self.apply_query_key_layer_scaling = getattr(
            self, "apply_query_key_layer_scaling", False
        )
        self.use_bias_in_attn_linear = getattr(self, "use_bias_in_attn_linear", False)
        self.scaled_upper_triang_masked_softmax_fusion = getattr(
            self, "scaled_upper_triang_masked_softmax_fusion", False
        )
        self.scaled_masked_softmax_fusion = getattr(
            self, "scaled_masked_softmax_fusion", True
        )
        self.onnx_safe = False

    @property
    def params_dtype(self):
        return torch.float16 if self.precision == "fp16" else torch.bfloat16

    def __getattr__(self, name):
        if "mup" in name or "bnb" in name:
            return None  # disable mup & bnb for now
        else:
            return object.__getattribute__(self, name)


def expand_attention_types(attention_config, num_layers):
    # if only strings are found in the config, we assume it's already expanded
    if (
        isinstance(attention_config, list)
        and len(attention_config) == 1
        and attention_config[0] == "flash"
    ):
        return ["flash" for _ in range(num_layers)]

    if all([isinstance(i, str) for i in attention_config]):
        return attention_config
    newlist = []

    for item in attention_config:
        # instead of specifying a number - we can specify 'all' to extend this pattern across all layers
        # if item[0] == "flash":
        #     return ["flash" for _ in range(num_layers)]

        if item[1] == "all":
            assert num_layers % len(item[0]) == 0, (
                f"Number of layers ({num_layers}) is not divisible by the length "
                f"of pattern: {item[0]}"
            )
            return item[0] * (num_layers // len(item[0]))
        for _ in range(item[1]):
            newlist.extend(item[0])
    return newlist


class UnimcPreTrainedModel(PreTrainedModel):
    """
    An abstract class to handle weights initialization and a simple interface for downloading and loading pretrained
    models.
    """

    config_class = UnimcConfig
    base_model_prefix = "unimc"
    supports_gradient_checkpointing = True

    def _init_weights(self, module):
        """Initialize the weights"""
        pass

    def _set_gradient_checkpointing(self, module, value=False):
        if isinstance(module, UnimcPreTrainedModel):
            module.gradient_checkpointing = value

    def checkpoint_enabled(self, b=True):
        for module in self.children():
            if isinstance(module, UnimcPreTrainedModel):
                module.gradient_checkpointing = b

    def post_init(self):
        # NOTE: we dont need gradient checkpointing
        # self.apply(self._set_gradient_checkpointing, value=False)
        super().post_init()
        self.checkpoint_enabled()


class UnimcModel(UnimcPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        config.attention_config = expand_attention_types(
            config.attention_config, config.num_hidden_layers
        )
        is_rotary = config.pos_emb == "rotary"
        assert is_rotary, "We must use rotary position embeddings"
        assert not config.is_causal, "Unimc is not a causal model"
        self.config = config
        self.init_method, self.output_layer_init_method = get_init_methods(config)
        self.embed_in = Embedding(
            config,
            config.hidden_size,
            config.vocab_size,
            config.max_position_embeddings,
            config.hidden_dropout,
            self.init_method,
            num_tokentypes=getattr(config, "type_vocab_size", 0),
        )
        self.layers = nn.ModuleList(
            [
                # NOTE: we use flash attention for all layers
                ParallelTransformerLayer(
                    config,
                    attention_mask_func=None,
                    init_method=self.init_method,
                    output_layer_init_method=self.output_layer_init_method,
                    layer_number=i,
                    rpe=None,
                    rotary=is_rotary,
                    use_cache=config.use_cache,
                    packing=True,
                )
                for i in range(config.num_hidden_layers)
            ]
        )
        norm, eps = get_norm(config)
        self.final_layer_norm = norm(
            config.hidden_size, eps=eps, device="cuda", dtype=config.params_dtype
        )
        # self.gradient_checkpointing = True

        # in each of transformer layers, we have a fused softmax

        self.post_init()

    def get_input_embeddings(self):
        return self.embed_in

    def set_input_embeddings(self, value):
        self.embed_in = value

    def forward(
        self,
        input_ids: Optional[torch.LongTensor] = None,
        token_type_ids: Optional[torch.LongTensor] = None,
        cu_seq_len: Optional[torch.LongTensor] = None,
        output_hidden_states: Optional[bool] = None,
    ) -> BaseModelOutputWithNoAttention:
        # NOTE: we dont need attention_mask, position_ids, ...
        output_hidden_states = (
            output_hidden_states
            if output_hidden_states
            else self.config.output_hidden_states
        )

        all_hidden_states = () if output_hidden_states else None

        # Embedding (token type and input embeddings)
        hidden_states = self.embed_in(
            input_ids, position_ids=None, tokentype_ids=token_type_ids
        )  # [sq, h]

        for i in range(self.config.num_hidden_layers):
            layer = self.layers[i]
            if output_hidden_states:
                all_hidden_states = all_hidden_states + (hidden_states,)

            if self.gradient_checkpointing:
                hidden_states = checkpoint(layer, hidden_states, None, cu_seq_len)
            else:
                hidden_states = layer(
                    hidden_states,
                    None,
                    cu_seq_len,
                )
        hidden_states = self.final_layer_norm(hidden_states)
        if output_hidden_states:
            all_hidden_states = all_hidden_states + (hidden_states,)

        return BaseModelOutputWithNoAttention(
            last_hidden_state=hidden_states,
            hidden_states=all_hidden_states,
        )


class UnimcMLMHead(UnimcPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.config = config

        self.init_method, self.output_layer_init_method = get_init_methods(config)
        # self.init_method = small_init_init_method(dim=config.hidden_size)

        self.activation = get_activation(config)  # change to gelu
        norm, eps = get_norm(config)
        self.layer_norm = norm(
            config.hidden_size, eps=eps, device="cuda", dtype=config.params_dtype
        )
        self.dense = mpu.ColumnParallelLinear(
            config,
            input_size=config.hidden_size,
            output_size=config.hidden_size,
            init_method=self.init_method,
            gather_output=True,
        )
        self.mlm_head = ParallelLinear(
            self.config,
            init_method=self.output_layer_init_method,
            parallel_output=True,
        )
        # Initialize weights and apply final processing
        self.post_init()

    def forward(self, hidden_states):
        # [s, h] -> [s, h]
        if self.gradient_checkpointing:
            hidden_states, _ = checkpoint(self.dense, hidden_states)
            hidden_states = self.activation(hidden_states)
            hidden_states = self.layer_norm(hidden_states)
            # [s, h] -> [s, vocab_size (parallel)]
            vocab_logits, _ = checkpoint(self.mlm_head, hidden_states)
        else:
            hidden_states, _ = self.dense(hidden_states)
            hidden_states = self.activation(hidden_states)
            hidden_states = self.layer_norm(hidden_states)
            # [s, h] -> [s, vocab_size (parallel)]
            vocab_logits, _ = self.mlm_head(hidden_states)
        return vocab_logits  # [s, vocab_size (parallel)]

    # def forward(self, hidden_states):
    #     # [s, h] -> [s, vocab_size (parallel)]
    #     if self.gradient_checkpointing:
    #         vocab_logits, _ = checkpoint(self.mlm_head, hidden_states)
    #     else:
    #         vocab_logits, _ = self.mlm_head(hidden_states)
    #     return vocab_logits


class UnimcSOPHead(UnimcPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.config = config
        # Initialize weights and apply final processing
        self.init_method, _ = get_init_methods(config)
        # self.init_method = small_init_init_method(dim=config.hidden_size)
        self.dense_in = mpu.ColumnParallelLinear(
            config,
            input_size=config.hidden_size,
            output_size=config.hidden_size,
            gather_output=False,
            init_method=self.init_method,
        )
        self.dense_out = mpu.RowParallelLinear(
            config,
            input_size=config.hidden_size,
            output_size=2,
            input_is_parallel=True,
            init_method=self.init_method,
        )

        self.activation = nn.Tanh()
        self.post_init()

    # sop head is so small so we dont need gradient checkpointing
    def forward(self, hidden_states, cu_seq_lens):
        # cu_seq_lens: ['b+1',]
        # hidden_states: [s, h]
        cu_seq_lens = cu_seq_lens[:-1].unsqueeze(1).to(dtype=torch.int64)
        cu_seq_lens = cu_seq_lens.expand(cu_seq_lens.size(0), hidden_states.size(1))
        # [s, h] -> ['b', h]
        pooled_output = torch.gather(hidden_states, 0, cu_seq_lens)
        pooled_output, _ = self.dense_in(pooled_output)
        pooled_output = self.activation(pooled_output)
        # TODO: ADD dropout
        pooled_output, _ = self.dense_out(pooled_output)
        return pooled_output  # ['b', 2]


class UnimcForMaskLM(UnimcPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)

        self.unimc = UnimcModel(config)
        self.init_method, self.output_layer_init_method = get_init_methods(config)
        self.mlm_head = UnimcMLMHead(config)
        self.sop_head = UnimcSOPHead(config)
        # Initialize weights and apply final processing
        self.post_init()

    def forward(
        self,
        input_ids,
        token_type_ids,
        cu_seq_len,
        cu_batch_size,
        *label_package,
        output_hidden_states: Optional[bool] = None,
        compute_loss: Optional[bool] = False,
        return_dict: Optional[bool] = False,
    ) -> BaseModelOutputWithNoAttention:
        cu_seq_len = cu_seq_len[:cu_batch_size]
        outputs = self.unimc(
            input_ids,
            token_type_ids,
            cu_seq_len,
            output_hidden_states,
        )

        last_hidden_states = outputs[0]  # [s, h]

        # [s, h] -> [s, vocab_size (parallel)]
        vocab_logits = self.mlm_head(last_hidden_states)

        # [s, h] -> ['b', 2]
        sop_logits = self.sop_head(last_hidden_states, cu_seq_len)
        # sop_logits = sop_logits.view(-1)

        # pad_length = vocab_logits.size(0) - sop_logits.size(0)
        # sop_logits = torch.cat(
        #     (
        #         sop_logits,
        #         torch.zeros(
        #             pad_length, dtype=sop_logits.dtype, device=sop_logits.device
        #         ),
        #     )
        # )  # ['b'*2,] -> ['b'*2 + pad_length,] = [s,]
        # # [s, vocab_size (parallel)+1]
        # bert_logits = torch.cat((vocab_logits, sop_logits.unsqueeze(1)), dim=1)
        if compute_loss:
            loss = unimc_pretraining_loss(
                vocab_logits,
                sop_logits,
                *label_package,
            )
            return loss

        if return_dict:
            return BaseModelOutputWithNoAttention(vocab_logits, outputs[1])
        else:
            return vocab_logits, sop_logits


from flash_attn.ops.triton.cross_entropy import (
    cross_entropy_loss as triton_cross_entropy,
)


# we dont need pipeline parallelism
def unimc_pretraining_loss(
    vocab_logits,
    sop_logits,
    vocab_labels,
    sop_labels,
    loss_mask,
    alpha=1.0,
    beta=1.0,
    ignored_index=-100,
    process_group=None,
):
    # sop_labels: ['b',]
    # sop_logits: ['b', 2]
    # loss : scaler
    # sop_loss = torch.nn.functional.cross_entropy(
    #     sop_logits, sop_labels, ignore_index=ignored_index, reduction="mean"
    # )  # reduction = 'mean'
    # isnan = torch.isnan(sop_loss)
    # if isnan.any():
    #     logging.info(f"Found NaN in sop_loss: {sop_loss}")
    #     return None
    # sop_loss = triton_cross_entropy(sop_logits, sop_labels, ignored_index=ignored_index)
    # sop_loss = sop_loss.mean()

    # vocab_labels: [s,]
    # vocab_logits: [s, vocab_size (parallel)]
    # loss: [s,]
    # mlm_loss = mpu.vocab_parallel_cross_entropy(vocab_logits, vocab_labels)
    mlm_loss = triton_cross_entropy(
        vocab_logits, vocab_labels, process_group=process_group
    )
    isnan = torch.isnan(mlm_loss)
    if isnan.any():
        logging.info(f"Found NaN in mlm_loss: {mlm_loss}")
        return None

    mlm_loss, loss_mask = mlm_loss.float(), loss_mask.float()

    mlm_loss = (mlm_loss * loss_mask).sum() / torch.sum(loss_mask)

    return alpha * mlm_loss
