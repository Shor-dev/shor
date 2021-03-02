import math

import numpy as np
import pytest

from shor.gates import (
    CCNOT,
    CH,
    CNOT,
    CRZ,
    CY,
    ID,
    QFT,
    SWAP,
    U1,
    U2,
    U3,
    Cr,
    CRk,
    Cx,
    Cz,
    H,
    Hadamard,
    Init_x,
    Init_y,
    PauliX,
    PauliY,
    PauliZ,
    Rx,
    Ry,
    Rz,
    S,
    Sdg,
    T,
    Tdg,
    X,
)
from shor.layers import Cbits, Qbits, Qubits
from shor.operations import Barrier, Measure
from shor.providers import QiskitProvider
from shor.quantum import QC, Circuit


def test_ch_integration():
    circuit = Circuit()
    circuit.add(Qubits(2))
    circuit.add(PauliX(0))
    circuit.add(PauliX(1))
    circuit.add(CH(0, 1))
    circuit.add(Measure(0, 1))

    job = circuit.run(1024)
    result = job.result
    assert result["11"] > 450
    assert result["00"] == 0
    assert result["10"] == 0
    assert result["01"] > 450


def test_crz_integration():
    circuit = Circuit()
    circuit.add(Qubits(2))
    circuit.add(CRZ(0, 1, angle=math.pi / 3))
    circuit.add(Measure(0, 1))
    job = circuit.run(1024)
    result = job.result
    assert result["11"] == 0
    assert result["00"] == 1024
    assert result["10"] == 0
    assert result["01"] == 0


def test_dblpx_integration():
    circuit = Circuit()
    circuit.add(Qubits(2))
    circuit.add(PauliX(0))
    circuit.add(PauliX(1))
    circuit.add(Measure(0, 1))
    job = circuit.run(1024)
    result = job.result
    assert result["11"] == 1024
    assert result["00"] == 0
    assert result["10"] == 0
    assert result["01"] == 0


def test_swap_integration():
    circuit = Circuit()
    circuit.add(Qubits(2))
    circuit.add(PauliX(0))
    circuit.add(SWAP(0, 1))
    circuit.add(Measure([0, 1]))
    job = circuit.run(1024)
    result = job.result
    assert result["11"] == 0
    assert result["00"] == 0
    assert result["01"] == 0
    assert result["10"] == 1024


def test_ccnot_integration():
    circuit = Circuit()
    circuit.add(Qubits(3))
    circuit.add(PauliX(0))
    circuit.add(PauliX(1))
    circuit.add(CCNOT(0, 1, 2))
    circuit.add(Measure([0, 1, 2]))
    job = circuit.run(1024)
    result = job.result

    assert result["000"] == 0
    assert result["001"] == 0
    assert result["010"] == 0
    assert result["100"] == 0
    assert result["110"] == 0
    assert result["101"] == 0
    assert result["011"] == 0
    assert result["111"] == 1024


def test_s_integration():
    circuit = Circuit()
    circuit.add(Qubits(1))
    circuit.add(S(0))  # Can also use H()
    circuit.add(Measure([0]))
    job = circuit.run(1024)
    result = job.result
    assert result["0"] == 1024
    assert result["1"] == 0


def test_sdg_integration():
    circuit = Circuit()
    circuit.add(Qubits(1))
    circuit.add(PauliX(0))
    circuit.add(Sdg(0))  # Can also use H()
    circuit.add(Measure([0]))
    job = circuit.run(1024)
    result = job.result
    assert result["1"] == 1024
    assert result["0"] == 0


def test_t_integration():
    circuit = Circuit()
    circuit.add(Qubits(1))
    circuit.add(T(0))  # Can also use H()
    circuit.add(Measure([0]))
    job = circuit.run(1024)
    result = job.result
    assert result["0"] == 1024
    assert result["1"] == 0


def test_tdg_integration():
    circuit = Circuit()
    circuit.add(Qubits(1))
    circuit.add(PauliX(0))
    circuit.add(Tdg(0))
    circuit.add(Measure([0]))
    job = circuit.run(1024)
    result = job.result
    assert result["1"] == 1024
    assert result["0"] == 0


def test_paulix_integration():
    circuit = Circuit()
    circuit.add(Qubits(1))
    circuit.add(PauliX(0))  # Can also use H()
    circuit.add(Measure([0]))
    job = circuit.run(1024)
    result = job.result
    # Accounting for random noise, results won't be exact
    assert result["0"] == 0
    assert result["1"] == 1024


