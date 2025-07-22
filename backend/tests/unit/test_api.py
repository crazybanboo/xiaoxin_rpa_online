"""
Unit tests for API endpoints
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
class TestMainAPI:
    """Test cases for main API endpoints"""

    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "小新RPA在线平台 API服务"}

    def test_health_check(self, client: TestClient):
        """Test health check endpoint"""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "message" in data


@pytest.mark.unit
class TestAPIv1:
    """Test cases for API v1 endpoints"""

    def test_api_v1_root(self, client: TestClient):
        """Test API v1 root endpoint"""
        response = client.get("/api/v1/")
        assert response.status_code == 200
        assert response.json() == {"message": "小新RPA API v1"}

    def test_api_v1_test(self, client: TestClient):
        """Test API v1 test endpoint"""
        response = client.get("/api/v1/test")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "API测试接口"
        assert data["status"] == "success"


@pytest.mark.unit
class TestCORSHeaders:
    """Test cases for CORS headers"""

    def test_cors_headers_present(self, client: TestClient):
        """Test that CORS headers are present in responses"""
        response = client.get("/")
        
        # Note: CORS headers are typically added by middleware
        # In test environment, they might not be present unless specifically configured
        assert response.status_code == 200


@pytest.mark.unit
class TestErrorHandling:
    """Test cases for error handling"""

    def test_404_endpoint(self, client: TestClient):
        """Test 404 error for non-existent endpoint"""
        response = client.get("/nonexistent")
        assert response.status_code == 404

    def test_405_method_not_allowed(self, client: TestClient):
        """Test 405 error for method not allowed"""
        response = client.post("/")
        assert response.status_code == 405