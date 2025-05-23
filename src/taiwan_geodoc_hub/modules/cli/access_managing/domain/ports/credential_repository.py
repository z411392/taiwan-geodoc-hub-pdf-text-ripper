from abc import ABC, abstractmethod
from taiwan_geodoc_hub.modules.cli.access_managing.dtos.credentials import Credentials
from typing import Optional


class CredentialRepository(ABC):
    @abstractmethod
    def load(self) -> Optional[Credentials]:
        raise NotImplementedError

    @abstractmethod
    def save(self, credential: Credentials) -> None:
        raise NotImplementedError
