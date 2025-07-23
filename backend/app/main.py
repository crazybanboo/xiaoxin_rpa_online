from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.core.middleware import JWTAuthMiddleware, RequestLoggingMiddleware
from app.core.logger import app_logger
# from app.services.monitoring import monitoring_service  # Temporarily disabled until APScheduler is installed

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="小新RPA在线平台 - 后端API服务",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add Request Logging Middleware
app.add_middleware(RequestLoggingMiddleware)

# Add JWT Authentication Middleware
# Note: 注释掉中间件，因为使用依赖注入方式更灵活
# app.add_middleware(JWTAuthMiddleware)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    """应用启动时的事件处理"""
    app_logger.info(f"🚀 {settings.PROJECT_NAME} v{settings.VERSION} 正在启动...")
    
    # 启动客户端监控服务
    # monitoring_service.start()  # Temporarily disabled until APScheduler is installed
    
    app_logger.info("✅ 应用启动完成")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的事件处理"""
    app_logger.info("🛑 应用正在关闭...")
    
    # 停止客户端监控服务
    # monitoring_service.stop()  # Temporarily disabled until APScheduler is installed
    
    app_logger.info("✅ 应用关闭完成")


@app.get("/")
async def root():
    return {"message": "小新RPA在线平台 API服务"}


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "服务运行正常"}