def test_pauliy_integration():
    circuit = Circuit()
    circuit.add(Qubits(1))
    circuit.add(PauliY(0))  # Can also use H()
    circuit.add(Measure([0]))
    job = circuit.run(1024)
    result = job.result
    # Accounting for random noise, results won't be exact
    assert result["0"] == 0
    assert result["1"] == 1024


def test_pauliz_integration():
    circuit = Circuit()
    circuit.add(Qubits(1))
    circuit.add(Hadamard(0))
    circuit.add(PauliZ(0))  # Can also use H()
    circuit.add(Measure([0]))
    job = circuit.run(1024)
    result = job.result
    # Accounting for random noise, results won't be exact
    assert result["0"] > 450
    assert result["1"] > 450


def test_id_qubit():
    circuit = Circuit()
    circuit.add(Qubits(1))
    circuit.add(ID(0))
    circuit.add(Measure([0]))
    job = circuit.run(1024)
    result = job.result
    # Accounting for random noise, results won't be exact
    assert result["1"] == 0
    assert result["0"] == 1024


def test_u1_integration():
    circuit = Circuit()
    circuit.add(Qubits(1))
    circuit.add(PauliX(0))
    circuit.add(U1(0))
    circuit.add(Measure([0]))
    job = circuit.run(1024)
    result = job.result
    assert result["0"] == 0
    assert result["1"] == 1024


def test_cx_int():
    circuit_1 = Circuit()
    circuit_1.add(Qubits(2))
    circuit_1.add(Hadamard(0))
    circuit_1.add(Cx(0, 1))
    circuit_1.add(Measure([0, 1]))

    circuit_2 = Circuit()
    circuit_2.add(Qubits(2))
    circuit_2.add(Hadamard(1))
    circuit_2.add(Cx(0, 1))
    circuit_2.add(Measure([0, 1]))
    result_1 = circuit_1.run(1024).result
    result_2 = circuit_2.run(1024).result

    assert result_1["01"] == 0
    assert result_1["10"] == 0
    assert result_1["00"] > 450
    assert result_1["11"] > 450

    assert result_2["01"] == 0
    assert result_2["10"] > 450
    assert result_2["00"] > 450
    assert result_2["11"] == 0


def test_cz_int():
    circuit = Circuit()
    circuit.add(Qubits(2))
    circuit.add(Hadamard(0))
    circuit.add(Hadamard(1))
    circuit.add(Cz(0, 1))
    circuit.add(Measure([0, 1]))
    job = circuit.run(1000)
    result = job.result
    assert result["00"] > 210
    assert result["01"] > 210
    assert result["10"] > 210
    assert result["11"] > 210


def test_cr_int():
    circuit = Circuit()
    circuit.add(Qubits(2))
    circuit.add(Cr(0, 1, angle=np.pi / 2))
    circuit.add(Measure(0, 1))

    result = circuit.run(1000).result

    assert result["00"] == 1000
    assert result["01"] == 0
    assert result["10"] == 0
    assert result["11"] == 0


@pytest.mark.xfail(reason="Not implemented by qiskit. Quantum-inspire does implement this")
def test_crk_int():
    circuit = Circuit()
    circuit.add(Qubits(2))
    circuit.add(CRk(0, 1, k=2))
    circuit.add(Measure(0, 1))

    result = circuit.run(1000).result

    assert result["00"] == 1000
    assert result["01"] == 0
    assert result["10"] == 0
    assert result["11"] == 0


def test_ry_int():
    circuit = Circuit()
    circuit.add(Qubits(1))
    circuit.add(Ry(0, angle=np.pi / 2))
    circuit.add(Measure([0]))
    job = circuit.run(1000)
    result = job.result

    assert result["0"] > 450
    assert result["1"] > 450


def test_rz_int():
    circuit = Circuit()
    circuit.add(Qubits(1))
    circuit.add(Rz(0, angle=np.pi / 2))
    circuit.add(Measure([0]))
    job = circuit.run(1000)
    result = job.result

    assert result["0"] == 1000
    assert result["1"] == 0


def test_u3_int():
    circuit_1 = Circuit()
    circuit_1.add(Qubits(1))
    circuit_1.add(U3(0, theta=np.pi / 2, phi=-np.pi / 2, lam=np.pi / 2))
    circuit_1.add(Measure([0]))

    circuit_2 = Circuit()
    circuit_2.add(Qubits(1))
    circuit_2.add(Rx(theta=np.pi))
    circuit_2.add(Measure([0]))
    result_1 = circuit_1.run(1024).result
    result_2 = circuit_2.run(1024).result

    assert result_1["0"] > 450
    assert result_1["1"] > 450
    assert result_2["0"] > 450
    assert result_2["1"] > 450


