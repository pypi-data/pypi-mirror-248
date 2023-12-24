from optimus import mpu
import torch
import torch.nn as nn
import math
import logging
import math


def map_int(x):
    try:
        return int(x)
    except ValueError:
        return 10000


XFORMER_READY = False
try:
    import xformers

    x_version = tuple(map(map_int, xformers.__version__.split(".")))
    if x_version < (0, 0, 21):
        raise ImportError
    import xformers.ops as xops

    XFORMER_READY = True
    logging.info("Xformers successfully loaded")
except ImportError:
    logging.error("Xformers >= 0.0.21 not found, when use ALIBI, back to fuse softmax")
    pass

# import optimus.mpu as mpu
from optimus.model.fused_softmax import FusedScaleMaskSoftmax
from optimus.model.utils import exists, get_fusion_type
from optimus.model.positional_embeddings import (
    RotaryEmbedding,
    apply_rotary_pos_emb_torch,
    apply_rotary_pos_emb,
    AliBi,
)
from optimus.model.utils import configure_sparse_attention


class ParallelSelfAttention(nn.Module):
    """Parallel self-attention layer abstract class.

    Self-attention layer takes input with size [b, s, h]
    and returns output of the same size.
    """

    def __init__(
        self,
        neox_args,
        attention_mask_func,
        init_method,
        output_layer_init_method,
        layer_number,
        rpe=None,
        rotary=False,
        use_cache=False,
        parallel_output=False,
    ):
        super().__init__()

        self.config = neox_args

        self.fp16 = neox_args.precision == "fp16"
        self.bf16 = neox_args.precision == "bfloat16"
        self.attention_mask_func = attention_mask_func
        self.apply_query_key_layer_scaling = neox_args.apply_query_key_layer_scaling
        self.use_cache = use_cache
        self.attention_softmax_in_fp32 = neox_args.attention_softmax_in_fp32
        if self.apply_query_key_layer_scaling:
            self.attention_softmax_in_fp32 = True
        self.layer_number = layer_number
        # Per attention head and per partition values.
        world_size = mpu.get_model_parallel_world_size()
        self.hidden_size_per_partition = mpu.divide(neox_args.hidden_size, world_size)
        self.hidden_size_per_attention_head = mpu.divide(
            neox_args.hidden_size, neox_args.num_attention_heads
        )
        self.num_attention_heads_per_partition = mpu.divide(
            neox_args.num_attention_heads, world_size
        )
        self.pos_emb = neox_args.pos_emb
        self.num_head_per_partition = mpu.divide(
            neox_args.num_attention_heads, world_size
        )

        self.isGQA = bool(
            getattr(neox_args, "isGQA", False)
        )  # prevent return None, must clarify in config
        if self.isGQA:
            if hasattr(neox_args, "num_key_value_heads"):
                self.num_kv_heads = neox_args.num_key_value_heads
            elif hasattr(neox_args, "num_kv_heads"):
                self.num_kv_heads = neox_args.num_kv_heads
            else:
                raise AttributeError("Must have some attribute for num_kv_heads")

            self.num_q_head_per_partition = mpu.divide(
                neox_args.num_attention_heads, world_size
            )
            self.num_kv_head_per_partition = mpu.divide(
                neox_args.num_kv_heads, world_size
            )
            self.head_size = mpu.divide(
                neox_args.hidden_size, neox_args.num_attention_heads
            )
            self.qkv_linear_output_size = (
                neox_args.hidden_size + neox_args.num_kv_heads * self.head_size * 2
            )  # q + kv, [q, k, v] order
        else:
            self.qkv_linear_output_size = neox_args.hidden_size * 3

        # Strided linear layer.
        self.query_key_value = mpu.ColumnParallelLinear(
            neox_args=neox_args,
            input_size=neox_args.hidden_size,
            # output_size=3 * neox_args.hidden_size,
            output_size=self.qkv_linear_output_size,  # always map hidden state to [q, k, v]
            gather_output=False,
            init_method=init_method,
            bias=neox_args.use_bias_in_attn_linear,
        )

        coeff = None
        self.norm_factor = math.sqrt(self.hidden_size_per_attention_head)
        if self.apply_query_key_layer_scaling:
            coeff = max(1, self.layer_number)
            self.norm_factor *= coeff

        if neox_args.use_mup:
            self.norm_factor = self.hidden_size_per_attention_head

        self.rpe = rpe

        if self.pos_emb == "alibi":
            self.alibi_embed = AliBi(
                neox_args.num_attention_heads,
                neox_args.model_parallel_size,
                mpu.get_model_parallel_rank(),
            )

        # TODO: this arg shouldn't need to be passed in - get from neox_args
        if rotary:
            if neox_args.rotary_pct == 1:
                self.rotary_ndims = None
            else:
                assert neox_args.rotary_pct < 1
                self.rotary_ndims = int(
                    self.hidden_size_per_attention_head * neox_args.rotary_pct
                )
            dim = (
                self.rotary_ndims
                if self.rotary_ndims is not None
                else self.hidden_size_per_attention_head
            )
            self.rotary_emb = RotaryEmbedding(
                dim, base=neox_args.rotary_emb_base, precision=neox_args.params_dtype
            )
        else:
            self.rotary_emb = None

        self.attention_type = neox_args.attention_config[layer_number]
        # self.use_flash_attention = self.attention_type == "flash"
        self.use_flash_attention = True
        self.sparse = self.attention_type not in ("global", "flash")
        if self.sparse:
            self.sparse_attn = configure_sparse_attention(
                neox_args,
                self.attention_type,
                self.num_attention_heads_per_partition,
                mpu=mpu,
            )
        else:
            if self.use_flash_attention:
                """
                Optimus only support flash attention > 2.1
                because only uppon 2.1, causal mask of fmha
                can handle the left padding generation
                """
                # self.use_flash_attn2 = False
                try:
                    import flash_attn

                    flash_attn_version = tuple(
                        map(map_int, flash_attn.__version__.split("."))
                    )
                    if flash_attn_version < (2, 3, 0):
                        raise ImportError("Please upgrade flash_attn to >= 2.3.0")
                    else:
                        from flash_attn import (
                            flash_attn_qkvpacked_func,
                            flash_attn_func,
                            flash_attn_kvpacked_func,
                            flash_attn_varlen_qkvpacked_func,
                            flash_attn_varlen_kvpacked_func,
                            flash_attn_with_kvcache,
                        )
                        from flash_attn.flash_attn_triton import (
                            flash_attn_qkvpacked_func as flash_triton_qkv_func,
                        )

                        self.flash_qkv_fn = flash_attn_qkvpacked_func
                        self.flash_attn_fn = flash_attn_func
                        self.flash_kv_fn = flash_attn_kvpacked_func

                        self.flash_var_qkv_fn = flash_attn_varlen_qkvpacked_func
                        self.flash_var_kv_fn = flash_attn_varlen_kvpacked_func
                        self.flash_attn_with_kvcache = flash_attn_with_kvcache

                        if self.layer_number == 0:
                            logging.info("Flash attention successfully loaded At layer0!!")

                        if self.pos_emb == "alibi":
                            if not XFORMER_READY:
                                raise ImportError

                except ImportError:
                    message = "`flash_attn` not found or `xformer` not found with alibi, using default attn"
                    logging.error(message)
                    self.use_flash_attention = False
                    # raise ImportError("Please install flash_attn >= 2.1.0")

            # use for flash attention not enabled
            self.scale_mask_softmax = FusedScaleMaskSoftmax(
                input_in_fp16=self.fp16,
                input_in_bf16=self.bf16,
                fusion_type=get_fusion_type(neox_args),
                mask_func=self.attention_mask_func,
                softmax_in_fp32=self.attention_softmax_in_fp32,
                scale=coeff,
            )

            # Dropout. Note that for a single iteration, this layer will generate
            # different outputs on different number of parallel partitions but
            # on average it should not be partition dependent.
            self.dropout_p = neox_args.attention_dropout
            self.attention_dropout = nn.Dropout(self.dropout_p)

        # Output.
        self.dense = mpu.RowParallelLinear(
            neox_args=neox_args,
            input_size=neox_args.hidden_size,
            output_size=neox_args.hidden_size,
            input_is_parallel=True,
            init_method=output_layer_init_method,
            skip_bias_add=True,
            parallel_output=parallel_output,
            # bias=neox_args.use_bias_in_attn_linear,
            bias=False,
        )

    def attention(
        self, query_layer, key_layer, value_layer, layer_past, attention_mask
    ):
        # ===================================
        # Raw attention scores. [b, np, s, s]
        # ===================================

        # [b, np, sq, sk]
        output_size = (
            query_layer.size(1),
            query_layer.size(2),
            query_layer.size(0),
            key_layer.size(0),
        )

        # [sq, b, np, hn] -> [sq, b * np, hn]
        query_layer = query_layer.view(
            output_size[2], output_size[0] * output_size[1], -1
        )
        key_layer = key_layer.view(output_size[3], output_size[0] * output_size[1], -1)

        # preallocating result tensor: [b * np, sq, sk]
        matmul_result = torch.empty(
            output_size[0] * output_size[1],
            output_size[2],
            output_size[3],
            dtype=query_layer.dtype,
            device=torch.cuda.current_device(),
        )

        # Raw attention scores. [b * np, sq, sk]
        matmul_result = torch.baddbmm(
            matmul_result,
            query_layer.transpose(0, 1),  # [b * np, sq, hn]
            key_layer.transpose(0, 1).transpose(1, 2),  # [b * np, hn, sk]
            beta=0.0,
            alpha=(1.0 / self.norm_factor),
        )

        # change view to [b, np, sq, sk]
        attention_scores = matmul_result.view(*output_size)

        # ==================================================
        # Update attention mask for inference. [b, np, sq, sk]
        # ==================================================

        if self.use_cache:
            with torch.no_grad():
                attention_mask = attention_mask[
                    ..., : attention_scores.size(3), : attention_scores.size(3)
                ]

        # ===========================
        # Attention probs and dropout
        # ===========================

        if exists(self.rpe):
            rpe = self.rpe(query_layer.size(0), key_layer.size(0))
            attention_scores += rpe  # [1, np, sq, sk]

        if self.pos_emb == "alibi":
            attention_scores = self.alibi_embed(attention_scores)

        # attention scores and attention mask [b, np, sq, sk]
        attention_probs = self.scale_mask_softmax(attention_scores, attention_mask)

        # This is actually dropping out entire tokens to attend to, which might
        # seem a bit unusual, but is taken from the original Transformer paper.
        with mpu.get_cuda_rng_tracker().fork():
            attention_probs = self.attention_dropout(attention_probs)

        # =========================
        # Context layer. [sq, b, hp]
        # =========================

        # value_layer -> context layer.
        # [sk, b, np, hn] --> [b, np, sq, hn]

        # context layer shape: [b, np, sq, hn]
        output_size = (
            value_layer.size(1),
            value_layer.size(2),
            query_layer.size(0),
            value_layer.size(3),
        )

        # change view [sk, b * np, hn]
        value_layer = value_layer.view(
            value_layer.size(0), output_size[0] * output_size[1], -1
        )

        # change view [b * np, sq, sk]
        attention_probs = attention_probs.view(
            output_size[0] * output_size[1], output_size[2], -1
        )

        # matmul: [b * np, sq, hn]
        context_layer = torch.bmm(attention_probs, value_layer.transpose(0, 1))

        # change view [b, np, sq, hn]
        context_layer = context_layer.view(*output_size)
        return context_layer

    def flash_attention(self, query_layer, key_layer, value_layer):
        # assert self.use_flash_attn2, "flash attn <2 not implemented in optimus"
        if self.pos_emb != "rotary":
            """ALIBI pos embedding"""

            def next_multiple_of_8(n):
                return n + (8 - n % 8) % 8

            # raise NotImplementedError(
            #     "Flash attention 2 requires rotary pos emb for now"
            # )
            sq, b, np, hn = query_layer.shape
            sk = key_layer.size(0)
            assert (
                sq == sk
            ), "sq != sk not supported yet, disable fmha by `model.llama.fmha_enbled(False)`"
            assert key_layer.size(2) == np, "ALIBI GQA & MQA supported yet"

            _bias = self.alibi_embed.bias(sq, sk, query_layer.device, query_layer.dtype)
            _bias = _bias.unsqueeze(0).tile((b, 1, 1, 1))
            bias = torch.empty(
                b,
                np,
                sq,
                next_multiple_of_8(sk),
                dtype=_bias.dtype,
                device=_bias.device,
            )
            bias[:, :, :, :sk] = _bias.contiguous()
            bias = bias[:, :, :, :sk]
            xops_q_shape = (b, sq, np, hn)
            xops_kv_shape = (b, sk, np, hn)

            causal_mask = xops.fmha.attn_bias.LowerTriangularMaskWithTensorBias(bias)
            query_layer = query_layer.transpose(0, 1).reshape(xops_q_shape)
            key_layer = key_layer.transpose(0, 1).reshape(xops_kv_shape)
            value_layer = value_layer.transpose(0, 1).reshape(xops_kv_shape)

            output = xops.memory_efficient_attention(
                query_layer,
                key_layer,
                value_layer,
                causal_mask,
                self.dropout_p if self.training else 0.0,
                None,
            )  # [b, sq, np, hn]

            output = output.transpose(0, 1).reshape(sq, b, np, hn)
            return output

        """
        This means we dont need to consider left padding situation,
        used in training and non-left padding generation, i.e. single sample
        generation
        """
        # [b, np, sq, sk]
        output_size = (
            query_layer.size(1),
            query_layer.size(2),
            query_layer.size(0),
            key_layer.size(0),
        )
        # [sq, b, np, hn] -> [b, sq, 1, np, hn] for both q,k,v
        kv_shape = key_layer.shape  # [sq, b, np_kv, hn]
        key_layer = key_layer.transpose(0, 1).reshape(
            kv_shape[1], kv_shape[0], 1, kv_shape[2], -1
        )
        value_layer = value_layer.transpose(0, 1).reshape(
            kv_shape[1], kv_shape[0], 1, kv_shape[2], -1
        )
        if self.isGQA:
            q_shape = query_layer.shape  # [sq, b, np_q, hn]
            query_layer = query_layer.transpose(0, 1).reshape(
                q_shape[1], q_shape[0], q_shape[2], -1
            )  # reshape to continguous
            kv = torch.cat([key_layer, value_layer], dim=2)
            # logging.info
            output = self.flash_kv_fn(
                query_layer,
                kv,
                self.dropout_p if self.training else 0.0,
                causal=True,
            )

        else:
            # Combined q/k/v into [b, s, 3, np, hn].
            query_layer = query_layer.transpose(0, 1).reshape(
                output_size[0], output_size[2], 1, output_size[1], -1
            )
            qkv = torch.cat([query_layer, key_layer, value_layer], dim=2)
            output = self.flash_qkv_fn(
                qkv,
                self.dropout_p if self.training else 0.0,
                softmax_scale=None,
                causal=True,
            )

        # qkv: (batch_size, seqlen, 3, nheads, headdim)
        # out: (batch_size, seqlen, nheads, headdim).
        matmul_result = output.view(
            output_size[0], output_size[2], output.shape[2], output.shape[3]
        )

        # [b, sq, np, hn] -> [b, np, sq, hn] (x)
        # return [sq, b, np, hn]
        matmul_result = matmul_result.transpose(0, 1)
        return matmul_result

        # """
        # Left padding generation
        # """
        # raise NotImplementedError(
        #     "generation not supported in flash attn normal forward now"
        # )

    def sparse_attention(self, query_layer, key_layer, value_layer, attention_mask):
        # TODO: sparse attn dropout?
        # TODO: pad to block size
        # shape of q/k/v is [sq, b, np, hn] and needs to be transposed to [b, np, sq, hn]
        query_layer, key_layer, value_layer = map(
            lambda t: t.permute(1, 2, 0, 3).contiguous(),
            (query_layer, key_layer, value_layer),
        )
        # output shape [b, np(heads), sq, hn]
        attn_mask = attention_mask.to(query_layer.dtype) * -10000
        if exists(self.rpe):
            rpe = self.rpe(query_layer.size(0), key_layer.size(0))
        else:
            rpe = None
        return self.sparse_attn(
            query_layer, key_layer, value_layer, attn_mask=attn_mask, rpe=rpe
        )

    def qkv_linear_gqa(self, hidden_states):
        # Attention heads [sq, b, h] --> [sq, b, (np * 3 * hn)]
        # if not self.isGQA else
        # [sq, b, (np + num_kv_heads/p * 2) * hn]
        mixed_x_layer, _ = self.query_key_value(hidden_states)
        q_size = self.num_q_head_per_partition * self.head_size
        kv_size = self.num_kv_head_per_partition * self.head_size
        query_layer, key_layer, value_layer = mixed_x_layer.split(
            [q_size, kv_size, kv_size], dim=-1
        )
        query_layer = query_layer.view(
            tuple(query_layer.size()[:-1])
            + (self.num_attention_heads_per_partition, self.head_size)
        )
        key_layer = key_layer.view(
            tuple(key_layer.size()[:-1])
            + (self.num_kv_head_per_partition, self.head_size)
        )
        value_layer = value_layer.view(
            tuple(value_layer.size()[:-1])
            + (self.num_kv_head_per_partition, self.head_size)
        )
        return query_layer, key_layer, value_layer

    def flash_attn_kv_forward(
        self, q, k, v, rcos, rsin, offset, layer_past, apply_rotary_fn, cache_sq_len
    ):
        """
        Flash attention with k/v cache, this function should
        return a `present` in order to align to transformers and
        non-flash forward
        """
        # First time forward
        if layer_past is None:
            q, k = apply_rotary_fn(q, k, rcos, rsin, offset=offset)
            # dont consider rotary ndim for now
            present = torch.stack((k, v))
            # use flash attention avoid more transpose
            output = self.flash_attention(q, k, v)
            return output, present

        # Normal forward

        # [sq, b, np, hn] -> [sq, b, np, hn]
        q, k = apply_rotary_fn(q, k, rcos, rsin, offset=offset)

        # [2, 1, b, np ,hn]
        kv = torch.stack([k, v], dim=0)
        present = torch.cat([layer_past, kv], dim=1)

        q = q.transpose(0, 1).contiguous()
        k = k.transpose(0, 1).contiguous()
        v = v.transpose(0, 1).contiguous()

        # [2, sq_cache, b, np, hn]
        layer_past = layer_past.transpose(1, 2).contiguous()

        # [b, sq_cache, np, hn] both
        k_cache, v_cache = layer_past[0], layer_past[1]
        k_cache = torch.cat([k_cache, k], dim=1)
        v_cache = torch.cat([v_cache, v], dim=1)

        # if self.layer_number == 10:
        #     logging.info(
        #         f"Go to flash kv part, k_cache shape: {k_cache.shape}, v_cache shape: {v_cache.shape}, q shape: {q.shape}"
        #     )
        # out: [b, sq, np ,hn]
        output = self.flash_attn_with_kvcache(
            q,
            k_cache,
            v_cache,
            None,
            None,
            None,
            None,
            cache_sq_len,
            causal=True,
        )
        output = output.transpose(0, 1).contiguous()
        # TODO: we should change k,v shape as [b, sq, np ,hn], fuck neox!

        # [b, sq+1, np, hn] -> [sq+1, b, np, hn]
        k_cache = k_cache.transpose(0, 1).contiguous()
        v_cache = v_cache.transpose(0, 1).contiguous()

        # presents: [sq_full_cached, b, np, hn]
        return output, present

    def forward(
        self,
        hidden_states,
        attention_mask,
        layer_past=None,
        cache_len=None,
    ):
        # Non causal attention mask is used for generating
        # hidden_states: [sq, b, h]

        # =====================
        # Query, Key, and Value
        # =====================

        # Attention heads [sq, b, h] --> [sq, b, (np * 3 * hn)]
        # if not self.isGQA else
        # [sq, b, (np + num_kv_heads/p * 2) * hn]
        if not self.isGQA:
            mixed_x_layer, _ = self.query_key_value(hidden_states)

            # [sq, b, (np * 3 * hn)] --> [sq, b, np, 3 * hn]
            new_tensor_shape = mixed_x_layer.size()[:-1] + (
                self.num_attention_heads_per_partition,
                3 * self.hidden_size_per_attention_head,
            )
            mixed_x_layer = mixed_x_layer.view(*new_tensor_shape)

            # [sq, b, np, 3 * hn] --> 3 [sq, b, np, hn]
            (query_layer, key_layer, value_layer) = mpu.split_tensor_along_last_dim(
                mixed_x_layer, 3
            )
        else:
            (query_layer, key_layer, value_layer) = self.qkv_linear_gqa(hidden_states)

        use_flash_kv = self.use_cache and self.use_flash_attention and not self.training

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

            apply_rotary_fn = (
                apply_rotary_pos_emb_torch if self.bf16 else apply_rotary_pos_emb
            )

            seq_len = key_layer.shape[0]
            offset = 0
            if exists(layer_past) and layer_past.numel() > 0:
                offset = layer_past[0].shape[0]
                seq_len += offset

            cos, sin = self.rotary_emb(value_layer, seq_len=seq_len)
            # NOTE: Conditions to use flash attention with kv forward is defined here
            if use_flash_kv:
                output, present = self.flash_attn_kv_forward(
                    query_rot,
                    key_rot,
                    value_layer,
                    cos,
                    sin,
                    offset,
                    layer_past,
                    apply_rotary_fn,
                    cache_len,
                )  # [s, b, h]
                output = output.view(output.shape[0], output.shape[1], -1)  # [s, b, h]
                output, bias = self.dense(output)  # [s, b, h]
                # if self.use_cache:
                output = [output, present]

                return output, bias

            query_layer, key_layer = apply_rotary_fn(
                query_rot, key_rot, cos, sin, offset=offset
            )

            if exists(self.rotary_ndims):
                query_layer = torch.cat((query_layer, query_pass), dim=-1)
                key_layer = torch.cat((key_layer, key_pass), dim=-1)

        # ==================================
        # Cache key and value for inference
        # ==================================

        if exists(layer_past) and layer_past.numel() > 0:
            past_key, past_value = layer_past
            key_layer = torch.cat((past_key.type_as(key_layer), key_layer), dim=0)
            value_layer = torch.cat(
                (past_value.type_as(value_layer), value_layer), dim=0
            )
            
        # NOTE: if use_cache and use_flash_attention_both enabled, we will not go in here
        assert not (
            self.use_cache and self.use_flash_attention
        ), "Flash attn with kv forward will determined earlier, maybe should convert to eval mode, \
even for baichuan or other abibi model, we should not use fmha in cache since not supported in xformers now"

        if self.use_cache:
            present = torch.stack((key_layer, value_layer))

        if self.use_flash_attention:
            # use flash attention avoid more transpose
            context_layer = self.flash_attention(query_layer, key_layer, value_layer)

            # context_layer = context_layer.permute(2, 0, 1, 3).contiguous()
            # logging.debug("flash attn output shape: {}".format(context_layer.shape))

            # [sq, b, np, hn] --> [sq, b, hp]
            new_context_layer_shape = context_layer.size()[:-2] + (
                self.hidden_size_per_partition,
            )
            context_layer = context_layer.view(*new_context_layer_shape)
            # Output. [sq, b, h]
            output, bias = self.dense(context_layer)

            # logging.debug("flash attn output shape: {}".format(output.shape))

            if self.use_cache:
                output = [output, present]

            return output, bias

        elif not self.sparse:
            context_layer = self.attention(
                query_layer, key_layer, value_layer, layer_past, attention_mask
            )
        else:
            context_layer = self.sparse_attention(
                query_layer, key_layer, value_layer, attention_mask
            )

        # [b, np, sq, hn] --> [sq, b, np, hn]
        context_layer = context_layer.permute(2, 0, 1, 3).contiguous()

        # [sq, b, np, hn] --> [sq, b, hp]
        new_context_layer_shape = context_layer.size()[:-2] + (
            self.hidden_size_per_partition,
        )
        context_layer = context_layer.view(*new_context_layer_shape)

        # =================
        # Output. [sq, b, h]
        # =================

        output, bias = self.dense(context_layer)

        if self.use_cache:
            output = [output, present]

        return output, bias


