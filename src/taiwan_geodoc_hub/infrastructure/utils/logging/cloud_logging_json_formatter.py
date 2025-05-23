from logging import Formatter
from datetime import datetime
from json import dumps
from firebase_admin.auth import UserRecord
from taiwan_geodoc_hub.modules.common.access_managing.dtos.tenant import Tenant
from taiwan_geodoc_hub.modules.common.access_managing.constants.roles import Roles


class CloudLoggingJSONFormatter(Formatter):
    def format(self, record):
        timestamp = datetime.fromtimestamp(record.created)
        entry = dict(
            name=record.name,
            severity=record.levelname,
            timestamp=f"{timestamp.isoformat()}Z",
            message=record.getMessage(),
        )

        if hasattr(record, "elapsed"):
            elapsed: float = getattr(record, "elapsed")
            entry["elapsed"] = elapsed

        if record.exc_info and isinstance(record.exc_info, tuple):
            (type, exception, _traceback) = record.exc_info
            error = dict(
                type=type.__name__ if type else None,
                message=str(exception) if exception else None,
            )
            entry["error"] = error

        labels = dict()
        if hasattr(record, "user"):
            user: UserRecord = getattr(record, "user")
            labels.update(userId=user.uid)

        if hasattr(record, "tenant"):
            tenant: Tenant = getattr(record, "tenant")
            labels.update(tenantId=tenant.get("id"))

        if hasattr(record, "role"):
            role: Roles = getattr(record, "role")
            labels.update(role=role.value)

        entry.update(labels=labels)

        return dumps(
            entry,
            ensure_ascii=False,
            indent=4,
        )
