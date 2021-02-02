from typing import List

from qiskit import Aer, execute

from shor.providers.base import Job, Provider, Result
from shor.quantum import QC
from shor.transpilers.qiskit import to_qiskit_circuit
from shor.utils.qbits import int_from_bit_string

DEFAULT_BACKEND = Aer.get_backend("qasm_simulator")
DEFAULT_PROVIDER = Aer


class QiskitResult(Result):
    def __init__(self, qiskit_result):
        self.qiskit_result = qiskit_result

    @property
    def counts(self):
        return {int_from_bit_string(k.split(" ")[0]): v for k, v in self.qiskit_result.get_counts().items()}

    @property
    def sig_bits(self):
        measurement_bases = list(self.qiskit_result.get_counts().keys())
        return len(measurement_bases[0]) if measurement_bases else 0


class QiskitJob(Job):
    def __init__(self, qiskit_job):
        self.qiskit_job = qiskit_job

    @property
    def status(self):
        return self.qiskit_job.status()

    @property
    def result(self) -> QiskitResult:
        return QiskitResult(self.qiskit_job.result())


class QiskitProvider(Provider):
    def __init__(self, **config):
        self.provider_delegate = config.get("provider", DEFAULT_PROVIDER)

        if "backend" in config:
            self.load_backend(config["backend"])
        else:
            self.backend = config.get("backend", DEFAULT_BACKEND)

    def backends(self):
        return self.provider_delegate.backends()

    def load_backend(self, backend: str):
        self.backend = self.provider_delegate.get_backend(backend)

    @property
    def jobs(self) -> List[Job]:
        return list(map(lambda j: QiskitJob(j), self.backend.get_jobs()))

    def login(self, token: str, remember: bool = False, **kwargs) -> None:
        self.backend.enable_account(token, **kwargs)
        if remember:
            self.backend.save_account(token, **kwargs)

    def logout(self) -> None:
        self.backend.disable_account()
        self.backend.delete_account()

    def run(self, circuit: QC, times: int) -> QiskitJob:
        job = execute(to_qiskit_circuit(circuit), self.backend, shots=times)

        return QiskitJob(job)
