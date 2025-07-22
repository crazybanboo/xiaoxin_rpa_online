# 小新RPA在线平台 - 前端应用

基于 Vue 3 + TypeScript + Vite 构建的现代化前端应用，为小新RPA在线平台提供直观易用的用户界面。

## 🚀 技术栈

- **Vue 3** - 渐进式JavaScript框架
- **TypeScript** - JavaScript的超集，提供类型安全
- **Vite** - 下一代前端构建工具
- **Vue Router 4** - Vue.js官方路由管理器
- **Pinia** - Vue的现代状态管理库
- **Element Plus** - 基于Vue 3的组件库
- **Axios** - HTTP客户端库
- **ESLint** - 代码质量检查工具
- **Prettier** - 代码格式化工具

## 📁 项目结构

```
frontend/
├── public/                 # 静态资源
├── src/                   # 源代码目录
│   ├── components/        # 公共组件
│   ├── views/            # 页面组件
│   │   ├── HomeView.vue  # 首页
│   │   └── AboutView.vue # 关于页面
│   ├── router/           # 路由配置
│   │   └── index.ts      # 路由定义
│   ├── stores/           # 状态管理
│   │   └── api.ts        # API状态管理
│   ├── utils/            # 工具函数
│   │   └── request.ts    # HTTP请求封装
│   ├── App.vue           # 根组件
│   └── main.ts           # 应用入口
├── package.json          # 项目配置和依赖
├── vite.config.ts        # Vite配置文件
├── tsconfig.json         # TypeScript配置
├── index.html            # HTML模板
└── README.md             # 项目说明文档
```

## 🛠️ 开发环境搭建

### 前置要求

- **Node.js** 16.0+ 
- **npm** 8.0+ 或 **yarn** 1.22+
- **现代浏览器** (支持ES6+)

### 安装步骤

1. **克隆项目并进入前端目录**
   ```bash
   cd frontend
   ```

2. **安装依赖**
   ```bash
   npm install
   # 或使用yarn
   yarn install
   ```

3. **启动开发服务器**
   ```bash
   npm run dev
   # 或使用yarn
   yarn dev
   ```

4. **访问应用**
   打开浏览器访问: http://localhost:3000

## 🚀 可用脚本

在项目目录中，你可以运行以下命令：

### `npm run dev`
启动开发服务器，支持热重载。
- 本地访问: http://localhost:3000
- 网络访问: 使用 `--host` 参数暴露到局域网

### `npm run build`
构建生产版本到 `dist` 目录。
- 代码压缩和优化
- TypeScript类型检查
- 资源打包和分块

### `npm run preview`
预览生产构建版本。
```bash
npm run build
npm run preview
```

### `npm run lint`
运行ESLint检查和修复代码问题。
```bash
npm run lint
```

### `npm run format`
使用Prettier格式化代码。
```bash
npm run format
```

### `npm run type-check`
运行TypeScript类型检查。
```bash
npm run type-check
```

## 🔧 开发配置

### Vite配置 (vite.config.ts)

```typescript
export default defineConfig({
  plugins: [
    vue(),
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver()],
    }),
  ],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
```

### API代理配置

前端开发服务器配置了API代理，将 `/api` 请求转发到后端服务:
- 前端: http://localhost:3000
- 后端: http://localhost:8000
- 代理规则: `/api/*` → `http://localhost:8000/api/*`

### 环境变量

支持以下环境变量配置：

```bash
# .env.local (本地开发)
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_TITLE=小新RPA在线平台

# .env.production (生产环境)
VITE_API_BASE_URL=https://api.xiaoxin-rpa.com
VITE_APP_TITLE=小新RPA在线平台
```

## 🎨 UI组件库

### Element Plus

项目使用 Element Plus 作为主要UI组件库：

```vue
<template>
  <el-button type="primary" @click="handleClick">
    点击按钮
  </el-button>
</template>
```

### 自动导入配置

通过 `unplugin-auto-import` 和 `unplugin-vue-components` 实现组件自动导入：

- Element Plus 组件自动导入
- Vue Composition API 自动导入
- 减少手动import语句

## 📡 HTTP请求

### Axios封装

