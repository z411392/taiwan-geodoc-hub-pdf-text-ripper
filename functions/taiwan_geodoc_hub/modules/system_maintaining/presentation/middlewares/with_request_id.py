from flask import g
from injector import Injector, InstanceProvider
from taiwan_geodoc_hub.modules.system_maintaining.application.resolve_request_id import (
    ResolveRequestId,
    ResolvingRequestId,
)
from functools import wraps
from typing import Callable, Any
from taiwan_geodoc_hub.modules.system_maintaining.domain.ports.request_id_generator import (
    RequestIdGenerator,
)
from taiwan_geodoc_hub.infrastructure.generators.request_id_generator_adapter import (
    RequestIdGeneratorAdapter,
)
from logging import getLogger, Logger


def with_request_id(func: Callable[[..., Any], Any]):
    @wraps(func)
    def wrapper(*args, **kwargs):
        injector: Injector = g.get("injector")
        injector.binder.bind(
            RequestIdGenerator, to=InstanceProvider(RequestIdGeneratorAdapter())
        )
        handler: ResolveRequestId = injector.get(ResolveRequestId)
        query = ResolvingRequestId()
        request_id = handler(query)
        g.request_id: str = request_id
        logger = getLogger(request_id)
        injector.binder.bind(Logger, to=InstanceProvider(logger))
        return func(*args, **kwargs)

    return wrapper
