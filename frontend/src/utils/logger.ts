/**
 * 前端日志系统
 * 
 * 功能特性：
 * - 多级日志（DEBUG, INFO, WARN, ERROR）
 * - 控制台彩色输出
 * - 本地存储持久化
 * - 日志文件下载
 * - 性能监控
 * - 错误追踪
 */

export enum LogLevel {
  DEBUG = 0,
  INFO = 1,
  WARN = 2,
  ERROR = 3
}

export interface LogEntry {
  timestamp: string
  level: LogLevel
  logger: string
  message: string
  data?: any
  stack?: string
  url?: string
  userAgent?: string
}

export class Logger {
  private name: string
  private static currentLevel: LogLevel = LogLevel.INFO
  private static maxStorageSize = 1024 * 1024 * 5 // 5MB
  private static storageKey = 'app_logs'
  
  // 控制台样式
  private static styles = {
    [LogLevel.DEBUG]: 'color: #6c757d; font-weight: normal;',
    [LogLevel.INFO]: 'color: #28a745; font-weight: bold;',
    [LogLevel.WARN]: 'color: #ffc107; font-weight: bold;',
    [LogLevel.ERROR]: 'color: #dc3545; font-weight: bold;'
  }

  private static levelNames = {
    [LogLevel.DEBUG]: 'DEBUG',
    [LogLevel.INFO]: 'INFO',
    [LogLevel.WARN]: 'WARN',
    [LogLevel.ERROR]: 'ERROR'
  }

  constructor(name: string) {
    this.name = name
  }

  /**
   * 设置全局日志级别
   */
  static setLevel(level: LogLevel) {
    Logger.currentLevel = level
  }

  /**
   * 获取当前日志级别
   */
  static getLevel(): LogLevel {
    return Logger.currentLevel
  }

  /**
   * DEBUG级别日志
   */
  debug(message: string, data?: any) {
    this.log(LogLevel.DEBUG, message, data)
  }

  /**
   * INFO级别日志
   */
  info(message: string, data?: any) {
    this.log(LogLevel.INFO, message, data)
  }

  /**
   * WARN级别日志
   */
  warn(message: string, data?: any) {
    this.log(LogLevel.WARN, message, data)
  }

  /**
   * ERROR级别日志
   */
  error(message: string, error?: Error | any) {
    let stack: string | undefined
    let errorData: any = error

    if (error instanceof Error) {
      stack = error.stack
      errorData = {
        name: error.name,
        message: error.message,
        stack: error.stack
      }
    }

    this.log(LogLevel.ERROR, message, errorData, stack)
  }

  /**
   * 记录API请求
   */
  logApiRequest(method: string, url: string, data?: any) {
    this.info(`🚀 API Request: ${method.toUpperCase()} ${url}`, {
      method,
      url,
      data,
      timestamp: new Date().toISOString()
    })
  }

  /**
   * 记录API响应
   */
  logApiResponse(method: string, url: string, status: number, responseTime?: number, data?: any) {
    const emoji = status < 400 ? '✅' : status < 500 ? '⚠️' : '❌'
    const level = status < 400 ? LogLevel.INFO : status < 500 ? LogLevel.WARN : LogLevel.ERROR
    
    const message = `${emoji} API Response: ${method.toUpperCase()} ${url} - ${status}`
    const logData = {
      method,
      url,
      status,
      responseTime,
      data,
      timestamp: new Date().toISOString()
    }

    this.log(level, message, logData)
  }

  /**
   * 记录用户行为
   */
  logUserAction(action: string, details?: any) {
    this.info(`👤 User Action: ${action}`, {
      action,
      details,
      url: window.location.href,
      timestamp: new Date().toISOString()
    })
  }

  /**
   * 记录性能信息
   */
  logPerformance(name: string, duration: number, details?: any) {
    const level = duration > 1000 ? LogLevel.WARN : LogLevel.INFO
    const emoji = duration > 1000 ? '🐌' : '⚡'
    
    this.log(level, `${emoji} Performance: ${name} - ${duration}ms`, {
      name,
      duration,
      details,
      timestamp: new Date().toISOString()
    })
  }

  /**
   * 核心日志方法
   */
  private log(level: LogLevel, message: string, data?: any, stack?: string) {
    // 检查日志级别
    if (level < Logger.currentLevel) {
      return
    }

    const timestamp = new Date().toISOString()
    const levelName = Logger.levelNames[level]
    
    // 创建日志条目
    const logEntry: LogEntry = {
      timestamp,
      level,
      logger: this.name,
      message,
      data,
      stack,
      url: window.location.href,
      userAgent: navigator.userAgent
    }

    // 控制台输出
    this.logToConsole(logEntry)
    
    // 存储到本地
    this.storeLog(logEntry)
  }

