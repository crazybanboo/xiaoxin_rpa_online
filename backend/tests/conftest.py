"""
Pytest configuration file with shared fixtures
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.models.base import Base
from app.api.deps import get_db


import tempfile
import uuid

@pytest.fixture(scope="function")
def db_session():
    """Create a database session for testing"""
    # Create a unique temporary database file for each test
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=f"_{uuid.uuid4().hex[:8]}.db")
    temp_db.close()
    
    database_url = f"sqlite:///{temp_db.name}"
    
    # Create engine and session for this test
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()
        # Clean up the temporary file
        import os
        try:
            os.unlink(temp_db.name)
        except OSError:
            pass


@pytest.fixture(scope="function")  
def client(db_session):
    """Create a test client"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
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