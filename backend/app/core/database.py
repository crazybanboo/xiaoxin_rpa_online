from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.base import Base

# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """获取数据库会话的依赖项"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库，创建所有表"""
    # 导入所有模型以确保它们被注册到Base
    from app.models import Admin, Client, UpgradePackage, UpgradeTask
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)


def drop_db():
    """删除所有表（用于测试或重置）"""
    Base.metadata.drop_all(bind=engine)