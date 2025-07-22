from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class UpgradePackageBase(BaseModel):
    """升级包基础schema"""
    name: str
    version: str
    file_path: str
    file_size: int


class UpgradePackageCreate(UpgradePackageBase):
    """创建升级包schema"""
    pass


class UpgradePackageUpdate(BaseModel):
    """更新升级包schema"""
    name: Optional[str] = None
    version: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None


class UpgradePackageInDBBase(UpgradePackageBase):
    """数据库中的升级包基础schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UpgradePackage(UpgradePackageInDBBase):
    """升级包schema（用于响应）"""
    pass


class UpgradePackageWithTasks(UpgradePackage):
    """包含升级任务的升级包schema"""
    upgrade_tasks: List["UpgradeTask"] = []