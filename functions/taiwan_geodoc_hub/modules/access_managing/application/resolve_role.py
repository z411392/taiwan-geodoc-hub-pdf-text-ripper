from typing import TypedDict
from injector import inject
from taiwan_geodoc_hub.modules.access_managing.domain.ports.role_dao import RoleDao
from logging import Logger


class ResolvingRole(TypedDict):
    user_id: str
    tenant_id: str


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

    def __call__(self, /, query: ResolvingRole):
        role = self._role_dao.of(user_id=query.get("user_id"))
        return role
