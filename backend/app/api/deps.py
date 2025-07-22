from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.security import jwt_handler
from app.crud.crud_admin import admin
from app.models.admin import Admin

security = HTTPBearer(auto_error=False)


def get_db() -> Generator:
    """获取数据库会话"""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_admin(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Admin:
    """
    获取当前登录的管理员
    
    这个依赖函数会验证JWT token并返回对应的管理员对象
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not credentials:
        raise credentials_exception
        
    try:
        # 验证token并获取用户名
        username = jwt_handler.verify_token(credentials.credentials)
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    
    # 从数据库获取管理员信息
    admin_user = admin.get_by_username(db, username=username)
    if admin_user is None:
        raise credentials_exception
    
    return admin_user


def get_current_admin_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[Admin]:
    """
    获取当前登录的管理员（可选）
    
    如果没有提供token或token无效，返回None而不是抛出异常
    """
    if not credentials:
        return None
        
    try:
        username = jwt_handler.verify_token(credentials.credentials)
        if username is None:
            return None
            
        admin_user = admin.get_by_username(db, username=username)
        return admin_user
    except Exception:
        return None