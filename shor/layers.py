from collections import Iterable


class _Layer(object):
    """Abstract base quantum layer class"""

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "Layer")
        pass

    def to_gates(self):
        pass


class Qbits(_Layer, Iterable):
    def __init__(self, num, state=0, **kwargs):
        self.num = num
        self.state = state
        self._qbits = [(i, self) for i in range(num)]

        super().__init__(name="Qbits ({})".format(str(num)), **kwargs)

    def to_gates(self):
        return []

    def add(self, qbit_list):
        self._qbits += qbit_list

    def __iter__(self):
        return self._qbits.__iter__()

    def __getitem__(self, key):
        return self._qbits[key]


class Cbits(_Layer, Iterable):
    def __init__(self, num, state=0, **kwargs):
        self.num = num
        self.state = state
        self._cbits = [(i, self) for i in range(num)]

        super().__init__(name="Cbits ({})".format(str(num)), **kwargs)

    def to_gates(self):
        return []

    def add(self, cbit_list):
        self._cbits += cbit_list

    def __iter__(self):
        return self._cbits.__iter__()

    def __getitem__(self, key):
        return self._cbits[key]


# Aliases
Qubits = Qbits
