from abc import ABC, abstractmethod


class OCRProcessor(ABC):
    @abstractmethod
    def __call__(self, image: bytes, language: str = "cht") -> str:
        raise NotImplementedError
