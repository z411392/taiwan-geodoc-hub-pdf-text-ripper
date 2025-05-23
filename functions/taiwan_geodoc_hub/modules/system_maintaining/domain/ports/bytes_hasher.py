from abc import ABC, abstractmethod


class BytesHasher(ABC):
    @abstractmethod
    def __call__(self, /, buffer: bytes) -> str:
        raise NotImplementedError
