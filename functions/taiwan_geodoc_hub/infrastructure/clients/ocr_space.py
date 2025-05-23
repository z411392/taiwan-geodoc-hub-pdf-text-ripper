from base64 import b64encode
import requests
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.ocr_processor import (
    OCRProcessor,
)
from taiwan_geodoc_hub.infrastructure.injection_tokens import (
    OCRSpaceApiKey,
)
from injector import inject


class OCRSpace(OCRProcessor):
    _endpoint: str = "https://api.ocr.space/parse/image"
    _api_key: str

    @inject
    def __init__(
        self,
        /,
        api_key: OCRSpaceApiKey,
    ):
        self._api_key = api_key

    def __call__(self, image: bytes, language: str = "cht"):
        base64_encoded = b64encode(image).decode("utf-8")
        base64_image = f"data:image/jpeg;base64,{base64_encoded}"
        body = {
            "apikey": self._api_key,
            "language": language,
            "base64Image": base64_image,
        }
        with requests.post(self._endpoint, data=body) as response:
            payload = response.json()
            if "ParsedResults" not in payload:
                return ""
            results = payload["ParsedResults"]
            joined = "".join((result["ParsedText"] for result in results))
            trimed = joined.replace("\r", "").replace("\n", "").strip()
            return trimed
