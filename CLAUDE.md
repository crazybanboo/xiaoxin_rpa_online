# Claude Code Instructions

## 通用

如果你是连接着ide的，请调用ide相关接口实时获得代码报错提示信息，并根据提示信息进行修改。

## Task Master AI Instructions
**Import Task Master's development workflow commands and guidelines, treat as if import is in the main CLAUDE.md file.**
@./.taskmaster/CLAUDE.md

# backend

如果你在开发backend，请使用以下命令：

先进入到backend目录下，然后执行以下命令：
```bash
# 激活虚拟环境
source .env/bin/activate

# 运行所有测试
./run_tests.sh
```

# frontend

如果你在开发frontend，请使用以下命令：

先进入到frontend目录下，然后执行以下命令：
```bash
# 开发环境运行
npm run dev

# 构建生产版本
npm run build

# 预览构建结果
npm run preview

# 代码检查
npm run lint

# 代码格式化
npm run format

# 类型检查
npm run type-check
```