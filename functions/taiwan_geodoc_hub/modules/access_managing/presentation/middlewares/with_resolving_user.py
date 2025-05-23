from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Coroutine, Optional
from taiwan_geodoc_hub.modules.access_managing.application.resolve_user import (
    ResolveUser,
)
from injector import Injector, InstanceProvider
from taiwan_geodoc_hub.modules.access_managing.exceptions.unauthenticated import (
    Unauthenticated,
)
from taiwan_geodoc_hub.infrastructure.injection_tokens import UserId
from re import split, IGNORECASE


class WithResolvingUser(BaseHTTPMiddleware):
    def _extract_id_token(self, authorization: Optional[str]):
        if authorization is None:
            return None
        segments = split(r"bearer\s+", authorization, flags=IGNORECASE)
        if len(segments) < 2:
            return None
        _, token = segments
        if token is None:
            return None
        stripped = str.strip(token)
        return stripped

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Coroutine[None, None, Response]],
    ):
        injector: Injector = request.scope["injector"]
        id_token = self._extract_id_token(request.headers.get("Authorization"))
        handler = injector.get(ResolveUser)
        user = await handler(id_token)
        if user is None:
            raise Unauthenticated()
        request.scope["user"] = user
        injector.binder.bind(UserId, to=InstanceProvider(user.uid))
        return await call_next(request)
