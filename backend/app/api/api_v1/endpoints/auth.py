from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.core.config import settings
from app.core.security import jwt_handler
from app.crud.crud_admin import admin
from app.schemas.auth import LoginRequest, TokenResponse, TokenRefreshRequest
from app.core.logger import auth_logger
from typing import Dict, Any

router = APIRouter()
security = HTTPBearer()


@router.post("/login", response_model=TokenResponse)
def login(
    login_data: LoginRequest, 
    request: Request,
    db: Session = Depends(get_db)
) -> TokenResponse:
    """
    管理员登录接口
    
    - **username**: 管理员用户名
    - **password**: 管理员密码
    
    Returns:
        TokenResponse: 包含访问token和刷新token
    """
    client_ip = request.client.host if request.client else "unknown"
    auth_logger.info(f"Login attempt for user: {login_data.username} from IP: {client_ip}")
    
    # 验证管理员账号密码
    admin_user = admin.authenticate(
        db, username=login_data.username, password=login_data.password
    )
    
    if not admin_user:
        auth_logger.warning(f"Failed login attempt for user: {login_data.username} from IP: {client_ip}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 生成访问token和刷新token
    access_token = jwt_handler.create_access_token(subject=admin_user.username)
    refresh_token = jwt_handler.create_refresh_token(subject=admin_user.username)
    
    auth_logger.info(f"Successful login for user: {admin_user.username} from IP: {client_ip}")
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60  # 转换为秒
    )


@router.post("/refresh", response_model=Dict[str, Any])
def refresh_token(
    refresh_data: TokenRefreshRequest,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    刷新访问token
    
    - **refresh_token**: 刷新token
    
    Returns:
        dict: 包含新的访问token
    """
    new_access_token = jwt_handler.refresh_access_token(refresh_data.refresh_token)
    
    if not new_access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="刷新token无效或已过期",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.post("/verify")
def verify_token(token: str = Depends(security)) -> Dict[str, Any]:
    """
    验证token有效性
    
    Returns:
        dict: token验证结果
    """
    username = jwt_handler.verify_token(token.credentials)
    
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token无效或已过期",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 解码token获取过期时间
    payload = jwt_handler.decode_token(token.credentials)
    expires_at = payload.get("exp") if payload else None
    
    return {
        "username": username,
        "is_valid": True,
        "expires_at": expires_at
    }


@router.post("/logout")
def logout(request: Request) -> Dict[str, str]:
    """
    用户登出接口
    
    注意: JWT是无状态的，真正的登出需要在客户端删除token
    这个接口主要用于记录登出日志等操作
    
    Returns:
        dict: 登出成功消息
    """
    client_ip = request.client.host if request.client else "unknown"
    # 尝试从请求状态获取用户信息
    username = getattr(request.state, 'current_user', 'unknown')
    
    auth_logger.info(f"User logout: {username} from IP: {client_ip}")
    return {"message": "登出成功"}