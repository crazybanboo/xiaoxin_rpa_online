# 小新RPA在线平台 - 后端API服务

基于 FastAPI 构建的高性能异步Web API服务，为小新RPA在线平台提供完整的后端支持。

## 📊 开发状态

- ✅ **Task 1**: 项目基础架构和配置 (已完成)
- ✅ **Task 2**: 数据库模型和数据层设计 (已完成并测试)  
- 🔄 **Task 3**: 管理员认证和权限系统 (进行中)
- 📋 **Task 4**: 客户端设备管理API (计划中)
- 📋 **Task 5**: 升级包管理系统 (计划中)
- 📋 **Task 6**: 升级任务调度系统 (计划中)

## 🚀 技术栈

- **Python 3.12+** - 主要编程语言
- **FastAPI** - 现代、快速的Web框架
- **Uvicorn** - ASGI服务器
- **SQLAlchemy 2.0** - ORM数据库操作
- **Alembic** - 数据库迁移工具
- **SQLite** - 轻量级数据库（开发环境）
- **PostgreSQL** - 生产数据库
- **Redis** - 缓存和会话存储
- **Pydantic** - 数据验证和序列化
- **Python-JOSE** - JWT令牌处理
- **Bcrypt** - 密码加密

## 📁 项目结构

```
backend/
├── app/                    # 应用核心代码
│   ├── __init__.py
│   ├── main.py            # FastAPI应用入口
│   ├── api/               # API路由
│   │   ├── __init__.py
│   │   └── api_v1/        # API v1版本
│   │       ├── __init__.py
│   │       └── api.py     # 路由定义
│   ├── core/              # 核心配置
│   │   ├── __init__.py
│   │   ├── config.py      # 应用配置
│   │   └── database.py    # 数据库连接配置
│   ├── models/            # SQLAlchemy数据模型
│   │   ├── __init__.py
│   │   ├── base.py        # 基础模型类
│   │   ├── admin.py       # 管理员模型
│   │   ├── client.py      # 客户端模型
│   │   ├── upgrade_package.py  # 升级包模型
│   │   └── upgrade_task.py     # 升级任务模型
│   ├── schemas/           # Pydantic数据验证模型
│   │   ├── __init__.py
│   │   ├── admin.py       # 管理员Schema
│   │   ├── client.py      # 客户端Schema
│   │   ├── upgrade_package.py  # 升级包Schema
│   │   └── upgrade_task.py     # 升级任务Schema
│   └── crud/              # 数据库CRUD操作
│       ├── __init__.py
│       ├── base.py        # 基础CRUD类
│       ├── crud_admin.py  # 管理员CRUD
│       ├── crud_client.py # 客户端CRUD
│       ├── crud_upgrade_package.py  # 升级包CRUD
│       └── crud_upgrade_task.py     # 升级任务CRUD
├── alembic/               # 数据库迁移工具
├── .env/                  # Python虚拟环境
├── requirements.txt       # Python依赖包
├── test_db.py            # 数据库测试脚本
├── test_api.py           # API测试脚本
├── test_relationships.py # 数据关系测试脚本
├── xiaoxin_rpa.db        # SQLite数据库文件
├── Dockerfile.dev        # Docker开发环境配置
└── README.md             # 项目说明文档
```

## 🛠️ 开发环境搭建

### 前置要求

- Python 3.12+
- SQLite (开发环境，已包含)
- PostgreSQL 12+ (生产环境)
- Redis 6+ (可选，用于缓存)

### 安装步骤

1. **创建并激活虚拟环境**
   ```bash
   cd backend
   python3.12 -m venv .env
   source .env/bin/activate  # Linux/macOS
   # 或
   .env\Scripts\activate     # Windows
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量**
   ```bash
   # 创建 .env 文件并配置以下变量
   cp .env.example .env
   
   # 编辑 .env 文件，配置数据库连接等信息
   POSTGRES_SERVER=localhost
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=xiaoxin_rpa
   SECRET_KEY=your-secret-key-here
   ```

4. **数据库初始化**
   ```bash
   # 开发环境使用SQLite，无需额外配置
   # 运行数据库测试以验证配置
   python test_db.py
   
   # 可选：使用Alembic进行数据库迁移管理
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

## 🚀 运行应用

### 开发模式
```bash
# 激活虚拟环境
source .env/bin/activate

# 启动开发服务器（支持热重载）
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 生产模式
```bash
# 使用Gunicorn启动
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Docker方式
```bash
# 构建镜像
docker build -f Dockerfile.dev -t xiaoxin-rpa-backend .

# 运行容器
docker run -p 8000:8000 xiaoxin-rpa-backend
```

## 📚 API文档

启动服务后，可通过以下地址访问API文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## 🔍 主要API端点

### 基础接口
- `GET /` - 服务根路径
- `GET /api/health` - 健康检查接口

