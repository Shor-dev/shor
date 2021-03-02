from collections import Iterable

from shor.errors import CircuitError
from shor.layers import _Layer


class _Operation(_Layer):
    """Abstract base quantum computing operation class

    Operations can be, but are not in general, pure quantum transformations (Unitary transformations)

    The generalized operaation is any legal quantum computer operation, which can include:
    - Unitary operations
    - Measurement
    - Logic conditioned on measurement
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_gates(self):
        return []


class Measure(_Operation):
    symbol = "measure"

    def __init__(self, *qbits, output_bits=None, axis="z", **kwargs):
        if not qbits:
            qbits = (0,)

        if len(qbits) == 1 and isinstance(qbits[0], Iterable):
            qbits = tuple(qbits[0])

        if output_bits:
            bits = output_bits
        else:
            bits = qbits[:]

        self.qbits = qbits
        self.bits = bits

        if len(bits) > len(qbits):
            raise CircuitError("Attempting to measure more bits than there are qbits.")

        super().__init__(**kwargs, axis=axis)


class Barrier(_Operation):
    symbol = "barrier"

    def __init__(self):
        super().__init__()


# Aliases
M = m = Measure
