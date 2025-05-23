import pytest
from injector import Injector
from taiwan_geodoc_hub.modules.access_managing.domain.ports.user_dao import UserDao
from os import getenv


# @pytest.mark.skip(reason="")
class TestUserDao:
    @pytest.fixture(scope="module")
    def user_dao(self, injector: Injector):
        return injector.get(UserDao)

    @pytest.mark.describe("要能夠解析 session cookie")
    def test_get_user_from_session_cookie(self, user_dao: UserDao):
        session_cookie = getenv("SESSION_COOKIE")
        user = user_dao.from_session_cookie(session_cookie)
        assert user is not None
