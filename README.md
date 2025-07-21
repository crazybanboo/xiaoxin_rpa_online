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

- RPA流程在线管理
- 可视化流程设计器
- 实时执行监控
- 用户权限管理
- 多租户支持
- API接口服务

## 开发指南

详细的开发文档请查看 `docs/` 目录。