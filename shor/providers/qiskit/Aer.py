from qiskit.providers.aer import Aer

from shor.providers.qiskit.base import QiskitProvider

DEFAULT_BACKEND = Aer.get_backend("qasm_simulator")


class AerProvider(QiskitProvider):
    def __init__(self, **config):
        config["backend"] = config.get("backend", DEFAULT_BACKEND)
        config["provider"] = Aer
        super().__init__(**config)
