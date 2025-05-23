from enum import Enum
from taiwan_geodoc_hub.infrastructure.environments import is_developing


class Collections(str, Enum):
    ocr_results = "ocr_results"
    tenants = "tenants"
    roles = "tenants/:tenant_id/roles"
    snapshots = "tenants/:tenant_id/snapshots"
    registrations = "tenants/:tenant_id/snapshots/:snapshot_id/registrations"

    def __str__(self):
        if self.name in ["ocr_results"]:
            return self.value
        if is_developing():
            return f"environments/dev/{self.value}"
        return f"environments/prod/{self.value}"
