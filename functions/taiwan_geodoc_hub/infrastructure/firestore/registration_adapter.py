from taiwan_geodoc_hub.modules.registration_managing.constants.registration_statuses import (
    RegistrationStatuses,
)

from google.cloud.firestore import Client, CollectionReference, Transaction
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.registration_repository import (
    RegistrationRepository,
)
from taiwan_geodoc_hub.modules.registration_managing.dtos.registration import (
    Registration,
)
from taiwan_geodoc_hub.infrastructure.collections import (
    Collections,
)
from taiwan_geodoc_hub.infrastructure.injection_tokens import (
    TenantId,
    SnapshotId,
)
from injector import inject


class RegistrationAdapter(RegistrationRepository):
    _collection: CollectionReference

    @inject
    def __init__(self, /, db: Client, tenant_id: TenantId, snapshot_id: SnapshotId):
        self._collection = db.collection(
            str(Collections.registrations)
            .replace(":tenant_id", tenant_id)
            .replace(":snapshot_id", snapshot_id)
        )

    def exists(self, registration_id: str, /, transaction: Transaction):
        document = self._collection.document(registration_id)
        document_snapshot = next(iter(transaction.get(document)))
        return document_snapshot.exists

    def save(
        self,
        registration_id: str,
        registration: Registration,
        /,
        transaction: Transaction,
    ):
        type, text = (
            registration.get("type"),
            registration.get("text"),
        )
        document = self._collection.document(registration_id)
        transaction.set(
            document,
            dict(
                type=type.value,
                text=text,
                status=RegistrationStatuses.pending.value,
            ),
            merge=True,
        )
