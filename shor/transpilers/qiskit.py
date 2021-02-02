from qiskit import QuantumCircuit

from shor.layers import _Layer
from shor.operations import _Operation
from shor.quantum import QC


def to_qiskit_circuit(shor_circuit: QC) -> QuantumCircuit:
    qiskit_circuit = QuantumCircuit(
        len(shor_circuit.initial_state()),
        len(shor_circuit.measure_bits()),
    )

    for gate_or_op in shor_circuit.to_gates(include_operations=True):
        transpile_gate(qiskit_circuit, gate_or_op)

    return qiskit_circuit


def to_qiskit_symbol(shor_layer: _Layer) -> str:
    return shor_layer.symbol.lower()


def transpile_gate(qiskit_circuit: QuantumCircuit, shor_layer: _Layer):
    symbol = to_qiskit_symbol(shor_layer)

    if isinstance(shor_layer, _Operation):
        if symbol == "measure":
            if len(shor_layer.qbits) == len(shor_layer.bits) == qiskit_circuit.size():
                qiskit_circuit.measure_active()
            else:
                for qbit, bit in zip(shor_layer.qbits, shor_layer.bits):
                    qiskit_circuit.measure(qbit, bit)

        return

    args = []
    kwargs = {}

    if symbol in ["crx", "cry", "crz", "cu1", "rx", "ry", "rz", "u1"]:
        args.append(shor_layer.angle)
    if symbol in ["u", "u3"]:
        args.append(shor_layer.theta)
    if symbol in ["u", "u2", "u3"]:
        args.append(shor_layer.phi)
        args.append(shor_layer.lam)

    args.extend(shor_layer.qbits)
    qiskit_circuit.__getattribute__(symbol)(*args, **kwargs)
