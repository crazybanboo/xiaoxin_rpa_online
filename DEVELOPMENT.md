# 开发环境管理指南

本文档介绍如何使用项目的服务管理脚本进行开发。

## 🚀 快速开始

### 启动开发环境
```bash
# 方法1：使用快捷脚本
./dev-start.sh

# 方法2：使用服务管理器
./scripts/service-manager.sh dev
```

### 停止开发环境
```bash
# 方法1：使用快捷脚本
./dev-stop.sh

# 方法2：使用服务管理器
./scripts/service-manager.sh stop
```

### 查看服务状态
```bash
# 使用快捷脚本
./dev-status.sh

# 使用服务管理器
./scripts/service-manager.sh status
```

### 查看日志
```bash
# 查看所有服务日志
./dev-logs.sh

# 查看指定服务日志
./dev-logs.sh backend 100    # 查看后端最近100行日志
./dev-logs.sh frontend 50    # 查看前端最近50行日志
```

## 📋 服务管理脚本

### 主服务管理器 (`scripts/service-manager.sh`)

这是主要的服务管理脚本，提供统一的服务管理接口。

```bash
# 基本命令
./scripts/service-manager.sh start     # 启动所有服务
./scripts/service-manager.sh stop      # 停止所有服务
./scripts/service-manager.sh restart   # 重启所有服务
./scripts/service-manager.sh status    # 查看服务状态
./scripts/service-manager.sh dev       # 开发模式启动

# 监控命令
./scripts/service-manager.sh health    # 健康检查
./scripts/service-manager.sh logs      # 查看日志
./scripts/service-manager.sh error-logs # 查看错误日志

# 构建命令
./scripts/service-manager.sh build     # 生产构建

# 维护命令
./scripts/service-manager.sh cleanup   # 清理旧日志
./scripts/service-manager.sh info      # 系统信息
```

### 后端服务管理 (`scripts/backend-service.sh`)

专门管理后端服务的脚本。

```bash
# 基本操作
./scripts/backend-service.sh start     # 启动后端服务
./scripts/backend-service.sh stop      # 停止后端服务
./scripts/backend-service.sh restart   # 重启后端服务
./scripts/backend-service.sh status    # 查看后端状态

# 日志管理
./scripts/backend-service.sh logs      # 查看日志
./scripts/backend-service.sh error-logs # 查看错误日志
./scripts/backend-service.sh monitor   # 实时监控日志

# 健康检查
./scripts/backend-service.sh health    # 健康检查
```

**后端服务信息：**
- 运行端口：8000
- API文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/api/health

### 前端服务管理 (`scripts/frontend-service.sh`)

专门管理前端服务的脚本。

```bash
# 基本操作
./scripts/frontend-service.sh start    # 启动前端服务
./scripts/frontend-service.sh stop     # 停止前端服务
./scripts/frontend-service.sh restart  # 重启前端服务
./scripts/frontend-service.sh status   # 查看前端状态

# 日志管理
./scripts/frontend-service.sh logs     # 查看日志
./scripts/frontend-service.sh error-logs # 查看错误日志
./scripts/frontend-service.sh monitor  # 实时监控日志

# 构建相关
./scripts/frontend-service.sh build    # 生产构建
./scripts/frontend-service.sh preview  # 预览构建
./scripts/frontend-service.sh lint     # 代码检查
./scripts/frontend-service.sh type-check # 类型检查

# 健康检查
./scripts/frontend-service.sh health   # 健康检查
```

**前端服务信息：**
- 开发端口：5173
- 应用地址：http://localhost:5173

## 🔧 个别服务管理

你也可以通过主服务管理器来操作个别服务：

```bash
# 操作后端服务
./scripts/service-manager.sh backend start
./scripts/service-manager.sh backend status
./scripts/service-manager.sh backend logs

# 操作前端服务
./scripts/service-manager.sh frontend start
./scripts/service-manager.sh frontend status
./scripts/service-manager.sh frontend build
```

## 📁 日志管理

