from google.cloud.firestore import Client, CollectionReference
from taiwan_geodoc_hub.infrastructure.collections import (
    Collections,
)
from taiwan_geodoc_hub.infrastructure.injection_tokens import (
    TenantId,
)
from injector import inject
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.snapshot_repository import (
    SnapshotRepository,
)
from taiwan_geodoc_hub.modules.registration_managing.dtos.snapshot import Snapshot
from google.cloud.firestore import Transaction


class SnapshotAdapter(SnapshotRepository):
    _collection: CollectionReference

    @inject
    def __init__(self, db: Client, tenant_id: TenantId):
        self._collection = db.collection(
            str(Collections.snapshots).replace(":tenant_id", tenant_id)
        )

    def exists(
        self,
        snapshot_id: str,
        /,
        transaction: Transaction,
    ):
        document = self._collection.document(snapshot_id)
        document_snapshot = next(iter(transaction.get(document)))
        return document_snapshot.exists

    def save(
        self,
        snapshot_id: str,
        snapshot: Snapshot,
        /,
        transaction: Transaction,
    ):
        document = self._collection.document(snapshot_id)
        transaction.set(
            document,
            dict(
                name=snapshot.get("name"),
            ),
            merge=True,
        )
