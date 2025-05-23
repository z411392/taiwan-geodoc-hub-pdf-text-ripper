from taiwan_geodoc_hub.modules.cli.access_managing.domain.ports.token_service import (
    TokenService,
)
from taiwan_geodoc_hub.modules.cli.access_managing.dtos.credentials import Credentials
from typing import Optional
import requests
import jwt
from time import time
from json import loads
from os import getenv
from operator import itemgetter


class TokenAdapter(TokenService):
    def __init__(self):
        firebase_config = loads(getenv("FIREBASE_CONFIG"))
        self.api_key = itemgetter("apiKey")(firebase_config)

    def refresh_token(self, refresh_token: str) -> Optional[Credentials]:
        url = f"https://securetoken.googleapis.com/v1/token?key={self.api_key}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        response = requests.post(url, headers=headers, data=body)
        if not response.ok:
            return None
        data = response.json()
        return Credentials(
            id_token=data["id_token"],
            refresh_token=data["refresh_token"],
        )

    def is_token_valid(self, id_token: str) -> bool:
        try:
            decoded = jwt.decode(id_token, options={"verify_signature": False})
            now = int(time())
            return "exp" in decoded and decoded["exp"] > now + 600
        except Exception:
            return False
