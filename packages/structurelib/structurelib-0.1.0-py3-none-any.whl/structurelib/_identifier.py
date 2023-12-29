# -*- coding=utf-8 -*-
r"""

"""
import hashlib
import typing as t


def struct_identifier(structure: t.Type) -> bytes:
    r"""
    Generate a unique identifier for a structure.
    This can be used to identify what structure is coming next. (e.g. over socket-connections)
    """
    identifier = hashlib.sha256(usedforsecurity=False)

    for attr, hint in t.get_type_hints(structure).items():
        identifier.update(f"{hint.__name__}{t.get_args(hint)}".encode())

    return identifier.digest()
