# 小新RPA在线平台 - 后端API服务

基于 FastAPI 构建的高性能异步Web API服务，为小新RPA在线平台提供完整的后端支持。

## 🚀 技术栈

- **Python 3.12+** - 主要编程语言
- **FastAPI** - 现代、快速的Web框架
- **Uvicorn** - ASGI服务器
- **SQLAlchemy 2.0** - ORM数据库操作
- **Alembic** - 数据库迁移工具
- **PostgreSQL** - 主数据库
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
│   └── core/              # 核心配置
│       ├── __init__.py
│       └── config.py      # 应用配置
├── .env/                  # Python虚拟环境
├── requirements.txt       # Python依赖包
├── Dockerfile.dev        # Docker开发环境配置
└── README.md             # 项目说明文档
```

## 🛠️ 开发环境搭建

### 前置要求

- Python 3.12+
- PostgreSQL 12+
- Redis 6+

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
   # 创建数据库迁移
   alembic init alembic
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
- 更多接口正在开发中...

## 🧪 测试

### 运行单元测试
```bash
# 激活虚拟环境
source .env/bin/activate

# 运行所有测试
pytest

# 运行指定测试文件
pytest tests/test_main.py

# 生成测试覆盖率报告
pytest --cov=app tests/
```

### API测试
```bash
# 测试健康检查接口
curl -X GET "http://localhost:8000/api/health"

# 预期响应
{"status":"ok","message":"服务运行正常"}
```

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