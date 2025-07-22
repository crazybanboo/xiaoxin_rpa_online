from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.upgrade_package import UpgradePackage
from app.schemas.upgrade_package import UpgradePackageCreate, UpgradePackageUpdate


class CRUDUpgradePackage(CRUDBase[UpgradePackage, UpgradePackageCreate, UpgradePackageUpdate]):
    """升级包CRUD操作"""
    
    def get_by_name(self, db: Session, *, name: str) -> Optional[UpgradePackage]:
        """根据名称获取升级包"""
        return db.query(UpgradePackage).filter(UpgradePackage.name == name).first()
    
    def get_by_version(self, db: Session, *, version: str) -> List[UpgradePackage]:
        """根据版本号获取升级包列表"""
        return db.query(UpgradePackage).filter(UpgradePackage.version == version).all()
    
    def get_latest_version(self, db: Session, *, name: str) -> Optional[UpgradePackage]:
        """获取指定名称的最新版本升级包"""
        return (
            db.query(UpgradePackage)
            .filter(UpgradePackage.name == name)
            .order_by(UpgradePackage.created_at.desc())
            .first()
        )
    
    def get_all_latest(self, db: Session) -> List[UpgradePackage]:
        """获取所有升级包的最新版本"""
        from sqlalchemy import func
        
        # 子查询获取每个名称的最新创建时间
        subquery = (
            db.query(
                UpgradePackage.name,
                func.max(UpgradePackage.created_at).label('max_created_at')
            )
            .group_by(UpgradePackage.name)
            .subquery()
        )
        
        # 连接子查询获取完整记录
        return (
            db.query(UpgradePackage)
            .join(
                subquery,
                (UpgradePackage.name == subquery.c.name) &
                (UpgradePackage.created_at == subquery.c.max_created_at)
            )
            .all()
        )


upgrade_package = CRUDUpgradePackage(UpgradePackage)