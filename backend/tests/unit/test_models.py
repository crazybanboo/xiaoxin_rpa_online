"""
Unit tests for SQLAlchemy models
"""

import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from app.models.admin import Admin
from app.models.client import Client
from app.models.upgrade_package import UpgradePackage
from app.models.upgrade_task import UpgradeTask


@pytest.mark.unit
class TestAdminModel:
    """Test cases for Admin model"""

    def test_admin_creation(self, db_session):
        """Test creating a new admin"""
        admin = Admin(
            username="test_admin",
            password_hash="hashed_password",
            email="test@example.com"
        )
        db_session.add(admin)
        db_session.commit()
        
        assert admin.id is not None
        assert admin.username == "test_admin"
        assert admin.email == "test@example.com"
        assert admin.created_at is not None
        assert admin.updated_at is not None

    def test_admin_unique_username(self, db_session):
        """Test username uniqueness constraint"""
        admin1 = Admin(
            username="test_admin",
            password_hash="hash1",
            email="test1@example.com"
        )
        admin2 = Admin(
            username="test_admin",
            password_hash="hash2", 
            email="test2@example.com"
        )
        
        db_session.add(admin1)
        db_session.commit()
        
        db_session.add(admin2)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_admin_unique_email(self, db_session):
        """Test email uniqueness constraint"""
        admin1 = Admin(
            username="test_admin1",
            password_hash="hash1",
            email="test@example.com"
        )
        admin2 = Admin(
            username="test_admin2",
            password_hash="hash2",
            email="test@example.com"
        )
        
        db_session.add(admin1)
        db_session.commit()
        
        db_session.add(admin2)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_admin_repr(self, db_session):
        """Test admin string representation"""
        admin = Admin(
            username="test_admin",
            password_hash="hashed_password", 
            email="test@example.com"
        )
        db_session.add(admin)
        db_session.commit()
        
        expected = f"<Admin(id={admin.id}, username='test_admin', email='test@example.com')>"
        assert repr(admin) == expected


@pytest.mark.unit 
class TestClientModel:
    """Test cases for Client model"""

    def test_client_creation(self, db_session):
        """Test creating a new client"""
        client = Client(
            name="测试客户端",
            ip_address="192.168.1.100",
            version="1.0.0",
            status="online"
        )
        db_session.add(client)
        db_session.commit()
        
        assert client.id is not None
        assert client.name == "测试客户端"
        assert client.ip_address == "192.168.1.100"
        assert client.version == "1.0.0"
        assert client.status == "online"
        assert client.created_at is not None
        assert client.updated_at is not None

    def test_client_default_values(self, db_session):
        """Test client model default values"""
        client = Client(
            name="测试客户端",
            ip_address="192.168.1.100",
            version="1.0.0"
        )
        db_session.add(client)
        db_session.commit()
        
        assert client.status == "offline"
        assert client.last_heartbeat is None

    def test_client_repr(self, db_session):
        """Test client string representation"""
        client = Client(
            name="测试客户端",
            ip_address="192.168.1.100",
            version="1.0.0"
        )
        db_session.add(client)
        db_session.commit()
        
        expected = f"<Client(id={client.id}, name='测试客户端', ip='192.168.1.100', status='offline')>"
        assert repr(client) == expected


@pytest.mark.unit
class TestUpgradePackageModel:
    """Test cases for UpgradePackage model"""

    def test_package_creation(self, db_session):
        """Test creating a new upgrade package"""
        package = UpgradePackage(
            name="测试升级包",
            version="2.0.0",
            file_path="/path/to/package.zip",
            file_size=1024000
        )
        db_session.add(package)
        db_session.commit()
        
        assert package.id is not None
        assert package.name == "测试升级包"
        assert package.version == "2.0.0"
        assert package.file_path == "/path/to/package.zip"
        assert package.file_size == 1024000
        assert package.created_at is not None
        assert package.updated_at is not None


    def test_package_repr(self, db_session):
        """Test package string representation"""
        package = UpgradePackage(
            name="测试升级包",
            version="2.0.0",
            file_path="/path/to/package.zip",
            file_size=1024000
        )
        db_session.add(package)
        db_session.commit()
        
        expected = f"<UpgradePackage(id={package.id}, name='测试升级包', version='2.0.0')>"
        assert repr(package) == expected


