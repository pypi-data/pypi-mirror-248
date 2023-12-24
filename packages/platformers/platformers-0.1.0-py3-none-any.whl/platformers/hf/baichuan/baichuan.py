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

from optimus.model.init_functions import get_init_methods
from optimus.model.norms import get_norm
from optimus.model.utils import get_fusion_type
from optimus.model.transformer import ParallelLinear, ParallelTransformerLayer
from optimus.model.word_embeddings import Embedding
from optimus.model.fused_softmax import FusedScaleMaskSoftmax
from optimus.generator.generator import Generator

"""
Baichuan is exactly LlamaModel with ALIBI
so we just change config, and for reusing of convert script
we set model prefix as `llama` and `llama.layers`
"""

class BaichuanConfig(PretrainedConfig):
    model_type = "baichuan"
    keys_to_ignore_at_inference = ["past_key_values"]

    def __init__(
        self,
        vocab_size=64000,
        hidden_size=5120,
        intermediate_size=13696,
        num_hidden_layers=40,
        num_attention_heads=40,
        hidden_act="silu",
        model_max_length=4096,
        initializer_range=0.02,
        rms_norm_eps=1e-6,
        use_cache=True,
        pad_token_id=0,
        bos_token_id=1,
        eos_token_id=2,
        tie_word_embeddings=False,
        **kwargs,
    ):
        self.vocab_size = vocab_size
        self.model_max_length = model_max_length
        self.hidden_size = hidden_size
        self.intermediate_size = intermediate_size
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads
        self.hidden_act = hidden_act
        self.initializer_range = initializer_range
        self.rms_norm_eps = rms_norm_eps
        self.use_cache = use_cache
        self.pos_emb = "alibi"
        super().__init__(
            pad_token_id=pad_token_id,
            bos_token_id=bos_token_id,
            eos_token_id=eos_token_id,
            tie_word_embeddings=tie_word_embeddings,
            **kwargs,
        )
        self.init_epilogue()

    def init_epilogue(self):
        self.num_layers = self.num_hidden_layers
        self.use_mup = False
        self.use_cpu_initialization = False
        self.opt_pos_emb_offset = False
        self.activation = getattr(self, "hidden_act", "silu")
        self.padded_vocab_size = self.vocab_size
        self.precision = "fp16" if self.torch_dtype == "float16" else "bfloat16"
        self.use_flash_attention = True
        self.use_cache = True

        self.isGQA = getattr(self, "isGQA", False)

    @property
    def params_dtype(self):
        return torch.float16 if self.precision == "fp16" else torch.bfloat16

    def __getattr__(self, name):
        if "mup" in name or "bnb" in name:
            return None  # disable mup & bnb for now
        else:
            return object.__getattribute__(self, name)

