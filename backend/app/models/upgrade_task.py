from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import BaseModel


class UpgradeTask(BaseModel):
    """升级任务模型 - 管理客户端升级任务的状态和进度"""
    
    __tablename__ = "upgrade_tasks"
    
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, comment="关联的客户端ID")
    package_id = Column(Integer, ForeignKey("upgrade_packages.id"), nullable=False, comment="关联的升级包ID")
    status = Column(String(20), nullable=False, default="pending", 
                   comment="任务状态: pending, downloading, installing, completed, failed")
    completed_at = Column(DateTime, nullable=True, comment="任务完成时间")
    
    # 关联关系
    client = relationship("Client", back_populates="upgrade_tasks")
    package = relationship("UpgradePackage", back_populates="upgrade_tasks")
    
    def __repr__(self):
        return f"<UpgradeTask(id={self.id}, client_id={self.client_id}, package_id={self.package_id}, status='{self.status}')>"