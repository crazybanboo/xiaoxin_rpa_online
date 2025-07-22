"""
Pytest configuration file with shared fixtures
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.models.base import Base
from app.core.database import get_db


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a database session for testing"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client"""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_admin_data():
    """Sample admin data for testing"""
    return {
        "username": "test_admin",
        "email": "test@example.com",
        "password": "test123"
    }


@pytest.fixture
def sample_client_data():
    """Sample client data for testing"""
    return {
        "name": "测试客户端",
        "ip_address": "192.168.1.100",
        "version": "1.0.0",
        "status": "online"
    }


@pytest.fixture
def sample_package_data():
    """Sample upgrade package data for testing"""
    return {
        "name": "测试升级包",
        "version": "2.0.0",
        "file_path": "/path/to/package.zip",
        "file_size": 1024000
    }