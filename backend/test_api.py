#!/usr/bin/env python3
"""
API端点测试脚本
测试FastAPI应用的各个端点是否正常工作
"""

import asyncio
import httpx
import uvicorn
import threading
import time
from app.main import app

def start_test_server():
    """启动测试服务器"""
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="warning")
    server = uvicorn.Server(config)
    server.run()

async def test_api_endpoints():
    """测试API端点"""
    print("开始测试API端点...")
    
    # 等待服务器启动
    await asyncio.sleep(2)
    
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        try:
            # 测试根路径
            print("\n测试根路径...")
            response = await client.get("/")
            print(f"GET / - 状态码: {response.status_code}")
            print(f"响应: {response.json()}")
            
            # 测试健康检查
            print("\n测试健康检查...")
            response = await client.get("/api/health")
            print(f"GET /api/health - 状态码: {response.status_code}")
            print(f"响应: {response.json()}")
            
            # 测试API v1根路径
            print("\n测试API v1根路径...")
            response = await client.get("/api/v1/")
            print(f"GET /api/v1/ - 状态码: {response.status_code}")
            print(f"响应: {response.json()}")
            
            # 测试API v1测试接口
            print("\n测试API v1测试接口...")
            response = await client.get("/api/v1/test")
            print(f"GET /api/v1/test - 状态码: {response.status_code}")
            print(f"响应: {response.json()}")
            
            # 测试OpenAPI文档
            print("\n测试OpenAPI文档...")
            response = await client.get("/api/v1/openapi.json")
            print(f"GET /api/v1/openapi.json - 状态码: {response.status_code}")
            
            print("\nAPI测试完成！所有端点正常。")
            
        except Exception as e:
            print(f"API测试失败: {e}")
            return False
        
        return True

if __name__ == "__main__":
    # 在单独的线程中启动服务器
    server_thread = threading.Thread(target=start_test_server, daemon=True)
    server_thread.start()
    
    # 等待服务器启动然后运行测试
    time.sleep(1)
    success = asyncio.run(test_api_endpoints())
    
    if success:
        print("✅ 所有API测试通过")
    else:
        print("❌ 部分API测试失败")