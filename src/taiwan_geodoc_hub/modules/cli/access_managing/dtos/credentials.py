from typing import TypedDict


class Credentials(TypedDict):
    id_token: str
    refresh_token: str
