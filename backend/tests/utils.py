"""
Test utilities and helper functions
"""

import random
import string
from datetime import datetime, timedelta
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.admin import Admin
from app.models.client import Client
from app.models.upgrade_package import UpgradePackage
from app.models.upgrade_task import UpgradeTask


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_random_string(length: int = 10) -> str:
    """Generate a random string of specified length"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_random_email() -> str:
    """Generate a random email address"""
    username = generate_random_string(8)
    domain = generate_random_string(6)
    return f"{username}@{domain}.com"


def generate_random_ip() -> str:
    """Generate a random IP address"""
    return f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"


def create_test_admin(db: Session, **kwargs) -> Admin:
    """Create a test admin with optional custom fields"""
    default_data = {
        "username": generate_random_string(8),
        "email": generate_random_email(),
        "password_hash": pwd_context.hash("test123")
    }
    default_data.update(kwargs)
    
    admin = Admin(**default_data)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


def create_test_client(db: Session, **kwargs) -> Client:
    """Create a test client with optional custom fields"""
    default_data = {
        "name": f"测试客户端_{generate_random_string(4)}",
        "ip_address": generate_random_ip(),
        "version": "1.0.0",
        "status": "online"
    }
    default_data.update(kwargs)
    
    client = Client(**default_data)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def create_test_package(db: Session, **kwargs) -> UpgradePackage:
    """Create a test upgrade package with optional custom fields"""
    default_data = {
        "name": f"测试升级包_{generate_random_string(4)}",
        "version": f"2.{random.randint(0, 9)}.{random.randint(0, 9)}",
        "file_path": f"/path/to/package_{generate_random_string(8)}.zip",
        "file_size": random.randint(1024, 1024000)
    }
    default_data.update(kwargs)
    
    package = UpgradePackage(**default_data)
    db.add(package)
    db.commit()
    db.refresh(package)
    return package


def create_test_task(db: Session, client_id: int = None, package_id: int = None, **kwargs) -> UpgradeTask:
    """Create a test upgrade task with optional custom fields"""
    # Create client and package if not provided
    if client_id is None:
        client = create_test_client(db)
        client_id = client.id
    
    if package_id is None:
        package = create_test_package(db)
        package_id = package.id
    
    default_data = {
        "client_id": client_id,
        "package_id": package_id,
        "status": "pending"
    }
    default_data.update(kwargs)
    
    task = UpgradeTask(**default_data)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def assert_datetime_recent(dt: datetime, seconds: int = 5):
    """Assert that datetime is within the last N seconds"""
    now = datetime.utcnow()
    assert (now - dt).total_seconds() <= seconds, f"Datetime {dt} is not recent enough"


def assert_models_equal(model1: Any, model2: Any, ignore_fields: List[str] = None):
    """Assert that two SQLAlchemy models are equal, ignoring specified fields"""
    if ignore_fields is None:
        ignore_fields = ['created_at', 'updated_at']
    
    # Get all column names from model1
    columns = [c.name for c in model1.__table__.columns if c.name not in ignore_fields]
    
    for column in columns:
        value1 = getattr(model1, column)
        value2 = getattr(model2, column)
        assert value1 == value2, f"Field {column} differs: {value1} != {value2}"


def create_test_data_set(db: Session) -> Dict[str, Any]:
    """Create a complete set of test data for integration tests"""
    # Create admins
    admin1 = create_test_admin(db, username="admin1", email="admin1@example.com")
    admin2 = create_test_admin(db, username="admin2", email="admin2@example.com")
    
    # Create clients
    client1 = create_test_client(db, name="客户端1", ip_address="192.168.1.101", status="online")
    client2 = create_test_client(db, name="客户端2", ip_address="192.168.1.102", status="offline")
    client3 = create_test_client(db, name="客户端3", ip_address="192.168.1.103", status="online")
    
    # Create packages
    package1 = create_test_package(db, name="升级包1", version="2.0.0")
    package2 = create_test_package(db, name="升级包2", version="2.1.0")
    
    # Create tasks
    task1 = create_test_task(db, client_id=client1.id, package_id=package1.id, status="pending")
    task2 = create_test_task(db, client_id=client2.id, package_id=package1.id, status="running")
    task3 = create_test_task(db, client_id=client3.id, package_id=package2.id, status="completed")
    
    return {
        "admins": [admin1, admin2],
        "clients": [client1, client2, client3],
        "packages": [package1, package2],
        "tasks": [task1, task2, task3]
    }


def cleanup_test_data(db: Session):
    """Clean up all test data from database"""
    # Delete in reverse order to respect foreign key constraints
    db.query(UpgradeTask).delete()
    db.query(UpgradePackage).delete()
    db.query(Client).delete()
    db.query(Admin).delete()
    db.commit()


class DatabaseTestCase:
    """Base test case class with common database operations"""
    
    def setup_method(self):
        """Setup method called before each test method"""
        pass
    
    def teardown_method(self):
        """Teardown method called after each test method"""
        pass
    
    @staticmethod
    def assert_count_equals(db: Session, model_class: Any, expected_count: int):
        """Assert that the count of model instances equals expected"""
        actual_count = db.query(model_class).count()
        assert actual_count == expected_count, f"Expected {expected_count} {model_class.__name__} instances, got {actual_count}"
    
    @staticmethod
    def assert_exists(db: Session, model_class: Any, **filters):
        """Assert that a model instance exists with given filters"""
        instance = db.query(model_class).filter_by(**filters).first()
        assert instance is not None, f"No {model_class.__name__} found with filters: {filters}"
        return instance
    
    @staticmethod
    def assert_not_exists(db: Session, model_class: Any, **filters):
        """Assert that no model instance exists with given filters"""
        instance = db.query(model_class).filter_by(**filters).first()
        assert instance is None, f"Found unexpected {model_class.__name__} with filters: {filters}"