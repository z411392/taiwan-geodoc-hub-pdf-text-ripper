from flask import g
from injector import Injector, InstanceProvider
from typing import Optional
from taiwan_geodoc_hub.modules.access_managing.application.resolve_role import (
    ResolveRole,
    ResolvingRole,
)
from taiwan_geodoc_hub.modules.access_managing.exceptions.permission_denied import (
    PermissionDenied,
)
from taiwan_geodoc_hub.modules.access_managing.constants.roles import Roles
from functools import wraps
from typing import Callable, Any
from firebase_admin.auth import UserRecord
from taiwan_geodoc_hub.modules.access_managing.dtos.tenant import Tenant
from taiwan_geodoc_hub.modules.access_managing.constants.roots import roots
from taiwan_geodoc_hub.infrastructure.injection_tokens import Role


def with_resolving_role(enforce: bool):
    def decorator(func: Callable[[..., Any], Any]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            injector: Injector = g.get("injector")
            user: UserRecord = g.get("user")
            tenant: Tenant = g.get("tenant")
            role: Optional[Roles] = None
            if user is not None and tenant is not None:
                if user.uid in roots:
                    role = Roles.manager
                else:
                    query = ResolvingRole(
                        tenant_id=tenant.get("id"),
                        user_id=user.uid,
                    )
                    handler = injector.get(ResolveRole)
                    role = handler(query=query)
            if enforce:
                if user.uid not in roots and role is None:
                    raise PermissionDenied()
            g.role = role
            if role is not None:
                injector.binder.bind(Role, to=InstanceProvider(role))
            return func(*args, **kwargs)

        return wrapper

    return decorator
