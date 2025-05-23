from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from injector import Injector, InstanceProvider, CallableProvider
from taiwan_geodoc_hub.modules.common.access_managing.application.resolve_tenant import (
    ResolveTenant,
)
from taiwan_geodoc_hub.modules.common.access_managing.exceptions.tenant_not_found import (
    TenantNotFound,
)
from typing import Callable, Coroutine
from taiwan_geodoc_hub.infrastructure.constants.types import (
    TenantId,
)
from logging import getLogger, Logger, LoggerAdapter


def with_resolving_tenant(enforce: bool):
    class Middleware(BaseHTTPMiddleware):
        async def dispatch(
            self,
            request: Request,
            call_next: Callable[[Request], Coroutine[None, None, Response]],
        ):
            injector: Injector = request.scope["injector"]
            tenant_id = request.path_params.get("tenant_id")
            handler = injector.get(ResolveTenant)
            tenant = handler(tenant_id)
            if tenant is None and enforce:
                raise TenantNotFound(tenant_id)
            if tenant:
                request.scope["tenant"] = tenant
                injector.binder.bind(
                    Logger,
                    to=CallableProvider(
                        lambda: LoggerAdapter(
                            getLogger(request.scope["request_id"]),
                            dict(
                                user=request.scope["user"],
                                tenant=request.scope["tenant"],
                            ),
                        ),
                    ),
                )
                injector.binder.bind(TenantId, to=InstanceProvider(tenant.get("id")))
            return await call_next(request)

    return Middleware
