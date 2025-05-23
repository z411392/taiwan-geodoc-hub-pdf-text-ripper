from abc import ABC, abstractmethod


class RoleDao(ABC):
    @abstractmethod
    def of(self, user_id: str):
        raise NotImplementedError
