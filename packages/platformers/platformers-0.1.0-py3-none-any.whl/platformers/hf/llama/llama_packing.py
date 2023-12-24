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
)
from transformers.modeling_utils import PreTrainedModel

# from transformers.utils import logging
import logging

from optimus import mpu
from optimus.model.init_functions import get_init_methods
from optimus.model.norms import get_norm
from optimus.model.utils import get_fusion_type
from optimus.model.transformer import ParallelLinear, ParallelTransformerLayer
from optimus.model.word_embeddings import Embedding
from optimus.model.fused_softmax import FusedScaleMaskSoftmax
from optimus.generator.generator import Generator
from functools import partial
import optimus.model.init_functions as init
from transformers.generation.utils import (
    LogitsProcessorList,
    StoppingCriteriaList,
    validate_stopping_criteria,
    # validate_torch_generate_args,
)
from optimus.hf.llama.llama import (
    LlamaConfig,
    expand_attention_types,
    gpt2_attention_mask_func,
    LlamaPreTrainedModel,
    LlamaModel,
    LlamaForCausalLM,
)


class LlamaModelPacking(LlamaModel):
    def __init__(self, config):
        super(LlamaModel, self).__init__(config)  # dont init by LlamaModel
        config.attention_config = expand_attention_types(
            config.attention_config, config.num_hidden_layers
        )
        max_seq_len = getattr(config, "max_position_embeddings", 8192)
        config.max_position_embeddings = max_seq_len

        is_rotary = config.pos_emb == "rotary"
        assert is_rotary, "Not support Alibi now"

        self.config = config
        self.init_method, self.output_layer_init_method = get_init_methods(config)
        self.embed_in = Embedding(
            config,
            config.hidden_size,
            config.vocab_size,
            config.max_position_embeddings,
            config.hidden_dropout,
            self.init_method,
            num_tokentypes=0,
        )
        self.layers = nn.ModuleList(
            [
                ParallelTransformerLayer(
                    config,
                    attention_mask_func=gpt2_attention_mask_func,
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
        self.final_layer_norm = norm(config.hidden_size, eps=eps)
        self.gradient_checkpointing = True

        # in each of transformer layers, we have a fused softmax

        self.post_init()
        self.kv_enabled(False)  # For now
        # NOTE: We will support kv_enabled later on flash decoding

    def forward(
        self,
        input_ids,
        cu_seq_len,
        output_attentions: Optional[bool] = False,
        output_hidden_states: Optional[bool] = False,
        use_cache: Optional[bool] = False,
    ):
        # NOTE: we dont need attention_mask, token_type_ids, position_ids, ...

        output_attentions = (
            output_attentions if output_attentions else self.config.output_attentions
        )
        output_hidden_states = (
            output_hidden_states
            if output_hidden_states
            else self.config.output_hidden_states
        )

        all_hidden_states = () if output_hidden_states else None

        # Embedding
        hidden_states = self.embed_in(input_ids, position_ids=None)  # [sq, h]
        for i in range(self.config.num_hidden_layers):
            layer = self.layers[i]
            if output_hidden_states:
                all_hidden_states = all_hidden_states + (hidden_states,)

            if self.gradient_checkpointing:
                # when use grad checkpoint, we don't use cache, then
                # we dont need left padding, use ROPE New version
                hidden_states = checkpoint(layer, hidden_states, None, cu_seq_len)
            else:
                # use cache should close grad checkpoint
                # we use position_ids when use cache and left padding
                # use ROPE old version
                hidden_states = layer(
                    hidden_states,
                    None,
                    cu_seq_len,
                )
        hidden_states = self.final_layer_norm(hidden_states)
        if output_hidden_states:
            all_hidden_states = all_hidden_states + (hidden_states,)

        return BaseModelOutputWithPast(
            last_hidden_state=hidden_states,
            hidden_states=all_hidden_states,
            past_key_values=None,
            attentions=None,
        )


class LlamaForCausalLMPacking(LlamaForCausalLM):
    def __init__(self, config):
        super(LlamaForCausalLM, self).__init__(config)
        self.llama = LlamaModelPacking(config)
        self.init_method, self.output_layer_init_method = get_init_methods(config)
        self.embed_out = ParallelLinear(
            self.config,
            init_method=self.init_method,
            parallel_output=False,
        )

        # Initialize weights and apply final processing
        self.post_init()

    def forward(
        self,
        input_ids,
        cu_seq_len,
        output_attentions: Optional[bool] = False,
        output_hidden_states: Optional[bool] = False,
        use_cache: Optional[bool] = False,
    ):
        hidden_states = self.llama(
            input_ids, cu_seq_len, output_attentions, output_hidden_states, use_cache
        )
        hidden_states = hidden_states[0]
        lm_logits = self.embed_out(hidden_states)[0]
        return lm_logits
