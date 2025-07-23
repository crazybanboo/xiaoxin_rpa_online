import { useClientStore } from '@/stores/client'
import type { ClientStatusUpdate } from '@/stores/client'

export interface WebSocketMessage {
  type: string
  data: any
}

export interface WebSocketAction {
  action: 'subscribe' | 'unsubscribe' | 'get_info'
  topic?: string
}

export class WebSocketService {
  private ws: WebSocket | null = null
  private url: string
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectInterval = 3000
  private pingInterval: NodeJS.Timeout | null = null
  private isIntentionallyClosed = false
  private subscriptions = new Set<string>()

  constructor(url: string) {
    this.url = url
  }

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        this.isIntentionallyClosed = false
        this.ws = new WebSocket(this.url)

        this.ws.onopen = () => {
          console.log('WebSocket connected')
          this.reconnectAttempts = 0
          this.resubscribeToTopics()
          this.startPing()
          resolve()
        }

        this.ws.onmessage = (event) => {
          this.handleMessage(event.data)
        }

        this.ws.onerror = (error) => {
          console.error('WebSocket error:', error)
          reject(error)
        }

        this.ws.onclose = () => {
          console.log('WebSocket disconnected')
          this.stopPing()
          
          if (!this.isIntentionallyClosed) {
            this.attemptReconnect()
          }
        }
      } catch (error) {
        reject(error)
      }
    })
  }

  disconnect(): void {
    this.isIntentionallyClosed = true
    this.stopPing()
    
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
  }

  subscribe(topic: string): void {
    this.subscriptions.add(topic)
    
    if (this.isConnected()) {
      const message: WebSocketAction = {
        action: 'subscribe',
        topic
      }
      this.send(message)
    }
  }

  unsubscribe(topic: string): void {
    this.subscriptions.delete(topic)
    
    if (this.isConnected()) {
      const message: WebSocketAction = {
        action: 'unsubscribe',
        topic
      }
      this.send(message)
    }
  }

  private send(data: any): void {
    if (this.isConnected()) {
      this.ws!.send(JSON.stringify(data))
    }
  }

  private isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN
  }

  private handleMessage(data: string): void {
    try {
      const message: WebSocketMessage = JSON.parse(data)
      
      switch (message.type) {
        case 'CLIENT_STATUS_UPDATE':
          this.handleClientStatusUpdate(message.data)
          break
        case 'CLIENT_CONNECTED':
          this.handleClientConnected(message.data)
          break
        case 'CLIENT_DISCONNECTED':
          this.handleClientDisconnected(message.data)
          break
        case 'HEARTBEAT_RECEIVED':
          this.handleHeartbeatReceived(message.data)
          break
        case 'SYSTEM_MESSAGE':
          this.handleSystemMessage(message.data)
          break
        case 'pong':
          // Pong response from server
          break
        default:
          console.log('Unknown message type:', message.type)
      }
    } catch (error) {
      console.error('Error parsing WebSocket message:', error)
    }
  }

  private handleClientStatusUpdate(data: ClientStatusUpdate): void {
    const clientStore = useClientStore()
    clientStore.handleStatusUpdate(data)
  }

  private handleClientConnected(data: any): void {
    console.log('Client connected:', data)
    // 可以添加通知或其他处理
  }

  private handleClientDisconnected(data: any): void {
    console.log('Client disconnected:', data)
    // 可以添加通知或其他处理
  }

  private handleHeartbeatReceived(data: any): void {
    const clientStore = useClientStore()
    clientStore.updateClient(data.client_id, {
      last_heartbeat: data.timestamp,
      status: 'online'
    })
  }

  private handleSystemMessage(data: any): void {
    console.log('System message:', data)
    // 可以显示系统消息给用户
  }

  private attemptReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached')
      return
    }

    this.reconnectAttempts++
    console.log(`Reconnecting... (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`)

    setTimeout(() => {
      this.connect().catch((error) => {
        console.error('Reconnection failed:', error)
      })
    }, this.reconnectInterval * this.reconnectAttempts)
  }

  private resubscribeToTopics(): void {
    // 重新订阅所有主题
    this.subscriptions.forEach(topic => {
      const message: WebSocketAction = {
        action: 'subscribe',
        topic
      }
      this.send(message)
    })
  }

  private startPing(): void {
    this.pingInterval = setInterval(() => {
      if (this.isConnected()) {
        this.send({ type: 'ping' })
      }
    }, 30000) // Ping every 30 seconds
  }

  private stopPing(): void {
    if (this.pingInterval) {
      clearInterval(this.pingInterval)
      this.pingInterval = null
    }
  }
}

// 创建单例
let wsService: WebSocketService | null = null

export function getWebSocketService(): WebSocketService {
  if (!wsService) {
    // 根据环境配置WebSocket URL
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = import.meta.env.VITE_API_BASE_URL || window.location.host
    const wsUrl = `${protocol}//${host}/api/v1/client/ws`
    
    wsService = new WebSocketService(wsUrl)
  }
  return wsService
}