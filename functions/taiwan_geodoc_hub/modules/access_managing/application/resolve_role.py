from injector import inject
from taiwan_geodoc_hub.modules.access_managing.domain.ports.role_dao import RoleDao
from logging import Logger


class ResolveRole:
    _role_dao: RoleDao
    _logger: Logger

    @inject
    def __init__(
        self,
        role_dao: RoleDao,
        logger: Logger,
    ):
        self._role_dao = role_dao
        self._logger = logger

    async def __call__(self, user_id: str):
        role = self._role_dao.of(user_id=user_id)
        return role
