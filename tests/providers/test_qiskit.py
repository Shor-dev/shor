import numpy as np
import pytest

from shor.gates import CNOT, H
from shor.layers import Qbits
from shor.operations import Measure
from shor.providers.qiskit.base import QiskitProvider
from shor.quantum import QC

BACKENDS_TO_TEST = ["qasm_simulator", "statevector_simulator", "unitary_simulator", "pulse_simulator"]


@pytest.fixture()
def simple_circuit():
    qc = QC()
    qc.add(Qbits(3))
    qc.add(H(1))
    qc.add(CNOT(1, 0))
    qc.add(Measure([0, 1]))
    return qc


@pytest.mark.usefixtures
class TestQiskitProviderAPI:
    def test_qasm_simulator_runs_circuit(self, simple_circuit):
        job = simple_circuit.run(1024, QiskitProvider(backend="qasm_simulator"))
        result = job.result

        assert result[0] == result["00"], "Indexing broken for simulator"
        assert result[3] == result["11"], "Indexing broken for simulator"

        assert result["00"] > 450 < result[3], "circuit failed with provider:qiskit, backend:qasm_simulator"

    def test_state_vector_simulator(self, simple_circuit):
        # This simulator only runs 1 time, no matter what count you pass.
        job = simple_circuit.run(1024, QiskitProvider(backend="statevector_simulator"))
        result = job.result

        assert sum(result.counts.values()) == 1, "The statevector_simulator is expected to always run 1 shot"
        assert np.allclose(
            result.qiskit_result.get_statevector(),
            [0.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j, 1.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j],
        ) or np.allclose(
            result.qiskit_result.get_statevector(),
            [1.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j],
        )

        assert result[0] == result["00"], "Indexing broken for simulator"
        assert result[3] == result["11"], "Indexing broken for simulator"

        assert result[0] == 1 or result[3] == 1, "One shot, so at least one of the outcomes should happen"

    def test_list_devices(self):
        ibm_provider = QiskitProvider()

        devices = ibm_provider.devices()

        assert len(devices) > 3

    def test_init_device(self):
        for backend_name in BACKENDS_TO_TEST:
            qiskit_provider = QiskitProvider(device=backend_name)

            assert qiskit_provider.device.name() == backend_name

            qiskit_provider = QiskitProvider(backend=backend_name)

            assert qiskit_provider.device.name() == backend_name
