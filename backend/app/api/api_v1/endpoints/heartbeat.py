from datetime import datetime
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
import json

from app.api import deps
from app.crud import crud_client
from app.schemas.client import Client
from app.core.websocket_manager import websocket_manager, MessageType

router = APIRouter()


class HeartbeatRequest(BaseModel):
    """心跳请求schema"""
    client_id: int = Field(..., description="客户端ID")
    timestamp: datetime = Field(..., description="客户端时间戳")
    status: str = Field("online", description="客户端状态")
    version: str = Field("", description="客户端版本")
    ip_address: str = Field("", description="客户端IP地址")


class HeartbeatResponse(BaseModel):
    """心跳响应schema"""
    success: bool
    message: str
    timestamp: datetime
    client_status: str


@router.post("/heartbeat", response_model=HeartbeatResponse)
async def receive_heartbeat(
    *,
    db: Session = Depends(deps.get_db),
    heartbeat_data: HeartbeatRequest
) -> Any:
    """
    接收客户端心跳
    
    - 验证客户端是否存在
    - 更新客户端的心跳时间和状态
    - 返回心跳确认
    """
    # 获取客户端
    client = crud_client.client.get(db, heartbeat_data.client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="客户端不存在"
        )
    
    # 更新客户端信息
    update_data = {
        "status": heartbeat_data.status,
        "last_heartbeat": datetime.utcnow()
    }
    
    # 如果提供了版本信息，也更新版本
    if heartbeat_data.version:
        update_data["version"] = heartbeat_data.version
    
    # 如果提供了IP地址，也更新IP地址
    if heartbeat_data.ip_address:
        update_data["ip_address"] = heartbeat_data.ip_address
    
    # 执行更新
    updated_client = crud_client.client.update(
        db=db, 
        db_obj=client, 
        obj_in=update_data
    )
    
    # 通过WebSocket发送状态更新通知
    await websocket_manager.send_client_status_update(
        client_id=updated_client.id,
        status=updated_client.status,
        last_heartbeat=updated_client.last_heartbeat
    )
    
    # 发送心跳接收通知
    await websocket_manager.send_heartbeat_received(
        client_id=updated_client.id,
        client_info={
            "name": updated_client.name,
            "ip_address": updated_client.ip_address,
            "version": updated_client.version,
            "status": updated_client.status
        }
    )
    
    return HeartbeatResponse(
        success=True,
        message="心跳接收成功",
        timestamp=datetime.utcnow(),
        client_status=updated_client.status
    )


@router.get("/heartbeat/status/{client_id}", response_model=Client)
def get_client_status(
    client_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    获取客户端状态信息
    """
    client = crud_client.client.get(db, client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="客户端不存在"
        )
    return client


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket端点，用于实时状态推送
    
    支持的消息格式:
    - 订阅: {"action": "subscribe", "topics": ["client_status", "heartbeat"]}
    - 取消订阅: {"action": "unsubscribe", "topics": ["client_status"]}
    - 获取连接信息: {"action": "get_info"}
    """
    connection_id = await websocket_manager.connect(websocket)
    
    try:
        while True:
            # 接收客户端消息
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                action = message.get("action")
                
                if action == "subscribe":
                    topics = message.get("topics", [])
                    await websocket_manager.subscribe(connection_id, topics)
                
                elif action == "unsubscribe":
                    topics = message.get("topics", [])
                    await websocket_manager.unsubscribe(connection_id, topics)
                
                elif action == "get_info":
                    info = websocket_manager.get_connection_info()
                    await websocket.send_text(json.dumps({
                        "type": MessageType.SYSTEM_MESSAGE,
                        "message": "连接信息",
                        "data": info,
                        "timestamp": datetime.utcnow().isoformat()
                    }, ensure_ascii=False))
                
                else:
                    await websocket.send_text(json.dumps({
                        "type": MessageType.SYSTEM_MESSAGE,
                        "message": f"未知操作: {action}",
                        "timestamp": datetime.utcnow().isoformat()
                    }, ensure_ascii=False))
            
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "type": MessageType.SYSTEM_MESSAGE,
                    "message": "无效的JSON格式",
                    "timestamp": datetime.utcnow().isoformat()
                }, ensure_ascii=False))
    
    except WebSocketDisconnect:
        websocket_manager.disconnect(connection_id)


@router.get("/ws/info")
async def get_websocket_info() -> Any:
    """
    获取WebSocket连接信息
    """
    return websocket_manager.get_connection_info()