import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { Ref } from 'vue'

export interface Client {
  id: number
  name: string
  description?: string
  ip_address?: string
  mac_address?: string
  status: 'online' | 'offline' | 'unknown'
  version?: string
  last_heartbeat?: string
  created_at: string
  updated_at: string
}

export interface ClientStatusUpdate {
  client_id: number
  name: string
  status: 'online' | 'offline'
  last_heartbeat?: string
  reason?: string
}

export const useClientStore = defineStore('client', () => {
  // State
  const clients: Ref<Client[]> = ref([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const searchQuery = ref('')
  const statusFilter = ref<'all' | 'online' | 'offline'>('all')
  const sortBy = ref<'name' | 'status' | 'last_heartbeat'>('name')
  const sortOrder = ref<'asc' | 'desc'>('asc')

  // Getters
  const filteredClients = computed(() => {
    let result = [...clients.value]

    // Apply search filter
    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase()
      result = result.filter(client =>
        client.name.toLowerCase().includes(query) ||
        client.ip_address?.toLowerCase().includes(query) ||
        client.mac_address?.toLowerCase().includes(query)
      )
    }

    // Apply status filter
    if (statusFilter.value !== 'all') {
      result = result.filter(client => client.status === statusFilter.value)
    }

    // Apply sorting
    result.sort((a, b) => {
      let aValue, bValue

      switch (sortBy.value) {
        case 'name':
          aValue = a.name.toLowerCase()
          bValue = b.name.toLowerCase()
          break
        case 'status':
          aValue = a.status
          bValue = b.status
          break
        case 'last_heartbeat':
          aValue = a.last_heartbeat || ''
          bValue = b.last_heartbeat || ''
          break
        default:
          return 0
      }

      const comparison = aValue < bValue ? -1 : aValue > bValue ? 1 : 0
      return sortOrder.value === 'asc' ? comparison : -comparison
    })

    return result
  })

  const onlineClients = computed(() =>
    clients.value.filter(client => client.status === 'online')
  )

  const offlineClients = computed(() =>
    clients.value.filter(client => client.status === 'offline')
  )

  const onlineCount = computed(() => onlineClients.value.length)
  const offlineCount = computed(() => offlineClients.value.length)
  const totalCount = computed(() => clients.value.length)

  // Actions
  function setClients(newClients: Client[]) {
    clients.value = newClients
  }

  function updateClient(clientId: number, updates: Partial<Client>) {
    const index = clients.value.findIndex(c => c.id === clientId)
    if (index !== -1) {
      clients.value[index] = { ...clients.value[index], ...updates }
    }
  }

  function addClient(client: Client) {
    clients.value.push(client)
  }

  function removeClient(clientId: number) {
    const index = clients.value.findIndex(c => c.id === clientId)
    if (index !== -1) {
      clients.value.splice(index, 1)
    }
  }

  function handleStatusUpdate(update: ClientStatusUpdate) {
    const client = clients.value.find(c => c.id === update.client_id)
    if (client) {
      client.status = update.status
      if (update.last_heartbeat) {
        client.last_heartbeat = update.last_heartbeat
      }
    } else {
      // 如果客户端不存在，可能需要从服务器获取完整信息
      // 这里暂时创建一个基本的客户端对象
      const newClient: Client = {
        id: update.client_id,
        name: update.name,
        status: update.status,
        last_heartbeat: update.last_heartbeat,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }
      addClient(newClient)
    }
  }

  function setSearchQuery(query: string) {
    searchQuery.value = query
  }

  function setStatusFilter(filter: 'all' | 'online' | 'offline') {
    statusFilter.value = filter
  }

  function setSorting(field: 'name' | 'status' | 'last_heartbeat', order?: 'asc' | 'desc') {
    sortBy.value = field
    if (order) {
      sortOrder.value = order
    } else {
      // Toggle order if same field
      if (sortBy.value === field) {
        sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
      } else {
        sortOrder.value = 'asc'
      }
    }
  }

  function setLoading(isLoading: boolean) {
    loading.value = isLoading
  }

  function setError(errorMessage: string | null) {
    error.value = errorMessage
  }

  function clearError() {
    error.value = null
  }

  function $reset() {
    clients.value = []
    loading.value = false
    error.value = null
    searchQuery.value = ''
    statusFilter.value = 'all'
    sortBy.value = 'name'
    sortOrder.value = 'asc'
  }

  return {
    // State
    clients,
    loading,
    error,
    searchQuery,
    statusFilter,
    sortBy,
    sortOrder,

    // Getters
    filteredClients,
    onlineClients,
    offlineClients,
    onlineCount,
    offlineCount,
    totalCount,

    // Actions
    setClients,
    updateClient,
    addClient,
    removeClient,
    handleStatusUpdate,
    setSearchQuery,
    setStatusFilter,
    setSorting,
    setLoading,
    setError,
    clearError,
    $reset
  }
})