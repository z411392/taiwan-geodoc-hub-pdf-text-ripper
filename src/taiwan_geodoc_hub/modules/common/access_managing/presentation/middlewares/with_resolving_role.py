from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from injector import Injector, InstanceProvider, CallableProvider
from taiwan_geodoc_hub.modules.common.access_managing.application.resolve_role import (
    ResolveRole,
)
from taiwan_geodoc_hub.modules.common.access_managing.exceptions.permission_denied import (
    PermissionDenied,
)
from taiwan_geodoc_hub.modules.common.access_managing.constants.roles import Roles
from typing import Optional, Callable, Coroutine
from firebase_admin.auth import UserRecord
from taiwan_geodoc_hub.infrastructure.constants.types import Role
from logging import getLogger, Logger, LoggerAdapter
from taiwan_geodoc_hub.modules.common.access_managing.domain.services.is_root import (
    is_root,
)


def with_resolving_role(enforce: bool):
    class Middleware(BaseHTTPMiddleware):
        async def dispatch(
            self,
            request: Request,
            call_next: Callable[[Request], Coroutine[None, None, Response]],
        ):
            injector: Injector = request.scope["injector"]
            user: UserRecord = request.scope["user"]
            role: Optional[Roles] = None
            if is_root(user.uid):
                role = Roles.manager
            else:
                handler = injector.get(ResolveRole)
                role = handler(user.uid)
            if role is None and enforce is True:
                raise PermissionDenied()
            if role:
                request.scope["role"] = role
                injector.binder.bind(
                    Logger,
                    to=CallableProvider(
                        lambda: LoggerAdapter(
                            getLogger(request.scope["request_id"]),
                            dict(
                                user=request.scope["user"],
                                tenant=request.scope["tenant"],
                                role=request.scope["role"],
                            ),
                        ),
                    ),
                )
                injector.binder.bind(Role, to=InstanceProvider(role))
            return await call_next(request)

    return Middleware
