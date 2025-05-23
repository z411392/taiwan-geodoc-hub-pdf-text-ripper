from firebase_functions.https_fn import on_request
from taiwan_geodoc_hub.infrastructure.starlette import app
from taiwan_geodoc_hub.infrastructure.loop import ensure_event_loop


@on_request()
def upload(request):
    ensure_event_loop()
    return app(request)
