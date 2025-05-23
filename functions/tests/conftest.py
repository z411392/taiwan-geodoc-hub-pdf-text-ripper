import pytest
from base64 import b64decode
from taiwan_geodoc_hub.lifespan import lifespan
from os import getenv


@pytest.fixture(scope="session")
def injector():
    with lifespan() as injector:
        yield injector


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
