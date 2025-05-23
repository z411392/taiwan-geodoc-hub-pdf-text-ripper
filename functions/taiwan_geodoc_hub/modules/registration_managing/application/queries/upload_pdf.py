from typing import Optional
from injector import inject
from taiwan_geodoc_hub.modules.registration_managing.domain.services.validate_snapshot import (
    validate_snapshot,
)
from google.cloud.firestore import Client, Transaction, transactional
from taiwan_geodoc_hub.infrastructure.firestore.ocr_result_adapter import (
    OCRResultAdapter as OCRResultAdapter,
)
from taiwan_geodoc_hub.infrastructure.firestore.registration_adapter import (
    RegistrationAdapter as RegistrationAdapter,
)
from logging import Logger
from taiwan_geodoc_hub.modules.registration_managing.domain.services.rip_text import (
    RipText,
)
from taiwan_geodoc_hub.modules.registration_managing.domain.services.split_registrations import (
    SplitRegistrations,
)
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.registration_repository import (
    RegistrationRepository,
)
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.snapshot_repository import (
    SnapshotRepository,
)
from taiwan_geodoc_hub.modules.registration_managing.dtos.snapshot import Snapshot


class UploadPDF:
    _db: Client
    _split_registrations: SplitRegistrations
    _rip_text: RipText
    _registration_repository: RegistrationRepository
    _snapshot_repository: SnapshotRepository
    _logger: Logger

    @inject
    def __init__(
        self,
        /,
        db: Client,
        split_registrations: SplitRegistrations,
        rip_text: RipText,
        registration_repository: RegistrationRepository,
        snapshot_repository: SnapshotRepository,
        logger: Logger,
    ):
        self._db = db
        self._split_registrations = split_registrations
        self._rip_text = rip_text
        self._registration_repository = registration_repository
        self._snapshot_repository = snapshot_repository
        self._logger = logger

    def __call__(
        self,
        name: str,
        pdf: bytes,
        /,
        user_id: Optional[str] = None,
        snapshot_id: Optional[str] = None,
    ):
        validate_snapshot(pdf)

        @transactional
        def run_in_transaction(transaction: Transaction):
            existing = self._snapshot_repository.exists(
                snapshot_id,
                transaction=transaction,
            )
            self._snapshot_repository.save(
                snapshot_id,
                Snapshot(
                    id=snapshot_id,
                    name=name,
                    pdf=pdf,
                ),
                transaction=transaction,
            )
            if existing:
                return
            full_text = self._rip_text(pdf=pdf)
            for registration in self._split_registrations(full_text, user_id=user_id):
                self._registration_repository.save(
                    registration.get("id"),
                    registration,
                    transaction=transaction,
                )
            return

        run_in_transaction(self._db.transaction())
