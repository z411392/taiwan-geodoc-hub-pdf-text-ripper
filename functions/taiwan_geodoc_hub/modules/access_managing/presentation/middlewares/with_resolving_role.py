from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from injector import Injector, InstanceProvider
from taiwan_geodoc_hub.modules.access_managing.application.resolve_role import (
    ResolveRole,
)
from taiwan_geodoc_hub.modules.access_managing.exceptions.permission_denied import (
    PermissionDenied,
)
from taiwan_geodoc_hub.modules.access_managing.constants.roles import Roles
from typing import Optional, Callable, Coroutine
from firebase_admin.auth import UserRecord
from taiwan_geodoc_hub.modules.access_managing.constants.roots import roots
from taiwan_geodoc_hub.infrastructure.injection_tokens import Role


class WithResolvingRole(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Coroutine[None, None, Response]],
    ):
        injector: Injector = request.scope["injector"]
        user: UserRecord = request.scope["user"]
        role: Optional[Roles] = None
        if user.uid in roots:
            role = Roles.manager
        else:
            handler = injector.get(ResolveRole)
            role = await handler(user.uid)
        if role is None:
            raise PermissionDenied()
        request.scope["role"] = role
        injector.binder.bind(Role, to=InstanceProvider(role))
        return await call_next(request)
