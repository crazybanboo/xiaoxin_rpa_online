# 小新RPA在线平台

基于前后端分离架构的RPA自动化平台，提供在线RPA流程管理和执行服务。

## 项目架构

### 技术栈

**后端 (Backend)**
- FastAPI - 高性能Python Web框架
- SQLAlchemy - ORM数据库操作
- Uvicorn - ASGI服务器
- Python-jose - JWT认证
- HTTPx - HTTP客户端
- APScheduler - 定时任务调度
- WebSocket - 实时通信支持

**前端 (Frontend)**
- Vue 3 - 渐进式JavaScript框架
- TypeScript - 类型安全的JavaScript
- Element Plus - Vue 3组件库
- Pinia - Vue状态管理
- Axios - HTTP客户端
- Vite - 构建工具

### 目录结构

```
xiaoxin_rpa_online/
├── backend/                 # FastAPI后端
│   ├── app/                # 应用核心代码
│   ├── tests/              # 后端测试
│   ├── alembic/            # 数据库迁移
│   └── requirements.txt    # Python依赖
├── frontend/               # Vue3前端
│   ├── src/                # 前端源码
│   ├── public/             # 静态资源
│   └── dist/               # 构建产物
├── docs/                   # 项目文档
├── deploy/                 # 部署配置
├── xiaoxin_rpa_pro/        # RPA核心引擎 (子模块)
└── README.md               # 项目说明
```

## 快速开始

### 后端启动

```bash
cd backend
python -m venv .env
.env\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

### Docker开发环境

```bash
docker-compose up -d
```

## 功能特性

### 核心功能
- RPA流程在线管理
- 可视化流程设计器
- 实时执行监控
- 用户权限管理
- 多租户支持
- API接口服务

### 客户端监控功能
- **心跳监控系统** - 实时监控客户端在线状态
  - 客户端心跳接收API
  - 自动离线检测机制
  - 心跳超时配置（默认60秒）
- **WebSocket实时通信** - 客户端状态实时推送
  - 订阅式消息模型
  - 自动重连机制
  - 多主题支持（client_status, heartbeat等）
- **后台监控任务** - 定时检查客户端状态
  - 使用APScheduler实现定时任务
  - 可配置检查间隔（默认30秒）
  - 自动标记离线客户端
- **客户端状态管理** - 前端状态管理和展示
  - Pinia状态存储
  - 客户端筛选和搜索
  - 实时状态更新
- **监控UI组件** - 可视化客户端状态
  - 客户端列表展示
  - 在线/离线状态指示
  - 最后心跳时间显示
  - WebSocket连接状态指示

## API文档

### 心跳监控API

#### 发送心跳
```
POST /api/v1/client/heartbeat
Content-Type: application/json

{
  "client_id": 1,
  "timestamp": "2025-07-23T12:00:00Z",
  "status": "online",
  "version": "1.0.0",
  "ip_address": "192.168.1.100"
}
```

#### 获取客户端状态
```
GET /api/v1/client/heartbeat/status/{client_id}
```

### WebSocket连接

#### 连接端点
```
ws://localhost:8000/api/v1/client/ws
```

#### 订阅主题
```json
{
  "action": "subscribe",
  "topic": "client_status"
}
```

#### 消息类型
- `CLIENT_STATUS_UPDATE` - 客户端状态更新
- `CLIENT_CONNECTED` - 客户端连接
- `CLIENT_DISCONNECTED` - 客户端断开
- `HEARTBEAT_RECEIVED` - 收到心跳
- `SYSTEM_MESSAGE` - 系统消息

## 配置说明

### 心跳监控配置

在 `backend/.env` 文件中添加：

```bash
# 心跳超时时间（秒）
HEARTBEAT_TIMEOUT_SECONDS=60

# 心跳检查间隔（秒）
HEARTBEAT_CHECK_INTERVAL_SECONDS=30
```

## 开发指南

详细的开发文档请查看 `docs/` 目录。