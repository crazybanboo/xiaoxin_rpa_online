import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import App from './App.vue'
import router from './router'
import { Logger, LogLevel, appLogger } from './utils/logger'

// 设置日志级别（根据环境变量）
const isDev = import.meta.env.DEV
Logger.setLevel(isDev ? LogLevel.DEBUG : LogLevel.INFO)

appLogger.info('🚀 Application starting...', {
  environment: isDev ? 'development' : 'production',
  timestamp: new Date().toISOString()
})

const app = createApp(App)

// 注册Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

app.mount('#app')

appLogger.info('✅ Application started successfully')