# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from ._dumping import loads, dumps


__all__ = ['Structure', 'make_structure']


T = t.TypeVar("T")


class Structure:
    r"""
    simple wrapper to offer convenient `load_struct` and `dump_struct` methods
    """

    @classmethod
    def load_struct(cls: t.Type[T], dump: t.Union[bytes, t.BinaryIO]) -> T:
        return loads(dump, cls)

    def dump_struct(self) -> bytes:
        return dumps(self)


def make_structure(name: str, attributes: t.Iterable[t.Tuple[str, t.Type]] = None, **struct_attributes: t.Type):
    r"""
    dynamically create a new structure class

    :param name: name of the new structure
    :param attributes: iterable of (attr, type) pairs
    :param struct_attributes: **kwargs way to specify attributes
    :return:
    """
    from dataclasses import make_dataclass
    attributes = list(attributes or [])
    for attr, tp in struct_attributes.items():
        attributes.append((attr, tp))
    return make_dataclass(name, attributes, bases=(Structure,))
