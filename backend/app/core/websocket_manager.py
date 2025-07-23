from typing import Dict, List, Set
import json
import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
from enum import Enum


class MessageType(str, Enum):
    """WebSocket消息类型枚举"""
    CLIENT_STATUS_UPDATE = "client_status_update"
    CLIENT_CONNECTED = "client_connected"
    CLIENT_DISCONNECTED = "client_disconnected"
    HEARTBEAT_RECEIVED = "heartbeat_received"
    SYSTEM_MESSAGE = "system_message"


class WebSocketManager:
    """WebSocket连接管理器"""
    
    def __init__(self):
        # 存储所有活跃的WebSocket连接
        self.active_connections: List[WebSocket] = []
        # 存储连接ID到WebSocket的映射
        self.connection_map: Dict[str, WebSocket] = {}
        # 存储每个连接的订阅主题
        self.subscriptions: Dict[str, Set[str]] = {}
    
    async def connect(self, websocket: WebSocket, connection_id: str = None) -> str:
        """
        接受新的WebSocket连接
        
        Args:
            websocket: WebSocket连接对象
            connection_id: 连接ID，如果未提供则自动生成
        
        Returns:
            连接ID
        """
        await websocket.accept()
        
        if not connection_id:
            connection_id = f"conn_{len(self.active_connections)}_{datetime.utcnow().timestamp()}"
        
        self.active_connections.append(websocket)
        self.connection_map[connection_id] = websocket
        self.subscriptions[connection_id] = set()
        
        # 发送连接成功消息
        await self._send_to_connection(connection_id, {
            "type": MessageType.SYSTEM_MESSAGE,
            "message": "WebSocket连接已建立",
            "connection_id": connection_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return connection_id
    
    def disconnect(self, connection_id: str):
        """
        断开WebSocket连接
        
        Args:
            connection_id: 连接ID
        """
        if connection_id in self.connection_map:
            websocket = self.connection_map[connection_id]
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)
            del self.connection_map[connection_id]
            if connection_id in self.subscriptions:
                del self.subscriptions[connection_id]
    
    async def subscribe(self, connection_id: str, topics: List[str]):
        """
        订阅特定主题
        
        Args:
            connection_id: 连接ID
            topics: 要订阅的主题列表
        """
        if connection_id in self.subscriptions:
            self.subscriptions[connection_id].update(topics)
            await self._send_to_connection(connection_id, {
                "type": MessageType.SYSTEM_MESSAGE,
                "message": f"已订阅主题: {', '.join(topics)}",
                "subscribed_topics": list(self.subscriptions[connection_id]),
                "timestamp": datetime.utcnow().isoformat()
            })
    
    async def unsubscribe(self, connection_id: str, topics: List[str]):
        """
        取消订阅特定主题
        
        Args:
            connection_id: 连接ID
            topics: 要取消订阅的主题列表
        """
        if connection_id in self.subscriptions:
            self.subscriptions[connection_id].difference_update(topics)
            await self._send_to_connection(connection_id, {
                "type": MessageType.SYSTEM_MESSAGE,
                "message": f"已取消订阅主题: {', '.join(topics)}",
                "subscribed_topics": list(self.subscriptions[connection_id]),
                "timestamp": datetime.utcnow().isoformat()
            })
    
    async def broadcast_to_all(self, message: dict):
        """
        向所有连接广播消息
        
        Args:
            message: 要广播的消息
        """
        if self.active_connections:
            message["timestamp"] = datetime.utcnow().isoformat()
            disconnected = []
            
            for connection in self.active_connections:
                try:
                    await connection.send_text(json.dumps(message, ensure_ascii=False))
                except Exception:
                    disconnected.append(connection)
            
            # 清理断开的连接
            for conn in disconnected:
                self._cleanup_connection(conn)
    
    async def broadcast_to_topic(self, topic: str, message: dict):
        """
        向订阅特定主题的连接广播消息
        
        Args:
            topic: 主题名称
            message: 要广播的消息
        """
        message["timestamp"] = datetime.utcnow().isoformat()
        message["topic"] = topic
        
        disconnected = []
        
        for connection_id, topics in self.subscriptions.items():
            if topic in topics and connection_id in self.connection_map:
                try:
                    websocket = self.connection_map[connection_id]
                    await websocket.send_text(json.dumps(message, ensure_ascii=False))
                except Exception:
                    disconnected.append(connection_id)
        
        # 清理断开的连接
        for conn_id in disconnected:
            self.disconnect(conn_id)
    
    async def send_client_status_update(self, client_id: int, status: str, last_heartbeat: datetime = None):
        """
        发送客户端状态更新消息
        
        Args:
            client_id: 客户端ID
            status: 客户端状态
            last_heartbeat: 最后心跳时间
        """
        message = {
            "type": MessageType.CLIENT_STATUS_UPDATE,
            "client_id": client_id,
            "status": status,
            "last_heartbeat": last_heartbeat.isoformat() if last_heartbeat else None,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # 广播到订阅了客户端状态更新的连接
        await self.broadcast_to_topic("client_status", message)
    
    async def send_heartbeat_received(self, client_id: int, client_info: dict):
        """
        发送心跳接收消息
        
        Args:
            client_id: 客户端ID
            client_info: 客户端信息
        """
        message = {
            "type": MessageType.HEARTBEAT_RECEIVED,
            "client_id": client_id,
            "client_info": client_info,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.broadcast_to_topic("heartbeat", message)
    
    async def _send_to_connection(self, connection_id: str, message: dict):
        """
        向特定连接发送消息
        
        Args:
            connection_id: 连接ID
            message: 要发送的消息
        """
        if connection_id in self.connection_map:
            try:
                websocket = self.connection_map[connection_id]
                await websocket.send_text(json.dumps(message, ensure_ascii=False))
            except Exception:
                self.disconnect(connection_id)
    
    def _cleanup_connection(self, websocket: WebSocket):
        """
        清理断开的连接
        
        Args:
            websocket: 要清理的WebSocket连接
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        
        # 从映射中移除
        to_remove = []
        for conn_id, ws in self.connection_map.items():
            if ws == websocket:
                to_remove.append(conn_id)
        
        for conn_id in to_remove:
            del self.connection_map[conn_id]
            if conn_id in self.subscriptions:
                del self.subscriptions[conn_id]
    
    def get_connection_count(self) -> int:
        """获取当前连接数"""
        return len(self.active_connections)
    
    def get_connection_info(self) -> dict:
        """获取连接信息"""
        return {
            "total_connections": len(self.active_connections),
            "active_connections": len(self.connection_map),
            "connection_ids": list(self.connection_map.keys()),
            "subscriptions": {
                conn_id: list(topics) 
                for conn_id, topics in self.subscriptions.items()
            }
        }
    
    # 测试辅助方法
    def connect_sync(self, websocket) -> str:
        """同步版本的连接方法，用于测试"""
        connection_id = f"test_conn_{len(self.active_connections)}_{datetime.utcnow().timestamp()}"
        self.active_connections.append(websocket)
        self.connection_map[connection_id] = websocket
        self.subscriptions[connection_id] = set()
        return connection_id
    
    def subscribe_sync(self, connection_id: str, topics: List[str]):
        """同步版本的订阅方法，用于测试"""
        if connection_id in self.subscriptions:
            self.subscriptions[connection_id].update(topics)
    
    @property
    def _connections(self):
        """获取连接映射，用于测试"""
        return self.connection_map
    
    @property  
    def _subscriptions(self):
        """获取订阅映射，用于测试"""
        return self.subscriptions


# 全局WebSocket管理器实例
websocket_manager = WebSocketManager()