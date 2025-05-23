from google.cloud.firestore import (
    CollectionReference,
    Client,
)

# from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from taiwan_geodoc_hub.modules.access_managing.dtos.tenant import Tenant
from taiwan_geodoc_hub.modules.access_managing.domain.ports.tenant_dao import TenantDao
from taiwan_geodoc_hub.infrastructure.collections import (
    Collections,
)
from injector import inject


class TenantAdapter(TenantDao):
    _collection: CollectionReference

    @inject
    def __init__(self, /, db: Client):
        self._collection = db.collection(str(Collections.tenants))

    def by_id(self, tenant_id: str):
        document = self._collection.document(tenant_id)
        document_snapshot = document.get()
        if not document_snapshot.exists:
            return None
        # create_time: DatetimeWithNanoseconds = document_snapshot.create_time
        # update_time: DatetimeWithNanoseconds = document_snapshot.update_time
        return Tenant(
            **document_snapshot.to_dict(),
            id=tenant_id,
            # created_at=int(create_time.timestamp() * 1000),
            # updated_at=int(update_time.timestamp() * 1000),
        )
