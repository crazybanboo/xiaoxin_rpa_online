"""
Unit tests for Pydantic schemas
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

from app.schemas.admin import AdminCreate, AdminUpdate, Admin, AdminInDB
from app.schemas.client import ClientCreate, ClientUpdate, Client
from app.schemas.upgrade_package import UpgradePackageCreate, UpgradePackageUpdate, UpgradePackage
from app.schemas.upgrade_task import UpgradeTaskCreate, UpgradeTaskUpdate, UpgradeTask


@pytest.mark.unit
class TestAdminSchemas:
    """Test cases for Admin schemas"""

    def test_admin_create_valid(self):
        """Test valid AdminCreate schema"""
        admin_data = {
            "username": "test_admin",
            "email": "test@example.com",
            "password": "test123"
        }
        admin = AdminCreate(**admin_data)
        assert admin.username == "test_admin"
        assert admin.email == "test@example.com"
        assert admin.password == "test123"

    def test_admin_create_invalid_email(self):
        """Test AdminCreate with invalid email"""
        admin_data = {
            "username": "test_admin",
            "email": "invalid_email",
            "password": "test123"
        }
        with pytest.raises(ValidationError):
            AdminCreate(**admin_data)

    def test_admin_create_missing_required_field(self):
        """Test AdminCreate with missing required field"""
        admin_data = {
            "username": "test_admin",
            "email": "test@example.com"
            # Missing password
        }
        with pytest.raises(ValidationError):
            AdminCreate(**admin_data)

    def test_admin_update_partial(self):
        """Test AdminUpdate with partial data"""
        admin_update = AdminUpdate(email="updated@example.com")
        assert admin_update.email == "updated@example.com"
        assert admin_update.username is None
        assert admin_update.password is None

    def test_admin_update_all_fields(self):
        """Test AdminUpdate with all fields"""
        admin_update = AdminUpdate(
            username="updated_admin",
            email="updated@example.com",
            password="new_password"
        )
        assert admin_update.username == "updated_admin"
        assert admin_update.email == "updated@example.com"
        assert admin_update.password == "new_password"

    def test_admin_response_schema(self):
        """Test Admin response schema"""
        admin_data = {
            "id": 1,
            "username": "test_admin",
            "email": "test@example.com",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        admin = Admin(**admin_data)
        assert admin.id == 1
        assert admin.username == "test_admin"
        assert admin.email == "test@example.com"

    def test_admin_in_db_schema(self):
        """Test AdminInDB schema with password hash"""
        admin_data = {
            "id": 1,
            "username": "test_admin",
            "email": "test@example.com",
            "password_hash": "hashed_password",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        admin = AdminInDB(**admin_data)
        assert admin.password_hash == "hashed_password"


@pytest.mark.unit
class TestClientSchemas:
    """Test cases for Client schemas"""

    def test_client_create_valid(self):
        """Test valid ClientCreate schema"""
        client_data = {
            "name": "测试客户端",
            "ip_address": "192.168.1.100",
            "version": "1.0.0",
            "status": "online"
        }
        client = ClientCreate(**client_data)
        assert client.name == "测试客户端"
        assert client.ip_address == "192.168.1.100"
        assert client.version == "1.0.0"
        assert client.status == "online"

    def test_client_create_minimal(self):
        """Test ClientCreate with minimal required fields"""
        client_data = {
            "name": "测试客户端",
            "ip_address": "192.168.1.100",
            "version": "1.0.0"
        }
        client = ClientCreate(**client_data)
        assert client.name == "测试客户端"
        assert client.ip_address == "192.168.1.100"
        assert client.version == "1.0.0"
        assert client.status == "offline"  # Default value

    def test_client_create_invalid_ip(self):
        """Test ClientCreate with invalid IP address format"""
        client_data = {
            "name": "测试客户端",
            "ip_address": "invalid_ip"
        }
        # Note: The schema doesn't enforce IP format validation currently
        # This test would fail if IP validation was added
        client = ClientCreate(**client_data)
        assert client.ip_address == "invalid_ip"

    def test_client_update_partial(self):
        """Test ClientUpdate with partial data"""
        client_update = ClientUpdate(status="offline")
        assert client_update.status == "offline"
        assert client_update.name is None

    def test_client_response_schema(self):
        """Test Client response schema"""
        client_data = {
            "id": 1,
            "name": "测试客户端",
            "ip_address": "192.168.1.100",
            "version": "1.0.0",
            "status": "online",
            "last_heartbeat": datetime.now(),
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        client = Client(**client_data)
        assert client.id == 1
        assert client.name == "测试客户端"


@pytest.mark.unit
class TestUpgradePackageSchemas:
    """Test cases for UpgradePackage schemas"""

    def test_package_create_valid(self):
        """Test valid UpgradePackageCreate schema"""
        package_data = {
            "name": "测试升级包",
            "version": "2.0.0",
            "file_path": "/path/to/package.zip",
            "file_size": 1024000
        }
        package = UpgradePackageCreate(**package_data)
        assert package.name == "测试升级包"
        assert package.version == "2.0.0"
        assert package.file_path == "/path/to/package.zip"
        assert package.file_size == 1024000

    def test_package_create_missing_field(self):
        """Test UpgradePackageCreate with missing required field"""
        package_data = {
            "name": "测试升级包",
            "version": "2.0.0",
            "file_path": "/path/to/package.zip"
            # Missing file_size
        }
        with pytest.raises(ValidationError):
            UpgradePackageCreate(**package_data)

    def test_package_create_invalid_file_size(self):
        """Test UpgradePackageCreate with invalid file size"""
        package_data = {
            "name": "测试升级包",
            "version": "2.0.0",
            "file_path": "/path/to/package.zip",
            "file_size": "invalid_size"  # Should be integer
        }
        with pytest.raises(ValidationError):
            UpgradePackageCreate(**package_data)

    def test_package_update_partial(self):
        """Test UpgradePackageUpdate with partial data"""
        package_update = UpgradePackageUpdate(name="更新的升级包")
        assert package_update.name == "更新的升级包"
        assert package_update.version is None

    def test_package_response_schema(self):
        """Test UpgradePackage response schema"""
        package_data = {
            "id": 1,
            "name": "测试升级包",
            "version": "2.0.0",
            "file_path": "/path/to/package.zip",
            "file_size": 1024000,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        package = UpgradePackage(**package_data)
        assert package.id == 1
        assert package.name == "测试升级包"


@pytest.mark.unit
class TestUpgradeTaskSchemas:
    """Test cases for UpgradeTask schemas"""

    def test_task_create_valid(self):
        """Test valid UpgradeTaskCreate schema"""
        task_data = {
            "client_id": 1,
            "package_id": 1,
            "status": "pending"
        }
        task = UpgradeTaskCreate(**task_data)
        assert task.client_id == 1
        assert task.package_id == 1
        assert task.status == "pending"

    def test_task_create_minimal(self):
        """Test UpgradeTaskCreate with minimal required fields"""
        task_data = {
            "client_id": 1,
            "package_id": 1
        }
        task = UpgradeTaskCreate(**task_data)
        assert task.client_id == 1
        assert task.package_id == 1

    def test_task_create_invalid_ids(self):
        """Test UpgradeTaskCreate with invalid ID types"""
        task_data = {
            "client_id": "invalid_id",  # Should be integer
            "package_id": 1
        }
        with pytest.raises(ValidationError):
            UpgradeTaskCreate(**task_data)

    def test_task_update_partial(self):
        """Test UpgradeTaskUpdate with partial data"""
        task_update = UpgradeTaskUpdate(status="completed")
        assert task_update.status == "completed"
        assert task_update.completed_at is None

    def test_task_response_schema(self):
        """Test UpgradeTask response schema"""
        task_data = {
            "id": 1,
            "client_id": 1,
            "package_id": 1,
            "status": "pending",
            "completed_at": None,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        task = UpgradeTask(**task_data)
        assert task.id == 1
        assert task.client_id == 1
        assert task.package_id == 1
        assert task.status == "pending"


@pytest.mark.unit
class TestSchemaValidation:
    """Test cases for general schema validation"""

    def test_datetime_serialization(self):
        """Test datetime field serialization"""
        admin_data = {
            "id": 1,
            "username": "test_admin",
            "email": "test@example.com",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        admin = Admin(**admin_data)
        
        # Test that datetime fields can be serialized
        admin_dict = admin.model_dump()
        assert "created_at" in admin_dict
        assert "updated_at" in admin_dict

    def test_from_attributes_config(self):
        """Test from_attributes configuration for ORM compatibility"""
        # This would typically be tested with actual SQLAlchemy model instances
        # Here we just verify the config is set correctly
        admin_data = {
            "id": 1,
            "username": "test_admin",
            "email": "test@example.com",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        admin = Admin(**admin_data)
        assert hasattr(admin.model_config, 'from_attributes') or hasattr(admin.Config, 'from_attributes')