from typing import Optional
from google.cloud.firestore import Client, CollectionReference, Transaction
from taiwan_geodoc_hub.modules.registration_managing.dtos.ocr_result import OCRResult
from taiwan_geodoc_hub.infrastructure.collections import (
    Collections,
)
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.ocr_result_repository import (
    OCRResultRepository,
)
from injector import inject


class OCRResultAdapter(OCRResultRepository):
    _collection: CollectionReference

    @inject
    def __init__(self, /, db: Client):
        self._collection = db.collection(str(Collections.ocr_results))

    def save(self, ocr_result_id: str, text: str, /, transaction: Transaction):
        document = self._collection.document(ocr_result_id)
        ocr_result = OCRResult(text=text)
        transaction.set(document, ocr_result, merge=True)

    def load(self, ocr_result_id: str, /, transaction: Transaction) -> Optional[str]:
        document = self._collection.document(ocr_result_id)
        document_snapshot = next(iter(transaction.get(document)))
        if not document_snapshot.exists:
            return None
        ocr_result: OCRResult = document_snapshot.to_dict()
        return ocr_result.get("text")