`src/utils/request.ts` 提供了统一的HTTP请求封装：

```typescript
import request from '@/utils/request'

// GET请求
const getData = () => request.get('/api/data')

// POST请求
const postData = (data) => request.post('/api/data', data)
```

### 请求拦截器
- 自动添加认证令牌
- 统一错误处理
- 加载状态管理

### 响应拦截器
- 统一响应数据格式
- 错误消息提示
- 状态码处理

## 🗂️ 状态管理

### Pinia Store

使用Pinia进行状态管理：

```typescript
// stores/api.ts
export const useApiStore = defineStore('api', () => {
  const data = ref([])
  
  const fetchData = async () => {
    const response = await request.get('/api/data')
    data.value = response.data
  }
  
  return { data, fetchData }
})
```

## 🛣️ 路由配置

### Vue Router 4

`src/router/index.ts` 配置应用路由：

```typescript
const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('@/views/AboutView.vue')
  }
]
```

### 路由特性
- 懒加载路由组件
- 路由守卫支持
- 动态路由配置

## 🧪 测试

### 单元测试 (即将支持)
```bash
# 运行单元测试
npm run test:unit

# 生成测试覆盖率报告
npm run test:coverage
```

### E2E测试 (即将支持)
```bash
# 运行端到端测试
npm run test:e2e
```

## 📦 构建和部署

### 生产构建
```bash
# 构建生产版本
npm run build

# 构建文件输出到 dist/ 目录
```

### 构建优化
- **Tree Shaking**: 自动移除未使用的代码
- **代码分割**: 按路由和组件分割代码块
- **资源优化**: 图片压缩、CSS提取
- **缓存优化**: 文件名哈希，支持长期缓存

### 部署选项

#### 静态托管
```bash
# 构建后部署到静态托管服务
npm run build
# 将 dist/ 目录上传到服务器
```

#### Docker部署
```bash
# 使用Docker部署
docker build -f Dockerfile.dev -t xiaoxin-rpa-frontend .
docker run -p 3000:3000 xiaoxin-rpa-frontend
```

#### Nginx配置示例
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        root /path/to/dist;
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔍 代码质量

### ESLint配置
- Vue3推荐规则
- TypeScript支持
- 自动修复功能

### Prettier配置
- 统一代码格式
- 保存时自动格式化
- 团队协作友好

### TypeScript配置
- 严格类型检查
- 路径别名支持 (`@/` → `src/`)
- 组件类型推导

## 🌐 浏览器支持

- **Chrome** 87+
- **Firefox** 78+
- **Safari** 14+
- **Edge** 88+

### Polyfill支持
自动添加必要的polyfill确保兼容性。

## 📊 性能优化

### 构建优化
- Vite快速冷启动
- HMR热模块替换
- 基于ES modules的开发

### 运行时优化
- Vue 3 Composition API
- 响应式系统优化
- 组件懒加载

### 网络优化
- HTTP/2支持
- 资源预加载
- 缓存策略

## 🔧 故障排除

### 常见问题

**1. 依赖安装失败**
```bash
# 清除缓存重新安装
rm -rf node_modules package-lock.json
npm install
```

**2. 端口占用**
```bash
# 修改开发端口
npm run dev -- --port 3001
```

**3. API请求失败**
- 检查后端服务是否启动
- 确认代理配置正确
- 查看浏览器网络面板

**4. TypeScript错误**
```bash
# 重新生成类型声明
npm run type-check
```

## 🤝 贡献指南

1. Fork项目仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 遵循代码规范 (`npm run lint && npm run format`)
4. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
5. 推送到分支 (`git push origin feature/AmazingFeature`)
6. 创建Pull Request

### 代码规范
- 使用TypeScript编写
- 遵循ESLint规则
- 组件使用PascalCase命名
- 文件使用kebab-case命名

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- 项目维护者: 小新RPA团队
- 问题反馈: 请在GitHub Issues中提出
- 邮箱: support@xiaoxin-rpa.com

---

**开发提示**: 
- 使用Vue DevTools浏览器扩展进行调试
- 推荐使用VS Code + Vetur/Volar插件
- 遵循Vue 3 Composition API最佳实践