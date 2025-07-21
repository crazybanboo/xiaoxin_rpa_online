#!/bin/bash

echo "启动小新RPA在线平台开发环境..."
echo ""

# 检查是否安装了依赖
if [ ! -d "backend/.env" ]; then
    echo "检测到后端虚拟环境不存在，正在创建..."
    cd backend
    python -m venv .env
    source .env/bin/activate
    pip install -r requirements.txt
    cd ..
fi

if [ ! -d "frontend/node_modules" ]; then
    echo "检测到前端依赖未安装，正在安装..."
    cd frontend
    npm install
    cd ..
fi

echo "启动后端服务..."
cd backend
source .env/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

echo "等待3秒后启动前端服务..."
sleep 3

echo "启动前端服务..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "开发环境启动完成！"
echo "前端地址: http://localhost:3000"
echo "后端地址: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 捕获退出信号，清理子进程
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM

# 等待子进程结束
wait