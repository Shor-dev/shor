from collections import deque
from functools import lru_cache
from typing import List, Deque, NamedTuple, Tuple, Dict

import numpy as np

from shor.gates import _Gate
from shor.quantum import Circuit


class _GateTuple(NamedTuple):
    qubits: List[int]
    matrix: np.ndarray


class _QuantumBackend(object):
    def run(self, initial_state, gates, measure_bits):
        pass


class QuantumSimulator(_QuantumBackend):

    @staticmethod
    @lru_cache(maxsize=10)
    def combine_gates(gates: Tuple[_Gate]) -> _GateTuple:
        to_combine: Deque[_GateTuple] = deque(_GateTuple(g.qubits, g.to_matrix()) for g in gates)
        combined: Deque[_GateTuple] = deque()

        while len(to_combine) > 1:
            while len(to_combine) > 1:
                gate1 = to_combine.popleft()
                gate2 = to_combine.popleft()

                can_combine_no_tensor = set(gate1.qubits) == set(gate2.qubits)
                can_combine_with_tensor = not any(q in gate2.qubits for q in gate1.qubits)

                if can_combine_no_tensor:
                    combined.append(_GateTuple(
                        gate1.qubits,
                        change_qubit_order(gate2.matrix, gate2.qubits, gate1.qubits).dot(gate1.matrix)
                    ))
                elif can_combine_with_tensor:
                    combined.append(_GateTuple(
                        gate1.qubits + gate2.qubits,
                        np.kron(
                            gate1.matrix,
                            gate2.matrix
                        )
                    ))
                else:
                    common_qubits = [q for q in gate1.qubits if q in gate2.qubits]
                    q1_only_qubits = [q for q in gate1.qubits if q not in common_qubits]
                    q2_only_qubits = [q for q in gate2.qubits if q not in common_qubits]
                    all_qubits = q1_only_qubits + common_qubits + q2_only_qubits

                    # Gate 1
                    # Rearrange gates so common qubits are on right side of gate 1
                    new_gate1_qubit_order = q1_only_qubits + common_qubits
                    new_gate1 = change_qubit_order(gate1.matrix, gate1.qubits, new_gate1_qubit_order)

                    # Tensor product with I to fill remaining qubits
                    num_qubits_to_add = len(all_qubits) - len(gate1.qubits)
                    if num_qubits_to_add > 0:
                        new_gate1 = np.kron(new_gate1, np.eye(np.power(2, num_qubits_to_add)))

                    # Gate 2
                    # Rearrange gates so common qubits are on left side of gate 2
                    new_gate2_qubit_order = common_qubits + q2_only_qubits
                    new_gate2 = change_qubit_order(gate2.matrix, gate2.qubits, new_gate2_qubit_order)

                    # Tensor product with I to fill remaining qubits
                    num_qubits_to_add = len(all_qubits) - len(gate2.qubits)
                    if num_qubits_to_add > 0:
                        new_gate2 = np.kron(np.eye(np.power(2, num_qubits_to_add)), new_gate2)

                    combined.append(_GateTuple(
                        all_qubits,
                        new_gate2.dot(new_gate1)
                    ))

            to_combine = combined

        return to_combine.pop()

    def run(self, initial_state: np.ndarray, gates: List[_Gate], measure_bits: List[int]):
        combined = self.combine_gates(tuple(gates))
        new_qubit_order = combined.qubits
        state_vector = get_entangled_initial_state(initial_state, new_qubit_order)

        probabilities = np.square(combined.matrix.dot(state_vector)).real
        probabilities /= np.sum(probabilities)#,dtype='float')
        assert np.sum(probabilities) == 1
        return np.random.choice(state_vector.shape[0], p=probabilities)


class QSession(object):
    def __init__(self, **kwargs):
        self.backend = kwargs.get('backend', QuantumSimulator())

    def run(self, circuit: Circuit, **kwargs):
        num_shots = kwargs.get('num_shots', 1024)

        initial_state = circuit.initial_state()
        gates = circuit.to_gates()
        measure_bits = circuit.measure_bits()

        counts = {}

        for i in range(num_shots):
            state = self.backend.run(initial_state, gates, measure_bits)
            counts[state] = counts.get(state, 0) + 1

        return QResult(counts, sig_bits=len(circuit.initial_state()))


class QResult(object):
    def __init__(self, counts: Dict[int, int], sig_bits: int):
        self.counts: Dict[int, int] = counts
        self.sig_bits: int = sig_bits

    def get(self, key, default=0):
        if isinstance(key, str):
            idx = int_from_bit_string(key)
        else:
            idx = key

        return self.counts.get(idx, default)

    def __getitem__(self, item):
        return self.get(item)

    def __repr__(self):
        return repr({int_to_bit_string(k, self.sig_bits): v for k, v in self.counts.items()})


def get_entangled_initial_state(initial_state, new_qubit_order):
    states_to_entangle: Deque[np.ndarray] = deque()

    states = list(map(lambda s: np.asarray([1 if s == 0 else 0, 1 if s == 1 else 0]), initial_state))

    for q in new_qubit_order:
        states_to_entangle.append(states[q])

    while len(states_to_entangle) > 1:
        entangled_states: Deque[np.ndarray] = deque()
        while len(states_to_entangle) > 1:
            entangled_states.append(np.kron(states_to_entangle.popleft(), states_to_entangle.popleft()))
        if len(states_to_entangle) == 1:
            entangled_states.append(states_to_entangle.popleft())
        states_to_entangle = entangled_states

    return states_to_entangle.pop()


def change_qubit_order(matrix: np.ndarray, old_order, new_order) -> np.ndarray:
    reorder_qubits = [new_order.index(q2) for q2 in old_order]
    initial_row_order = [i for i in range(np.power(2, len(old_order)))]

    reorder_rows = list(map(lambda i: rearrange_bits(i, reorder_qubits), initial_row_order))

    return matrix[reorder_rows][:, reorder_rows]


def rearrange_bits(num: int, new_bit_order: List[int]):
    sig_bits = len(new_bit_order)
    bit_string = int_to_bit_string(num, sig_bits)
    result = int_from_bit_string(''.join(bit_string[-b] for b in new_bit_order))
    return result


def int_to_bits(num: int, sig_bits: int) -> str:
    return format(num, '#0%sb' % np.power(2, sig_bits))


def int_from_bit_string(bits: str) -> int:
    return int(bits, 2) if bits.startswith('0b') else int('0b' + bits, 2)


def int_to_bit_string(i: int, sig_bits: int) -> str:
    return '{0:b}'.format(i).zfill(sig_bits)
