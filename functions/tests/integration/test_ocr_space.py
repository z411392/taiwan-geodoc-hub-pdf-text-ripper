import pytest
from injector import Injector
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.ocr_processor import (
    OCRProcessor,
)


# @pytest.mark.skip(reason="")
class TestOCRSpace:
    @pytest.fixture(scope="module")
    def ocr_service(self, injector: Injector):
        return injector.get(OCRProcessor)

    @pytest.mark.describe("要能夠 ocr")
    def test_ocr(
        self,
        sample_image: bytes,
        ocr_service: OCRProcessor,
        sample_ocr_result: str,
    ):
        text = ocr_service(sample_image)
        assert text == sample_ocr_result
