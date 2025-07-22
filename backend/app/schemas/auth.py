from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    """登录请求模型"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Token响应模型"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # 秒数


class TokenRefreshRequest(BaseModel):
    """Token刷新请求模型"""
    refresh_token: str


class TokenVerifyResponse(BaseModel):
    """Token验证响应模型"""
    username: str
    is_valid: bool
    expires_at: Optional[str] = None