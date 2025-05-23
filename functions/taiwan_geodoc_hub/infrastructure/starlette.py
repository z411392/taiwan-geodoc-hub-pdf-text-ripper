from starlette.applications import Starlette
from starlette.routing import Route
from vellox import Vellox
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.exceptions import ExceptionMiddleware
from taiwan_geodoc_hub.infrastructure.lifespan import lifespan
from taiwan_geodoc_hub.modules.system_maintaining.presentation.controllers.on_checking_health import (
    on_checking_health,
)
from taiwan_geodoc_hub.modules.system_maintaining.presentation.middlewares.with_request_container import (
    WithRequestContainer,
)
from taiwan_geodoc_hub.modules.system_maintaining.presentation.middlewares.with_request_id import (
    WithRequestId,
)
from taiwan_geodoc_hub.modules.system_maintaining.presentation.middlewares.exception_handler import (
    exception_handler,
)
from taiwan_geodoc_hub.modules.registration_managing.presentation.controllers.on_uploading_pdf import (
    on_uploading_pdf,
)
from taiwan_geodoc_hub.modules.access_managing.presentation.middlewares.with_resolving_user import (
    WithResolvingUser,
)
from taiwan_geodoc_hub.modules.access_managing.presentation.middlewares.with_resolving_tenant import (
    WithResolvingTenant,
)
from taiwan_geodoc_hub.modules.access_managing.presentation.middlewares.with_resolving_role import (
    WithResolvingRole,
)

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(
        WithRequestContainer,
    ),
    Middleware(
        WithRequestId,
    ),
    Middleware(
        ExceptionMiddleware,
        handlers={Exception: exception_handler},
    ),
]

routes = [
    Route("/__/health", on_checking_health, methods=["GET"]),
    Route(
        "/tenants/{tenant_id}/pdf",
        on_uploading_pdf,
        methods=["POST"],
        middleware=[
            Middleware(
                WithResolvingUser,
            ),
            Middleware(
                WithResolvingTenant,
            ),
            Middleware(
                WithResolvingRole,
            ),
        ],
    ),
]
app = Vellox(
    Starlette(
        middleware=middleware,
        lifespan=lifespan,
        routes=routes,
        debug=True,
    )
)
