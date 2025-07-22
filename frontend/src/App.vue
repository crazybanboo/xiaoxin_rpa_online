<template>
  <div id="app">
    <!-- 导航栏 -->
    <el-container v-if="!isLoginPage">
      <el-header class="app-header">
        <div class="header-left">
          <h1>小新RPA在线平台</h1>
        </div>
        <div class="header-right" v-if="authStore.isLoggedIn">
          <span class="username">{{ authStore.userInfo?.username }}</span>
          <el-button type="danger" size="small" @click="handleLogout">
            退出登录
          </el-button>
        </div>
      </el-header>
      
      <el-container>
        <el-aside width="200px" class="app-aside" v-if="authStore.isLoggedIn">
          <el-menu
            :default-active="$route.path"
            router
            class="app-menu"
          >
            <el-menu-item index="/">
              <el-icon><House /></el-icon>
              <span>首页</span>
            </el-menu-item>
            <el-menu-item index="/about">
              <el-icon><InfoFilled /></el-icon>
              <span>关于</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        
        <el-main class="app-main">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
    
    <!-- 登录页面不显示导航栏 -->
    <router-view v-else />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { House, InfoFilled } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// 判断是否是登录页面
const isLoginPage = computed(() => route.path === '/login')

// 处理登出
const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

// 页面加载时初始化认证状态
onMounted(async () => {
  await authStore.initAuth()
})
</script>

<style scoped>
#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  height: 100vh;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  padding: 0 20px;
  height: 60px;
}

.header-left h1 {
  margin: 0;
  color: #409eff;
  font-size: 20px;
  font-weight: 600;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.username {
  color: #606266;
  font-size: 14px;
}

.app-aside {
  background: #f5f5f5;
  border-right: 1px solid #e4e7ed;
}

.app-menu {
  border: none;
  background: transparent;
}

.app-main {
  padding: 20px;
  background: #f0f2f5;
  height: calc(100vh - 60px);
  overflow-y: auto;
}
</style>