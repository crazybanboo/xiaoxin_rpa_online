# 小新RPA后端单元测试文档

本文档描述了小新RPA在线平台后端的测试架构、配置和使用方法。

## 📁 测试结构

```
tests/
├── __init__.py
├── conftest.py              # pytest配置和共享fixture
├── utils.py                 # 测试工具和辅助函数
├── unit/                    # 单元测试
│   ├── __init__.py
│   ├── test_models.py       # 数据模型测试
│   ├── test_crud.py         # CRUD操作测试
│   ├── test_api.py          # API端点测试
│   └── test_schemas.py      # Pydantic Schema测试
├── integration/             # 集成测试
│   ├── __init__.py
│   ├── test_api_integration.py
│   └── test_database_integration.py
└── fixtures/                # 测试夹具和数据
    ├── __init__.py
    ├── database.py          # 数据库相关fixture
    └── sample_data.py       # 示例测试数据
```

## 🛠️ 测试配置

### pytest.ini
主要配置包括：
- 测试目录：`tests/`
- 覆盖率报告：HTML和终端输出
- 覆盖率阈值：80%
- 测试标记：unit, integration, slow, crud, api, models, schemas

### 测试数据库
- 使用SQLite内存数据库进行测试
- 每个测试函数使用独立的数据库会话
- 自动创建和清理测试表结构

## 🚀 运行测试

### 使用测试运行脚本（推荐）

```bash
# 运行所有测试
./run_tests.sh

# 运行特定类型的测试
./run_tests.sh unit          # 单元测试
./run_tests.sh integration   # 集成测试
./run_tests.sh models        # 模型测试
./run_tests.sh crud          # CRUD测试
./run_tests.sh api           # API测试
./run_tests.sh schemas       # Schema测试

# 生成覆盖率报告
./run_tests.sh coverage

# 快速测试（无覆盖率）
./run_tests.sh quick

# 显示帮助
./run_tests.sh help
```

### 使用Python测试运行器

```bash
# 激活虚拟环境
source .env/bin/activate

# 使用自定义测试运行器
python test_runner.py all
python test_runner.py unit
python test_runner.py coverage
python test_runner.py parallel
```

### 直接使用pytest

```bash
# 激活虚拟环境
source .env/bin/activate

# 运行所有测试
pytest

# 运行单元测试
pytest tests/unit/ -v

# 运行特定测试文件
pytest tests/unit/test_models.py -v

# 运行特定测试类
pytest tests/unit/test_models.py::TestAdminModel -v

# 运行特定测试方法
pytest tests/unit/test_models.py::TestAdminModel::test_admin_creation -v

# 生成覆盖率报告
pytest --cov=app --cov-report=html

# 并行运行测试
pytest -n auto

# 只运行失败的测试
pytest --lf
```

## 📊 测试覆盖

### 当前测试覆盖的功能

#### 1. **模型测试 (test_models.py)**
- ✅ 管理员模型 (Admin)
  - 创建、唯一性约束、字符串表示
  - 用户名和邮箱唯一性测试
- ✅ 客户端模型 (Client)  
  - 创建、默认值、字符串表示
- ✅ 升级包模型 (UpgradePackage)
  - 创建、字符串表示
- ✅ 升级任务模型 (UpgradeTask)
  - 创建、关联关系、字符串表示
- ✅ 时间戳Mixin
  - 自动创建和更新时间戳

#### 2. **CRUD操作测试 (test_crud.py)**
- ✅ 管理员CRUD
  - 创建（带密码加密）、查询、认证、更新、删除
- ✅ 客户端CRUD
  - 创建、IP查询、在线客户端查询、心跳更新
- ✅ 升级包CRUD
  - 创建、版本查询、获取最新版本
- ✅ 升级任务CRUD
  - 创建、客户端查询、状态查询、任务完成

#### 3. **API端点测试 (test_api.py)**
- ✅ 主要端点
  - 根路径、健康检查
- ✅ API v1端点
  - v1根路径、测试端点
- ✅ 错误处理
  - 404、405错误

#### 4. **Schema验证测试 (test_schemas.py)**
- ✅ 管理员Schema
  - 创建、更新、响应Schema验证
  - 邮箱格式验证、必填字段验证
- ✅ 客户端Schema
  - 创建、更新、响应Schema验证
