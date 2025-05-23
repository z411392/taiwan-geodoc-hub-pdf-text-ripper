from taiwan_geodoc_hub.modules.registration_managing.domain.factories.registration_factory import (
    RegistrationFactory,
)
from re import split
from typing import Optional
from injector import inject


class SplitRegistrations:
    _registration_factory: RegistrationFactory

    @inject
    def __init__(self, /, registration_factory: RegistrationFactory):
        self._registration_factory = registration_factory

    def __call__(self, full_text: str, /, user_id: Optional[str] = None):
        for text in split("〈 本謄本列印完畢 〉", full_text):
            registration = self._registration_factory(text=text, user_id=user_id)
            if registration is None:
                continue
            yield registration
