from taiwan_geodoc_hub.modules.access_managing.application.resolve_user import (
    ResolveUser,
    ResolvingUser,
)
from flask import g, request
from injector import Injector, InstanceProvider
from taiwan_geodoc_hub.modules.access_managing.exceptions.unauthenticated import (
    Unauthenticated,
)
from firebase_admin.auth import UserRecord
from functools import wraps
from typing import Callable, Any
from taiwan_geodoc_hub.modules.access_managing.constants.cookies import Cookies
from taiwan_geodoc_hub.infrastructure.injection_tokens import UserId


def with_resolving_user(enforce: bool):
    def decorator(func: Callable[[..., Any], Any]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            injector: Injector = g.get("injector")
            session_cookie = request.cookies[Cookies.session.value]
            query = ResolvingUser(
                session_cookie=session_cookie,
            )
            handler = injector.get(ResolveUser)
            user = handler(query=query)
            if enforce and user is None:
                raise Unauthenticated()
            g.user: UserRecord = user
            if user is not None:
                injector.binder.bind(UserId, to=InstanceProvider(user.uid))
            return func(*args, **kwargs)

        return wrapper

    return decorator
