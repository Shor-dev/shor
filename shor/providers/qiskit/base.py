from typing import List, Union

from qiskit import Aer, execute
from qiskit.providers import BaseBackend, BaseProvider

from shor.errors import ProviderError
from shor.providers.base import Job, Provider, Result
from shor.quantum import QC
from shor.transpilers.qiskit import to_qiskit_circuit
from shor.utils.qbits import int_from_bit_string

DEFAULT_DEVICE = Aer.get_backend("qasm_simulator")
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
            self.device = config.get("backend", DEFAULT_DEVICE)

    def devices(self, **kwargs) -> List[str]:
        return [d.name for d in self.provider.backends(**kwargs)]

    def use_device(self, device: Union[str, BaseBackend], **kwargs) -> bool:
        if type(device) is str:
            self.device = self.provider.get_backend(name=device, **kwargs)
        elif issubclass(device.__class__, BaseBackend):
            self.device = device

        return self.device is not None

    def run(self, circuit: QC, times: int) -> QiskitJob:
        job = execute(to_qiskit_circuit(circuit), self.device, shots=times)

        return QiskitJob(job)

    @property
    def jobs(self) -> List[Job]:
        return list(map(lambda j: QiskitJob(j), self.device.get_jobs()))
