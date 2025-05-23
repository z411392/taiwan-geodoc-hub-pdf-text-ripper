from taiwan_geodoc_hub.modules.registration_managing.domain.ports.cached_ocr_processor import (
    CachedOCRProcessor,
)
from injector import inject
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.ocr_processor import (
    OCRProcessor,
)
from google.cloud.firestore import Client, transactional, Transaction
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.ocr_result_repository import (
    OCRResultRepository,
)
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.bytes_hasher import (
    BytesHasher,
)


class PerformOCR(CachedOCRProcessor):
    _ocr_processor: OCRProcessor
    _db: Client
    _ocr_result_repository: OCRResultRepository
    _bytes_hasher: BytesHasher

    @inject
    def __init__(
        self,
        /,
        ocr_processor: OCRProcessor,
        db: Client,
        ocr_result_repository: OCRResultRepository,
        bytes_hasher: BytesHasher,
    ):
        self._ocr_processor = ocr_processor
        self._db = db
        self._ocr_result_repository = ocr_result_repository
        self._bytes_hasher = bytes_hasher

    def __call__(self, image: bytes, language: str = "cht"):
        ocr_result_id = self._bytes_hasher(image)

        @transactional
        def run_in_transaction(transaction: Transaction):
            ocr_result = self._ocr_result_repository.load(
                ocr_result_id,
                transaction=transaction,
            )
            if ocr_result is not None:
                return ocr_result
            ocr_result = self._ocr_processor(image, language)
            self._ocr_result_repository.save(
                ocr_result_id,
                ocr_result,
                transaction=transaction,
            )
            return ocr_result

        ocr_result = run_in_transaction(self._db.transaction())
        return ocr_result
