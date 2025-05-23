from flask import Response, request, g
from injector import Injector, InstanceProvider
from typing import Optional
from json import dumps
from taiwan_geodoc_hub.modules.access_managing.presentation.middlewares.with_resolving_user import (
    with_resolving_user,
)
from taiwan_geodoc_hub.modules.access_managing.presentation.middlewares.with_resolving_tenant import (
    with_resolving_tenant,
)
from taiwan_geodoc_hub.modules.access_managing.presentation.middlewares.with_resolving_role import (
    with_resolving_role,
)
from firebase_admin.auth import UserRecord
from base64 import b64decode
from taiwan_geodoc_hub.modules.registration_managing.application.queries.upload_pdf import (
    UploadPDF,
)
from taiwan_geodoc_hub.modules.system_maintaining.presentation.middlewares.with_request_id import (
    with_request_id,
)
from taiwan_geodoc_hub.modules.system_maintaining.presentation.middlewares.with_exception_handling import (
    with_exception_handling,
)
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.bytes_hasher import (
    BytesHasher,
)
from taiwan_geodoc_hub.infrastructure.injection_tokens import (
    SnapshotId,
)


@with_request_id
@with_exception_handling(name=UploadPDF.__name__)
@with_resolving_user(enforce=True)
@with_resolving_tenant(enforce=True)
@with_resolving_role(enforce=True)
def on_uploading_pdf():
    response = Response()
    response.headers["Content-Type"] = "application/json"
    injector: Injector = g.get("injector")
    request_id: Optional[str] = g.get("request_id")
    user: UserRecord = g.get("user")
    json: dict = request.get_json()
    pdf = b64decode(json.get("content"))
    name: str = json.get("name")
    bytes_hasher = injector.get(BytesHasher)
    snapshot_id = bytes_hasher(pdf)
    injector.binder.bind(SnapshotId, to=InstanceProvider(snapshot_id))
    handler = injector.get(UploadPDF)
    handler(
        name,
        pdf,
        user_id=user.uid,
        snapshot_id=snapshot_id,
    )
    response.data = dumps(
        dict(
            request_id=request_id,
            success=True,
            data=dict(
                snapshot_id=snapshot_id,
            ),
        ),
    )
    response.status = 200
    return response
