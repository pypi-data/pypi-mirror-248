import torch
from flash_attn.ops.triton.rotary import apply_rotary
from typing import Optional, Union

import torch


class RotaryEmbeddingPacking(torch.nn.Module):
    def __init__(
        self,
        dim,
        max_seq_len,
        base=10000,
        precision=torch.bfloat16,
        rope_scale=1.0,
        max_position_embeddings=None,
        ntk=False,
        ntk_factor=1.0,
    ):
        super().__init__()
        self.base = base
        self.dim = dim
        inv_freq = 1.0 / (
            base ** (torch.arange(0, dim, 2, device="cuda").float() / dim)
        )
        self.inv_freq = inv_freq
        self.cos_cached = None
        self.sin_cached = None
        self.precision = precision
        self.max_seq_len = max_seq_len
        self.rope_scale = rope_scale
        self.ntk_factor = ntk_factor

        self.use_ntk = ntk

        self.max_position_embeddings = (
            max_position_embeddings
            if max_position_embeddings is not None
            else self.max_seq_len
        )

        assert (
            self.max_seq_len >= self.max_position_embeddings
            and self.max_seq_len % self.max_position_embeddings == 0
        ), "max_seq_len must be divisible by max_position_embeddings"

        if not ntk:
            assert (
                self.max_position_embeddings * int(rope_scale) == self.max_seq_len
            ), "Linear scaling mimatches"

        else:
            assert rope_scale == 1.0, "NTK only supports rope_scale=1.0"

        self._set_sin_cos()

    def _set_sin_cos(self):
        seq_len = self.max_seq_len
        if self.use_ntk:
            # base = self.base * (
            #     (self.ntk_factor * seq_len / self.max_position_embeddings)
            #     - (self.ntk_factor - 1)
            # ) ** (self.dim / (self.dim - 2))
            base = self.base * self.ntk_factor ** (self.dim / (self.dim - 2))
            print(
                f"Now use NTK ROPE, base: {base}, rope_scale: {self.rope_scale}, nt_factor: {self.ntk_factor}"
            )
            dim = self.dim

            inv_freq = 1.0 / (
                base ** (torch.arange(0, dim, 2, device="cuda").float() / dim)
            )
            self.inv_freq = inv_freq
            t = torch.arange(seq_len, device="cuda", dtype=torch.float32)
            freqs = torch.einsum("i,j->ij", t, inv_freq)
            emb = freqs

        else:
            t = torch.arange(seq_len, device="cuda", dtype=torch.float32)
            t = t / self.rope_scale
            freqs = torch.einsum("i,j->ij", t, self.inv_freq)
            emb = freqs  # [seq_len, dim / 2]

        # if self.precision == torch.bfloat16:
        emb = emb.float()
        self.cos_cached = emb.cos()
        self.sin_cached = emb.sin()
        # if self.precision == torch.bfloat16:
        #     self.cos_cached = self.cos_cached.bfloat16()
        #     self.sin_cached = self.sin_cached.bfloat16()

        return

    def forward(self, x):
        # seq_len = self.max_seq_len
        # if seq_len != self.seq_len_cached:
        #     self.seq_len_cached = seq_len
        #     t = torch.arange(seq_len, device=x.device, dtype=torch.float32)
        #     t = t / self.rope_scale
        #     # print(f"[{len(t)}]t: {t}")
        #     freqs = torch.einsum("i,j->ij", t, self.inv_freq)
        #     # emb = torch.cat((freqs, freqs), dim=-1).to(x.device)
        #     emb = freqs  # [seq_len, dim / 2]
        #     if self.precision == torch.bfloat16:
        #         emb = emb.float()
        #
        #     self.cos_cached = emb.cos()
        #     self.sin_cached = emb.sin()
        #     if self.precision == torch.bfloat16:
        #         self.cos_cached = self.cos_cached.bfloat16()
        #         self.sin_cached = self.sin_cached.bfloat16()
        return self.cos_cached.to(dtype=x.dtype), self.sin_cached.to(dtype=x.dtype)


class ApplyRotaryEmb(torch.autograd.Function):
    @staticmethod
    def forward(
        ctx,
        x,
        cos,
        sin,
        interleaved=False,
        inplace=False,
        seqlen_offsets: Union[int, torch.Tensor] = 0,
        cu_seqlens: Optional[torch.Tensor] = None,
        max_seqlen: Optional[int] = None,
    ):
        out = apply_rotary(
            x,
            cos,
            sin,
            seqlen_offsets=seqlen_offsets,
            cu_seqlens=cu_seqlens,
            max_seqlen=max_seqlen,
            interleaved=interleaved,
            inplace=inplace,
        )
        if isinstance(seqlen_offsets, int):
            ctx.save_for_backward(
                cos, sin, cu_seqlens
            )  # Can't save int with save_for_backward
            ctx.seqlen_offsets = seqlen_offsets
        else:
            ctx.save_for_backward(cos, sin, cu_seqlens, seqlen_offsets)
            ctx.seqlen_offsets = None
        ctx.interleaved = interleaved
        ctx.inplace = inplace
        ctx.max_seqlen = max_seqlen
        return out if not inplace else x

    @staticmethod
    def backward(ctx, do):
        seqlen_offsets = ctx.seqlen_offsets
        if seqlen_offsets is None:
            cos, sin, cu_seqlens, seqlen_offsets = ctx.saved_tensors
        else:
            cos, sin, cu_seqlens = ctx.saved_tensors
        # TD [2023-09-02]: For some reason Triton (2.0.0.post1) errors with
        # "[CUDA]: invalid device context", and cloning makes it work. Idk why. Triton 2.1.0 works.
        if not ctx.interleaved and not ctx.inplace:
            do = do.clone()
        dx = apply_rotary(
            do,
            cos,
            sin,
            seqlen_offsets=seqlen_offsets,
            cu_seqlens=cu_seqlens,
            max_seqlen=ctx.max_seqlen,
            interleaved=ctx.interleaved,
            inplace=ctx.inplace,
            conjugate=True,
        )
        return dx, None, None, None, None, None, None, None


def apply_rotary_emb(
    x,
    cos,
    sin,
    interleaved=False,
    inplace=False,
    seqlen_offsets: Union[int, torch.Tensor] = 0,
    cu_seqlens: Optional[torch.Tensor] = None,
    max_seqlen: Optional[int] = None,
):
    """
    Arguments:
        x: (batch_size, seqlen, nheads, headdim) if cu_seqlens is None
            else (total_seqlen, nheads, headdim)
        cos, sin: (seqlen_rotary, rotary_dim / 2)
        interleaved: if True, rotate pairs of even and odd dimensions (GPT-J style) instead
            of 1st half and 2nd half (GPT-NeoX style).
        inplace: if True, apply rotary embedding in-place.
        seqlen_offsets: (batch_size,) or int. Each sequence in x is shifted by this amount.
            Most commonly used in inference when we have KV cache.
        cu_seqlens: (batch + 1,) or None
        max_seqlen: int
    Return:
        out: (batch_size, seqlen, nheads, headdim) if cu_seqlens is None
            else (total_seqlen, nheads, headdim)
    rotary_dim must be <= headdim
    Apply rotary embedding to the first rotary_dim of x.
    """
    return ApplyRotaryEmb.apply(
        x, cos, sin, interleaved, inplace, seqlen_offsets, cu_seqlens, max_seqlen
    )
