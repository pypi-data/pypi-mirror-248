import torch
from optimus import mpu
from optimus.model.attention import ParallelSelfAttention
from optimus.model.utils import exists
from optimus.model.packing.rotary import RotaryEmbeddingPacking, apply_rotary_emb

import torch
import logging



class ParallelSelfAttentionPacking(ParallelSelfAttention):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Assume alaways use flash attention
        assert (
            self.use_flash_attention
        ), "Packed only support flash attention, you see this means flash attention is not ready"

        from flash_attn import (
            flash_attn_varlen_qkvpacked_func,
            flash_attn_varlen_kvpacked_func,
        )

        self.flash_var_qkv_fn = flash_attn_varlen_qkvpacked_func
        self.flash_var_kv_fn = flash_attn_varlen_kvpacked_func
        if hasattr(self.config, "max_seq_len"):
            self.max_seq_len = self.config.max_seq_len
        else:
            self.max_seq_len = self.config.max_position_embeddings

        # If we use MLM, we noly use packing
        self.is_causal = getattr(self.config, "is_causal", True)
        self.use_ntk = getattr(self.config, "use_ntk", False)
        self.ntk_factor = getattr(self.config, "ntk_factor", 1.0)
        rope_scale = getattr(self.config, "rope_scale", 1.0)

        self.rotary_emb = RotaryEmbeddingPacking(
            self.hidden_size_per_attention_head,
            max_seq_len=self.max_seq_len,
            base=self.config.rotary_emb_base,
            precision=self.config.params_dtype,
            max_position_embeddings=self.config.max_position_embeddings,
            rope_scale=rope_scale,
            ntk=self.use_ntk,
            ntk_factor=self.ntk_factor,
        )
        self.use_cache = False
        # logging.info(f"ParallelSelfAttentionPacking is_causal: {self.is_causal}")

    def forward(self, hidden_states, cu_seqlen):
        """
        attention mask here is special for packing
        for one sample in batch, it's a list of num_samples
        for alignment, we need to pad to max_len
        """
        if not self.isGQA:
            mixed_x_layer, _ = self.query_key_value(hidden_states)

            # [sq, (np * 3 * hn)] --> [sq, np, 3 * hn]
            new_tensor_shape = mixed_x_layer.size()[:-1] + (
                self.num_attention_heads_per_partition,
                3 * self.hidden_size_per_attention_head,
            )
            mixed_x_layer = mixed_x_layer.view(*new_tensor_shape)

            # [sq, np, 3 * hn] --> 3 [sq, np, hn]
            (query_layer, key_layer, value_layer) = mpu.split_tensor_along_last_dim(
                mixed_x_layer, 3
            )

        else:
            # GQA
            # Attention heads [sq, h] --> [sq, (np * 3 * hn)]
            (query_layer, key_layer, value_layer) = self.qkv_linear_gqa(hidden_states)

        if exists(self.rotary_emb):
            if exists(self.rotary_ndims):
                # partial rotary
                query_rot, query_pass = (
                    query_layer[..., : self.rotary_ndims],
                    query_layer[..., self.rotary_ndims :],
                )
                key_rot, key_pass = (
                    key_layer[..., : self.rotary_ndims],
                    key_layer[..., self.rotary_ndims :],
                )
            else:
                # full rotary
                query_rot, key_rot = query_layer, key_layer

            cos, sin = self.rotary_emb(value_layer)  # only need to get cos, sin
            # logging.error(f"cos: {cos.size()}, sin: {sin.size()}")
            # cos, sin [max_seq_len, dim / 2]
            # query_rot, key_rot [sq, np, hn]
            apply_rotary_emb(
                query_rot,
                cos,
                sin,
                cu_seqlens=cu_seqlen,
                max_seqlen=self.max_seq_len,
                inplace=True,
            )
            apply_rotary_emb(
                key_rot,
                cos,
                sin,
                cu_seqlens=cu_seqlen,
                max_seqlen=self.max_seq_len,
                inplace=True,
            )

            # NOTE: we dont test this branch, so we dont support it
            if exists(self.rotary_ndims):
                query_layer = torch.cat((query_layer, query_pass), dim=-1)
                key_layer = torch.cat((key_layer, key_pass), dim=-1)
            else:
                query_layer = query_rot
                key_layer = key_rot

        assert (
            query_layer.size(0) == key_layer.size(0) == value_layer.size(0)
        ), "Not support kv cache now"

        if not self.isGQA:
            # 3[sq, np, hn] --> [sq, 3, np, hn]
            qkv = torch.stack((query_layer, key_layer, value_layer), dim=1)

            # [sq, 3, np, hn] --> [sq, np, hn]
            output = self.flash_var_qkv_fn(
                qkv,
                cu_seqlen,
                self.max_seq_len,
                dropout_p=self.dropout_p if self.training else 0.0,
                causal=self.is_causal,  # for unimc
            )
        else:
            # 2[sq, np, hn] --> [sq, 2, np, hn]
            kv = torch.stack((key_layer, value_layer), dim=1)

            # [sq, np_q, hn_q], [sq, 2, np_kv, hn] --> [sq, np_q, hn]
            # note that np_q is the number of heads in fact
            output = self.flash_var_kv_fn(
                query_layer,
                kv,
                cu_seqlen,
                cu_seqlen,
                self.max_seq_len,
                self.max_seq_len,
                dropout_p=self.dropout_p if self.training else 0.0,
                causal=self.is_causal,
            )

        sq, np, hn = output.size()
        output = output.view(sq, np * hn).contiguous()

        output, bias = self.dense(output)
        return output, bias
