from flask import Response, g, request
from json import dumps
from functools import wraps
from typing import Callable, Any, Optional
from injector import Injector
from logging import Logger
from time import time
from taiwan_geodoc_hub.modules.access_managing.exceptions.unauthenticated import (
    Unauthenticated,
)
from taiwan_geodoc_hub.modules.access_managing.exceptions.tenant_not_found import (
    TenantNotFound,
)
from taiwan_geodoc_hub.modules.access_managing.exceptions.permission_denied import (
    PermissionDenied,
)


def with_exception_handling(name: str):
    def decoractor(func: Callable[[..., Any], Any]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            started_at = int(time() * 1000)
            remote_addr = request.remote_addr
            request_id: Optional[str] = g.get("request_id")
            injector: Injector = g.get("injector")
            logger: Logger = injector.get(Logger)
            error: Optional[dict] = None
            try:
                return func(*args, **kwargs)
            except Unauthenticated as exception:
                error = dict(exception)
                response = Response()
                response.headers["Content-Type"] = "application/json"
                response.data = dumps(
                    dict(
                        request_id=request_id,
                        success=False,
                        data=dict(exception),
                    ),
                )
                response.status_code = 401
                return response
            except TenantNotFound as exception:
                error = dict(exception)
                response = Response()
                response.headers["Content-Type"] = "application/json"
                response.data = dumps(
                    dict(
                        request_id=request_id,
                        success=False,
                        data=dict(exception),
                    ),
                )
                response.status_code = 404
                return response
            except PermissionDenied as exception:
                error = dict(exception)
                response = Response()
                response.headers["Content-Type"] = "application/json"
                response.data = dumps(
                    dict(
                        request_id=request_id,
                        success=False,
                        data=dict(exception),
                    ),
                )
                response.status_code = 403
                return response
            except Exception as exception:
                error = dict(exception=str(exception))
                response = Response()
                response.headers["Content-Type"] = "application/json"
                response.data = dumps(
                    dict(
                        request_id=request_id,
                        success=False,
                        data=str(exception),
                    ),
                )
                response.status_code = 500
                return response
            finally:
                ended_at = int(time() * 1000)
                cost = ended_at - started_at
                logger.info(
                    dumps(
                        dict(
                            name=name,
                            started_at=started_at,
                            error=error,
                            remote_addr=remote_addr,
                            cost=cost,
                        )
                    )
                )

        return wrapper

    return decoractor
