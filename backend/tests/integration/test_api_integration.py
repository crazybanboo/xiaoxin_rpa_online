"""
Integration tests for API endpoints
"""

import pytest
from fastapi.testclient import TestClient

from tests.utils import create_test_data_set, cleanup_test_data


@pytest.mark.integration
class TestAPIIntegration:
    """Integration tests for API endpoints with database"""

    def test_api_health_check_integration(self, client: TestClient, db_session):
        """Test health check endpoint with database connection"""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "message" in data

    def test_api_root_integration(self, client: TestClient, db_session):
        """Test root endpoint integration"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_api_v1_endpoints_integration(self, client: TestClient, db_session):
        """Test API v1 endpoints integration"""
        # Test v1 root
        response = client.get("/api/v1/")
        assert response.status_code == 200
        assert response.json()["message"] == "小新RPA API v1"
        
        # Test v1 test endpoint
        response = client.get("/api/v1/test")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_full_workflow_integration(self, client: TestClient, db_session):
        """Test full API workflow with test data"""
        # Create test data
        test_data = create_test_data_set(db_session)
        
        # Test that endpoints still work with data in database
        response = client.get("/api/health")
        assert response.status_code == 200
        
        response = client.get("/api/v1/")
        assert response.status_code == 200
        
        # Cleanup
        cleanup_test_data(db_session)


@pytest.mark.integration
class TestErrorHandlingIntegration:
    """Integration tests for error handling"""

    def test_404_with_database(self, client: TestClient, db_session):
        """Test 404 errors with database connected"""
        response = client.get("/nonexistent/endpoint")
        assert response.status_code == 404

    def test_405_with_database(self, client: TestClient, db_session):
        """Test method not allowed with database connected"""
        response = client.patch("/api/health")
        assert response.status_code == 405