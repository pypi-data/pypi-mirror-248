# -*- coding=utf-8 -*-
r"""

"""
import io
import typing as t
from ._dumpers import *


__all__ = ['dumps', 'loads']


T = t.TypeVar("T")


DUMPERS: t.Dict[t.Type, t.Callable[[t.Any, t.Type], bytes]] = {
    int: dump_int,
    float: dump_float,
    str: dump_str,
    bytes: dump_bytes,
    bool: dump_bool,
}

LOADERS: t.Dict[t.Type, t.Callable[[t.BinaryIO, t.Type], t.Any]] = {
    int: load_int,
    float: load_float,
    str: load_str,
    bytes: load_bytes,
    bool: load_bool,
}


def _isbuiltin(tp: t.Type) -> bool:
    return tp.__module__ in {'__builtin__', '__builtins__', 'builtins'}


def dumps(obj: object) -> bytes:
    r"""
    dump an object

    :param obj: object to dump
    :return: dumped data
    """
    t_obj = type(obj)

    stream = io.BytesIO()

    for attr, hint in t.get_type_hints(t_obj).items():
        origin = t.get_origin(hint) or hint
        value = getattr(obj, attr)
        if origin in DUMPERS:
            dumped = DUMPERS[origin](value, hint)
            stream.write(dumped)
        elif _isbuiltin(origin):
            raise ValueError(f"Unsupported builtin type found: {origin.__qualname__}")
        else:
            stream.write(dumps(value))

    return stream.getvalue()


def loads(dump: t.Union[bytes, t.BinaryIO], cls: t.Type[T]) -> T:
    r"""
    reconstruct a dumped object

    :param dump: dumped data or stream of dumped data
    :param cls: object to parse to
    :return: reconstructed object
    """
    if isinstance(dump, bytes):
        dump = io.BytesIO(dump)

    instance = object.__new__(cls)
    # used for problem with object.__new__(list)
    # try:
    #     instance = object.__new__(cls)
    # except TypeError:
    #     instance = cls.__new__(cls)

    for attr, hint in t.get_type_hints(cls).items():
        origin = t.get_origin(hint) or hint
        if origin in LOADERS:
            loaded = LOADERS[origin](dump, hint)
            setattr(instance, attr, loaded)
        elif _isbuiltin(origin):
            raise ValueError(f"Unsupported builtin type found: {origin}")
        else:
            setattr(instance, attr, loads(dump, cls=origin))

    return instance
