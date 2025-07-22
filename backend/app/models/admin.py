from sqlalchemy import Column, String
from .base import BaseModel


class Admin(BaseModel):
    """管理员模型 - 用于系统管理员认证和权限管理"""
    
    __tablename__ = "admins"
    
    username = Column(String(50), unique=True, index=True, nullable=False, comment="管理员用户名")
    password_hash = Column(String(255), nullable=False, comment="密码哈希值")
    email = Column(String(100), unique=True, index=True, nullable=False, comment="邮箱地址")
    
    def __repr__(self):
        return f"<Admin(id={self.id}, username='{self.username}', email='{self.email}')>"