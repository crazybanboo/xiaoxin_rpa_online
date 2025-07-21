<template>
  <div class="home">
    <el-container>
      <el-header height="60px">
        <div class="header-content">
          <h1>小新RPA在线平台</h1>
          <el-button @click="testApi" type="primary">测试API连接</el-button>
        </div>
      </el-header>
      <el-main>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card>
              <template #header>
                <span>RPA流程管理</span>
              </template>
              <p>创建和管理自动化流程</p>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card>
              <template #header>
                <span>任务监控</span>
              </template>
              <p>实时监控任务执行状态</p>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card>
              <template #header>
                <span>系统设置</span>
              </template>
              <p>配置系统参数和用户权限</p>
            </el-card>
          </el-col>
        </el-row>
        
        <el-divider />
        
        <div v-if="apiStatus">
          <el-alert :title="apiStatus.message" :type="apiStatus.type" show-icon />
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useApiStore } from '@/stores/api'

const apiStore = useApiStore()
const apiStatus = ref<{ message: string; type: 'success' | 'error' } | null>(null)

const testApi = async () => {
  try {
    const result = await apiStore.testConnection()
    apiStatus.value = { message: `API连接成功: ${result.message}`, type: 'success' }
  } catch (error) {
    apiStatus.value = { message: `API连接失败: ${error}`, type: 'error' }
  }
}
</script>

<style scoped>
.home {
  height: 100vh;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.header-content h1 {
  margin: 0;
  color: #409eff;
}

.el-card {
  margin-bottom: 20px;
}
</style>