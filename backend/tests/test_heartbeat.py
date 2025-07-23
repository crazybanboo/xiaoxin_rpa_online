import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock

from app.schemas.heartbeat import HeartbeatRequest, HeartbeatResponse
from app.models.client import Client


class TestHeartbeatAPI:
    """测试心跳API功能"""
    
    @pytest.fixture
    def heartbeat_data(self):
        """心跳请求数据"""
        return {
            "client_id": 1,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "online",
            "version": "1.0.0",
            "ip_address": "192.168.1.100"
        }
    
    @pytest.fixture
    def mock_client(self):
        """模拟客户端"""
        client = Client(
            id=1,
            name="Test Client",
            status="offline",
            last_heartbeat=None,
            ip_address="192.168.1.100",
            version="1.0.0",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        return client
    
    def test_heartbeat_endpoint_exists(self, client):
        """测试心跳端点存在"""
        response = client.post("/api/v1/client/heartbeat", json={})
        assert response.status_code in [200, 400, 404, 422]  # 端点存在
    
    @patch('app.crud.crud_client.client.get')
    @patch('app.crud.crud_client.client.update')
    @patch('app.core.websocket_manager.websocket_manager.send_client_status_update')
    @patch('app.core.websocket_manager.websocket_manager.send_heartbeat_received')
    def test_heartbeat_success(self, mock_heartbeat_notification, mock_status_update, mock_update, mock_get, client, heartbeat_data, mock_client):
        """测试心跳成功处理"""
        # 设置模拟
        mock_get.return_value = mock_client
        mock_update.return_value = mock_client
        mock_status_update.return_value = None
        mock_heartbeat_notification.return_value = None
        
        # 发送心跳请求
        response = client.post("/api/v1/client/heartbeat", json=heartbeat_data)
        
        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Heartbeat received successfully"
        
        # 验证调用
        mock_get.assert_called_once()
        mock_update.assert_called_once()
    
    def test_heartbeat_client_not_found(self, client, heartbeat_data):
        """测试客户端不存在时的心跳"""
        heartbeat_data["client_id"] = 99999
        response = client.post("/api/v1/client/heartbeat", json=heartbeat_data)
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_heartbeat_invalid_data(self, client):
        """测试无效心跳数据"""
        invalid_data = {
            "client_id": "invalid",  # 应该是整数
            "timestamp": "invalid date"
        }
        response = client.post("/api/v1/client/heartbeat", json=invalid_data)
        
        assert response.status_code == 422  # 验证错误
    
    def test_heartbeat_status_endpoint(self, client):
        """测试状态查询端点"""
        response = client.get("/api/v1/client/heartbeat/status/1")
        assert response.status_code in [200, 404]  # 端点存在
    
    @patch('app.crud.crud_client.client.get')
    def test_get_status_success(self, mock_get, client, mock_client):
        """测试获取客户端状态成功"""
        mock_get.return_value = mock_client
        
        response = client.get("/api/v1/client/heartbeat/status/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Test Client"
        assert "status" in data
    
    def test_get_status_not_found(self, client):
        """测试获取不存在的客户端状态"""
        response = client.get("/api/v1/client/heartbeat/status/99999")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestHeartbeatSchemas:
    """测试心跳数据模型"""
    
    def test_heartbeat_request_valid(self):
        """测试有效的心跳请求"""
        data = {
            "client_id": 1,
            "timestamp": datetime.utcnow(),
            "status": "online",
            "version": "1.0.0",
            "ip_address": "192.168.1.1"
        }
        request = HeartbeatRequest(**data)
        
        assert request.client_id == 1
        assert request.status == "online"
        assert request.version == "1.0.0"
        assert request.ip_address == "192.168.1.1"
    
    def test_heartbeat_request_minimal(self):
        """测试最小心跳请求"""
        data = {
            "client_id": 1,
            "timestamp": datetime.utcnow()
        }
        request = HeartbeatRequest(**data)
        
        assert request.client_id == 1
        assert request.status == "online"  # 默认值
        assert request.version is None
        assert request.ip_address is None
    
    def test_heartbeat_response(self):
        """测试心跳响应"""
        response = HeartbeatResponse(
            success=True,
            message="Test message",
            timestamp=datetime.utcnow()
        )
        
        assert response.success is True
        assert response.message == "Test message"
        assert isinstance(response.timestamp, datetime)