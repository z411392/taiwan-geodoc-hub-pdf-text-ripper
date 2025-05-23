class TenantNotFound(Exception):
    _tenant_id: str

    def __init__(self, /, tenant_id: str):
        self._tenant_id = tenant_id

    def __iter__(self):
        yield "type", __class__.__name__
        yield "tenant_id", self._tenant_id
