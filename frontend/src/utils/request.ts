import axios, { type AxiosResponse, type AxiosError } from 'axios'
import { ElMessage } from 'element-plus'
import { apiLogger } from './logger'

// 创建axios实例
const service = axios.create({
  baseURL: '/api',
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json;charset=UTF-8'
  }
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 记录请求开始时间
    config.metadata = { startTime: Date.now() }
    
    // 记录API请求
    apiLogger.logApiRequest(config.method || 'unknown', config.url || '', {
      params: config.params,
      data: config.data
    })
    
    // 自动添加token到请求头
    const token = localStorage.getItem('access_token')
    const tokenType = localStorage.getItem('token_type') || 'bearer'
    
    if (token && !config.headers.Authorization) {
      config.headers.Authorization = `${tokenType} ${token}`
    }
    
    return config
  },
  error => {
    // 对请求错误做些什么
    apiLogger.error('Request interceptor error', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse) => {
    // 计算响应时间
    const responseTime = response.config.metadata?.startTime 
      ? Date.now() - response.config.metadata.startTime 
      : undefined
    
    // 记录API响应
    apiLogger.logApiResponse(
      response.config.method || 'unknown',
      response.config.url || '',
      response.status,
      responseTime,
      response.data
    )
    
    // 对响应数据做点什么
    const res = response.data
    return res
  },
  async (error: AxiosError) => {
    // 计算响应时间
    const responseTime = error.config?.metadata?.startTime 
      ? Date.now() - error.config.metadata.startTime 
      : undefined
    
    // 记录API错误响应
    if (error.response) {
      apiLogger.logApiResponse(
        error.config?.method || 'unknown',
        error.config?.url || '',
        error.response.status,
        responseTime,
        error.response.data
      )
    } else {
      apiLogger.error('API request failed', {
        method: error.config?.method,
        url: error.config?.url,
        message: error.message,
        responseTime
      })
    }
    
    // 对响应错误做点什么
    let message = '网络错误'
    
    if (error.response) {
      switch (error.response.status) {
        case 400:
          message = '请求参数错误'
          break
        case 401:
          message = '未授权，请重新登录'
          // 处理401错误 - token过期
          const refreshToken = localStorage.getItem('refresh_token')
          if (refreshToken && error.config) {
            try {
              // 尝试刷新token
              const response = await axios.post('/api/v1/auth/refresh', {
                refresh_token: refreshToken
              })
              
              const { access_token, token_type } = response.data
              localStorage.setItem('access_token', access_token)
              localStorage.setItem('token_type', token_type)
              
              // 重新发送原请求
              error.config.headers.Authorization = `${token_type} ${access_token}`
              return service.request(error.config)
            } catch (refreshError) {
              // 刷新失败，清除token并跳转到登录页
              localStorage.removeItem('access_token')
              localStorage.removeItem('refresh_token')
              localStorage.removeItem('token_type')
              // 可以在这里触发路由跳转到登录页
              window.location.href = '/login'
            }
          } else {
            // 没有refresh token，直接跳转登录页
            window.location.href = '/login'
          }
          break
        case 403:
          message = '拒绝访问'
          break
        case 404:
          message = '请求地址不存在'
          break
        case 500:
          message = '服务器内部错误'
          break
        default:
          message = `连接错误${error.response.status}`
      }
    } else if (error.request) {
      message = '网络连接异常'
    }
    
    ElMessage.error(message)
    return Promise.reject(error)
  }
)

export default service