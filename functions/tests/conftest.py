import pytest
from base64 import b64decode
from taiwan_geodoc_hub.infrastructure.lifespan import lifespan
from os import getenv
from taiwan_geodoc_hub.infrastructure.loop import ensure_event_loop


@pytest.fixture(scope="session")
def injector():
    loop = ensure_event_loop()
    context = lifespan()
    try:
        injector = loop.run_until_complete(context.__aenter__())
        yield injector
        loop.run_until_complete(context.__aexit__(None, None, None))
    except Exception as exception:
        loop.run_until_complete(
            context.__aexit__(type(exception), exception, exception.__traceback__)
        )


@pytest.fixture(scope="session")
def sample_image():
    return b64decode(getenv("SAMPLE_IMAGE"))


@pytest.fixture(scope="session")
def sample_image_hash():
    return getenv("SAMPLE_IMAGE_HASH")


@pytest.fixture(scope="session")
def sample_ocr_result():
    return getenv("SAMPLE_OCR_RESULT")


@pytest.fixture(scope="session")
def tenant_id():
    return getenv("TENANT_ID")


@pytest.fixture(scope="session")
def user_id():
    return getenv("USER_ID")