### 日志文件位置
所有日志文件都保存在 `logs/` 目录下：

```
logs/
├── backend.log           # 后端服务日志
├── backend-error.log     # 后端错误日志
├── backend.pid           # 后端进程ID
├── frontend.log          # 前端服务日志
├── frontend-error.log    # 前端错误日志
└── frontend.pid          # 前端进程ID
```

### 日志滚动策略

**后端日志（Python）：**
- 应用日志：`backend/logs/app.log` （按大小滚动，10MB，保留5个文件）
- 错误日志：`backend/logs/error.log` （按大小滚动，10MB，保留3个文件）
- 每日日志：`backend/logs/daily.log` （按天滚动，保留30天）

**前端日志（开发服务器）：**
- 开发日志：`logs/frontend.log` （服务器启动和构建输出）
- 错误日志：`logs/frontend-error.log` （错误输出）

**浏览器日志（JavaScript）：**
- 存储在浏览器 localStorage 中
- 最大存储 5MB
- 可以通过开发者工具下载

### 日志清理

```bash
# 清理7天前的日志（默认）
./scripts/service-manager.sh cleanup

# 清理3天前的日志
./scripts/service-manager.sh cleanup 3
```

## 🔍 故障排除

### 服务启动失败

1. **检查端口占用：**
   ```bash
   # 检查8000端口（后端）
   lsof -i :8000
   
   # 检查5173端口（前端）
   lsof -i :5173
   ```

2. **查看错误日志：**
   ```bash
   ./scripts/service-manager.sh error-logs
   ```

3. **检查依赖：**
   ```bash
   # 后端依赖
   cd backend && source .env/bin/activate && pip list
   
   # 前端依赖
   cd frontend && npm list
   ```

### 健康检查失败

```bash
# 检查所有服务健康状态
./scripts/service-manager.sh health

# 单独检查
./scripts/backend-service.sh health
./scripts/frontend-service.sh health
```

### 日志文件过大

```bash
# 查看日志目录使用情况
du -sh logs/

# 清理旧日志
./scripts/service-manager.sh cleanup 1
```

## 🏗️ 生产部署

### 构建前端
```bash
./scripts/service-manager.sh build
```

构建结果在 `frontend/dist/` 目录。

### 运行测试
```bash
# 后端测试
cd backend && ./run_tests.sh

# 前端测试（如果配置了）
cd frontend && npm test
```

## 📱 开发工作流推荐

1. **启动开发环境：**
   ```bash
   ./dev-start.sh
   ```

2. **实时查看日志：**
   ```bash
   # Terminal 2
   ./scripts/backend-service.sh monitor
   
   # Terminal 3  
   ./scripts/frontend-service.sh monitor
   ```

3. **检查服务状态：**
   ```bash
   ./dev-status.sh
   ```

4. **开发完成后停止：**
   ```bash
   ./dev-stop.sh
   ```

## ⚙️ 环境变量

### 后端环境变量 (backend/.env)
```bash
LOG_LEVEL=INFO                    # 日志级别
LOG_FILE_MAX_SIZE=10485760       # 日志文件最大大小（字节）
LOG_FILE_BACKUP_COUNT=5          # 日志文件备份数量
LOG_DAILY_BACKUP_COUNT=30        # 每日日志保留天数
```

### 前端环境变量
```bash
VITE_API_BASE_URL=http://localhost:8000  # API基础地址
```

## 🤝 协作开发

当多人协作时，建议的工作流：

1. **独立的开发环境：** 每个开发者运行自己的服务实例
2. **共享后端数据库：** 使用共享的开发数据库（可选）
3. **日志隔离：** 每个开发者的日志保存在各自的 `logs/` 目录
4. **端口冲突：** 如有需要，可以修改脚本中的端口配置

---

## 📞 技术支持

如果遇到问题：

1. 查看相关日志文件
2. 运行健康检查
3. 检查系统信息：`./scripts/service-manager.sh info`
4. 查看本文档的故障排除部分

祝开发愉快！ 🎉