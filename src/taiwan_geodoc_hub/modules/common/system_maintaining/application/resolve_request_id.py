from taiwan_geodoc_hub.modules.common.system_maintaining.domain.ports.request_id_generator import (
    RequestIdGenerator,
)
from injector import inject


class ResolveRequestId:
    _request_id_generator: RequestIdGenerator

    @inject
    def __init__(
        self,
        /,
        request_id_generator: RequestIdGenerator,
    ):
        self._request_id_generator = request_id_generator

    def __call__(self) -> str:
        return self._request_id_generator()
