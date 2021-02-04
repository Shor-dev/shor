from typing import List

from qiskit import Aer, execute
from qiskit.providers import BaseProvider

from shor.errors import ProviderError
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
    def __init__(self, device=None, provider=DEFAULT_PROVIDER, **config):

        if not issubclass(provider.__class__, BaseProvider):
            raise ProviderError(
                f"Qiskit Provider improperly initialized - must be a subclass of "
                f"<Qiskit.providers.BaseProvider>. The provided provider is not: {provider}"
            )

        self.provider = provider

        if device:
            self.use_device(device)
        elif "backend" in config:
            # Qiskit uses the language "backend" instead of device, attempt to load this as well
            self.use_device(config["backend"])
        else:
            self.backend = config.get("backend", DEFAULT_BACKEND)

    def devices(self, **kwargs) -> List[str]:
        return self.provider.backends(**kwargs)

    def use_device(self, device: str, **kwargs) -> bool:
        backend = self.provider.get_backend(name=device, **kwargs)
        self.backend = backend
        return backend is not None

    @property
    def account(self) -> str:
        """Accounts not supported for base Qiskit provider, are you looking for `shor.providers.IBMQ`?"""
        return ""

    @classmethod
    def login(cls, token: str, remember: bool = False, **kwargs) -> bool:
        print(
            "Login not implemented for general qiskit provider `shor.providers.QiskitProvider`."
            "Are you looking for IBMQ? Then use `shor.providers.IBMQ`"
        )
        return False

    @classmethod
    def logout(cls, forget: bool = False) -> None:
        print(
            "Logout not supported general qiskit provider `shor.providers.QiskitProvider`."
            "Are you looking for IBMQ? Then use `shor.providers.IBMQ`"
        )

    def run(self, circuit: QC, times: int) -> QiskitJob:
        job = execute(to_qiskit_circuit(circuit), self.backend, shots=times)

        return QiskitJob(job)

    @property
    def jobs(self) -> List[Job]:
        return list(map(lambda j: QiskitJob(j), self.backend.get_jobs()))
