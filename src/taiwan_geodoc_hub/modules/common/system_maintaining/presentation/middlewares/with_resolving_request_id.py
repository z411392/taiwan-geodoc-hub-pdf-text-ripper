from starlette.middleware.base import BaseHTTPMiddleware
from injector import Injector, CallableProvider
from taiwan_geodoc_hub.modules.common.system_maintaining.application.resolve_request_id import (
    ResolveRequestId,
)
from logging import getLogger, Logger


class WithResolvingRequestId(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        injector: Injector = request.scope["injector"]
        handler: ResolveRequestId = injector.get(ResolveRequestId)
        request_id = handler()
        request.scope["request_id"] = request_id
        injector.binder.bind(
            Logger, to=CallableProvider(lambda: getLogger(request.scope["request_id"]))
        )
        response = await call_next(request)
        response.headers["X-Request-Id"] = request_id
        return response
