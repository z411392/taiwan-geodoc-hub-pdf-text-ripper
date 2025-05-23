from flask import g, request
from injector import Injector, InstanceProvider
from taiwan_geodoc_hub.modules.access_managing.application.resolve_tenant import (
    ResolveTenant,
    ResolvingTenant,
)
from taiwan_geodoc_hub.modules.access_managing.exceptions.tenant_not_found import (
    TenantNotFound,
)
from taiwan_geodoc_hub.modules.access_managing.dtos.tenant import Tenant
from functools import wraps
from typing import Callable, Any
from taiwan_geodoc_hub.infrastructure.injection_tokens import (
    TenantId,
)


def with_resolving_tenant(enforce: bool):
    def decorator(func: Callable[[..., Any], Any]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            injector: Injector = g.get("injector")
            json: dict = request.get_json()
            tenant_id = json.get("tenant_id")
            query = ResolvingTenant(
                tenant_id=tenant_id,
            )
            handler = injector.get(ResolveTenant)
            tenant = handler(query=query)
            if enforce:
                if tenant is None:
                    raise TenantNotFound(tenant_id)
            g.tenant: Tenant = tenant
            if tenant is not None:
                injector.binder.bind(TenantId, to=InstanceProvider(tenant.get("id")))
            return func(*args, **kwargs)

        return wrapper

    return decorator
