from abc import ABC, abstractmethod
from google.cloud.firestore import Transaction


class OCRResultRepository(ABC):
    @abstractmethod
    def load(self, ocr_result_id: str, transaction: Transaction) -> str:
        raise NotImplementedError

    @abstractmethod
    def save(self, ocr_result_id: str, text: str, transaction: Transaction):
        raise NotImplementedError