- ✅ 升级包Schema
  - 创建、更新、响应Schema验证
- ✅ 升级任务Schema
  - 创建、更新、响应Schema验证

#### 5. **集成测试 (test_*_integration.py)**
- ✅ API集成测试
  - 带数据库的端点测试
- ✅ 数据库集成测试
  - 完整工作流测试、级联删除、并发操作

## 🔧 测试工具和Fixture

### 共享Fixture (conftest.py)
- `db_session`: 测试数据库会话
- `client`: FastAPI测试客户端
- `sample_*_data`: 各种示例数据

### 测试工具 (utils.py)
- `generate_random_*`: 随机数据生成器
- `create_test_*`: 测试数据创建助手
- `assert_*`: 自定义断言助手
- `DatabaseTestCase`: 数据库测试基类

### 示例数据 (fixtures/sample_data.py)
- 各种模型的示例数据fixture
- 批量测试数据创建fixture
- 复杂关联关系测试数据

## 📈 测试指标

### 覆盖率目标
- **最低覆盖率**: 80%
- **目标覆盖率**: 90%+

### 性能指标
- 单个测试执行时间 < 1秒
- 完整测试套件执行时间 < 30秒
- 并行测试可进一步减少执行时间

## 🐛 调试测试

### 调试单个测试
```bash
# 使用PDB调试
pytest tests/unit/test_models.py::TestAdminModel::test_admin_creation -s --pdb

# 显示详细输出
pytest tests/unit/test_models.py::TestAdminModel::test_admin_creation -v -s

# 停在第一个失败
pytest -x

# 显示最慢的10个测试
pytest --durations=10
```

### 常见问题解决

1. **数据库连接问题**
   - 确保测试使用独立的测试数据库
   - 检查fixture的数据库清理逻辑

2. **导入错误**
   - 确保PYTHONPATH正确设置
   - 检查相对导入路径

3. **异步测试问题**
   - 使用pytest-asyncio插件
   - 确保async/await语法正确

## 🔄 持续集成

### GitHub Actions配置示例
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.12
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          ./run_tests.sh coverage
      - name: Upload coverage
        uses: codecov/codecov-action@v1
```

## 📝 编写新测试

### 测试命名约定
- 测试文件：`test_*.py`
- 测试类：`Test*`
- 测试方法：`test_*`

### 测试结构模板
```python
import pytest
from app.models.your_model import YourModel

@pytest.mark.unit
class TestYourModel:
    """Test cases for YourModel"""

    def test_create_your_model(self, db_session):
        """Test creating YourModel"""
        # Arrange
        data = {"field": "value"}
        
        # Act
        instance = YourModel(**data)
        db_session.add(instance)
        db_session.commit()
        
        # Assert
        assert instance.field == "value"
        assert instance.id is not None
```

### 最佳实践
1. **AAA模式**: Arrange-Act-Assert
2. **独立性**: 每个测试应该独立运行
3. **命名**: 测试名称应该清晰描述测试内容
4. **文档**: 使用docstring描述测试目的
5. **数据**: 使用fixture提供测试数据
6. **标记**: 使用pytest.mark进行测试分类

## 🎯 测试最佳实践

### 1. 测试隔离
- 每个测试使用独立的数据库事务
- 避免测试间的数据依赖
- 使用fixture提供干净的测试环境

### 2. 测试数据
- 使用有意义的测试数据
- 避免硬编码值，使用fixture
- 测试边界条件和异常情况

### 3. 断言
- 使用具体的断言而不是通用的assertTrue
- 提供清晰的错误消息
- 测试预期的行为而不是实现细节

### 4. 性能
- 保持测试快速执行
- 使用内存数据库进行单元测试
- 合理使用并行测试

## 🛡️ 测试安全

### 敏感数据处理
- 不在测试中使用真实的生产数据
- 使用模拟对象进行外部API调用
- 确保测试数据不包含敏感信息

### 环境隔离
- 测试环境与生产环境完全隔离
- 使用环境变量区分测试和生产配置
- 自动清理测试产生的文件和数据

---

通过完整的测试套件，我们确保了小新RPA在线平台后端的质量和稳定性。测试不仅验证了功能的正确性，还为重构和新功能开发提供了安全保障。