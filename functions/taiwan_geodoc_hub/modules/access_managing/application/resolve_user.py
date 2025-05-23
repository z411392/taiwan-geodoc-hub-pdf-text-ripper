from injector import inject
from taiwan_geodoc_hub.modules.access_managing.domain.ports.user_dao import UserDao
from logging import Logger


class ResolveUser:
    _user_dao: UserDao
    _logger: Logger

    @inject
    def __init__(self, user_dao: UserDao, logger: Logger):
        self._user_dao = user_dao
        self._logger = logger

    async def __call__(self, id_token: str):
        user = self._user_dao.from_id_token(id_token)
        return user
