from starlette.responses import JSONResponse
from starlette.requests import Request
from injector import Injector, InstanceProvider
from typing import Optional
from base64 import b64decode
from taiwan_geodoc_hub.modules.registration_managing.application.queries.upload_pdf import (
    UploadPDF,
)
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.bytes_hasher import (
    BytesHasher,
)
from taiwan_geodoc_hub.infrastructure.injection_tokens import (
    SnapshotId,
)


async def on_uploading_pdf(request: Request):
    injector: Injector = request.scope["injector"]
    request_id: Optional[str] = request.scope["request_id"]
    json: dict = await request.json()
    pdf = b64decode(json["content"])
    name: str = json["name"]
    bytes_hasher = injector.get(BytesHasher)
    snapshot_id = bytes_hasher(pdf)
    injector.binder.bind(SnapshotId, to=InstanceProvider(snapshot_id))
    handler = injector.get(UploadPDF)
    await handler(name, pdf)
    return JSONResponse(
        dict(
            request_id=request_id,
            success=True,
            data=dict(
                snapshot_id=snapshot_id,
            ),
        )
    )
