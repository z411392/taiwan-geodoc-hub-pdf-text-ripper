from abc import ABC, abstractmethod
from taiwan_geodoc_hub.modules.cli.access_managing.dtos.credentials import Credentials
from typing import Optional


class TokenService(ABC):
    @abstractmethod
    def refresh_token(self, refresh_token: str) -> Optional[Credentials]:
        raise NotImplementedError

    @abstractmethod
    def is_token_valid(self, id_token: str) -> bool:
        raise NotImplementedError
