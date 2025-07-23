import time
from typing import List, Optional
from fastapi import Request, HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.core.security import jwt_handler
from app.core.config import settings
from app.core.logger import auth_logger, api_logger


class JWTAuthMiddleware(BaseHTTPMiddleware):
    """
    JWT认证中间件
    
    自动验证请求中的JWT token，除非路径在白名单中
    """
    
    def __init__(
        self, 
        app,
        whitelist_paths: Optional[List[str]] = None,
        whitelist_prefixes: Optional[List[str]] = None
    ):
        super().__init__(app)
        # 默认白名单路径（不需要认证）
        self.whitelist_paths = whitelist_paths or [
            "/",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/api/v1/auth/login",
            "/api/v1/auth/refresh",
            "/api/v1",
            "/api/v1/test"
        ]
        # 白名单前缀（以这些前缀开头的路径不需要认证）
        self.whitelist_prefixes = whitelist_prefixes or [
            "/static/",
            "/assets/",
            "/favicon.ico"
        ]
    
    async def dispatch(self, request: Request, call_next):
        """处理请求"""
        path = request.url.path
        
        # 检查是否在白名单中
        if self._is_whitelisted(path):
            response = await call_next(request)
            return response
        
        # 提取Authorization头
        authorization = request.headers.get("Authorization")
        scheme, token = get_authorization_scheme_param(authorization)
        
        if not authorization or scheme.lower() != "bearer":
            auth_logger.warning(f"Missing or invalid authorization header for {path} from {request.client.host if request.client else 'unknown'}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "缺少认证凭据"},
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # 验证token
        username = jwt_handler.verify_token(token)
        if not username:
            auth_logger.warning(f"Invalid token for {path} from {request.client.host if request.client else 'unknown'}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "无效的认证凭据"},
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # 将用户信息添加到请求状态中
        request.state.current_user = username
        auth_logger.debug(f"Authenticated user {username} for {path}")
        
        response = await call_next(request)
        return response
    
    def _is_whitelisted(self, path: str) -> bool:
        """检查路径是否在白名单中"""
        # 精确匹配
        if path in self.whitelist_paths:
            return True
        
        # 前缀匹配
        for prefix in self.whitelist_prefixes:
            if path.startswith(prefix):
                return True
        
        return False


def get_current_user_from_state(request: Request) -> Optional[str]:
    """从请求状态中获取当前用户"""
    return getattr(request.state, 'current_user', None)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    请求日志中间件
    
    记录所有API请求的详细信息，包括请求时间、响应时间、状态码等
    """
    
    async def dispatch(self, request: Request, call_next):
        """处理请求并记录日志"""
        start_time = time.time()
        
        # 获取请求信息
        method = request.method
        url = str(request.url)
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("User-Agent", "unknown")
        
        # 记录请求开始
        api_logger.info(f"🚀 {method} {url} - IP: {client_ip}")
        
        try:
            # 处理请求
            response = await call_next(request)
            
            # 计算处理时间
            process_time = time.time() - start_time
            
            # 记录响应
            status_code = response.status_code
            if status_code < 400:
                api_logger.info(f"✅ {method} {url} - {status_code} - {process_time:.3f}s")
            elif status_code < 500:
                api_logger.warning(f"⚠️ {method} {url} - {status_code} - {process_time:.3f}s")
            else:
                api_logger.error(f"❌ {method} {url} - {status_code} - {process_time:.3f}s")
            
            # 添加处理时间到响应头
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            # 计算处理时间
            process_time = time.time() - start_time
            
            # 记录异常
            api_logger.error(f"💥 {method} {url} - Exception: {str(e)} - {process_time:.3f}s")
            raise