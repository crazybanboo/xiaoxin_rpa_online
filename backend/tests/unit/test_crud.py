"""
Unit tests for CRUD operations
"""

import pytest
from passlib.context import CryptContext

from app.crud import admin, client, upgrade_package, upgrade_task
from app.schemas.admin import AdminCreate, AdminUpdate
from app.schemas.client import ClientCreate, ClientUpdate
from app.schemas.upgrade_package import UpgradePackageCreate, UpgradePackageUpdate
from app.schemas.upgrade_task import UpgradeTaskCreate, UpgradeTaskUpdate
from app.models.admin import Admin
from app.models.client import Client
from app.models.upgrade_package import UpgradePackage
from app.models.upgrade_task import UpgradeTask


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.mark.unit
class TestCRUDAdmin:
    """Test cases for Admin CRUD operations"""

    def test_create_admin(self, db_session, sample_admin_data):
        """Test creating an admin with base create method (no password hashing)"""
        # For base create method, we need to provide password_hash directly
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Create admin using direct model creation (not recommended for passwords)
        from app.models.admin import Admin
        admin_model = Admin(
            username=sample_admin_data["username"],
            email=sample_admin_data["email"],
            password_hash=pwd_context.hash(sample_admin_data["password"])
        )
        db_session.add(admin_model)
        db_session.commit()
        db_session.refresh(admin_model)
        
        assert admin_model.username == sample_admin_data["username"]
        assert admin_model.email == sample_admin_data["email"]
        assert admin_model.password_hash is not None

    def test_create_admin_with_password(self, db_session, sample_admin_data):
        """Test creating admin with password hashing"""
        admin_create = AdminCreate(**sample_admin_data)
        created_admin = admin.create_with_password(db_session, obj_in=admin_create)
        
        assert created_admin.username == sample_admin_data["username"]
        assert created_admin.email == sample_admin_data["email"]
        assert pwd_context.verify(sample_admin_data["password"], created_admin.password_hash)

    def test_get_admin_by_id(self, db_session, sample_admin_data):
        """Test getting admin by ID"""
        admin_create = AdminCreate(**sample_admin_data)
        created_admin = admin.create_with_password(db_session, obj_in=admin_create)
        
        retrieved_admin = admin.get(db_session, id=created_admin.id)
        assert retrieved_admin
        assert retrieved_admin.id == created_admin.id
        assert retrieved_admin.username == created_admin.username

    def test_get_admin_by_username(self, db_session, sample_admin_data):
        """Test getting admin by username"""
        admin_create = AdminCreate(**sample_admin_data)
        created_admin = admin.create_with_password(db_session, obj_in=admin_create)
        
        retrieved_admin = admin.get_by_username(db_session, username=sample_admin_data["username"])
        assert retrieved_admin
        assert retrieved_admin.id == created_admin.id
        assert retrieved_admin.username == sample_admin_data["username"]

    def test_get_admin_by_email(self, db_session, sample_admin_data):
        """Test getting admin by email"""
        admin_create = AdminCreate(**sample_admin_data)
        created_admin = admin.create_with_password(db_session, obj_in=admin_create)
        
        retrieved_admin = admin.get_by_email(db_session, email=sample_admin_data["email"])
        assert retrieved_admin
        assert retrieved_admin.id == created_admin.id
        assert retrieved_admin.email == sample_admin_data["email"]

    def test_authenticate_admin_success(self, db_session, sample_admin_data):
        """Test successful admin authentication"""
        admin_create = AdminCreate(**sample_admin_data)
        created_admin = admin.create_with_password(db_session, obj_in=admin_create)
        
        authenticated_admin = admin.authenticate(
            db_session,
            username=sample_admin_data["username"],
            password=sample_admin_data["password"]
        )
        assert authenticated_admin
        assert authenticated_admin.id == created_admin.id

    def test_authenticate_admin_wrong_password(self, db_session, sample_admin_data):
        """Test admin authentication with wrong password"""
        admin_create = AdminCreate(**sample_admin_data)
        admin.create_with_password(db_session, obj_in=admin_create)
        
        authenticated_admin = admin.authenticate(
            db_session,
            username=sample_admin_data["username"],
            password="wrong_password"
        )
        assert authenticated_admin is None

    def test_authenticate_admin_nonexistent(self, db_session):
        """Test admin authentication with non-existent user"""
        authenticated_admin = admin.authenticate(
            db_session,
            username="nonexistent_user",
            password="any_password"
        )
        assert authenticated_admin is None

    def test_update_admin(self, db_session, sample_admin_data):
        """Test updating admin"""
        admin_create = AdminCreate(**sample_admin_data)
        created_admin = admin.create_with_password(db_session, obj_in=admin_create)
        
        admin_update = AdminUpdate(email="updated@example.com")
        updated_admin = admin.update(db_session, db_obj=created_admin, obj_in=admin_update)
        
        assert updated_admin.email == "updated@example.com"
        assert updated_admin.username == sample_admin_data["username"]

    def test_delete_admin(self, db_session, sample_admin_data):
        """Test deleting admin"""
        admin_create = AdminCreate(**sample_admin_data)
        created_admin = admin.create_with_password(db_session, obj_in=admin_create)
        
        admin.remove(db_session, id=created_admin.id)
        deleted_admin = admin.get(db_session, id=created_admin.id)
        assert deleted_admin is None