@pytest.mark.unit
class TestUpgradeTaskModel:
    """Test cases for UpgradeTask model"""

    def test_task_creation(self, db_session):
        """Test creating a new upgrade task"""
        # Create client and package first
        client = Client(name="测试客户端", ip_address="192.168.1.100", version="1.0.0")
        package = UpgradePackage(
            name="测试升级包",
            version="2.0.0", 
            file_path="/path.zip",
            file_size=1024
        )
        db_session.add(client)
        db_session.add(package)
        db_session.commit()
        
        task = UpgradeTask(
            client_id=client.id,
            package_id=package.id,
            status="pending"
        )
        db_session.add(task)
        db_session.commit()
        
        assert task.id is not None
        assert task.client_id == client.id
        assert task.package_id == package.id
        assert task.status == "pending"
        assert task.created_at is not None
        assert task.updated_at is not None

    def test_task_default_status(self, db_session):
        """Test task default status"""
        client = Client(name="测试客户端", ip_address="192.168.1.100", version="1.0.0")
        package = UpgradePackage(
            name="测试升级包",
            version="2.0.0",
            file_path="/path.zip", 
            file_size=1024
        )
        db_session.add(client)
        db_session.add(package)
        db_session.commit()
        
        task = UpgradeTask(
            client_id=client.id,
            package_id=package.id
        )
        db_session.add(task)
        db_session.commit()
        
        assert task.status == "pending"

    def test_task_relationships(self, db_session):
        """Test task relationships with client and package"""
        client = Client(name="测试客户端", ip_address="192.168.1.100", version="1.0.0")
        package = UpgradePackage(
            name="测试升级包",
            version="2.0.0",
            file_path="/path.zip",
            file_size=1024
        )
        db_session.add(client)
        db_session.add(package)
        db_session.commit()
        
        task = UpgradeTask(
            client_id=client.id,
            package_id=package.id
        )
        db_session.add(task)
        db_session.commit()
        
        # Test relationships
        assert task.client.name == "测试客户端"
        assert task.package.name == "测试升级包"
        assert len(client.upgrade_tasks) == 1
        assert client.upgrade_tasks[0].id == task.id

    def test_task_repr(self, db_session):
        """Test task string representation"""
        client = Client(name="测试客户端", ip_address="192.168.1.100", version="1.0.0")
        package = UpgradePackage(
            name="测试升级包",
            version="2.0.0",
            file_path="/path.zip",
            file_size=1024
        )
        db_session.add(client)
        db_session.add(package)
        db_session.commit()
        
        task = UpgradeTask(
            client_id=client.id,
            package_id=package.id,
            status="pending"
        )
        db_session.add(task)
        db_session.commit()
        
        expected = f"<UpgradeTask(id={task.id}, client_id={client.id}, package_id={package.id}, status='pending')>"
        assert repr(task) == expected


@pytest.mark.unit
class TestTimestampMixin:
    """Test cases for timestamp functionality"""

    def test_timestamps_auto_created(self, db_session):
        """Test that timestamps are automatically created"""
        admin = Admin(
            username="test_admin",
            password_hash="hash",
            email="test@example.com"
        )
        db_session.add(admin)
        db_session.commit()
        
        assert admin.created_at is not None
        assert admin.updated_at is not None
        assert isinstance(admin.created_at, datetime)
        assert isinstance(admin.updated_at, datetime)

    def test_updated_at_changes(self, db_session):
        """Test that updated_at changes on update"""
        import time
        
        admin = Admin(
            username="test_admin",
            password_hash="hash",
            email="test@example.com"
        )
        db_session.add(admin)
        db_session.commit()
        
        original_updated = admin.updated_at
        
        # Wait a small amount to ensure timestamp difference
        time.sleep(0.01)
        
        # Update the admin
        admin.username = "updated_admin"
        db_session.commit()
        db_session.refresh(admin)
        
        assert admin.updated_at >= original_updated