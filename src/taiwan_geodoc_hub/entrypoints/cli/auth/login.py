from operator import itemgetter
from taiwan_geodoc_hub.infrastructure.lifespan import lifespan
from taiwan_geodoc_hub.modules.cli.access_managing.application.resolve_credentials import (
    ResolveCredentials,
)


async def login():
    async with lifespan() as container:
        handler = container.get(ResolveCredentials)
        try:
            credentials = await handler()
            id_token = itemgetter("id_token")(credentials)
            print(id_token)
        except Exception as exception:
            print(str(exception))
