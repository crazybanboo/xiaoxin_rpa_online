import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import request from '@/utils/request'
import { ElMessage } from 'element-plus'
import { authLogger } from '@/utils/logger'

interface LoginData {
  username: string
  password: string
}

interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

interface UserInfo {
  username: string
  is_valid: boolean
  expires_at?: string
}

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const accessToken = ref<string>(localStorage.getItem('access_token') || '')
  const refreshToken = ref<string>(localStorage.getItem('refresh_token') || '')
  const userInfo = ref<UserInfo | null>(null)
  const isLoading = ref(false)

  // 计算属性
  const isLoggedIn = computed(() => !!accessToken.value)
  const tokenType = ref('bearer')

  // 设置token
  const setTokens = (tokens: TokenResponse) => {
    accessToken.value = tokens.access_token
    refreshToken.value = tokens.refresh_token
    tokenType.value = tokens.token_type
    
    // 存储到localStorage
    localStorage.setItem('access_token', tokens.access_token)
    localStorage.setItem('refresh_token', tokens.refresh_token)
    localStorage.setItem('token_type', tokens.token_type)
    
    // 设置axios默认header
    request.defaults.headers.common['Authorization'] = `${tokens.token_type} ${tokens.access_token}`
  }

  // 清除token
  const clearTokens = () => {
    accessToken.value = ''
    refreshToken.value = ''
    userInfo.value = null
    
    // 清除localStorage
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('token_type')
    
    // 清除axios默认header
    delete request.defaults.headers.common['Authorization']
  }

  // 登录
  const login = async (loginData: LoginData): Promise<boolean> => {
    try {
      isLoading.value = true
      authLogger.info(`Login attempt for user: ${loginData.username}`)
      
      const response = await request.post<TokenResponse>('/v1/auth/login', loginData)
      
      console.log('Response structure:', response)
      console.log('Response.data:', response.data)
      setTokens(response)
      authLogger.info(`Login successful for user: ${loginData.username}`)
      ElMessage.success('登录成功')
      
      // 获取用户信息
      await getUserInfo()
      
      return true
    } catch (error: any) {
      authLogger.error(`Login failed for user: ${loginData.username}`, error)
      const message = error.response?.data?.detail || '登录失败'
      ElMessage.error(message)
      return false
    } finally {
      isLoading.value = false
    }
  }

  // 登出
  const logout = async () => {
    try {
      authLogger.info(`User logout initiated: ${userInfo.value?.username || 'unknown'}`)
      // 调用后端登出接口
      await request.post('/v1/auth/logout')
    } catch (error) {
      authLogger.error('Logout API call failed', error)
    } finally {
      clearTokens()
      authLogger.info('User logged out and tokens cleared')
      ElMessage.success('已退出登录')
    }
  }

  // 刷新token
  const refreshAccessToken = async (): Promise<boolean> => {
    if (!refreshToken.value) {
      authLogger.warn('No refresh token available')
      return false
    }

    try {
      authLogger.debug('Attempting to refresh access token')
      const response = await request.post<{access_token: string, token_type: string, expires_in: number}>(
        '/v1/auth/refresh',
        { refresh_token: refreshToken.value }
      )
      
      // 更新访问token
      accessToken.value = response.data.access_token
      localStorage.setItem('access_token', response.data.access_token)
      request.defaults.headers.common['Authorization'] = `${response.data.token_type} ${response.data.access_token}`
      
      authLogger.info('Access token refreshed successfully')
      return true
    } catch (error) {
      authLogger.error('Token refresh failed', error)
      // 刷新失败，清除所有token
      clearTokens()
      return false
    }
  }

  // 获取用户信息
  const getUserInfo = async (): Promise<boolean> => {
    if (!accessToken.value) {
      authLogger.warn('No access token available for user info')
      return false
    }

    try {
      authLogger.debug('Fetching user information')
      const response = await request.post<UserInfo>('/v1/auth/verify')
      userInfo.value = response.data
      authLogger.info(`User info retrieved: ${response.data.username}`)
      return true
    } catch (error) {
      authLogger.error('Failed to get user info', error)
      return false
    }
  }

  // 初始化认证状态
  const initAuth = async () => {
    if (accessToken.value) {
      authLogger.info('Initializing auth state from stored token')
      // 设置axios默认header
      request.defaults.headers.common['Authorization'] = `${tokenType.value} ${accessToken.value}`
      
      // 验证token有效性
      const isValid = await getUserInfo()
      if (!isValid) {
        authLogger.warn('Stored token is invalid, attempting refresh')
        // token无效，尝试刷新
        const refreshed = await refreshAccessToken()
        if (!refreshed) {
          authLogger.warn('Token refresh failed, clearing all tokens')
          clearTokens()
        }
      }
    } else {
      authLogger.debug('No stored token found')
    }
  }

  return {
    // 状态
    accessToken,
    refreshToken,
    userInfo,
    isLoading,
    // 计算属性
    isLoggedIn,
    // 方法
    login,
    logout,
    refreshAccessToken,
    getUserInfo,
    initAuth,
    clearTokens
  }
})