### API v1接口
- `GET /api/v1/` - API版本信息
- `GET /api/v1/test` - API测试接口

### 数据模型API（规划中）
- 管理员管理API
- 客户端设备管理API  
- 升级包管理API
- 升级任务管理API

## 🧪 测试

### 运行内置测试脚本
```bash
# 激活虚拟环境
source .env/bin/activate

# 测试数据库基础功能
python test_db.py

# 测试数据模型关系
python test_relationships.py

# 测试API端点
python test_api.py

# 运行综合测试总结
python test_summary_task2.py
```

### 单元测试（使用pytest）

**现已完全实现完整的单元测试套件！** 包含模型、CRUD、API和Schema的全面测试。

```bash
# 激活虚拟环境
source .env/bin/activate

# 使用测试运行脚本（推荐）
./run_tests.sh              # 运行所有测试
./run_tests.sh coverage     # 生成覆盖率报告
./run_tests.sh unit         # 只运行单元测试
./run_tests.sh models       # 只运行模型测试

# 或直接使用pytest
pytest                      # 运行所有测试
pytest tests/unit/ -v       # 运行单元测试（详细输出）
pytest --cov=app           # 生成覆盖率报告
pytest -n auto             # 并行运行测试
```

#### 测试覆盖范围
- ✅ **数据模型测试**: Admin, Client, UpgradePackage, UpgradeTask
- ✅ **CRUD操作测试**: 创建、查询、更新、删除操作
- ✅ **API端点测试**: FastAPI路由和错误处理
- ✅ **Schema验证测试**: Pydantic数据验证和序列化
- ✅ **集成测试**: 完整工作流和数据库集成
- ✅ **测试覆盖率**: 目标80%+，生成HTML覆盖率报告

详细测试文档请查看 [TESTING.md](TESTING.md)

### API测试
```bash
# 测试健康检查接口
curl -X GET "http://localhost:8000/api/health"

# 预期响应
{"status":"ok","message":"服务运行正常"}
```

### 测试结果
✅ **Task 2 - 数据库模型和数据层设计** 已通过全部测试：
- ✅ 数据库连接和初始化
- ✅ SQLAlchemy ORM模型定义
- ✅ CRUD操作完整性
- ✅ 模型关联关系
- ✅ Pydantic Schema验证
- ✅ FastAPI基础框架
- ✅ 高级查询功能

## 🔧 代码质量

### 代码格式化
```bash
# 使用Black格式化代码
black app/

# 使用isort排序导入
isort app/

# 使用flake8检查代码规范
flake8 app/
```

### 预提交钩子
```bash
# 安装pre-commit
pip install pre-commit

# 安装钩子
pre-commit install

# 手动运行所有钩子
pre-commit run --all-files
```

## 📝 数据库管理

### 数据模型
当前已实现的核心数据模型：

1. **Admin** - 管理员模型
   - 用户认证和权限管理
   - 密码加密存储

2. **Client** - 客户端模型  
   - 设备信息管理
   - 在线状态跟踪
   - 心跳检测

3. **UpgradePackage** - 升级包模型
   - 版本信息管理
   - 文件路径和大小跟踪

4. **UpgradeTask** - 升级任务模型
   - 任务状态管理
   - 客户端与升级包关联
   - 执行时间跟踪

### Alembic迁移命令
```bash
# 创建新的迁移文件
alembic revision --autogenerate -m "描述更改内容"

# 升级到最新版本
alembic upgrade head

# 回滚到上一个版本
alembic downgrade -1

# 查看迁移历史
alembic history
```

## 🔐 安全配置

### JWT配置
- 在生产环境中务必更改 `SECRET_KEY`
- 合理设置 `ACCESS_TOKEN_EXPIRE_MINUTES`
- 启用HTTPS传输

### CORS配置
- 在 `config.py` 中配置允许的前端域名
- 生产环境中不要使用通配符 `*`

## 📊 监控和日志

### 应用监控
- 健康检查: `/api/health`
- 性能指标通过Prometheus暴露
- 日志输出到标准输出，支持结构化日志

### 日志级别
```bash
# 设置日志级别环境变量
export LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
```

## 🚀 部署

### Docker部署
```bash
# 使用docker-compose
docker-compose -f docker-compose.dev.yml up -d
```

### 手动部署
1. 配置反向代理（Nginx）
2. 使用Supervisor管理进程
3. 配置SSL证书
4. 设置数据库备份

## 🤝 贡献指南

1. Fork项目仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- 项目维护者: 小新RPA团队
- 问题反馈: 请在GitHub Issues中提出
- 邮箱: support@xiaoxin-rpa.com

---

**注意**: 这是开发版本，请不要在生产环境中直接使用。生产部署前请确保完成安全配置和性能优化。