import { onMounted, onUnmounted, ref } from 'vue'
import { getWebSocketService } from '@/services/websocket'
import type { WebSocketService } from '@/services/websocket'

export function useWebSocket() {
  const wsService = getWebSocketService()
  const isConnected = ref(false)
  const connectionError = ref<Error | null>(null)

  const connect = async () => {
    try {
      await wsService.connect()
      isConnected.value = true
      connectionError.value = null
    } catch (error) {
      isConnected.value = false
      connectionError.value = error as Error
      console.error('Failed to connect WebSocket:', error)
    }
  }

  const disconnect = () => {
    wsService.disconnect()
    isConnected.value = false
  }

  const subscribe = (topic: string) => {
    wsService.subscribe(topic)
  }

  const unsubscribe = (topic: string) => {
    wsService.unsubscribe(topic)
  }

  onMounted(() => {
    connect()
  })

  onUnmounted(() => {
    disconnect()
  })

  return {
    isConnected,
    connectionError,
    connect,
    disconnect,
    subscribe,
    unsubscribe
  }
}

export function useClientStatusWebSocket() {
  const { subscribe, unsubscribe, ...rest } = useWebSocket()

  onMounted(() => {
    // 订阅客户端状态相关主题
    subscribe('client_status')
    subscribe('heartbeat')
  })

  onUnmounted(() => {
    // 取消订阅
    unsubscribe('client_status')
    unsubscribe('heartbeat')
  })

  return rest
}