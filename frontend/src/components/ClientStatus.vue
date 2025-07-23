<template>
  <div class="client-status-container">
    <!-- 统计信息 -->
    <el-row :gutter="20" class="status-summary">
      <el-col :span="8">
        <el-card shadow="hover">
          <el-statistic title="总客户端数" :value="clientStore.totalCount">
            <template #prefix>
              <el-icon color="#409eff"><Monitor /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <el-statistic title="在线客户端" :value="clientStore.onlineCount">
            <template #prefix>
              <el-icon color="#67c23a"><CircleCheckFilled /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <el-statistic title="离线客户端" :value="clientStore.offlineCount">
            <template #prefix>
              <el-icon color="#f56c6c"><CircleCloseFilled /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
    </el-row>

    <!-- 搜索和筛选栏 -->
    <el-card class="filter-card">
      <el-row :gutter="20" align="middle">
        <el-col :span="8">
          <el-input
            v-model="clientStore.searchQuery"
            placeholder="搜索客户端名称、IP或MAC地址"
            clearable
            @input="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
        <el-col :span="8">
          <el-radio-group v-model="clientStore.statusFilter" @change="handleStatusFilter">
            <el-radio-button label="all">全部</el-radio-button>
            <el-radio-button label="online">在线</el-radio-button>
            <el-radio-button label="offline">离线</el-radio-button>
          </el-radio-group>
        </el-col>
        <el-col :span="8">
          <el-button type="primary" @click="refreshClients" :loading="clientStore.loading">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- 客户端列表 -->
    <el-card class="client-list-card">
      <template #header>
        <div class="card-header">
          <span>客户端列表</span>
          <el-tag type="info">{{ clientStore.filteredClients.length }} 个客户端</el-tag>
        </div>
      </template>

      <el-table
        :data="clientStore.filteredClients"
        style="width: 100%"
        v-loading="clientStore.loading"
        empty-text="暂无客户端数据"
      >
        <el-table-column prop="id" label="ID" width="80" />
        
        <el-table-column prop="name" label="客户端名称" min-width="150">
          <template #default="{ row }">
            <div class="client-name">
              <span>{{ row.name }}</span>
              <el-tag v-if="row.version" size="small" type="info">v{{ row.version }}</el-tag>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <div class="status-cell">
              <span class="status-dot" :class="`status-${row.status}`"></span>
              <span>{{ row.status === 'online' ? '在线' : '离线' }}</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="ip_address" label="IP地址" width="150" />
        
        <el-table-column prop="mac_address" label="MAC地址" width="180" />
        
        <el-table-column prop="last_heartbeat" label="最后心跳" width="180" sortable>
          <template #default="{ row }">
            <span v-if="row.last_heartbeat">
              {{ formatTime(row.last_heartbeat) }}
            </span>
            <span v-else class="no-heartbeat">从未</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
        
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" link @click="viewDetail(row)">
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- WebSocket连接状态 -->
    <div class="connection-status">
      <el-tag :type="isConnected ? 'success' : 'danger'" effect="dark">
        <el-icon>
          <Connection v-if="isConnected" />
          <Disconnect v-else />
        </el-icon>
        {{ isConnected ? 'WebSocket已连接' : 'WebSocket未连接' }}
      </el-tag>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Monitor,
  CircleCheckFilled,
  CircleCloseFilled,
  Search,
  Refresh,
  Connection,
  Disconnect
} from '@element-plus/icons-vue'
import { useClientStore } from '@/stores/client'
import { useClientStatusWebSocket } from '@/composables/useWebSocket'
import { useApiStore } from '@/stores/api'
import type { Client } from '@/stores/client'

const clientStore = useClientStore()
const { isConnected } = useClientStatusWebSocket()
const apiStore = useApiStore()

// 格式化时间
const formatTime = (timeStr: string) => {
  const date = new Date(timeStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  // 小于1分钟
  if (diff < 60000) {
    return '刚刚'
  }
  
  // 小于1小时
  if (diff < 3600000) {
    const minutes = Math.floor(diff / 60000)
    return `${minutes}分钟前`
  }
  
  // 小于24小时
  if (diff < 86400000) {
    const hours = Math.floor(diff / 3600000)
    return `${hours}小时前`
  }
  
  // 显示具体日期时间
  return date.toLocaleString('zh-CN')
}

// 搜索处理
const handleSearch = (value: string) => {
  clientStore.setSearchQuery(value)
}

// 状态筛选
const handleStatusFilter = (value: 'all' | 'online' | 'offline') => {
  clientStore.setStatusFilter(value)
}

// 刷新客户端列表
const refreshClients = async () => {
  try {
    clientStore.setLoading(true)
    const response = await apiStore.getClients()
    clientStore.setClients(response.data)
    ElMessage.success('刷新成功')
  } catch (error) {
    ElMessage.error('获取客户端列表失败')
    console.error('Failed to fetch clients:', error)
  } finally {
    clientStore.setLoading(false)
  }
}

// 查看客户端详情
const viewDetail = (client: Client) => {
  // TODO: 跳转到客户端详情页面或显示详情弹窗
  ElMessage.info(`查看客户端 ${client.name} 的详情`)
}

// 初始化
onMounted(() => {
  refreshClients()
})
</script>

<style scoped>
.client-status-container {
  padding: 20px;
}

.status-summary {
  margin-bottom: 20px;
}

.filter-card {
  margin-bottom: 20px;
}

.client-list-card {
  position: relative;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.client-name {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-cell {
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.status-dot.status-online {
  background-color: #67c23a;
  animation: pulse 2s infinite;
}

.status-dot.status-offline {
  background-color: #f56c6c;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(103, 194, 58, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(103, 194, 58, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(103, 194, 58, 0);
  }
}

.no-heartbeat {
  color: #909399;
}

.connection-status {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 100;
}
</style>