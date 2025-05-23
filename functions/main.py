from firebase_functions.https_fn import on_request, Request
from taiwan_geodoc_hub.lifespan import lifespan
from taiwan_geodoc_hub.http import app
from flask import g, request

context = lifespan()
injector = context.__enter__()


@on_request()
def upload(firebase_functions_request: Request):
    with app.request_context(firebase_functions_request.environ):
        g.injector = injector.create_child_injector()
        request._cached_data = firebase_functions_request.get_data()
        return app.full_dispatch_request()
