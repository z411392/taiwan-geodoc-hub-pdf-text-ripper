import pytest
from starlette.testclient import TestClient
from taiwan_geodoc_hub.entrypoints.http.cms.cms import app


# @pytest.mark.skip(reason="")
class TestSystemMaintaining:
    @pytest.fixture(scope="module")
    def client(self):
        with TestClient(app) as client:
            yield client

    @pytest.mark.describe("要能夠檢查系統是否正常運作")
    def test_checking_health(self, client: TestClient):
        response = client.get("/__/health")
        assert response.status_code == 200
