from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.crud.base import CRUDBase
from app.models.upgrade_task import UpgradeTask
from app.schemas.upgrade_task import UpgradeTaskCreate, UpgradeTaskUpdate


class CRUDUpgradeTask(CRUDBase[UpgradeTask, UpgradeTaskCreate, UpgradeTaskUpdate]):
    """升级任务CRUD操作"""
    
    def get_by_client(self, db: Session, *, client_id: int) -> List[UpgradeTask]:
        """根据客户端ID获取升级任务列表"""
        return (
            db.query(UpgradeTask)
            .filter(UpgradeTask.client_id == client_id)
            .order_by(desc(UpgradeTask.created_at))
            .all()
        )
    
    def get_by_package(self, db: Session, *, package_id: int) -> List[UpgradeTask]:
        """根据升级包ID获取升级任务列表"""
        return (
            db.query(UpgradeTask)
            .filter(UpgradeTask.package_id == package_id)
            .order_by(desc(UpgradeTask.created_at))
            .all()
        )
    
    def get_by_status(self, db: Session, *, status: str) -> List[UpgradeTask]:
        """根据状态获取升级任务列表"""
        return (
            db.query(UpgradeTask)
            .filter(UpgradeTask.status == status)
            .order_by(desc(UpgradeTask.created_at))
            .all()
        )
    
    def get_pending_tasks(self, db: Session) -> List[UpgradeTask]:
        """获取待执行的升级任务"""
        return self.get_by_status(db, status="pending")
    
    def get_active_tasks(self, db: Session) -> List[UpgradeTask]:
        """获取正在执行的升级任务"""
        return (
            db.query(UpgradeTask)
            .filter(UpgradeTask.status.in_(["downloading", "installing"]))
            .order_by(desc(UpgradeTask.created_at))
            .all()
        )
    
    def complete_task(self, db: Session, *, task_id: int, success: bool = True) -> Optional[UpgradeTask]:
        """完成升级任务"""
        from datetime import datetime
        
        task = self.get(db, task_id)
        if task:
            task.status = "completed" if success else "failed"
            task.completed_at = datetime.utcnow()
            db.add(task)
            db.commit()
            db.refresh(task)
        return task
    
    def get_client_active_task(self, db: Session, *, client_id: int) -> Optional[UpgradeTask]:
        """获取客户端当前的活跃任务"""
        return (
            db.query(UpgradeTask)
            .filter(
                UpgradeTask.client_id == client_id,
                UpgradeTask.status.in_(["pending", "downloading", "installing"])
            )
            .order_by(desc(UpgradeTask.created_at))
            .first()
        )


upgrade_task = CRUDUpgradeTask(UpgradeTask)