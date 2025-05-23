from starlette.requests import Request
from starlette.responses import JSONResponse
from taiwan_geodoc_hub.modules.access_managing.exceptions.unauthenticated import (
    Unauthenticated,
)
from taiwan_geodoc_hub.modules.access_managing.exceptions.tenant_not_found import (
    TenantNotFound,
)
from taiwan_geodoc_hub.modules.access_managing.exceptions.permission_denied import (
    PermissionDenied,
)


class ExceptionHandler:
    async def __call__(self, request: Request, exception: Exception):
        request_id = request.scope["request_id"]
        if isinstance(exception, Unauthenticated):
            return JSONResponse(
                dict(
                    request_id=request_id,
                    success=False,
                    data=dict(exception),
                ),
                status_code=401,
            )
        if isinstance(exception, TenantNotFound):
            return JSONResponse(
                dict(
                    request_id=request_id,
                    success=False,
                    data=dict(exception),
                ),
                status_code=404,
            )
        if isinstance(exception, PermissionDenied):
            return JSONResponse(
                dict(
                    request_id=request_id,
                    success=False,
                    data=dict(exception),
                ),
                status_code=403,
            )
        return JSONResponse(
            dict(
                request_id=request_id,
                success=False,
                data=dict(exception=str(exception)),
            ),
            status_code=500,
        )


exception_handler = ExceptionHandler()
