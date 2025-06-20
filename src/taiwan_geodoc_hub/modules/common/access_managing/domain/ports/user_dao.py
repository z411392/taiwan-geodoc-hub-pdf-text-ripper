from abc import ABC, abstractmethod
from typing import Optional
from firebase_admin.auth import UserRecord


class UserDao(ABC):
    @abstractmethod
    def by_id(self, uid: str) -> Optional[UserRecord]:
        raise NotImplementedError

    @abstractmethod
    def from_id_token(self, id_token: str) -> Optional[UserRecord]:
        raise NotImplementedError
