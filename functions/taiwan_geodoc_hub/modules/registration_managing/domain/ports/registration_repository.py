from abc import ABC, abstractmethod
from taiwan_geodoc_hub.modules.registration_managing.dtos.registration import (
    Registration,
)
from google.cloud.firestore import Transaction


class RegistrationRepository(ABC):
    @abstractmethod
    def exists(self, registration_id: str, /, transaction: Transaction) -> bool:
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        registration_id: str,
        registration: Registration,
        /,
        transaction: Transaction,
    ):
        raise NotImplementedError
