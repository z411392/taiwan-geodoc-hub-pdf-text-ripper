from contextlib import contextmanager
from injector import Injector, InstanceProvider, ClassProvider
from os import getenv
from google.cloud.firestore import Client
from firebase_admin.firestore import client
from firebase_admin import initialize_app
from dotenv import load_dotenv
from firebase_admin.credentials import Certificate
from re import sub
from os.path import exists
from logging import basicConfig, INFO
from taiwan_geodoc_hub.modules.access_managing.domain.ports.user_dao import (
    UserDao,
)
from taiwan_geodoc_hub.infrastructure.auth.user_dao_adapter import UserDaoAdapter
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.bytes_hasher import (
    BytesHasher,
)
from taiwan_geodoc_hub.infrastructure.hashers.bytes_hasher_adapter import (
    BytesHasherAdapter,
)
from firebase_admin import get_app, delete_app
from taiwan_geodoc_hub.modules.access_managing.domain.ports.tenant_dao import (
    TenantDao,
)
from taiwan_geodoc_hub.infrastructure.firestore.tenant_adapter import (
    TenantAdapter,
)
from taiwan_geodoc_hub.infrastructure.injection_tokens import (
    OCRSpaceApiKey,
)
from taiwan_geodoc_hub.infrastructure.firestore.ocr_result_adapter import (
    OCRResultAdapter,
)
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.ocr_result_repository import (
    OCRResultRepository,
)
from taiwan_geodoc_hub.infrastructure.firestore.registration_adapter import (
    RegistrationAdapter,
)
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.registration_repository import (
    RegistrationRepository,
)
from taiwan_geodoc_hub.modules.access_managing.domain.ports.role_dao import RoleDao
from taiwan_geodoc_hub.infrastructure.firestore.role_adapter import RoleAdapter
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.ocr_processor import (
    OCRProcessor,
)
from taiwan_geodoc_hub.infrastructure.clients.ocr_space import OCRSpace
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.cached_ocr_processor import (
    CachedOCRProcessor,
)
from taiwan_geodoc_hub.modules.registration_managing.application.queries.perform_ocr import (
    PerformOCR,
)
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.snapshot_repository import (
    SnapshotRepository,
)
from taiwan_geodoc_hub.infrastructure.firestore.snapshot_adapter import (
    SnapshotAdapter,
)


@contextmanager
def lifespan():
    if exists(".env"):
        load_dotenv(".env", override=True)
    initialize_app(
        credential=Certificate(
            dict(
                type="service_account",
                project_id=getenv("PROJECT_ID"),
                private_key=sub(r"\\n", "\n", getenv("PRIVATE_KEY")),
                client_email=getenv("CLIENT_EMAIL"),
                token_uri="https://oauth2.googleapis.com/token",
            )
        )
    )
    basicConfig(
        level=INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    injector = Injector()
    injector.binder.bind(
        OCRSpaceApiKey, to=InstanceProvider(getenv("OCR_SPACE_API_KEY"))
    )
    injector.binder.bind(BytesHasher, to=ClassProvider(BytesHasherAdapter))
    injector.binder.bind(UserDao, to=ClassProvider(UserDaoAdapter))
    injector.binder.bind(Client, to=InstanceProvider(client()))
    injector.binder.bind(OCRResultRepository, to=ClassProvider(OCRResultAdapter))
    injector.binder.bind(RegistrationRepository, to=ClassProvider(RegistrationAdapter))
    injector.binder.bind(RoleDao, to=ClassProvider(RoleAdapter))
    injector.binder.bind(TenantDao, to=ClassProvider(TenantAdapter))
    injector.binder.bind(OCRProcessor, to=ClassProvider(OCRSpace))
    injector.binder.bind(CachedOCRProcessor, to=ClassProvider(PerformOCR))
    injector.binder.bind(SnapshotRepository, to=ClassProvider(SnapshotAdapter))
    yield injector
    delete_app(get_app())
