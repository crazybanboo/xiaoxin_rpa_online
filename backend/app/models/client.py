from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from .base import BaseModel


class Client(BaseModel):
    """客户端模型 - 管理连接到系统的RPA客户端信息"""
    
    __tablename__ = "clients"
    
    name = Column(String(100), nullable=False, comment="客户端名称")
    ip_address = Column(String(45), nullable=False, comment="客户端IP地址")
    version = Column(String(20), nullable=False, comment="客户端版本号")
    status = Column(String(20), nullable=False, default="offline", comment="客户端状态: online, offline, error")
    last_heartbeat = Column(DateTime, nullable=True, comment="最后心跳时间")
    
    # 关联关系
    upgrade_tasks = relationship("UpgradeTask", back_populates="client", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Client(id={self.id}, name='{self.name}', ip='{self.ip_address}', status='{self.status}')>"