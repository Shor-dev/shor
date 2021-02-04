from qiskit.providers.aer import Aer as QiskitAer

from shor.providers.qiskit.base import QiskitProvider

DEFAULT_BACKEND = "qasm_simulator"


class Aer(QiskitProvider):
    def __init__(self, **config):
        config["backend"] = config.get("backend", DEFAULT_BACKEND)
        config["provider"] = QiskitAer
        super().__init__(**config)
