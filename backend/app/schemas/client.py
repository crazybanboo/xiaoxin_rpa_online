from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class ClientBase(BaseModel):
    """客户端基础schema"""
    name: str
    ip_address: str
    version: str
    status: str = "offline"


class ClientCreate(ClientBase):
    """创建客户端schema"""
    pass


class ClientUpdate(BaseModel):
    """更新客户端schema"""
    name: Optional[str] = None
    ip_address: Optional[str] = None
    version: Optional[str] = None
    status: Optional[str] = None
    last_heartbeat: Optional[datetime] = None


class ClientInDBBase(ClientBase):
    """数据库中的客户端基础schema"""
    id: int
    last_heartbeat: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Client(ClientInDBBase):
    """客户端schema（用于响应）"""
    pass


class ClientWithTasks(Client):
    """包含升级任务的客户端schema"""
    upgrade_tasks: List["UpgradeTask"] = []