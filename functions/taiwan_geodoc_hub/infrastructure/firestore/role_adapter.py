from google.cloud.firestore import Client, CollectionReference
from taiwan_geodoc_hub.infrastructure.collections import (
    Collections,
)
from taiwan_geodoc_hub.modules.access_managing.constants.roles import Roles
from taiwan_geodoc_hub.modules.access_managing.domain.ports.role_dao import (
    RoleDao,
)
from taiwan_geodoc_hub.infrastructure.injection_tokens import (
    TenantId,
)
from injector import inject


class RoleAdapter(RoleDao):
    _collection: CollectionReference

    @inject
    def __init__(self, /, db: Client, tenant_id: TenantId):
        self._collection = db.collection(
            str(Collections.roles).replace(":tenant_id", tenant_id)
        )

    def of(self, user_id: str):
        document = self._collection.document(user_id)
        document_snapshot = document.get()
        if not document_snapshot.exists:
            return None
        role: Roles = Roles(document_snapshot.get("role"))
        return role
