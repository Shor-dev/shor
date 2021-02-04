from qiskit.providers.ibmq import IBMQ as QiskitIBMQ
from qiskit.providers.ibmq import IBMQAccountCredentialsNotFound

from shor.framework.docstring_utils import _Hints
from shor.providers import Aer
from shor.providers.qiskit.base import QiskitProvider

DEFAULT_BACKEND = "qasm_simulator"


class _IBMQHints(_Hints):
    LOGIN = """
To login and remember your IBMQ account use `IBMQ.login(TOKEN, remember=True)`
Your TOKEN can be found at: https://quantum-computing.ibm.com/account
"""


class IBMQ(QiskitProvider):
    __doc__ = f"""{{pdoc}}
    IBMQ quantum computer provider, provided through Qiskit

    An IBMQ Experience account is required to use IBM quantum computers.
    If no account is provided, `{DEFAULT_BACKEND}` will be chosen as the device

    {_IBMQHints.LOGIN.indent(4)}
    """

    def __init__(self, device=DEFAULT_BACKEND, **config):
        IBMQ._try_login_saved_account()
        """
        Initialize an IBMQ provider. Uses Qiskit to run programs on IBMQ quantum computers.

        If you need to access the Qiskit provider directly for any reason, use `.provider`

        :param config: Additional Qiskit provider configuration. Passed along as key word arguments to Qiskit's IBMQ provider
        """
        provider = QiskitIBMQ.providers()[0] if QiskitIBMQ.providers() else Aer

        config["provider"] = provider

        if "backend" in config:
            if not isinstance(config["backend"], str):
                config["backend"] = provider.get_backend(DEFAULT_BACKEND) if provider and provider.backends() else None

        super().__init__(**config)

    @classmethod
    def account(cls) -> str:
        active_account = QiskitIBMQ.active_account()
        if not active_account:
            print("No active account")
        return active_account if active_account else ""

    @classmethod
    def login(cls, token: str = "", remember: bool = False, **kwargs) -> bool:
        if not token:
            return cls._try_login_saved_account()
        else:
            QiskitIBMQ.enable_account(token, **kwargs)
            if remember:
                QiskitIBMQ.save_account(token, **kwargs)

    @classmethod
    def logout(cls, forget: bool = False) -> None:
        if cls.account():
            if forget:
                QiskitIBMQ.delete_account()
            QiskitIBMQ.disable_account()

    @classmethod
    def _try_login_saved_account(cls) -> bool:
        if not QiskitIBMQ.active_account():
            try:
                QiskitIBMQ.load_account()
            except IBMQAccountCredentialsNotFound:
                print(f"No saved account found for IBMQ. Only simulator devices will be available. {_IBMQHints.LOGIN}")
                return False  # Failed login
        return True  # Successful login
