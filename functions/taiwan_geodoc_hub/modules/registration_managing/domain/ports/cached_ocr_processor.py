from abc import ABC, abstractmethod


class CachedOCRProcessor(ABC):
    @abstractmethod
    async def __call__(self, image: bytes, language: str = "cht") -> str:
        raise NotImplementedError
