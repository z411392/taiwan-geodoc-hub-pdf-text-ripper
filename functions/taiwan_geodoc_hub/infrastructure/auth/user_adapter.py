from firebase_admin.auth import get_user, UserRecord
from typing import Optional
from firebase_admin.auth import verify_id_token
from taiwan_geodoc_hub.modules.access_managing.domain.ports.user_dao import (
    UserDao,
)


class UserAdapter(UserDao):
    def by_id(self, user_id: str) -> Optional[UserRecord]:
        try:
            user: Optional[UserRecord] = get_user(user_id)
            return user
        except Exception as _:
            return None

    def from_id_token(self, id_token: str):
        try:
            decoded_claims: Optional[dict] = verify_id_token(id_token)
            if decoded_claims is None:
                return None
            user_id: Optional[str] = decoded_claims.get("uid")
            if user_id is None:
                return None
            user: Optional[UserRecord] = self.by_id(user_id)
            return user
        except Exception as _:
            return None
