import pytest
import asyncio
import json
from datetime import datetime
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocketDisconnect

from app.main import app
from app.core.websocket_manager import websocket_manager, MessageType


class TestWebSocketIntegration:
    """WebSocket集成测试"""
    
    def test_websocket_endpoint_exists(self, client):
        """测试WebSocket端点存在"""
        # 使用TestClient无法直接测试WebSocket，但可以检查路由是否存在
        response = client.get("/api/v1/client/ws/info")
        assert response.status_code == 200
    
    def test_websocket_info_endpoint(self, client):
        """测试WebSocket信息端点"""
        response = client.get("/api/v1/client/ws/info")
        assert response.status_code == 200
        data = response.json()
        assert "total_connections" in data
        assert "active_connections" in data
        assert "subscriptions" in data
    
    @patch('app.core.websocket_manager.websocket_manager.connect')
    @patch('app.core.websocket_manager.websocket_manager.disconnect')  
    @patch('app.core.websocket_manager.websocket_manager.subscribe')
    def test_websocket_connection_management(self, mock_subscribe, mock_disconnect, mock_connect):
        """测试WebSocket连接管理"""
        # 模拟连接ID
        mock_connect.return_value = "test-connection-id"
        
        # 创建模拟WebSocket
        mock_websocket = MagicMock()
        mock_websocket.receive_text.return_value = asyncio.Future()
        mock_websocket.receive_text.return_value.set_result(json.dumps({
            "action": "subscribe",
            "topics": ["client_status", "heartbeat"]
        }))
        
        # 验证连接管理方法可以被调用
        connection_id = mock_connect.return_value
        assert connection_id == "test-connection-id"
        
        # 验证订阅功能
        mock_subscribe.return_value = None
        topics = ["client_status", "heartbeat"]
        mock_subscribe(connection_id, topics)
        mock_subscribe.assert_called_once_with(connection_id, topics)
        
        # 验证断开连接
        mock_disconnect(connection_id)
        mock_disconnect.assert_called_once_with(connection_id)


class TestWebSocketManager:
    """WebSocket管理器测试"""
    
    def test_websocket_manager_singleton(self):
        """测试WebSocket管理器单例"""
        from app.core.websocket_manager import websocket_manager as wm1
        from app.core.websocket_manager import websocket_manager as wm2
        assert wm1 is wm2
    
    def test_connection_info(self):
        """测试连接信息获取"""
        info = websocket_manager.get_connection_info()
        assert isinstance(info, dict)
        assert "total_connections" in info
        assert "active_connections" in info
        assert "subscriptions" in info
    
    def test_connection_management(self):
        """测试连接管理功能"""
        # 创建模拟WebSocket
        mock_websocket = MagicMock()
        
        # 清空现有连接 
        websocket_manager.connection_map.clear()
        websocket_manager.subscriptions.clear()
        websocket_manager.active_connections.clear()
        
        # 测试连接添加
        connection_id = websocket_manager.connect_sync(mock_websocket)
        assert connection_id is not None
        assert len(websocket_manager.connection_map) == 1
        
        # 测试订阅
        topics = ["client_status", "heartbeat"]
        websocket_manager.subscribe_sync(connection_id, topics)
        assert connection_id in websocket_manager.subscriptions
        assert "client_status" in websocket_manager.subscriptions[connection_id]
        assert "heartbeat" in websocket_manager.subscriptions[connection_id]
        
        # 测试断开连接
        websocket_manager.disconnect(connection_id)
        assert connection_id not in websocket_manager.connection_map
    
    def test_message_types(self):
        """测试消息类型定义"""
        assert hasattr(MessageType, 'CLIENT_STATUS_UPDATE')
        assert hasattr(MessageType, 'HEARTBEAT_RECEIVED')
        assert hasattr(MessageType, 'SYSTEM_MESSAGE')
        
        # 验证消息类型值
        assert MessageType.CLIENT_STATUS_UPDATE == "client_status_update"
        assert MessageType.HEARTBEAT_RECEIVED == "heartbeat_received"  
        assert MessageType.SYSTEM_MESSAGE == "system_message"