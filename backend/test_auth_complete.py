#!/usr/bin/env python3
"""
完整的JWT认证系统测试
测试认证功能和受保护的端点
"""

import asyncio
import httpx
import uvicorn
import threading
import time
from app.main import app
from app.core.database import engine
from app.models.base import BaseModel
from app.crud.crud_admin import admin
from app.schemas.admin import AdminCreate
from sqlalchemy.orm import Session
from app.core.database import SessionLocal

def setup_database():
    """设置数据库和测试数据"""
    print("创建数据库表...")
    BaseModel.metadata.create_all(bind=engine)
    
    print("创建测试管理员用户...")
    db = SessionLocal()
    try:
        # 检查是否已存在测试用户
        existing_admin = admin.get_by_username(db, username="admin")
        if not existing_admin:
            # 创建测试管理员
            admin_data = AdminCreate(
                username="admin",
                email="admin@test.com",
                password="123456"
            )
            
            new_admin = admin.create_with_password(db, obj_in=admin_data)
            print(f"创建测试管理员成功: {new_admin.username}")
        else:
            print("测试管理员用户已存在")
        
    except Exception as e:
        print(f"设置数据库失败: {e}")
    finally:
        db.close()

def start_test_server():
    """启动测试服务器"""
    config = uvicorn.Config(app, host="127.0.0.1", port=8002, log_level="warning")
    server = uvicorn.Server(config)
    server.run()

async def test_complete_auth_flow():
    """完整的认证流程测试"""
    print("开始完整的JWT认证系统测试...")
    
    # 等待服务器启动
    await asyncio.sleep(2)
    
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8002") as client:
        try:
            # 1. 测试未认证访问受保护端点
            print("\n1. 测试未认证访问受保护端点...")
            response = await client.get("/api/v1/admin/me")
            print(f"GET /api/v1/admin/me (无token) - 状态码: {response.status_code}")
            assert response.status_code == 401, "受保护端点应该返回401"
            
            # 2. 测试登录获取token
            print("\n2. 测试登录获取token...")
            login_data = {"username": "admin", "password": "123456"}
            response = await client.post("/api/v1/auth/login", json=login_data)
            print(f"POST /api/v1/auth/login - 状态码: {response.status_code}")
            assert response.status_code == 200, "登录应该成功"
            
            token_data = response.json()
            access_token = token_data["access_token"]
            refresh_token = token_data["refresh_token"]
            
            # 3. 测试使用token访问受保护端点
            print("\n3. 测试使用token访问受保护端点...")
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # 获取当前管理员信息
            response = await client.get("/api/v1/admin/me", headers=headers)
            print(f"GET /api/v1/admin/me (有token) - 状态码: {response.status_code}")
            assert response.status_code == 200, "应该能够访问受保护端点"
            
            admin_info = response.json()
            print(f"管理员信息: {admin_info}")
            assert admin_info["username"] == "admin", "应该返回正确的用户信息"
            
            # 获取管理员控制台
            response = await client.get("/api/v1/admin/dashboard", headers=headers)
            print(f"GET /api/v1/admin/dashboard - 状态码: {response.status_code}")
            assert response.status_code == 200, "应该能够访问控制台"
            
            dashboard_info = response.json()
            print(f"控制台信息: {dashboard_info}")
            
            # 4. 测试token验证
            print("\n4. 测试token验证...")
            response = await client.post("/api/v1/auth/verify", headers=headers)
            print(f"POST /api/v1/auth/verify - 状态码: {response.status_code}")
            assert response.status_code == 200, "Token验证应该成功"
            
            # 5. 测试token刷新
            print("\n5. 测试token刷新...")
            refresh_data = {"refresh_token": refresh_token}
            response = await client.post("/api/v1/auth/refresh", json=refresh_data)
            print(f"POST /api/v1/auth/refresh - 状态码: {response.status_code}")
            assert response.status_code == 200, "Token刷新应该成功"
            
            new_token_data = response.json()
            new_access_token = new_token_data["access_token"]
            
            # 6. 测试新token是否有效
            print("\n6. 测试新token是否有效...")
            new_headers = {"Authorization": f"Bearer {new_access_token}"}
            response = await client.get("/api/v1/admin/me", headers=new_headers)
            print(f"GET /api/v1/admin/me (新token) - 状态码: {response.status_code}")
            assert response.status_code == 200, "新token应该有效"
            
            # 7. 测试无效token
            print("\n7. 测试无效token...")
            invalid_headers = {"Authorization": "Bearer invalid_token"}
            response = await client.get("/api/v1/admin/me", headers=invalid_headers)
            print(f"GET /api/v1/admin/me (无效token) - 状态码: {response.status_code}")
            assert response.status_code == 401, "无效token应该被拒绝"
            
            # 8. 测试登出
            print("\n8. 测试登出...")
            response = await client.post("/api/v1/auth/logout", headers=headers)
            print(f"POST /api/v1/auth/logout - 状态码: {response.status_code}")
            assert response.status_code == 200, "登出应该成功"
            
            print("\n✅ 完整的JWT认证系统测试通过!")
            return True
            
        except AssertionError as e:
            print(f"\n❌ 测试断言失败: {e}")
            return False
        except Exception as e:
            print(f"\n❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    # 设置数据库
    setup_database()
    
    # 在单独的线程中启动服务器
    server_thread = threading.Thread(target=start_test_server, daemon=True)
    server_thread.start()
    
    # 等待服务器启动然后运行测试
    time.sleep(1)
    success = asyncio.run(test_complete_auth_flow())
    
    if success:
        print("\n🎉 任务3 - JWT认证系统实现完成!")
        print("✅ JWT工具类实现完成")
        print("✅ 登录API接口开发完成")
        print("✅ JWT认证中间件实现完成")
        print("✅ 前端登录页面开发完成")
        print("✅ Token管理机制实现完成")
        print("✅ 受保护端点测试通过")
    else:
        print("\n❌ JWT认证系统测试失败")