@pytest.mark.unit
class TestCRUDClient:
    """Test cases for Client CRUD operations"""

    def test_create_client(self, db_session, sample_client_data):
        """Test creating a client"""
        client_create = ClientCreate(**sample_client_data)
        created_client = client.create(db_session, obj_in=client_create)
        
        assert created_client.name == sample_client_data["name"]
        assert created_client.ip_address == sample_client_data["ip_address"]
        assert created_client.version == sample_client_data["version"]
        assert created_client.status == sample_client_data["status"]

    def test_get_client_by_ip(self, db_session, sample_client_data):
        """Test getting client by IP address"""
        client_create = ClientCreate(**sample_client_data)
        created_client = client.create(db_session, obj_in=client_create)
        
        retrieved_client = client.get_by_ip(db_session, ip_address=sample_client_data["ip_address"])
        assert retrieved_client
        assert retrieved_client.id == created_client.id
        assert retrieved_client.ip_address == sample_client_data["ip_address"]

    def test_get_online_clients(self, db_session):
        """Test getting online clients"""
        # Create online client
        online_client_data = {
            "name": "在线客户端",
            "ip_address": "192.168.1.100",
            "version": "1.0.0",
            "status": "online"
        }
        client_create_online = ClientCreate(**online_client_data)
        client.create(db_session, obj_in=client_create_online)
        
        # Create offline client
        offline_client_data = {
            "name": "离线客户端",
            "ip_address": "192.168.1.101",
            "version": "1.0.0",
            "status": "offline"
        }
        client_create_offline = ClientCreate(**offline_client_data)
        client.create(db_session, obj_in=client_create_offline)
        
        online_clients = client.get_online_clients(db_session)
        assert len(online_clients) == 1
        assert online_clients[0].status == "online"

    def test_update_heartbeat(self, db_session, sample_client_data):
        """Test updating client heartbeat"""
        client_create = ClientCreate(**sample_client_data)
        created_client = client.create(db_session, obj_in=client_create)
        
        updated_client = client.update_heartbeat(db_session, client_id=created_client.id)
        assert updated_client.last_heartbeat is not None


@pytest.mark.unit
class TestCRUDUpgradePackage:
    """Test cases for UpgradePackage CRUD operations"""

    def test_create_package(self, db_session, sample_package_data):
        """Test creating an upgrade package"""
        package_create = UpgradePackageCreate(**sample_package_data)
        created_package = upgrade_package.create(db_session, obj_in=package_create)
        
        assert created_package.name == sample_package_data["name"]
        assert created_package.version == sample_package_data["version"]
        assert created_package.file_path == sample_package_data["file_path"]
        assert created_package.file_size == sample_package_data["file_size"]

    def test_get_package_by_version(self, db_session, sample_package_data):
        """Test getting packages by version"""
        package_create = UpgradePackageCreate(**sample_package_data)
        created_package = upgrade_package.create(db_session, obj_in=package_create)
        
        retrieved_packages = upgrade_package.get_by_version(db_session, version=sample_package_data["version"])
        assert len(retrieved_packages) == 1
        assert retrieved_packages[0].id == created_package.id
        assert retrieved_packages[0].version == sample_package_data["version"]

    def test_get_latest_version_package(self, db_session):
        """Test getting latest version of a specific package"""
        # Create packages with same name but different versions
        package1_data = {
            "name": "测试包",
            "version": "1.0.0",
            "file_path": "/path1.zip",
            "file_size": 1024
        }
        package2_data = {
            "name": "测试包",
            "version": "2.0.0",
            "file_path": "/path2.zip",
            "file_size": 2048
        }
        
        package1_create = UpgradePackageCreate(**package1_data)
        package2_create = UpgradePackageCreate(**package2_data)
        
        upgrade_package.create(db_session, obj_in=package1_create)
        created_package2 = upgrade_package.create(db_session, obj_in=package2_create)
        
        latest_package = upgrade_package.get_latest_version(db_session, name="测试包")
        assert latest_package
        assert latest_package.id == created_package2.id


