from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass

from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor(8)

@dataclass(frozen=True)
class Context:
    client_provider: object


class Collector(ABC):
    @abstractmethod
    def collect(self, context: Context):
        pass


def collector(fn):
    class _Cls(Collector):
        def collect(self, context: Context):
            return fn(context)
    return _Cls
