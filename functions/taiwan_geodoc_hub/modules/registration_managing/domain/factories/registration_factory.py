from enum import Enum
from re import search, IGNORECASE, sub, DOTALL
from taiwan_geodoc_hub.modules.registration_managing.constants.registration_types import (
    RegistrationTypes,
)
from typing import Optional
from taiwan_geodoc_hub.infrastructure.hashers.bytes_hasher_adapter import (
    BytesHasherAdapter,
)
from taiwan_geodoc_hub.modules.registration_managing.dtos.registration import (
    Registration,
)
from injector import inject


class RegistrationFactory:
    _bytes_hasher: BytesHasherAdapter

    @inject
    def __init__(self, /, bytes_hasher: BytesHasherAdapter):
        self._bytes_hasher = bytes_hasher

    class Regexps(Enum):
        building = r"建物登記第(?:一|二|三)類謄本"
        land = r"土地登記第(?:一|二|三)類謄本"

    def _determine_registration_type(self, text: str):
        if search(self.Regexps.building.value, text, IGNORECASE):
            return RegistrationTypes.building
        if search(self.Regexps.land.value, text, IGNORECASE):
            return RegistrationTypes.land
        return None

    def _remove_supplementary_text(
        self, text: str, registration_type: RegistrationTypes
    ):
        text = sub(r"\(續次頁\)[\s\S]*?列印時間:.*", "", text)
        if registration_type == RegistrationTypes.building:
            text = sub(
                rf"^.*?(?={self.Regexps.building.value})", "", text, flags=DOTALL
            )
        if registration_type == RegistrationTypes.land:
            text = sub(rf"^.*?(?={self.Regexps.land.value})", "", text, flags=DOTALL)
        return text

    def __call__(self, /, text: str, user_id: str):
        registration_type: Optional[RegistrationTypes] = (
            self._determine_registration_type(text)
        )
        if registration_type is None:
            return None
        text = self._remove_supplementary_text(text, registration_type)
        registration_id = self._bytes_hasher(text.encode("utf-8"))
        return Registration(
            id=registration_id,
            type=registration_type,
            text=text,
            user_id=user_id,
        )
