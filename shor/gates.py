import math

import numpy as np

from shor.layers import _BaseLayer


class _Gate(_BaseLayer):
    """Abstract base quantum gate class

    # Properties
    input_length = valid length of input qubits
    qubits = indices of qubits, to be used as input to gate.
    """

    def __init__(self, *qubits: int, **kwargs):
        super().__init__(**kwargs)
        self.dimension = kwargs.get('dimension', 1)
        self.qubits = qubits if qubits else [0]

        assert all(map(lambda q: type(q) == int, self.qubits))
        assert len(self.qubits) == self.dimension

    def to_gates(self):
        return [self]

    @property
    def num_states(self):
        return np.power(2, self.dimension)


class CNOT(_Gate):
    def __init__(self, *qubits, **kwargs):
        kwargs['dimension'] = 2
        if not qubits:
            qubits = [0, 1]

        super().__init__(*qubits, **kwargs)

    @staticmethod
    def to_matrix() -> np.ndarray:
        return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])


class CSWAP(_Gate):
    def __init__(self, *qubits, **kwargs):
        kwargs['dimension'] = 3
        if not qubits:
            qubits = [0, 1, 2]

        super().__init__(*qubits, **kwargs)

    @staticmethod
    def to_matrix() -> np.ndarray:
        cswap_matrix = np.eye(8)
        cswap_matrix[:, [5, 6]] = cswap_matrix[:, [6, 5]]
        return cswap_matrix


class Hadamard(_Gate):
    def __init__(self, *qubits, **kwargs):
        kwargs['dimension'] = 1
        if not qubits:
            qubits = [0]

        super().__init__(*qubits, **kwargs)

    def to_matrix(self) -> np.ndarray:
        return np.multiply(np.divide(1, np.sqrt(self.num_states)), np.array([[1, 1], [1, -1]]))


class PauliX(_Gate):
    def __init__(self, *qubits, **kwargs):
        kwargs['dimension'] = 1
        if not qubits:
            qubits = [0]

        super().__init__(*qubits, **kwargs)

    @staticmethod
    def to_matrix() -> np.ndarray:
        return np.array([[0, 1], [1, 0]])


class PauliY(_Gate):
    def __init__(self, *qubits, **kwargs):
        kwargs['dimension'] = 1
        if not qubits:
            qubits = [0]

        super().__init__(*qubits, **kwargs)

    @staticmethod
    def to_matrix() -> np.ndarray:
        return np.array([[0, -1j], [1j, 0]])


class PauliZ(_Gate):
    def __init__(self, *qubits, **kwargs):
        kwargs['dimension'] = 1
        if not qubits:
            qubits = [0]

        super().__init__(*qubits, **kwargs)

    @staticmethod
    def to_matrix() -> np.ndarray:
        return np.array([[1, 0], [0, -1]])


class QFT(_Gate):
    def __init__(self, *qubits, **kwargs):
        if not qubits:
            qubits = [0, 1]

        super().__init__(*qubits, dimension=len(qubits), **kwargs)

    # def to_gates(self):
    #     # TODO: translate this gate to base gates / CNOTs
    #     pass

    def get_nth_unity_root(self, k):
        return np.exp((2j * np.pi * k) / self.num_states)

    def to_matrix(self) -> np.ndarray:
        m = np.array(np.ones((self.num_states, self.num_states)), dtype='complex')

        for i in range(1, self.num_states):
            for j in range(i, self.num_states):
                w = self.get_nth_unity_root(i * j)
                m[i, j] = w
                m[j, i] = w

        return np.around(
            np.multiply(
                1 / np.sqrt(self.num_states),
                m
            ), decimals=15)


class Rx(_Gate):
    def __init__(self, *qubits, angle=math.pi/2, **kwargs):
        kwargs['dimension'] = 1
        self.angle=angle
        if not qubits:
            qubits = [0]

        super().__init__(*qubits, **kwargs)

    def to_matrix(self) -> np.ndarray:
        return np.array([
        [math.cos(self.angle / 2), -math.sin(self.angle / 2) * 1j],
        [-math.sin(self.angle / 2) * 1j, math.cos(self.angle / 2)]
    ])


class SWAP(_Gate):
    def __init__(self, *qubits, **kwargs):
        kwargs['dimension'] = 2
        if not qubits:
            qubits = [0, 1]

        super().__init__(*qubits, **kwargs)

    @staticmethod
    def to_matrix() -> np.ndarray:
        return np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])


class U3(_Gate):
    def __init__(self, *qubits, theta,phi,alpha, **kwargs):
        kwargs['dimension'] = 1
        self.theta=theta
        self.phi=phi
        self.alpha=alpha
        if not qubits:
            qubits = [0]

        super().__init__(*qubits, **kwargs)

    def to_matrix(self) -> np.ndarray:
        return np.array([
        [math.cos(self.theta/2), -np.exp(1j*self.alpha)*math.sin(self.theta/2)],
        [np.exp(1j*self.phi)*math.sin(self.theta / 2), np.exp(1j*(self.phi+self.alpha))*math.cos(self.theta / 2)]
    ])
    

class U2(_Gate):
    def __init__(self, *qubits, phi, alpha, **kwargs):
        self.phi = phi
        self.alpha = alpha
        theta = np.pi/2
        self.U3_class = U3(0,theta,self.phi,self.alpha)
    
    def to_matrix(self) -> np.ndarray:
        return self.U3_class.to_matrix()


# Aliases
H = h = Hadamard
X = x = PauliX
Y = y = PauliY
Z = z = PauliZ
swap = SWAP
CX = cx = CNOT
Fredkin = cswap = CSWAP