from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class HeartbeatRequest(BaseModel):
    """心跳请求schema"""
    client_id: int = Field(..., description="客户端ID")
    timestamp: datetime = Field(..., description="客户端时间戳")
    status: str = Field("online", description="客户端状态")
    version: Optional[str] = Field(None, description="客户端版本")
    ip_address: Optional[str] = Field(None, description="客户端IP地址")


class HeartbeatResponse(BaseModel):
    """心跳响应schema"""
    success: bool
    message: str
    timestamp: datetime
    client_status: Optional[str] = None