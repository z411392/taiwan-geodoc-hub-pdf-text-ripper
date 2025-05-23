from flask import Response
from json import dumps


def on_checking_health():
    response = Response()
    response.headers["Content-Type"] = "application/json"
    response.data = dumps(
        dict(
            success=True,
        )
    )
    response.status_code = 200
    return response