def test_u2_int():
    circuit_1 = Circuit()
    circuit_1.add(Qubits(1))
    circuit_1.add(U2(0, phi=-np.pi / 2, alpha=np.pi / 2))
    circuit_1.add(Measure([0]))
    result_1 = circuit_1.run(1024).result

    assert result_1["0"] > 450
    assert result_1["1"] > 450


def test_multi_gate_int():
    circuit_1 = Circuit()
    circuit_1.add(Qubits(2))
    circuit_1.add(PauliX(0))
    circuit_1.add(CNOT(0, 1))
    circuit_1.add(CH(0, 1))
    circuit_1.add(Measure(0, 1))

    result_1 = circuit_1.run(1024).result

    assert result_1["00"] == 0
    assert result_1["11"] > 450
    assert result_1["01"] > 450
    assert result_1["10"] == 0
    # I don't know if im screwing something up here or if the index order is wrong


def test_switch_input_int():
    circuit_1 = Circuit()
    circuit_1.add(Qubits(2))
    circuit_1.add(PauliX(0))
    circuit_1.add(CNOT(1, 0))
    circuit_1.add(Measure(0, 1))

    result_1 = circuit_1.run(1024).result

    assert result_1["00"] == 0
    assert result_1["11"] == 0
    assert result_1["01"] == 1024
    assert result_1["10"] == 0


@pytest.mark.xfail(reason="Not implemented by qiskit. Quantum-inspire does implement this")
def test_initx_int():
    circuit_1 = Circuit()
    circuit_1.add(Qubits(1))
    circuit_1.add(Init_x(0))
    circuit_1.add(Measure(0))

    result_1 = circuit_1.run(1024).result

    assert result_1["0"] > 450
    assert result_1["1"] > 450


@pytest.mark.xfail(reason="Not implemented by qiskit. Quantum-inspire does implement this")
def test_inity_int():
    circuit_1 = Circuit()
    circuit_1.add(Qubits(1))
    circuit_1.add(Init_y(0))
    circuit_1.add(Measure([0]))

    result_1 = circuit_1.run(1024).result

    assert result_1["0"] > 450
    assert result_1["1"] > 450


@pytest.mark.xfail(reason="Not implemented by qiskit. Quantum-inspire does implement this")
def test_QFT():
    qbits = Qbits(4)
    X = Circuit()
    X.add(qbits)
    X.add(H(0)).add(H(1)).add(H(2)).add(H(3))
    X.add(QFT(0, 1, 2, 3))
    X.add(Measure([0, 1, 2, 3]))
    #
    # qc2 = QuantumCircuit() + H(qbits[0]) + X(qbits[1])
    #
    # qbits = Qbits(4)
    # qc = H(qbits) * QFT(qbits)
    #
    # qc += QFT(qbits[0:3])
    # qc += qc2
    #
    # qc.add(H())
    #
    # qc = H(qc[0:3])
    # qc = Z(qc[1])
    #
    # qbits = Qbits(4)
    # cbits = Cbits(4)
    #
    # qc = QuantumCircuit(qbits=qbits, cbits=cbits)
    # -> err
    # qc += Hadamard(qbits[0]) + Z(qbits[1])
    #
    # qc.add(Measure([qbits[0]]))
    # qc += Measure(qbits[0])
    #
    # qc.add(Measure(qbits), name='Output')

    # X = Circuit(qbits)
    # X = H(X)
    # Y = Z(X)
    # A = H(X)
    #
    # qbits = Qbits(4)
    # X = Circuit() + qbits + H(qbits) + QFT(qbits) + Measure(qbits)
    #
    # Y = X.run(QuantumSimulator, times=100)
    job = X.run(1024)
    result = job.result
    assert result
    # plot_results(result)


def test_cy_int():
    circuit_1 = Circuit()
    circuit_1.add(Qubits(2))
    circuit_1.add(PauliX(0))
    circuit_1.add(CY(0, 1))
    circuit_1.add(Measure(0, 1))

    result_1 = circuit_1.run(1024).result

    assert result_1["00"] == 0
    assert result_1["11"] == 1024
    assert result_1["10"] == 0
    assert result_1["01"] == 0


def test_cz2_int():
    circuit_1 = Circuit()
    circuit_1.add(Qubits(2))
    circuit_1.add(PauliX(0))
    circuit_1.add(Cz(0, 1))
    circuit_1.add(Measure(0, 1))

    result_1 = circuit_1.run(1024).result

    assert result_1["00"] == 0
    assert result_1["11"] == 0
    assert result_1["01"] == 1024
    assert result_1["10"] == 0


