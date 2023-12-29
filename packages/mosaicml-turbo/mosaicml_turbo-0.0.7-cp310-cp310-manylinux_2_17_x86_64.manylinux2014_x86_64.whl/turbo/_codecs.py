import abc
from typing import (Any, Dict, Optional, Protocol, Sequence, Tuple,
                    runtime_checkable)

import numpy as np
import torch
from torch import Tensor

from ._quantize import GROUP_SIZE, dequantize_signed, quantize_signed
from ._utils import div_round_up


class Codec(abc.ABC):

    @abc.abstractmethod
    def encode(self, X: Tensor, out: Optional[Tensor] = None) -> Tensor:
        ...

    @abc.abstractmethod
    def decode(self, X_enc: Tensor, out: Optional[Tensor] = None) -> Tensor:
        ...

    @property
    def state(self) -> Dict[str, Any]:
        return getattr(self, '_state', {})


class SequentialCodec(Codec):

    def __init__(self, codecs: Sequence[Codec]):
        self.codecs = list(codecs)

    def encode(self, X: Tensor, out: Optional[Tensor] = None) -> Tensor:
        for c in self.codecs:
            X = c.encode(X, out)
        return X

    def decode(self, X_enc: Tensor, out: Optional[Tensor] = None) -> Tensor:
        for c in self.codecs[::-1]:
            X_enc = c.decode(X_enc, out)
        return X_enc


def _identity(X: Tensor, out: Optional[Tensor] = None) -> Tensor:
    if out is not None:
        out.copy_(X)
        return out
    return X


class LambdaCodec(Codec):

    # avoid illegible function signature and make partial functions that
    # take in an `out` kwarg work (includes a lot of torch funcs)
    @runtime_checkable  # just so type checking asserts work
    class CodecFunction(Protocol):

        def __call__(self, X: Tensor, out: Optional[Tensor] = None) -> Tensor:
            ...

    def __init__(self,
                 f_encode: Optional[CodecFunction] = None,
                 f_decode: Optional[CodecFunction] = None):
        self.f_encode = f_encode or _identity
        self.f_decode = f_decode or _identity

    def encode(self, X: Tensor, out: Optional[Tensor] = None) -> Tensor:
        return self.f_encode(X, out=out)

    def decode(self, X_enc: Tensor, out: Optional[Tensor] = None) -> Tensor:
        return self.f_decode(X_enc, out=out)


class IdentityCodec(Codec):
    """For debugging."""

    def encode(self, X: Tensor, out: Optional[Tensor] = None) -> Tensor:
        if out is None:
            return X
        out.copy_(X)
        return out

    def decode(self, X_enc: Tensor, out: Optional[Tensor] = None) -> Tensor:
        return self.encode(X_enc, out)


def _round_up_to_multiple(x: int, multiple_of: int) -> int:
    remainder = x % multiple_of
    if remainder != 0:
        return multiple_of - remainder
    return 0


class SignedIntQuantizer(Codec):

    def __init__(self,
                 num_bits: int = 8,
                 pad_scales_to_bytes: int = 16,
                 pad_encode_to_bytes: int = 1):
        self._num_bits = num_bits
        self._bytes_per_scale = 2
        self._group_size = GROUP_SIZE
        self._scales_dtype = torch.float16
        self._pad_scales_to_bytes = pad_scales_to_bytes
        self._pad_encode_to_bytes = pad_encode_to_bytes
        self._state: Dict[str, Any] = {}

    def _compressed_offsets(self, numel: int) -> Tuple[int, int, int, int]:
        num_groups = div_round_up(numel, self._group_size)
        elems_size = div_round_up(numel * self._num_bits, 8)
        scales_size = num_groups * self._bytes_per_scale
        # pad such that scales are aligned and encoded output is a multiple
        # of the requested number of bytes
        middle_padding = _round_up_to_multiple(elems_size,
                                               self._pad_scales_to_bytes)
        end_padding = _round_up_to_multiple(scales_size,
                                            self._pad_encode_to_bytes)
        in_size = elems_size + middle_padding + scales_size + end_padding
        scales_start = elems_size + middle_padding
        scales_end = scales_start + scales_size
        return in_size, elems_size, scales_start, scales_end

    def encode(self, X: Tensor, out: Optional[Tensor] = None) -> Tensor:
        if out is not None:
            raise NotImplementedError('Argument out must be None')

        numel = X.numel()
        in_size, elems_size, scales_start, scales_end = self._compressed_offsets(
            numel)

        X_comp = torch.empty(in_size, dtype=torch.int8, device=X.device)
        scales_out = X_comp[scales_start:scales_end].view(
            dtype=self._scales_dtype)
        quantize_signed(X,
                        num_bits=self._num_bits,
                        scales_out=scales_out,
                        x_q_out=X_comp[:elems_size])

        self._state['shape'] = X.shape
        self._state['dtype'] = X.dtype
        return X_comp

    def decode(self, X_comp: Tensor, out: Optional[Tensor] = None) -> Tensor:
        assert X_comp.dtype == torch.int8, 'Broken compression pipeline!'
        shape = self._state['shape']
        numel = np.prod(shape)
        in_size, elems_size, scales_start, scales_end = self._compressed_offsets(
            numel)
        assert X_comp.numel() == in_size, 'Broken compression pipeline!'
        scales = X_comp[scales_start:scales_end].view(dtype=self._scales_dtype)

        # NOTE: our encoding enforces alignment of the inputs to the decoding,
        # but caller has to enforce alignment of x_out
        return dequantize_signed(X_comp[:elems_size],
                                 scales=scales,
                                 num_bits=self._num_bits,
                                 x_out=out,
                                 out_shape=shape,
                                 out_dtype=self._state['dtype'])
