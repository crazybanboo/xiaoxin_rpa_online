from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from .base import BaseModel


class UpgradePackage(BaseModel):
    """升级包模型 - 管理系统升级包文件和版本信息"""
    
    __tablename__ = "upgrade_packages"
    
    name = Column(String(100), nullable=False, comment="升级包名称")
    version = Column(String(20), nullable=False, comment="升级包版本号")
    file_path = Column(String(500), nullable=False, comment="升级包文件路径")
    file_size = Column(Integer, nullable=False, comment="文件大小（字节）")
    
    # 关联关系
    upgrade_tasks = relationship("UpgradeTask", back_populates="package", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<UpgradePackage(id={self.id}, name='{self.name}', version='{self.version}')>"