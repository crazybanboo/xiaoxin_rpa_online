from typing import Optional, TYPE_CHECKING
from datetime import datetime
from pydantic import BaseModel

if TYPE_CHECKING:
    from .client import Client
    from .upgrade_package import UpgradePackage


class UpgradeTaskBase(BaseModel):
    """升级任务基础schema"""
    client_id: int
    package_id: int
    status: str = "pending"


class UpgradeTaskCreate(UpgradeTaskBase):
    """创建升级任务schema"""
    pass


class UpgradeTaskUpdate(BaseModel):
    """更新升级任务schema"""
    status: Optional[str] = None
    completed_at: Optional[datetime] = None


class UpgradeTaskInDBBase(UpgradeTaskBase):
    """数据库中的升级任务基础schema"""
    id: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UpgradeTask(UpgradeTaskInDBBase):
    """升级任务schema（用于响应）"""
    pass


class UpgradeTaskWithRelations(UpgradeTask):
    """包含关联关系的升级任务schema"""
    client: Optional["Client"] = None
    package: Optional["UpgradePackage"] = None