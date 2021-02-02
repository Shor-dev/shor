import random

import pytest

from shor.algorithms.shor import factor, quantum_amod_15
from shor.gates import CNOT, H
from shor.layers import Qbits
from shor.operations import Measure
from shor.providers.qiskit.base import QiskitProvider
from shor.quantum import Circuit, QuantumCircuit

# Seed for tests
random.seed(0)


@pytest.mark.xfail(reason="Not implemented correctly")
def test_shor_factoring():
    N = 3 * 5

    a, b = factor(N)

    assert a == 3 or a == 5
    assert b == N / a

    N = 3 * 7

    a, b = factor(N)

    assert a == 3 or a == 7
    assert b == N / a


def test_modulus_circuit():
    circuit = Circuit()
    circuit.add(Qbits(5))
    circuit.add(quantum_amod_15(4))
    circuit.add(Measure([0, 1]))

    job = circuit.run(1024)
    result = job.result

    print(result)


def test_simons():
    qbits = Qbits(6)

    # Q = QuantumCircuit(qbits)  # Doesn't work, not implemented
    Q = QuantumCircuit().add(qbits)
    Q.add(H(0)).add(H(1)).add(H(2))
    Q.add(CNOT(0, 3)).add(CNOT(1, 4)).add(CNOT(2, 5))
    Q.add(CNOT(1, 4)).add(CNOT(1, 5))
    Q.add(H(0)).add(H(1)).add(H(2))
    Q.add(Measure(qbits[:3]))  # Doesn't work, partial measurements...

    job = Q.run(1000, provider=QiskitProvider())
    result = job.result

    print(result)
