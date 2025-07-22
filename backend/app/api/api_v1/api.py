from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, admin

api_router = APIRouter()

# 认证相关路由
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# 管理员相关路由 (需要认证)
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])


@api_router.get("/")
async def api_root():
    return {"message": "小新RPA API v1"}


@api_router.get("/test")
async def api_test():
    return {"message": "API测试接口", "status": "success"}