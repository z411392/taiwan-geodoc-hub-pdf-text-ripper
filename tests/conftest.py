import pytest
from base64 import b64decode
from taiwan_geodoc_hub.infrastructure.lifespan import lifespan
from taiwan_geodoc_hub.infrastructure.utils.event_loop import ensure_event_loop
from os.path import exists
from json import loads
from operator import itemgetter
from os import environ
from asyncio import AbstractEventLoop
from typing import Optional
from types import TracebackType


@pytest.fixture(scope="function", autouse=True)
def set_environment_variables():
    if exists("credentials.json"):
        with open("credentials.json", encoding="utf-8") as file:
            environ["ID_TOKEN"] = itemgetter("id_token")(loads(file.read()))


@pytest.fixture(scope="session", autouse=True)
def loop():
    return ensure_event_loop()


@pytest.fixture(scope="session")
def injector(loop: AbstractEventLoop):
    context = lifespan()
    exc_info: Optional[
        tuple[type[BaseException], BaseException, Optional[TracebackType]]
    ] = (None, None, None)
    try:
        injector = loop.run_until_complete(context.__aenter__())
        yield injector
    except Exception as exception:
        exc_info = type(exception), exception, exception.__traceback__
    finally:
        loop.run_until_complete(context.__aexit__(*exc_info))


@pytest.fixture(scope="function")
def sample_image():
    with open("assets/sample_image.dat", encoding="utf-8") as file:
        return b64decode(file.read())


@pytest.fixture(scope="function")
def sample_image_hash():
    with open("assets/sample_image_hash.dat", encoding="utf-8") as file:
        return file.read()


@pytest.fixture(scope="function")
def sample_ocr_result():
    with open("assets/sample_ocr_result.txt", encoding="utf-8") as file:
        return file.read()


@pytest.fixture(scope="function")
def sample_pdf():
    with open("assets/sample_pdf.dat", encoding="utf-8") as file:
        return file.read()
