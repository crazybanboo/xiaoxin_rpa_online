import axios, { AxiosResponse, AxiosError } from 'axios'
import { ElMessage } from 'element-plus'

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
    // 在发送请求之前做些什么
    // 可以在此处添加token等认证信息
    return config
  },
  error => {
    // 对请求错误做些什么
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse) => {
    // 对响应数据做点什么
    const res = response.data
    return res
  },
  (error: AxiosError) => {
    // 对响应错误做点什么
    let message = '网络错误'
    
    if (error.response) {
      switch (error.response.status) {
        case 400:
          message = '请求参数错误'
          break
        case 401:
          message = '未授权，请重新登录'
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