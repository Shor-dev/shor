from qiskit.providers.ibmq import IBMQ

from shor.providers.qiskit.base import QiskitProvider

DEFAULT_BACKEND = "qasm_simulator"


class IBMQProvider(QiskitProvider):
    def __init__(self, **config):
        if not IBMQ.active_account():
            IBMQ.load_account()

        provider = IBMQ.providers()[0] if IBMQ.providers() else None
        config["provider"] = provider

        if "backend" in config:
            if not isinstance(config["backend"], str):
                config["backend"] = provider.get_backend(DEFAULT_BACKEND) if provider and provider.backends() else None

        super().__init__(**config)
