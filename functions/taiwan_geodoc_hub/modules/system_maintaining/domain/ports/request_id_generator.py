from abc import ABC, abstractmethod


class RequestIdGenerator(ABC):
    @abstractmethod
    def __call__(self) -> str:
        pass
