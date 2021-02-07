from abc import ABC, abstractmethod
from enum import Enum
from typing import List

from shor.framework.docstring import _DocExtender
from shor.quantum import QuantumCircuit
from shor.utils.qbits import int_from_bit_string, int_to_bit_string


class Result(ABC):
    @property
    @abstractmethod
    def counts(self):
        pass

    @property
    @abstractmethod
    def sig_bits(self):
        pass

    def get(self, key, default=0):
        if isinstance(key, str):
            idx = int_from_bit_string(key)
        else:
            idx = key

        return self.counts.get(idx, default)

    def __getitem__(self, item):
        return self.get(item)

    def __repr__(self):
        return repr({int_to_bit_string(k, sig_bits=self.sig_bits): v for k, v in self.counts.items()})


class JobStatusCode(Enum):
    COMPLETED = ("completed",)
    ERROR = ("error",)
    RUNNING = ("running",)
    WAITING = "waiting"


class JobStatus(object):
    def __init__(self, code: JobStatusCode, message: str = "", api_error_code: int = None):
        self.code = code
        self.message = message
        self.api_error_code = api_error_code


class Job(ABC):
    @property
    @abstractmethod
    def result(self):
        pass

    @property
    @abstractmethod
    def status(self):
        pass


class Provider(metaclass=_DocExtender):
    """Shor quantum computing providers support:
    - Running shor `QuantumCircuits`
    - Keeping track of running programs (jobs)
    - Listing and selecting devices
    - (Optional) Login and logout

    """

    @abstractmethod
    def devices(self) -> List[str]:
        """List available devices (quantum computers or simulators) for provider
        :return: A list of device names
        """
        pass

    @abstractmethod
    def use_device(self, device: str) -> bool:
        """Choose active device for provider. See `devices()` to list available devices
        :param device: the name of the desired quantum computer or similator
        :return: whether or not operation was successful
        """
        pass

    @abstractmethod
    def run(self, circuit: QuantumCircuit, times: int) -> Job:
        pass

    @property
    @abstractmethod
    def jobs(self) -> List[Job]:
        pass


class WithLoginMixin(metaclass=_DocExtender):
    @abstractmethod
    def account(self) -> str:
        """Shows active account credentials, if logged in."""
        pass

    @abstractmethod
    def login(self, token: str, remember: bool = False, **kwargs) -> bool:
        """Login to provider with API token.

        :param token: API token
        :param remember: Flag to save credentials to file system for future use
        :param kwargs: Additional params to pass to the downstream provider login function
        :return: boolean if login was successful
        """
        pass

    @abstractmethod
    def logout(self, forget: bool = False) -> None:
        """Logout of provider.

        :param forget: Param to forget saved credentials
        """
        pass
