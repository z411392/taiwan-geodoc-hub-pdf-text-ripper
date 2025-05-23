import pytest
from injector import Injector, InstanceProvider
from taiwan_geodoc_hub.modules.common.access_managing.domain.ports.role_dao import (
    RoleDao,
)
from taiwan_geodoc_hub.modules.common.access_managing.constants.roles import Roles
from taiwan_geodoc_hub.infrastructure.constants.types import (
    TenantId,
)
from os import getenv


# @pytest.mark.skip(reason="")
class TestRoleDao:
    @pytest.fixture(scope="module")
    def role_dao(self, injector: Injector):
        injector.binder.bind(TenantId, to=InstanceProvider(getenv("TENANT_ID")))
        role_dao = injector.get(RoleDao)
        return role_dao

    @pytest.mark.describe("要能夠取得 role")
    def test_get_role_under_tenant(self, role_dao: RoleDao):
        user_id = getenv("USER_ID")
        role = role_dao.of(user_id=user_id)
        assert role is None
