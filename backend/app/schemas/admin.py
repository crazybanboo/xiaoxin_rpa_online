from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class AdminBase(BaseModel):
    """管理员基础schema"""
    username: str
    email: EmailStr


class AdminCreate(AdminBase):
    """创建管理员schema"""
    password: str


class AdminUpdate(BaseModel):
    """更新管理员schema"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class AdminInDBBase(AdminBase):
    """数据库中的管理员基础schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Admin(AdminInDBBase):
    """管理员schema（用于响应）"""
    pass


class AdminInDB(AdminInDBBase):
    """数据库中的管理员schema（包含密码哈希）"""
    password_hash: str