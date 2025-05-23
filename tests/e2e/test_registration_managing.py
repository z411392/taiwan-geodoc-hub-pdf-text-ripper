import pytest
from starlette.testclient import TestClient
from taiwan_geodoc_hub.entrypoints.http.cms.cms import app
from os import getenv
from json import dumps


# @pytest.mark.skip(reason="")
class TestRegistrationManaging:
    @pytest.fixture(scope="module")
    def client(self):
        with TestClient(app) as client:
            yield client

    @pytest.mark.describe("要能夠上傳謄本並解析 PDF 中的文字")
    def test_uploading_pdf(
        self,
        client: TestClient,
        sample_pdf: bytes,
    ):
        response = client.post(
            f"/tenants/{getenv('TENANT_ID')}/pdf",
            content=dumps(
                dict(
                    name="建物謄本.pdf",
                    content=sample_pdf,
                ),
                ensure_ascii=False,
            ).encode("utf-8"),
            headers=dict(Authorization=f"bearer {getenv('ID_TOKEN')}"),
        )
        assert response.status_code == 200
