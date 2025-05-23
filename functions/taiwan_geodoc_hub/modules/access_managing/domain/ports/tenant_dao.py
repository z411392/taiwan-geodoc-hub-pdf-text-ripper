from abc import ABC, abstractmethod
from typing import Optional
from taiwan_geodoc_hub.modules.access_managing.dtos.tenant import Tenant


class TenantDao(ABC):
    @abstractmethod
    def by_id(self, tenant_id: str) -> Optional[Tenant]:
        raise NotImplementedError
