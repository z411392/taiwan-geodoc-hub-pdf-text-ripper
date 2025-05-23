from starlette.middleware.base import BaseHTTPMiddleware
from injector import Injector, InstanceProvider
from taiwan_geodoc_hub.modules.system_maintaining.application.resolve_request_id import (
    ResolveRequestId,
)
from logging import getLogger, Logger


class WithRequestId(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        injector: Injector = request.scope["injector"]
        handler: ResolveRequestId = injector.get(ResolveRequestId)
        request_id = await handler()
        request.scope["request_id"] = request_id
        logger = getLogger(request_id)
        injector.binder.bind(Logger, to=InstanceProvider(logger))
        return await call_next(request)
