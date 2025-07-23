#!/usr/bin/env python3
"""
WebSocket测试脚本 - 用于验证WebSocket功能
"""

import asyncio
import websockets
import json
from datetime import datetime


async def test_websocket():
    """测试WebSocket连接和消息处理"""
    
    uri = "ws://localhost:8000/api/v1/client/ws"
    
    print(f"[{datetime.now()}] 尝试连接到 {uri}")
    
    try:
        async with websockets.connect(uri) as websocket:
            print(f"[{datetime.now()}] WebSocket连接成功")
            
            # 1. 订阅主题
            subscribe_message = {
                "action": "subscribe",
                "topics": ["client_status", "heartbeat"]
            }
            await websocket.send(json.dumps(subscribe_message))
            print(f"[{datetime.now()}] 发送订阅消息: {subscribe_message}")
            
            # 2. 获取连接信息
            info_message = {"action": "get_info"}
            await websocket.send(json.dumps(info_message))
            print(f"[{datetime.now()}] 发送获取信息消息: {info_message}")
            
            # 3. 监听消息
            print(f"[{datetime.now()}] 开始监听消息...")
            
            timeout_count = 0
            max_timeout = 3
            
            while timeout_count < max_timeout:
                try:
                    # 等待消息，超时时间5秒
                    message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    print(f"[{datetime.now()}] 收到消息: {message}")
                    
                    # 解析消息
                    try:
                        parsed = json.loads(message)
                        print(f"[{datetime.now()}] 解析消息: {parsed}")
                    except json.JSONDecodeError as e:
                        print(f"[{datetime.now()}] JSON解析错误: {e}")
                    
                except asyncio.TimeoutError:
                    timeout_count += 1
                    print(f"[{datetime.now()}] 等待消息超时 ({timeout_count}/{max_timeout})")
            
            print(f"[{datetime.now()}] 测试完成")
            
    except websockets.exceptions.ConnectionRefused:
        print(f"[{datetime.now()}] 连接被拒绝 - 请确保后端服务器正在运行")
    except Exception as e:
        print(f"[{datetime.now()}] 连接错误: {e}")


if __name__ == "__main__":
    print("WebSocket测试脚本")
    print("=" * 50)
    print("注意: 请确保后端服务器已启动 (uvicorn app.main:app --reload)")
    print("=" * 50)
    
    asyncio.run(test_websocket())