from uuid import uuid1, uuid4, uuid5
from shortuuid import encode
from taiwan_geodoc_hub.modules.system_maintaining.domain.ports.request_id_generator import (
    RequestIdGenerator,
)


class RequestIdGeneratorAdapter(RequestIdGenerator):
    def __call__(self):
        return encode(uuid5(uuid1(), str(uuid4())))
