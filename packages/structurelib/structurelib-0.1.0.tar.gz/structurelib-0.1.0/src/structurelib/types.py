# -*- coding=utf-8 -*-
r"""

"""
import typing as _t
from typing import _alias as __alias  # noqa


__all__ = [
    'int8', 'int16', 'int32', 'int64',
    'uint8', 'uint16', 'uint32', 'uint64',
    'float32', 'float64',
    'integer', 'string',
]


class _StructType(_t._SpecialGenericAlias, _root=True):  # noqa
    _nparams: int

    def __getitem__(self, params: _t.Any):
        if params == ():
            return self.copy_with(())
        if not isinstance(params, tuple):
            params = (params,)
        if self._nparams != -1 and len(params) != self._nparams:
            raise TypeError(f"Expected {self._nparams} argument. Got {len(params)}")
        return self.copy_with(params)


# string[nbytes=None]
string: _t.TypeAlias = _StructType(str, 1, inst=True, name="string")
char: _t.TypeAlias = string[1]

# integer[nbytes=None, signed=True]
integer: _t.TypeAlias = _StructType(int, -1, inst=True, name="integer")

# int: _t.TypeAlias = integer[None, True]  # same as builtin-int and integer
int8: _t.TypeAlias = integer[1, True]
int16: _t.TypeAlias = integer[2, True]
int32: _t.TypeAlias = integer[4, True]
int64: _t.TypeAlias = integer[8, True]

uint: _t.TypeAlias = integer[None, False]
uint8: _t.TypeAlias = integer[1, False]
uint16: _t.TypeAlias = integer[2, False]
uint32: _t.TypeAlias = integer[4, False]
uint64: _t.TypeAlias = integer[8, False]

# floating
floating: _t.TypeAlias = _StructType(float, 0, inst=True, name="floating")
float32: _t.TypeAlias = __alias(float, 0, inst=True, name="float32")
float64: _t.TypeAlias = __alias(float, 0, inst=True, name="float64")

# binary[nbytes=None]
binary: _t.TypeAlias = _StructType(bytes, 1, inst=True, name="binary")

byte: _t.TypeAlias = binary[1]

# boolean
boolean: _t.TypeAlias = _StructType(bool, 0, inst=True, name="boolean")
