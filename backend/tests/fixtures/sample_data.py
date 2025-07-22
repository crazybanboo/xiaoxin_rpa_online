"""
Sample data fixtures for testing
"""

import pytest
from datetime import datetime, timedelta
from app.models.admin import Admin
from app.models.client import Client
from app.models.upgrade_package import UpgradePackage
from app.models.upgrade_task import UpgradeTask
from app.schemas.admin import AdminCreate
from app.schemas.client import ClientCreate
from app.schemas.upgrade_package import UpgradePackageCreate
from app.schemas.upgrade_task import UpgradeTaskCreate


@pytest.fixture
def sample_admin_dict():
    """Sample admin dictionary data"""
    return {
        "username": "test_admin",
        "email": "test@example.com", 
        "password": "test123"
    }


@pytest.fixture
def sample_client_dict():
    """Sample client dictionary data"""
    return {
        "name": "测试客户端",
        "ip_address": "192.168.1.100",
        "version": "1.0.0",
        "status": "online"
    }


@pytest.fixture
def sample_package_dict():
    """Sample upgrade package dictionary data"""
    return {
        "name": "测试升级包",
        "version": "2.0.0",
        "file_path": "/path/to/package.zip",
        "file_size": 1024000
    }


@pytest.fixture
def sample_task_dict():
    """Sample upgrade task dictionary data"""
    return {
        "client_id": 1,
        "package_id": 1,
        "status": "pending"
    }


@pytest.fixture
def sample_admin_create():
    """Sample AdminCreate schema"""
    return AdminCreate(
        username="test_admin",
        email="test@example.com",
        password="test123"
    )


@pytest.fixture
def sample_client_create():
    """Sample ClientCreate schema"""
    return ClientCreate(
        name="测试客户端",
        ip_address="192.168.1.100",
        version="1.0.0",
        status="online"
    )


@pytest.fixture
def sample_package_create():
    """Sample UpgradePackageCreate schema"""
    return UpgradePackageCreate(
        name="测试升级包",
        version="2.0.0",
        file_path="/path/to/package.zip",
        file_size=1024000
    )


@pytest.fixture
def sample_admin_model(db_session):
    """Create a sample admin model in database"""
    from passlib.context import CryptContext
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    admin = Admin(
        username="test_admin",
        email="test@example.com",
        password_hash=pwd_context.hash("test123")
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin


@pytest.fixture
def sample_client_model(db_session):
    """Create a sample client model in database"""
    client = Client(
        name="测试客户端",
        ip_address="192.168.1.100",
        version="1.0.0",
        status="online"
    )
    db_session.add(client)
    db_session.commit()
    db_session.refresh(client)
    return client


@pytest.fixture
def sample_package_model(db_session):
    """Create a sample upgrade package model in database"""
    package = UpgradePackage(
        name="测试升级包",
        version="2.0.0",
        file_path="/path/to/package.zip",
        file_size=1024000
    )
    db_session.add(package)
    db_session.commit()
    db_session.refresh(package)
    return package


@pytest.fixture
def sample_task_model(db_session, sample_client_model, sample_package_model):
    """Create a sample upgrade task model in database"""
    task = UpgradeTask(
        client_id=sample_client_model.id,
        package_id=sample_package_model.id,
        status="pending"
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task


@pytest.fixture
def multiple_clients(db_session):
    """Create multiple client models in database"""
    clients = []
    for i in range(3):
        client = Client(
            name=f"客户端{i+1}",
            ip_address=f"192.168.1.{100+i}",
            version="1.0.0",
            status="online" if i % 2 == 0 else "offline"
        )
        db_session.add(client)
        clients.append(client)
    
    db_session.commit()
    for client in clients:
        db_session.refresh(client)
    return clients


@pytest.fixture
def multiple_packages(db_session):
    """Create multiple upgrade package models in database"""
    packages = []
    for i in range(3):
        package = UpgradePackage(
            name=f"升级包{i+1}",
            version=f"2.{i}.0",
            file_path=f"/path/to/package{i+1}.zip",
            file_size=1024000 * (i+1)
        )
        db_session.add(package)
        packages.append(package)
    
    db_session.commit()
    for package in packages:
        db_session.refresh(package)
    return packages


@pytest.fixture
def multiple_tasks(db_session, multiple_clients, multiple_packages):
    """Create multiple upgrade task models in database"""
    tasks = []
    statuses = ["pending", "running", "completed", "failed"]
    
    for i, client in enumerate(multiple_clients):
        for j, package in enumerate(multiple_packages[:2]):  # Only use first 2 packages
            task = UpgradeTask(
                client_id=client.id,
                package_id=package.id,
                status=statuses[(i + j) % len(statuses)]
            )
            db_session.add(task)
            tasks.append(task)
    
    db_session.commit()
    for task in tasks:
        db_session.refresh(task)
    return tasks