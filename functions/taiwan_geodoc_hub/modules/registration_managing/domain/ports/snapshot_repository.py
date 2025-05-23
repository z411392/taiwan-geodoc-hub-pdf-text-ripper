from abc import ABC, abstractmethod
from taiwan_geodoc_hub.modules.registration_managing.dtos.snapshot import Snapshot
from google.cloud.firestore import Transaction


class SnapshotRepository(ABC):
    @abstractmethod
    def exists(
        self,
        snapshot_id: str,
        /,
        transaction: Transaction,
    ):
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        snapshot_id: str,
        snapshot: Snapshot,
        /,
        transaction: Transaction,
    ):
        raise NotImplementedError
