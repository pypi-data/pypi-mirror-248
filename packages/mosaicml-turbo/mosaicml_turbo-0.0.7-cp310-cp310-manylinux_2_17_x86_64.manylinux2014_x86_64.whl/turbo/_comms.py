import dataclasses
import functools
from typing import Callable, Optional, Protocol

import torch
from torch._C._distributed_c10d import AllgatherOptions  # type: ignore
from torch.distributed import ProcessGroup, Work  # type: ignore

from . import _codecs as codecs
from ._codecs import Codec


class Waitable(Protocol):
    """An object you can call wait() on.

    Meaning varies. Mostly for typing.
    """

    def wait(self) -> None:
        ...


@dataclasses.dataclass
class SimpleFuture:
    callback: Callable

    def wait(self) -> None:
        self.callback()


def _default_compressed_allgather_codec(clip_min: float,
                                        clip_max: float) -> Codec:
    f_nan2num = functools.partial(torch.nan_to_num, neginf=0, posinf=0)
    f_clip = functools.partial(torch.clip, min=clip_min, max=clip_max)
    assert isinstance(f_nan2num, codecs.LambdaCodec.CodecFunction)  # pyright
    assert isinstance(f_clip, codecs.LambdaCodec.CodecFunction)  # pyright
    return codecs.SequentialCodec([
        codecs.LambdaCodec(f_nan2num),
        codecs.LambdaCodec(f_clip),
        codecs.SignedIntQuantizer(num_bits=8, pad_encode_to_bytes=16)
    ])


# TODO this state machine is a bit confusing. Maybe just expose the
# whitelist directly to avoid leaky abstractions.
_patched_allgather_process_groups = set()
_raw_allgather_base = ProcessGroup._allgather_base


def disable_compressed_allgathers(pg: Optional[ProcessGroup] = None) -> None:
    """Replaces compressed allgathers with unmodified ones.

    See ~`.enable_compressed_allgathers` for more details.

    Args:
        pg: If `None`, compressed allgathers are disabled for all process
            groups and the whitelist is cleared. If not `None`, `pg`
            is just removed from the whitelist.

    Raises:
        ValueError: If `pg` is not in the whitelist of process groups
            with allgather compression enabled.
    """
    global _allgathers_globally_enabled
    if pg is None:
        _patched_allgather_process_groups.clear()
        ProcessGroup._allgather_base = _raw_allgather_base  # type: ignore
        return
    if pg not in _patched_allgather_process_groups:
        raise ValueError(f'ProcessGroup {pg} not found in whitelist: ' +
                         f'{list(_patched_allgather_process_groups)}')
    _patched_allgather_process_groups.remove(pg)
    # don't accidentally turn on compression for *all* pgs by
    # removing the last element of the whitelist
    if not len(_patched_allgather_process_groups):
        ProcessGroup._allgather_base = _raw_allgather_base  # type: ignore


def enable_compressed_allgathers(pg: Optional[ProcessGroup] = None,
                                 codec: Optional[Codec] = None,
                                 clip_abs_threshold: float = 4) -> None:
    """Turns on 8-bit compression for allgather operations.

    Because this function requires us to monkey patch the `ProcessGroup`
    itself (not particular instances), the function works as follows:

    * When you first call this function, `ProcessGroup` gets monkey patched
    * If given a `ProcessGroup`, that group is added to a whitelist.
    * If there is a non-empty whitelist, ProcessGroup instances not in
        the whitelist will use regular, non-compressed allgathers.

    The subltety here is that, if there was a non-empty whitelist and you
    remove the last group from it via `disable_compressed_allgathers`,
    allgathers remain globally disabled until you call
    `enable_compressed_allgathers` again. This is so that going from a
    non-empty whitelist to an empty one doesn't suddenly turn on compressed
    allgathers for all `ProcessGroup`s.

    Args:
        pg: A `ProcessGroup` whose allgathers should be compressed. If `None`,
        codec: A `turbo._codecs.Codec` to run on the allgather inputs and
            each shard of the allgather outputs. If `None`, a default Codec
            will be used that replaces NaNs and Infs with zeros, clips
            inputs, and then performs 8-bit quantization.
        clip_abs_threshold: In the default codec, inputs will be clipped to
            the range [-clip_abs_threshold, clip_abs_threshold]. The clipping
            is present to deal with uninitialized bytes in FSDP flat buffers.
            If `codec` is not None, this argument has no effect.

    Raises:
        ValueError: If `codec` is `None` but `clip_abs_threshold` is <= 0
    """
    if codec is None:
        if clip_abs_threshold <= 0:
            raise ValueError('clip_abs_threshold must be > 0 if no codec' +
                             f'is provided; got {clip_abs_threshold}')
        codec = _default_compressed_allgather_codec(
            clip_min=-clip_abs_threshold, clip_max=clip_abs_threshold)

    global _patched_allgather_process_groups
    if pg is not None:
        _patched_allgather_process_groups.add(pg)

    @functools.wraps(ProcessGroup._allgather_base)
    def _allgather_base(pg_self: ProcessGroup,
                        out_tensor: torch.Tensor,
                        in_tensor: torch.Tensor,
                        opts: AllgatherOptions,
                        _codec: Codec = codec):

        # just behave normally if this isn't a group we wanted to patch
        whitelisted = pg_self in _patched_allgather_process_groups
        whitelisted = whitelisted or not len(_patched_allgather_process_groups)
        if not whitelisted:
            return _raw_allgather_base(pg_self, out_tensor, in_tensor, opts)

        in_compressed = _codec.encode(in_tensor)
        num_ranks = out_tensor.numel() // in_tensor.numel()
        out_compressed_numel = num_ranks * in_compressed.numel()
        out_compressed = torch.empty(out_compressed_numel,
                                     dtype=in_compressed.dtype,
                                     device=in_compressed.device)

        # allgather_into_tensor still calls pg's _allgather_base:
        # https://github.com/pytorch/pytorch/blob/362bc6d7cbcac57466a52701fac3ba3bfb668000/torch/distributed/distributed_c10d.py#L2811 # noqa
        # the python functional wrapper returns Optional[Work], but the pg
        # itself always returns work
        handle: Work = _raw_allgather_base(pg_self, out_compressed,
                                           in_compressed, opts)

        # decompression callback to run after the async call waits
        def _copy_into_output(_out_compressed: torch.Tensor = out_compressed,
                              _out_raw: torch.Tensor = out_tensor,
                              _num_chunks: int = num_ranks,
                              _codec: Codec = _codec,
                              _handle: Work = handle) -> None:
            handle.wait()
            _out_compressed = _out_compressed.view(_num_chunks, -1)
            _out_raw = _out_raw.view(_num_chunks, -1)
            for c in range(_num_chunks):  # TODO batched decompression kernel
                _codec.decode(_out_compressed[c], out=_out_raw[c])

        if getattr(opts, 'asyncOp', False):  # not an option until torch 2.2
            return SimpleFuture(callback=_copy_into_output)
        _copy_into_output()
        return handle

    ProcessGroup._allgather_base = _allgather_base  # type: ignore
