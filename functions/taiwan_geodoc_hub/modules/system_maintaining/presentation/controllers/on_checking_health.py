from starlette.requests import Request
from starlette.responses import JSONResponse


async def on_checking_health(request: Request):
    return JSONResponse(
        dict(
            request_id=request.scope["request_id"],
            success=True,
            data=dict(),
        )
    )