  /**
   * 控制台输出
   */
  private logToConsole(entry: LogEntry) {
    const { timestamp, level, logger, message, data } = entry
    const levelName = Logger.levelNames[level]
    const style = Logger.styles[level]
    
    const prefix = `%c[${timestamp}] [${levelName}] ${logger}:`
    
    if (data !== undefined) {
      console.log(prefix, style, message, data)
    } else {
      console.log(prefix, style, message)
    }

    // 错误级别显示堆栈信息
    if (level === LogLevel.ERROR && entry.stack) {
      console.error('Stack trace:', entry.stack)
    }
  }

  /**
   * 存储日志到本地存储
   */
  private storeLog(entry: LogEntry) {
    try {
      const stored = localStorage.getItem(Logger.storageKey)
      let logs: LogEntry[] = stored ? JSON.parse(stored) : []
      
      logs.push(entry)
      
      // 检查存储大小限制
      const serialized = JSON.stringify(logs)
      if (serialized.length > Logger.maxStorageSize) {
        // 删除最老的日志，保留最新的
        const half = Math.floor(logs.length / 2)
        logs = logs.slice(half)
      }
      
      localStorage.setItem(Logger.storageKey, JSON.stringify(logs))
    } catch (error) {
      // 如果存储失败，在控制台警告但不影响程序运行
      console.warn('Failed to store log:', error)
    }
  }

  /**
   * 获取存储的日志
   */
  static getLogs(): LogEntry[] {
    try {
      const stored = localStorage.getItem(Logger.storageKey)
      return stored ? JSON.parse(stored) : []
    } catch (error) {
      console.error('Failed to retrieve logs:', error)
      return []
    }
  }

  /**
   * 清除存储的日志
   */
  static clearLogs() {
    localStorage.removeItem(Logger.storageKey)
  }

  /**
   * 下载日志文件
   */
  static downloadLogs() {
    const logs = Logger.getLogs()
    const content = logs.map(log => {
      const { timestamp, level, logger, message, data } = log
      const levelName = Logger.levelNames[level]
      let line = `[${timestamp}] [${levelName}] ${logger}: ${message}`
      
      if (data) {
        line += ` | Data: ${JSON.stringify(data)}`
      }
      
      return line
    }).join('\n')

    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `app-logs-${new Date().toISOString().split('T')[0]}.txt`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  /**
   * 获取日志统计信息
   */
  static getLogStats() {
    const logs = Logger.getLogs()
    const stats = {
      total: logs.length,
      debug: 0,
      info: 0,
      warn: 0,
      error: 0,
      lastHour: 0,
      today: 0
    }

    const now = new Date()
    const oneHourAgo = new Date(now.getTime() - 60 * 60 * 1000)
    const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate())

    logs.forEach(log => {
      // 统计各级别数量
      switch (log.level) {
        case LogLevel.DEBUG:
          stats.debug++
          break
        case LogLevel.INFO:
          stats.info++
          break
        case LogLevel.WARN:
          stats.warn++
          break
        case LogLevel.ERROR:
          stats.error++
          break
      }

      // 统计时间范围
      const logTime = new Date(log.timestamp)
      if (logTime > oneHourAgo) {
        stats.lastHour++
      }
      if (logTime > todayStart) {
        stats.today++
      }
    })

    return stats
  }
}

// 创建常用的日志器实例
export const appLogger = new Logger('App')
export const apiLogger = new Logger('API')
export const authLogger = new Logger('Auth')
export const routerLogger = new Logger('Router')
export const storeLogger = new Logger('Store')
export const wsLogger = new Logger('WebSocket')
export const uiLogger = new Logger('UI')

// 默认日志实例
export const logger = appLogger

// 全局错误处理
window.addEventListener('error', (event) => {
  appLogger.error('Global error caught', {
    message: event.message,
    filename: event.filename,
    lineno: event.lineno,
    colno: event.colno,
    error: event.error
  })
})

// 全局未处理的Promise错误
window.addEventListener('unhandledrejection', (event) => {
  appLogger.error('Unhandled promise rejection', {
    reason: event.reason,
    promise: event.promise
  })
})

// 导出日志级别枚举供外部使用
export { LogLevel as LogLevelEnum }

export default Logger