import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { routerLogger } from '@/utils/logger'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('@/views/AboutView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/client-monitor',
    name: 'ClientMonitor',
    component: () => import('@/views/ClientMonitorView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { requiresGuest: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  routerLogger.info(`Navigating from ${from.path} to ${to.path}`, {
    from: from.name,
    to: to.name,
    meta: to.meta
  })
  
  const authStore = useAuthStore()
  
  // 初始化认证状态（仅在首次加载时）
  if (!authStore.isLoggedIn && localStorage.getItem('access_token')) {
    routerLogger.debug('Initializing auth state from stored token')
    await authStore.initAuth()
  }
  
  // 检查需要认证的路由
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    routerLogger.warn(`Access denied to ${to.path} - user not authenticated`)
    next('/login')
    return
  }
  
  // 检查需要游客状态的路由（如登录页面）
  if (to.meta.requiresGuest && authStore.isLoggedIn) {
    routerLogger.info(`Redirecting authenticated user from ${to.path} to home`)
    next('/')
    return
  }
  
  routerLogger.info(`Navigation to ${to.path} allowed`)
  next()
})

// 路由错误处理
router.onError((error) => {
  routerLogger.error('Router error', error)
})

export default router