def test_mult_gate_inputs1():
    circuit_1 = Circuit()
    circuit_1.add(Qubits(2))
    circuit_1.add(H([0, 1]))
    circuit_1.add(Measure(0, 1))

    result_1 = circuit_1.run(1024).result

    assert result_1["00"] > 215
    assert result_1["11"] > 215
    assert result_1["10"] > 215
    assert result_1["01"] > 215


def test_quantum_multi_hadamard_partial_measure():
    circuit_1 = Circuit()
    circuit_1.add(Qubits(4))
    circuit_1.add(H(range(4)))
    circuit_1.add(Measure(0, 1))

    result_1 = circuit_1.run(1024).result

    print(result_1.counts)

    assert all(r > 215 for r in [result_1["0000"], result_1["0001"], result_1["0010"], result_1["0011"]])

    # Ony measuring the 2 right-most qbits. Shouldn't see measurements for other qbits.
    assert result_1["1000"] == result_1["1001"] == result_1["1010"] == result_1["1011"] == 0
    assert result_1["1100"] == result_1["1101"] == result_1["1110"] == result_1["1111"] == 0
    assert result_1["0100"] == result_1["0101"] == result_1["0110"] == result_1["0111"] == 0


def test_grover_search_for_6():
    grover = Circuit()
    grover.add(Qubits(3))
    grover.add(H(range(3)))

    for i in range(2):
        grover.add(H(2))
        grover.add(PauliX(0))
        grover.add(CCNOT(0, 1, 2))
        grover.add(PauliX(0))
        grover.add(H(2))

        grover.add(H(range(3)))
        grover.add(PauliX(range(3)))
        grover.add(H(2))
        grover.add(CCNOT(0, 1, 2))
        grover.add(H(2))
        grover.add(PauliX(range(3)))
        grover.add(H(range(3)))

    grover.add(Measure(0, 1, 2))
    job = grover.run(1024, QiskitProvider(backend="qasm_simulator"))
    result = job.result

    assert result[6] > 900
    assert result[0] < 25
    assert result[1] < 25
    assert result[2] < 25
    assert result[3] < 25
    assert result[4] < 25
    assert result[5] < 25


@pytest.mark.xfail(reason="Don't have capability to multiple qbit classes in one QC and index between them")
def test_mlt_qbit_mlt_cbit1():
    qbits1 = Qbits(1)
    qbits2 = Qbits(1)
    circ = QC()
    circ.add(qbits1)
    circ.add(qbits2)
    circ.add(H(qbits1))
    circ.add(X(qbits2[2]))
    circ.add(Measure(qbits1[0], qbits2[1], Cbits[2]))

    result = X.run(200).result
    assert result["01"] > 180
    assert result["11"] > 180


def test_mlt_qbit_mlt_cbit3():
    qbits1 = Qbits(1)
    qbits2 = Qbits(2)
    circ = QC()
    circ.add(qbits1)
    circ.add(qbits2)
    circ.add(H(0))
    circ.add(X(1))
    circ.add(CH(1, 2))
    circ.add(Measure(0, 1, output_bits=[0, 1]))

    result = circ.run(1000).result
    print(result)
    assert result["10"] > 450
    assert result["11"] > 450


def test_mlt_qbit_mlt_cbit4():
    qbits1 = Qbits(1)
    qbits2 = Qbits(3)
    circ = QC()
    circ.add(qbits1)
    circ.add(qbits2)
    circ.add(Cbits(3))
    circ.add(H(0))
    circ.add(X(1))
    circ.add(CH(1, 2))
    circ.add(Measure(0, 1, output_bits=[0, 1]))

    result = circ.run(1000).result
    print(result)
    assert result["10"] > 450
    assert result["11"] > 450


def test_partial_teleportation():
    teleportation_circuit = Circuit()
    teleportation_circuit.add(Qubits(3))
    teleportation_circuit.add(Cbits(2))  # Should be able to Circuit.add(Qubits(3),Cbits(2))
    teleportation_circuit.add(X(0))
    teleportation_circuit.add(H(1))
    teleportation_circuit.add(CNOT(1, 2))
    teleportation_circuit.add(Barrier())
    teleportation_circuit.add(CNOT(0, 1))
    teleportation_circuit.add(H(0))
    teleportation_circuit.add(Barrier())
    teleportation_circuit.add(Measure(0, 1))
    job = teleportation_circuit.run(1024, QiskitProvider(backend="qasm_simulator"))
    result = job.result

    assert result["00"] > 225
    assert result["01"] > 225
    assert result["10"] > 225
    assert result["11"] > 225
