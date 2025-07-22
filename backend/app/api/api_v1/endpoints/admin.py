from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_admin
from app.models.admin import Admin
from typing import Dict, Any

router = APIRouter()


@router.get("/me")
def get_current_admin_info(
    current_admin: Admin = Depends(get_current_admin)
) -> Dict[str, Any]:
    """
    获取当前登录管理员的信息
    
    Returns:
        dict: 管理员信息
    """
    return {
        "id": current_admin.id,
        "username": current_admin.username,
        "email": current_admin.email,
        "created_at": current_admin.created_at.isoformat() if current_admin.created_at else None,
        "updated_at": current_admin.updated_at.isoformat() if current_admin.updated_at else None
    }


@router.get("/dashboard")
def get_admin_dashboard(
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取管理员控制台信息
    
    Returns:
        dict: 控制台数据
    """
    return {
        "message": f"欢迎, {current_admin.username}！",
        "admin_info": {
            "username": current_admin.username,
            "email": current_admin.email
        },
        "stats": {
            "total_admins": 1,  # 这里可以查询实际的管理员数量
            "status": "active"
        }
    }