"""
JWT认证系统测试
测试认证相关的端点和功能
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.crud.crud_admin import admin
from app.schemas.admin import AdminCreate


@pytest.mark.api
class TestAuthEndpoints:
    """认证端点测试"""

    @pytest.fixture
    def test_admin_data(self):
        """测试管理员数据"""
        return {
            "username": "test_admin_auth",
            "email": "test_admin_auth@test.com", 
            "password": "test123456"
        }

    @pytest.fixture
    def created_admin(self, db_session: Session, test_admin_data):
        """创建测试管理员"""
        admin_create = AdminCreate(**test_admin_data)
        created_admin = admin.create_with_password(db_session, obj_in=admin_create)
        return created_admin

    def test_login_success(self, client: TestClient, created_admin, test_admin_data):
        """测试成功登录"""
        login_data = {
            "username": test_admin_data["username"],
            "password": test_admin_data["password"]
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 200
        token_data = response.json()
        assert "access_token" in token_data
        assert "refresh_token" in token_data
        assert token_data["token_type"] == "bearer"

    def test_login_wrong_username(self, client: TestClient, created_admin, test_admin_data):
        """测试错误用户名登录"""
        login_data = {
            "username": "wrong_username",
            "password": test_admin_data["password"]
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 401
        assert "用户名或密码错误" in response.json()["detail"]

    def test_login_wrong_password(self, client: TestClient, created_admin, test_admin_data):
        """测试错误密码登录"""
        login_data = {
            "username": test_admin_data["username"],
            "password": "wrong_password"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 401
        assert "用户名或密码错误" in response.json()["detail"]

    def test_token_verification_success(self, client: TestClient, created_admin, test_admin_data):
        """测试token验证成功"""
        # 先登录获取token
        login_data = {
            "username": test_admin_data["username"],
            "password": test_admin_data["password"]
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        token_data = login_response.json()
        access_token = token_data["access_token"]
        
        # 验证token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.post("/api/v1/auth/verify", headers=headers)
        
        assert response.status_code == 200
        verify_data = response.json()
        assert verify_data["valid"] is True
        assert verify_data["user_id"] == created_admin.id

    def test_token_verification_invalid(self, client: TestClient):
        """测试无效token验证"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.post("/api/v1/auth/verify", headers=headers)
        
        assert response.status_code == 401
        assert "无效的token" in response.json()["detail"]

    def test_token_verification_missing(self, client: TestClient):
        """测试缺少token验证"""
        response = client.post("/api/v1/auth/verify")
        
        assert response.status_code == 401
        assert "未提供认证token" in response.json()["detail"]

    def test_token_refresh_success(self, client: TestClient, created_admin, test_admin_data):
        """测试token刷新成功"""
        # 先登录获取token
        login_data = {
            "username": test_admin_data["username"],
            "password": test_admin_data["password"]
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        token_data = login_response.json()
        refresh_token = token_data["refresh_token"]
        
        # 刷新token
        refresh_data = {"refresh_token": refresh_token}
        response = client.post("/api/v1/auth/refresh", json=refresh_data)
        
        assert response.status_code == 200
        new_token_data = response.json()
        assert "access_token" in new_token_data
        assert "refresh_token" in new_token_data

    def test_token_refresh_invalid(self, client: TestClient):
        """测试无效refresh token"""
        refresh_data = {"refresh_token": "invalid_refresh_token"}
        response = client.post("/api/v1/auth/refresh", json=refresh_data)
        
        assert response.status_code == 401
        assert "无效的refresh token" in response.json()["detail"]

    def test_logout_success(self, client: TestClient, created_admin, test_admin_data):
        """测试登出成功"""
        # 先登录获取token
        login_data = {
            "username": test_admin_data["username"],
            "password": test_admin_data["password"]
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        token_data = login_response.json()
        access_token = token_data["access_token"]
        
        # 登出
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.post("/api/v1/auth/logout", headers=headers)
        
        assert response.status_code == 200
        logout_data = response.json()
        assert logout_data["message"] == "登出成功"

    def test_logout_without_token(self, client: TestClient):
        """测试未提供token的登出"""
        response = client.post("/api/v1/auth/logout")
        
        assert response.status_code == 401
        assert "未提供认证token" in response.json()["detail"]

    def test_protected_endpoint_access(self, client: TestClient, created_admin, test_admin_data):
        """测试受保护端点的访问"""
        # 先登录获取token
        login_data = {
            "username": test_admin_data["username"],
            "password": test_admin_data["password"]
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        token_data = login_response.json()
        access_token = token_data["access_token"]
        
        # 访问受保护的端点（如果有的话）
        headers = {"Authorization": f"Bearer {access_token}"}
        # 这里可以添加对实际受保护端点的测试
        # response = client.get("/api/v1/protected-endpoint", headers=headers)
        # assert response.status_code == 200

    def test_login_empty_data(self, client: TestClient):
        """测试空数据登录"""
        login_data = {}
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 422  # 验证错误

    def test_login_partial_data(self, client: TestClient):
        """测试部分数据登录"""
        login_data = {"username": "test_user"}  # 缺少密码
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 422  # 验证错误


@pytest.mark.unit
class TestAuthSecurity:
    """认证安全测试"""

    def test_password_hashing(self, db_session: Session):
        """测试密码哈希"""
        admin_data = AdminCreate(
            username="test_hash_user",
            email="test_hash@test.com",
            password="plain_password"
        )
        
        created_admin = admin.create_with_password(db_session, obj_in=admin_data)
        
        # 验证密码不以明文存储
        assert created_admin.password_hash != "plain_password"
        assert len(created_admin.password_hash) > 0
        
        # 验证密码验证功能
        assert admin.authenticate(
            db_session, 
            username="test_hash_user",
            password="plain_password"
        )
        
        # 验证错误密码不通过
        assert not admin.authenticate(
            db_session,
            username="test_hash_user", 
            password="wrong_password"
        )

    def test_token_expiration_format(self, client: TestClient, db_session: Session):
        """测试token格式和过期时间"""
        # 创建测试用户
        admin_data = AdminCreate(
            username="test_token_user",
            email="test_token@test.com",
            password="test_password"
        )
        created_admin = admin.create_with_password(db_session, obj_in=admin_data)
        
        # 登录获取token
        login_data = {
            "username": "test_token_user",
            "password": "test_password"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 200
        token_data = response.json()
        
        # 验证token结构
        assert "access_token" in token_data
        assert "refresh_token" in token_data
        assert "token_type" in token_data
        assert "expires_in" in token_data
        
        # 验证token类型
        assert token_data["token_type"] == "bearer"
        
        # 验证过期时间是数字
        assert isinstance(token_data["expires_in"], int)
        assert token_data["expires_in"] > 0