@pytest.mark.unit
class TestCRUDUpgradeTask:
    """Test cases for UpgradeTask CRUD operations"""

    def test_create_task(self, db_session, sample_client_data, sample_package_data):
        """Test creating an upgrade task"""
        # Create client and package first
        client_create = ClientCreate(**sample_client_data)
        created_client = client.create(db_session, obj_in=client_create)
        
        package_create = UpgradePackageCreate(**sample_package_data)
        created_package = upgrade_package.create(db_session, obj_in=package_create)
        
        task_data = {
            "client_id": created_client.id,
            "package_id": created_package.id,
            "status": "pending"
        }
        task_create = UpgradeTaskCreate(**task_data)
        created_task = upgrade_task.create(db_session, obj_in=task_create)
        
        assert created_task.client_id == created_client.id
        assert created_task.package_id == created_package.id
        assert created_task.status == "pending"

    def test_get_tasks_by_client(self, db_session, sample_client_data, sample_package_data):
        """Test getting tasks by client ID"""
        # Create client and package first
        client_create = ClientCreate(**sample_client_data)
        created_client = client.create(db_session, obj_in=client_create)
        
        package_create = UpgradePackageCreate(**sample_package_data)
        created_package = upgrade_package.create(db_session, obj_in=package_create)
        
        # Create task
        task_data = {
            "client_id": created_client.id,
            "package_id": created_package.id,
            "status": "pending"
        }
        task_create = UpgradeTaskCreate(**task_data)
        upgrade_task.create(db_session, obj_in=task_create)
        
        client_tasks = upgrade_task.get_by_client(db_session, client_id=created_client.id)
        assert len(client_tasks) == 1
        assert client_tasks[0].client_id == created_client.id

    def test_get_tasks_by_status(self, db_session, sample_client_data, sample_package_data):
        """Test getting tasks by status"""
        # Create client and package first
        client_create = ClientCreate(**sample_client_data)
        created_client = client.create(db_session, obj_in=client_create)
        
        package_create = UpgradePackageCreate(**sample_package_data)
        created_package = upgrade_package.create(db_session, obj_in=package_create)
        
        # Create tasks with different statuses
        task1_data = {
            "client_id": created_client.id,
            "package_id": created_package.id,
            "status": "pending"
        }
        task2_data = {
            "client_id": created_client.id,
            "package_id": created_package.id,
            "status": "completed"
        }
        
        task1_create = UpgradeTaskCreate(**task1_data)
        task2_create = UpgradeTaskCreate(**task2_data)
        
        upgrade_task.create(db_session, obj_in=task1_create)
        upgrade_task.create(db_session, obj_in=task2_create)
        
        pending_tasks = upgrade_task.get_by_status(db_session, status="pending")
        assert len(pending_tasks) == 1
        assert pending_tasks[0].status == "pending"

    def test_complete_task(self, db_session, sample_client_data, sample_package_data):
        """Test completing a task"""
        # Create client and package first
        client_create = ClientCreate(**sample_client_data)
        created_client = client.create(db_session, obj_in=client_create)
        
        package_create = UpgradePackageCreate(**sample_package_data)
        created_package = upgrade_package.create(db_session, obj_in=package_create)
        
        # Create task
        task_data = {
            "client_id": created_client.id,
            "package_id": created_package.id,
            "status": "pending"
        }
        task_create = UpgradeTaskCreate(**task_data)
        created_task = upgrade_task.create(db_session, obj_in=task_create)
        
        # Complete task successfully
        completed_task = upgrade_task.complete_task(db_session, task_id=created_task.id, success=True)
        assert completed_task.status == "completed"
        assert completed_task.completed_at is not None