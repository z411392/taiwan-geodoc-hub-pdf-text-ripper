from injector import inject
from taiwan_geodoc_hub.modules.access_managing.domain.ports.tenant_dao import TenantDao
from logging import Logger


class ResolveTenant:
    _tenant_dao: TenantDao
    _logger: Logger

    @inject
    def __init__(
        self,
        tenant_dao: TenantDao,
        logger: Logger,
    ):
        self._tenant_dao = tenant_dao
        self._logger = logger

    async def __call__(self, tenant_id: str):
        tenant = self._tenant_dao.by_id(tenant_id)
        return tenant
