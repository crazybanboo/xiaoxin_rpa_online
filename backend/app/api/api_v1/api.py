from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/")
async def api_root():
    return {"message": "小新RPA API v1"}


@api_router.get("/test")
async def api_test():
    return {"message": "API测试接口", "status": "success"}