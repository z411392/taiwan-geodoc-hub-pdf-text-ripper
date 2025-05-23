from taiwan_geodoc_hub.modules.cli.access_managing.domain.ports.credential_repository import (
    CredentialRepository,
)
from taiwan_geodoc_hub.modules.cli.access_managing.dtos.credentials import Credentials
from typing import Optional
from json import loads, dumps
from os.path import exists


class CredentialAdapter(CredentialRepository):
    _credentials_path: str = "credentials.json"

    def load(self) -> Optional[Credentials]:
        if not exists(self._credentials_path):
            return None
        with open(self._credentials_path, "r", encoding="utf-8") as file:
            data = loads(file.read())
            return Credentials(**data)

    def save(self, credential: Credentials) -> None:
        with open(self._credentials_path, "w", encoding="utf-8") as file:
            file.write(dumps(credential, indent=4, ensure_ascii=False))
