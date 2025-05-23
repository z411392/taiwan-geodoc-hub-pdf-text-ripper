from firebase_functions.https_fn import on_request
from taiwan_geodoc_hub.entrypoints.http.cms.cms import vellox as handle_request
from taiwan_geodoc_hub.infrastructure.utils.event_loop import ensure_event_loop
from async_typer import AsyncTyper
from taiwan_geodoc_hub.entrypoints.cli.auth.login import login


@on_request(cors=True)
def upload(request):
    ensure_event_loop()
    return handle_request(request)


if __name__ == "__main__":
    loop = ensure_event_loop()
    app = AsyncTyper()
    auth, add_auth_command = (_ := AsyncTyper(name="auth")), (_.async_command())
    add_auth_command(login)
    app.add_typer(auth)
    loop.run_until_complete(app())
