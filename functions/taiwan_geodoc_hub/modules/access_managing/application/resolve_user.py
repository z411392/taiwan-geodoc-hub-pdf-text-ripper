from typing import TypedDict
from injector import inject
from taiwan_geodoc_hub.modules.access_managing.domain.ports.user_dao import UserDao
from logging import Logger


class ResolvingUser(TypedDict):
    session_cookie: str


class ResolveUser:
    _user_dao: UserDao
    _logger: Logger

    @inject
    def __init__(self, user_dao: UserDao, logger: Logger):
        self._user_dao = user_dao
        self._logger = logger

    def __call__(self, /, query: ResolvingUser):
        user = self._user_dao.from_session_cookie(query.get("session_cookie"))
        return user
