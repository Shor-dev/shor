from abc import ABC, abstractmethod
from enum import Enum
from typing import List

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


class Provider(ABC):
    @property
    @abstractmethod
    def jobs(self) -> List[Job]:
        pass

    @abstractmethod
    def login(self, token: str) -> bool:
        pass

    @abstractmethod
    def logout(self):
        pass

    @abstractmethod
    def run(self, circuit: QuantumCircuit, times: int) -> Job:
        pass
