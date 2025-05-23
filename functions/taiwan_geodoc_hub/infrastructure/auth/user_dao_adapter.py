from firebase_admin.auth import get_user, UserRecord
from typing import Optional
from firebase_admin.auth import verify_session_cookie
from taiwan_geodoc_hub.modules.access_managing.domain.ports.user_dao import (
    UserDao,
)


class UserDaoAdapter(UserDao):
    def by_id(self, user_id: str) -> Optional[UserRecord]:
        try:
            user: Optional[UserRecord] = get_user(user_id)
            return user
        except Exception as _:
            return None

    def from_session_cookie(self, session_cookie: str):
        try:
            decoded_claims: Optional[dict] = verify_session_cookie(session_cookie)
            if decoded_claims is None:
                return None
            user_id: Optional[str] = decoded_claims.get("uid")
            if user_id is None:
                return None
            user: Optional[UserRecord] = self.by_id(user_id)
            return user
        except Exception as _:
            return None
