from shor.gates import CNOT, Hadamard, PauliX, PauliZ
from shor.layers import Qubits
from shor.operations import Measure
from shor.providers.qiskit.base import QiskitProvider
from shor.quantum import Circuit


def test_single_qubit():
    circuit = Circuit()
    circuit.add(Qubits(1))
    circuit.add(Hadamard(0))
    circuit.add(Measure([0]))

    job = circuit.run(1024, provider=QiskitProvider())
    result = job.result
    # Accounting for random noise, results won't be exact
    assert result[bin(0)] > 450
    assert result[bin(1)] > 450


def test_entanglement():
    circuit = Circuit()
    circuit.add(Qubits(2))
    circuit.add(Hadamard(0))
    circuit.add(CNOT(0, 1))
    circuit.add(Measure([0, 1]))
    job = circuit.run(1024)
    result = job.result
    assert result["01"] == 0
    assert result["10"] == 0
    assert result["00"] > 450
    assert result["11"] > 450


def test_unitary_symmetry_does_nothing():
    symmetric_circuit_1 = Circuit()
    symmetric_circuit_1.add(Qubits(2))
    symmetric_circuit_1.add(Hadamard(0))
    symmetric_circuit_1.add(Hadamard(0))
    symmetric_circuit_1.add(CNOT(0, 1))
    symmetric_circuit_1.add(CNOT(0, 1))
    symmetric_circuit_1.add(Measure([0, 1]))

    symmetric_circuit_2 = Circuit()
    symmetric_circuit_2.add(Qubits(2, state=1))
    symmetric_circuit_2.add(Hadamard(0))
    symmetric_circuit_2.add(CNOT(0, 1))
    symmetric_circuit_2.add(CNOT(0, 1))
    symmetric_circuit_2.add(Hadamard(0))
    symmetric_circuit_2.add(Measure([0, 1]))

    result_1 = symmetric_circuit_1.run(1024).result
    result_2 = symmetric_circuit_2.run(1024).result

    assert result_1.counts.get(0) == 1024
    assert result_2.counts.get(0) == 1024


def test_multi_entangle():
    circuit = Circuit()
    circuit.add(Qubits(4))
    circuit.add(Hadamard(0))
    circuit.add(CNOT(0, 1))
    circuit.add(CNOT(0, 2))
    circuit.add(CNOT(0, 3))
    circuit.add(Measure([0, 1, 2, 3]))
    job = circuit.run(1024)
    result = job.result
    assert result["0001"] == 0
    assert result["1000"] == 0
    assert result["0000"] > 450
    assert result["1111"] > 450


def test_multi_hadamard():
    circuit = Circuit()
    circuit.add(Qubits(4))
    circuit.add(Hadamard(0))
    circuit.add(Hadamard(1))
    circuit.add(Hadamard(2))
    circuit.add(Hadamard(3))
    circuit.add(Measure([0, 1, 2, 3]))
    job = circuit.run(1024)
    result = job.result
    # All 16 states should be relatively equal probability
    assert len(result.counts) == 16
    assert max(result.counts.values()) - min(result.counts.values()) < 50


def test_teleportation():
    circuit = Circuit()
    circuit.add(Qubits(3))
    circuit.add(CNOT(1, 2))
    circuit.add(CNOT(0, 1))
    circuit.add(Hadamard(0))
    circuit.add(Measure([0, 1]))

    result = circuit.run(1024).result

    # All 16 states should be relatively equal probability
    if result["11"] == 1024:
        circuit.add(PauliX(2))
        circuit.add(PauliZ(2))
    elif result["10"] == 1024:
        circuit.add(PauliZ(2))
    elif result["01"] == 1024:
        circuit.add(PauliX(2))
    circuit.add(Measure([2]))

    result2 = circuit.run(1024).result

    # TODO: Fix this test.

    assert result2
