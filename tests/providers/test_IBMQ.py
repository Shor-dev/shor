import pytest
from qiskit import IBMQ as QiskitIBMQ
from qiskit.providers import QiskitBackendNotFoundError

from shor.gates import CNOT, H
from shor.layers import Qbits
from shor.operations import Measure
from shor.providers.qiskit.ibmq import IBMQ
from shor.quantum import QC

BACKENDS_TO_TEST = [
    "ibmq_qasm_simulator",
    "ibmqx2",
    "ibmq_16_melbourne",
    "ibmq_vigo",
    "ibmq_ourense",
    "ibmq_valencia",
    "ibmq_armonk",
    "ibmq_athens",
    "ibmq_santiago",
]


@pytest.mark.skipif(lambda: not QiskitIBMQ.active_account(), reason="Only works if you are logged into IBMQ")
class TestIBMQProviderAPI:
    @classmethod
    def setup_class(cls):
        QiskitIBMQ.load_account()

    def test_circuit_on_simulator(self):
        qc = QC()
        qc.add(Qbits(3))
        qc.add(H(1))
        qc.add(CNOT(1, 0))
        qc.add(Measure([0, 1]))

        ibm_provider = IBMQ()
        job = qc.run(1024, ibm_provider)
        result = job.result
        counts = result.counts
        assert counts[0] > 450 < counts[3]

    def test_list_backends(self):
        ibm_provider = IBMQ()

        backends = ibm_provider.backends()
        assert len(backends) > 5

    def test_init_backend(self):
        for backend_name in BACKENDS_TO_TEST:
            try:
                ibm_provider = IBMQ(backend=backend_name)
            except QiskitBackendNotFoundError:
                raise Exception(f"Backend not found: {backend_name}")

            assert ibm_provider.backend.name() == backend_name
