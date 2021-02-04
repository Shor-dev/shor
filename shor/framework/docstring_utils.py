from abc import ABCMeta
from enum import Enum
from inspect import getdoc
from textwrap import indent


class _Hints(Enum):
    def indent(self, n):
        return indent(self.value, prefix=" " * n)

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class _DocExtender(ABCMeta):
    def __new__(cls, name, bases, spec):
        for key, value in spec.items():
            doc = getattr(value, "__doc__", "{pdoc}")

            try:
                pdoc = getdoc(getattr(bases[0], key))
            except (IndexError, AttributeError):
                pdoc = ""
            try:
                value.__doc__ = doc.format(pdoc=pdoc)
            except AttributeError:
                pass

        if bases:
            pdoc = getattr(bases[0], "__doc__")
            if "__doc__" in spec and spec["__doc__"]:
                spec["__doc__"] = spec["__doc__"].format(pdoc=pdoc)
            else:
                spec["__doc__"] = pdoc

        return ABCMeta.__new__(cls, name, bases, spec)
