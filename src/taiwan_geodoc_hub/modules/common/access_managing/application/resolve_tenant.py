from injector import inject
from taiwan_geodoc_hub.modules.common.access_managing.domain.ports.tenant_dao import (
    TenantDao,
)
from logging import Logger
from time import perf_counter


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

    def __call__(self, tenant_id: str):
        start = perf_counter()
        try:
            tenant = self._tenant_dao.by_id(tenant_id)
            self._logger.info(
                "ResolveTenant finished", extra=dict(elapsed=perf_counter() - start)
            )
            return tenant
        except Exception:
            self._logger.exception(
                "ResolveTenant failed",
            )
            raise
