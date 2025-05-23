import pytest
from injector import Injector, InstanceProvider
from taiwan_geodoc_hub.modules.access_managing.domain.ports.role_dao import RoleDao
from taiwan_geodoc_hub.modules.access_managing.constants.roles import Roles
from taiwan_geodoc_hub.infrastructure.injection_tokens import (
    TenantId,
)


# @pytest.mark.skip(reason="")
class TestRoleDao:
    @pytest.fixture(scope="module")
    def role_dao(self, injector: Injector, tenant_id: str):
        injector.binder.bind(TenantId, to=InstanceProvider(tenant_id))
        role_dao = injector.get(RoleDao)
        return role_dao

    @pytest.mark.describe("要能夠取得 role")
    def test_get_role_under_tenant(self, role_dao: RoleDao, user_id: str):
        role = role_dao.of(user_id=user_id)
        if role is None:
            return pytest.fail(f"無法取得 role, user_id={user_id}")
        assert role == Roles.manager
