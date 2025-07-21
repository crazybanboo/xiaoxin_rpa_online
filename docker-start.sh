#!/bin/bash

echo "启动小新RPA在线平台Docker开发环境..."
echo ""

# 检查Docker是否运行
if ! docker info >/dev/null 2>&1; then
    echo "错误: Docker未运行，请先启动Docker"
    exit 1
fi

# 检查docker-compose是否安装
if ! command -v docker-compose >/dev/null 2>&1; then
    echo "错误: docker-compose未安装"
    exit 1
fi

echo "清理现有容器..."
docker-compose -f docker-compose.dev.yml down

echo "构建并启动服务..."
docker-compose -f docker-compose.dev.yml up --build -d

echo ""
echo "Docker开发环境启动完成！"
echo ""
echo "服务访问地址:"
echo "前端: http://localhost:3000"
echo "后端: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
echo "PostgreSQL: localhost:5432 (用户: postgres, 密码: postgres123)"
echo "Redis: localhost:6379"
echo ""
echo "常用命令:"
echo "查看服务状态: docker-compose -f docker-compose.dev.yml ps"
echo "查看日志: docker-compose -f docker-compose.dev.yml logs -f"
echo "停止服务: docker-compose -f docker-compose.dev.yml down"
echo ""