class BaichuanRopeConfig(PretrainedConfig):
    model_type = "llama"

    def __init__(
        self,
        vocab_size=32000,
        hidden_size=4096,
        num_hidden_layers=32,
        num_attention_heads=32,
        intermediate_size=11008,
        hidden_act="silu",
        rotary_pct=1,
        rotary_emb_base=10000,
        max_position_embeddings=2048,
        initializer_range=0.02,
        rms_norm_epsilon=1.0e-6,
        use_cache=True,
        pad_token_id=0,
        bos_token_id=1,
        eos_token_id=2,
        tie_word_embeddings=False,
        use_parallel_residual=True,
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
        self.use_cache = use_cache
        self.tie_word_embeddings = tie_word_embeddings
        self.use_parallel_residual = use_parallel_residual
        self.pos_emb = "rotary"
        super().__init__(
            pad_token_id=pad_token_id,
            bos_token_id=bos_token_id,
            eos_token_id=eos_token_id,
            tie_word_embeddings=tie_word_embeddings,
            **kwargs,
        )
        self.init_epilogue()

    def init_epilogue(self):
        self.num_layers = self.num_hidden_layers
        self.use_mup = False
        self.use_cpu_initialization = False
        self.opt_pos_emb_offset = False
        self.activation = getattr(self, "hidden_act", "silu")
        self.padded_vocab_size = self.vocab_size
        self.precision = "fp16" if self.torch_dtype == "float16" else "bfloat16"
        self.use_flash_attention = True
        self.use_cache = True

        self.isGQA = getattr(self, "isGQA", False)

    @property
    def params_dtype(self):
        return torch.float16 if self.precision == "fp16" else torch.bfloat16

    def __getattr__(self, name):
        if "mup" in name or "bnb" in name:
            return None  # disable mup & bnb for now
        else:
            return object.__getattribute__(self, name)

class BaichuanPreTrainedModel(PreTrainedModel):
    """
    An abstract class to handle weights initialization and a simple interface for downloading and loading pretrained
    models.
    """

    config_class = BaichuanConfig
    base_model_prefix = "llama"
    supports_gradient_checkpointing = True
    _no_split_modules = ["LLamaLayer"]

    def _init_weights(self, module):
        """Initialize the weights"""
        pass

    def _set_gradient_checkpointing(self, module, value=False):
        if isinstance(module, BaichuanPreTrainedModel):
            module.gradient_checkpointing = value

def expand_attention_types(attention_config, num_layers):
    """
    Expands an `attention_config` list in the following format:

        [
        [['attention_type_1', ..., `attention_type_n`], 12]
        ]

    to a flattened list of length `num_layers`.

    :param params_list:
    :return:
    """

    # if only strings are found in the config, we assume it's already expanded
    if isinstance(attention_config, list) and len(attention_config) == 1 and attention_config[0] == "flash":
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


def gpt2_attention_mask_func(attention_scores, ltor_mask):
    attention_scores.masked_fill_(ltor_mask, torch.finfo(attention_scores.dtype).min)
    return attention_scores

class BaichuanModel(BaichuanPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        config.attention_config = expand_attention_types(
            config.attention_config, config.num_hidden_layers
        )
        is_rotary = config.pos_emb == "rotary"
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
                )
                for i in range(config.num_hidden_layers)
            ]
        )
        norm, eps = get_norm(config)
        self.final_layer_norm = norm(config.hidden_size, eps=eps)
        self.gradient_checkpointing = True

        self.post_init()
        self.kv_enabled(config.use_cache)

    def get_input_embeddings(self):
        return self.embed_in

    def set_input_embeddings(self, value):
        self.embed_in = value

    def fmha_enabled(self, use_fmha):
        for layer in self.layers:
            layer.attention.use_flash_attention = use_fmha

    def kv_enabled(self, use_cache):
        if use_cache is None:
            use_cache = False

        for layer in self.layers:
            layer.use_cache = use_cache
            layer.attention.use_cache = use_cache

            # disable flash attention if cache is enabled
            # use_fmha = layer.attention.use_flash_attention
            # layer.attention.use_flash_attention = (not use_cache) and use_fmha

        self.use_cache = use_cache
        # self.gradient_checkpointing = not use_cache

    def checkpointing_enabled(self, c: bool):
        self.gradient_checkpointing = c  # done in kv_enabled

    def forward(
        self,
        input_ids: Optional[torch.LongTensor] = None,
        attention_mask: Optional[torch.FloatTensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[Tuple[Tuple[torch.FloatTensor]]] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
        cache_len: torch.Tensor = None,
    ) -> Union[Tuple, BaseModelOutputWithPast]:
        """
        cache_len respect to flash attention `cache len` option, it idicates
        the kv cache length in situation of right padding, shape is [b,]
        """

        if use_cache is None:
            use_cache = False

        if self.use_cache != use_cache:
            self.kv_enabled(use_cache)
        use_cache = self.use_cache

        output_attentions = (
            output_attentions
            if output_attentions is not None
            else self.config.output_attentions
        )
        output_hidden_states = (
            output_hidden_states
            if output_hidden_states is not None
            else self.config.output_hidden_states
        )
        return_dict = (
            return_dict if return_dict is not None else self.config.use_return_dict
        )
        use_cache = use_cache if use_cache is not None else self.config.use_cache

        batch_size, seq_length = input_ids.size()

        if past_key_values is None:
            past_length = 0
            past_key_values = [None] * self.config.num_hidden_layers
        else:
            past_length = past_key_values[0][0].size(0)

        # presents = past_key_values if use_cache else None

        if position_ids is None:
            position_ids = torch.arange(
                past_length,
                seq_length + past_length,
                dtype=torch.long,
                device=input_ids.device,
            )
            position_ids = position_ids.unsqueeze(0).view(-1, seq_length)
        else:
            position_ids = position_ids.view(-1, seq_length).long()

        if attention_mask is not None:
            assert batch_size > 0, "batch_size has to be defined and > 0"
            attention_mask = attention_mask.view(batch_size, -1)
            attention_mask = attention_mask[:, None, None, :]
            tril_mask = torch.tril(
                torch.ones((1, seq_length, seq_length), device=attention_mask.device)
            ).view(1, 1, seq_length, seq_length)
            attention_mask = attention_mask * tril_mask
            attention_mask = attention_mask < 0.5

        hidden_states = self.embed_in(input_ids, position_ids=position_ids)
        hidden_states = hidden_states.transpose(0, 1).contiguous()
        all_attentions = () if output_attentions else None
        all_hidden_states = () if output_hidden_states else None

        # for _, (layer, layer_past) in enumerate(zip(self.layers, past_key_values)):
        for i in range(self.config.num_hidden_layers):
            layer = self.layers[i]
            if output_hidden_states:
                all_hidden_states = all_hidden_states + (hidden_states,)

            if self.gradient_checkpointing:
                # when use grad checkpoint, we don't use cache, then
                # we dont need left padding, use ROPE New version
                hidden_states = checkpoint(layer, hidden_states, attention_mask)
            else:
                # use cache should close grad checkpoint
                # we use position_ids when use cache and left padding
                # use ROPE old version
                out = layer(
                    hidden_states,
                    attention_mask=attention_mask,
                    layer_past=past_key_values[i],
                    cache_len=cache_len,
                )
                if self.use_cache:
                    hidden_states, cache = out
                    past_key_values[i] = cache
                else:
                    hidden_states = out

            if output_attentions:
                all_attentions = all_attentions + (layer.layer_past,)

        hidden_states = hidden_states.transpose(0, 1).contiguous()
        hidden_states = self.final_layer_norm(hidden_states)
        # Add last hidden state
        if output_hidden_states:
            all_hidden_states = all_hidden_states + (hidden_states,)

        if not return_dict:
            return tuple(
                v
                for v in [hidden_states, all_hidden_states, all_attentions]
                if v is not None
            )

        return BaseModelOutputWithPast(
            last_hidden_state=hidden_states,
            hidden_states=all_hidden_states,
            past_key_values=past_key_values if self.use_cache else None,
            attentions=all_attentions,
        )

    def resize_token_embeddings(self, new_num_tokens: Optional[int] = None):
        old_vocab_size = self.config.vocab_size
        self.config.vocab_size = new_num_tokens
        new_embed_in = Embedding(
            self.config,
            self.config.hidden_size,
            self.config.vocab_size,
            self.config.max_position_embeddings,
            self.config.hidden_dropout,
            self.init_method,
            num_tokentypes=0,
        )
        new_embed_in.word_embeddings.weight.data[
            :old_vocab_size, :
        ] = self.embed_in.word_embeddings.weight.data[:old_vocab_size, :]

        self.embed_in = new_embed_in
        return


class BaichuanForCausalLM(BaichuanPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)

        self.llama = BaichuanModel(config)
        self.init_method, self.output_layer_init_method = get_init_methods(config)
        self.embed_out = ParallelLinear(
            self.config,
            init_method=self.init_method,
            parallel_output=False,
        )

        # Initialize weights and apply final processing
        self.post_init()

    def get_output_embeddings(self):
        return self.embed_out

    def set_output_embeddings(self, new_embeddings):
        self.embed_out = new_embeddings

    def generate_mode(self):
        # self.eval()
        self.llama.kv_enabled(True)
        self.llama.checkpointing_enabled(False)
        self.llama.fmha_enabled(False)

    def train_mode(self, checkpointing=True):
        # self.train()
        self.llama.kv_enabled(False)
        self.llama.checkpointing_enabled(checkpointing)
        self.llama.fmha_enabled(True)

    def eval_mode(self):
        logging.waring(
            "Eval mode usually used at special case, if generating, use `self.generate_mode`"
        )
        self.llama.kv_enabled(False)
        self.llama.checkpointing_enabled(False)
        self.llama.fmha_enabled(True)

    def train(self, *args, **kwargs):
        self.train_mode()
        return super().train(*args, **kwargs)

    def eval(self, generate=True, *args, **kwargs):
        if generate:
            self.generate_mode()
        else:
            self.eval_mode()
        return super().eval(*args, **kwargs)

    def forward(
        self,
        input_ids: Optional[torch.LongTensor] = None,
        attention_mask: Optional[torch.LongTensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
        compute_lm_loss: Optional[bool] = False,
        labels: Optional[torch.LongTensor] = None,
        past_key_values: List[torch.Tensor] = None,
        in_generaton: bool = False,
        cache_len: torch.Tensor = None,
    ) -> Union[Tuple, CausalLMOutputWithPast]:
        return_dict = (
            return_dict if return_dict is not None else self.config.use_return_dict
        )

        if attention_mask is None:
            attention_mask = input_ids.new_ones(input_ids.shape)

        if attention_mask is not None and position_ids is None:
            # create position_ids on the fly for batch generation
            position_ids = attention_mask.long().cumsum(-1) - 1
            position_ids.masked_fill_(attention_mask == 0, 1)

        outputs = self.llama(
            input_ids,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_values=past_key_values,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
            cache_len=cache_len,
        )

        # NOTE: attention mask used here is [b, s]

        if in_generaton:
            # First forward
            if cache_len is None:
                last_hidden_states = outputs[0]
                last_index = attention_mask.cumsum(dim=1).argmax(dim=1)
                last_hidden_states = last_hidden_states.gather(
                    1,
                    last_index.view(-1, 1, 1).expand(
                        -1, 1, last_hidden_states.size(-1)
                    ),
                ).squeeze(
                    1
                )  # (b, h)
            else:
                last_hidden_states = outputs[0]  # (b, 1, h)
                last_hidden_states = last_hidden_states.squeeze(1)  # (b, h)
            lm_logits = self.embed_out(last_hidden_states)[0]
            return lm_logits, outputs.past_key_values  # (b, h)

        hidden_states = outputs[0]
        lm_logits = self.embed_out(hidden_states)[0]
        lm_loss = None

        if labels is not None and compute_lm_loss:
            # we are doing next-token prediction; shift prediction scores and input ids by one
            shift_logits = lm_logits[:, :-1, :].contiguous()
            labels = labels[:, 1:].contiguous()
            loss_fct = CrossEntropyLoss(reduction="none")
            lm_loss = loss_fct(
                shift_logits.view(-1, shift_logits.size(-1)), labels.view(-1)
            )
            # loss_weight = loss_weight[:, 1:].contiguous().view(-1)
            # lm_loss = (lm_loss * loss_weight).sum() / loss_weight.sum()
            lm_loss = lm_loss.mean()

        if not return_dict:
            output = (lm_logits,) + outputs[1:]
            return ((lm_loss,) + output) if lm_loss is not None else output

        return CausalLMOutputWithPast(
            loss=lm_loss,
            logits=lm_logits,
            past_key_values=outputs.past_key_values,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
        )

    @staticmethod
    def process_next_tokens(input_ids, last_idx, next_token, eos_token_id):
        # next token should be [b,]
        last_input_ids = input_ids.gather(1, last_idx.view(-1, 1)).squeze(1)  # [b, ]
        last_token_eos = last_input_ids == eos_token_id
        next_token[last_token_eos] = eos_token_id
        return next_token

    # @torch.no_grad()
    # def greedy_search(
    #     self,
    #     input_ids: torch.LongTensor,
    #     attention_mask: Optional[torch.LongTensor] = None,
    #     max_length: Optional[int] = None,
    #     pad_token_id: Optional[int] = None,
    #     eos_token_id: Optional[Union[int, List[int]]] = None,
    # ):
    #     # run first time
    #     position_ids = attention_mask.long().cumsum(-1) - 1
    #     position_ids.masked_fill_(attention_mask == 0, 1)
    #     logits, kv = self(
    #         input_ids=input_ids,
    #         attention_mask=attention_mask,
    #         position_ids=position_ids,
    #         use_cache=True,
    #         in_generaton=True,
    #     )
    #     next_token = torch.argmax(logits, dim=-1).view(-1, 1)
    #     last_idx = attention_mask.cumsum(dim=1).argmax(dim=1)
    #     next_token = self.process_next_tokens(
    #         input_ids, position_ids, next_token, eos_token_id
    #     )
    #
    #     pad_tokens = torch.full(
    #         (input_ids.shape[0], 1), pad_token_id, dtype=torch.long, device="cuda"
    #     )
    #     attn_tokens = torch.full(
    #         (input_ids.shape[0], 1), 0, dtype=torch.long, device="cuda"
    #     )
    #
    #     attention_mask = torch.cat([attention_mask, attn_tokens], dim=1)
    #     input_ids = torch.cat([input_ids, pad_tokens], dim=1)
    #     last_idx = attention_mask.cumsum(dim=1).argmax(dim=1) + 1
    #     input_ids.scatter_(1, last_idx.view(-1, 1), next_token)
    #     attention_mask.scatter_(1, last_idx.view(-1, 1), 1)

    def prepare_inputs_for_generation(
        self, input_ids, past_key_values=None, attention_mask=None, **kwargs
    ):
        if past_key_values and past_key_values[0] is not None:
            input_ids = input_ids[:, -1:]

        position_ids = kwargs.get("position_ids", None)
        if attention_mask is not None and position_ids is None:
            # create position_ids on the fly for batch generation
            position_ids = attention_mask.long().cumsum(-1) - 1
            position_ids.masked_fill_(attention_mask == 0, 1)
            if past_key_values:
                position_ids = position_ids[:, -1].unsqueeze(-1)

        # if model is used as a decoder in encoder-decoder model, the decoder attention mask is created on the fly
        if attention_mask is None:
            attention_mask = input_ids.new_ones(input_ids.shape)

        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "position_ids": position_ids,
            "past_key_values": past_key_values,
            **kwargs,
        }

    def _reorder_cache(self, past_key_values, beam_idx):
        reordered_past = ()
        for layer_past in past_key_values:
            reordered_past += (
                tuple(
                    past_state.index_select(0, beam_idx)
                    for past_state in layer_past[:2]
                )
                + layer_past[2:],
            )
        return reordered_past

    def resize_token_embeddings(self, new_num_tokens: Optional[int] = None):
        self.llama.resize_token_embeddings(new_num_tokens)
        old_vocab_size = self.config.vocab_size
        new_embed_out = ParallelLinear(
            config=self.config, init_method=self.init_method, parallel_output=False
        )
        new_embed_out.final_linear.weight.data[
            :old_vocab_size, :
        ] = self.embed_out.final_linear.weight.data[:old_vocab_size, :]
        self.embed_out = new_embed_out
        return
