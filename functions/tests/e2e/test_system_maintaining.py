import pytest
from injector import Injector
from taiwan_geodoc_hub.infrastructure.flask import app
from flask import g
from flask.testing import FlaskClient


# @pytest.mark.skip(reason="")
class TestSystemMaintaining:
    @pytest.fixture(scope="module")
    def client(self, injector: Injector):
        with app.test_client() as client:
            with app.app_context():
                g.injector = injector.create_child_injector()
                yield client

    @pytest.mark.describe("要能夠檢查系統是否正常運作")
    def test_checking_health(
        self,
        client: FlaskClient,
    ):
        response = client.get("/__/health")
        assert response.status_code == 200
