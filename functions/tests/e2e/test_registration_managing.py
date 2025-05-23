import pytest
from injector import Injector
from taiwan_geodoc_hub.infrastructure.flask import app
from flask import g
from flask.testing import FlaskClient
from os import getenv
from json import dumps


# @pytest.mark.skip(reason="")
class TestRegistrationManaging:
    @pytest.fixture(scope="module")
    def client(self, injector: Injector):
        with app.test_client() as client:
            with app.app_context():
                g.injector = injector.create_child_injector()
                yield client

    @pytest.mark.describe("要能夠上傳謄本並解析 PDF 中的文字")
    def test_uploading_pdf(
        self,
        client: FlaskClient,
    ):
        client.set_cookie("SESSION", getenv("SESSION_COOKIE"))
        response = client.post(
            "/",
            data=dumps(
                dict(
                    tenant_id=getenv("TENANT_ID"),
                    name="建物謄本.pdf",
                    content=getenv("PDF_SAMPLE"),
                )
            ),
            content_type="application/json",
        )
        assert response.status_code == 200
