# -*- coding=utf-8 -*-
r"""

"""
import struct
import typing as t
from ..types import *


__all__ = [
    'dump_int', 'load_int',
    'dump_float', 'load_float',
    'dump_str', 'load_str',
    'dump_bytes', 'load_bytes',
    'dump_bool', 'load_bool',
]


def _dump_size(size: int) -> bytes:
    large_flag = 0b10000000
    if not (size & large_flag):
        # size is small enough. save it in one byte and first bit is 0 as flag
        return int.to_bytes(size, 1, "big", signed=False)
    else:
        # size is too big. save it multiple bytes and save that amount in the first byte. mark first bit is 1 as flag
        size_bytes = _dump_int_min(size, signed=False)
        return int.to_bytes(len(size_bytes) | large_flag, 1, "big", signed=False) + size_bytes


def _load_size(stream: t.BinaryIO) -> int:
    large_flag = 0b10000000
    head = stream.read(1)
    size = int.from_bytes(head, "big", signed=False)
    if not (size & large_flag):
        return size
    else:
        length = size ^ large_flag  # removes flag bits
        return int.from_bytes(stream.read(length), "big", signed=False)


def _dump_int_min(value: int, *, signed: bool) -> bytes:
    r"""
    dumps an integer in the smalled possible bytes
    """
    n_bytes = 1
    while True:
        try:
            return int.to_bytes(value, n_bytes, "big", signed=signed)
        except OverflowError:
            n_bytes += 1


def dump_int(value: int, hint: t.TypeAlias) -> bytes:
    args = iter(t.get_args(hint))
    length = next(args, None)
    signed = next(args, True)
    if length is not None:
        return int.to_bytes(value, length, "big", signed=signed)
    else:
        dump = _dump_int_min(value, signed=signed)
        return _dump_size(len(dump)) + dump


def load_int(stream: t.BinaryIO, hint: t.TypeAlias) -> int:
    args = iter(t.get_args(hint))
    length = next(args, None)
    signed = next(args, True)
    if length is not None:
        return int.from_bytes(stream.read(length), "big", signed=signed)
    else:
        length = _load_size(stream=stream)
        return int.from_bytes(stream.read(length), "big", signed=signed)


def dump_float(value: float, hint: t.TypeAlias) -> bytes:
    fmt = '!f' if hint == float32 else '!d'
    return struct.pack(fmt, value)


def load_float(stream: t.BinaryIO, hint: t.TypeAlias) -> float:
    fmt = '!f' if hint == float32 else '!d'
    return struct.unpack(fmt, stream.read(struct.calcsize(fmt)))[0]


def dump_str(value: str, hint: t.TypeAlias) -> bytes:
    args = iter(t.get_args(hint))
    length = next(args, None)
    encoded = value.encode()
    if length is not None:
        if len(encoded) > length:
            raise ValueError(f"{value!r} is longer than {length} bytes")
        return encoded.ljust(length, b'\0')
    else:
        return _dump_size(len(encoded)) + encoded


def load_str(stream: t.BinaryIO, hint: t.TypeAlias) -> str:
    args = iter(t.get_args(hint))
    length = next(args, None)
    if length is not None:
        return stream.read(length).rstrip(b'\0').decode()
    else:
        length = _load_size(stream=stream)
        return stream.read(length).decode()


def dump_bytes(value: bytes, hint: t.TypeAlias) -> bytes:
    args = iter(t.get_args(hint))
    length = next(args, None)
    if length is not None:
        if len(value) > length:
            raise ValueError(f"{value!r} is longer than {length} bytes")
        return value.ljust(length, b'\0')
    else:
        return _dump_size(len(value)) + value


def load_bytes(stream: t.BinaryIO, hint: t.TypeAlias) -> bytes:
    args = iter(t.get_args(hint))
    length = next(args, None)
    if length is not None:
        return stream.read(length).rstrip(b'\0')
    else:
        length = _load_size(stream=stream)
        return stream.read(length)


def dump_bool(value: bool, _hint: t.TypeAlias) -> bytes:
    return b'\x01' if value else b'\x00'


def load_bool(stream: t.BinaryIO, _hint: t.TypeAlias) -> bool:
    return stream.read(1) != b'\x00'
