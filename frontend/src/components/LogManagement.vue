<template>
  <div class="log-management">
    <div class="log-header">
      <h3>日志管理</h3>
      <div class="log-actions">
        <el-button @click="refreshStats" :loading="loading">
          <i class="fas fa-sync-alt"></i> 刷新
        </el-button>
        <el-button @click="downloadLocalLogs">
          <i class="fas fa-download"></i> 下载本地日志
        </el-button>
        <el-button @click="clearLocalLogs" type="danger">
          <i class="fas fa-trash"></i> 清除本地日志
        </el-button>
      </div>
    </div>

    <!-- 本地日志统计 -->
    <div class="log-section">
      <h4>本地存储日志统计</h4>
      <div class="stats-grid">
        <div class="stat-item">
          <div class="stat-label">总计</div>
          <div class="stat-value">{{ localStats.total }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">DEBUG</div>
          <div class="stat-value debug">{{ localStats.debug }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">INFO</div>
          <div class="stat-value info">{{ localStats.info }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">WARN</div>
          <div class="stat-value warn">{{ localStats.warn }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">ERROR</div>
          <div class="stat-value error">{{ localStats.error }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">最近1小时</div>
          <div class="stat-value">{{ localStats.lastHour }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">今天</div>
          <div class="stat-value">{{ localStats.today }}</div>
        </div>
      </div>
    </div>

    <!-- 文件日志统计 -->
    <div class="log-section">
      <h4>文件日志统计</h4>
      <div v-if="fileStats.files && Object.keys(fileStats.files).length > 0">
        <div class="file-stats">
          <div v-for="(file, filename) in fileStats.files" :key="filename" class="file-item">
            <div class="file-info">
              <h5>{{ filename }}</h5>
              <div class="file-details">
                <span>大小: {{ formatFileSize(file.size) }}</span>
                <span>行数: {{ file.lines }}</span>
                <span>修改时间: {{ formatDate(file.modified) }}</span>
              </div>
            </div>
            <div class="file-actions">
              <el-button size="small" @click="viewLogFile(filename)">
                <i class="fas fa-eye"></i> 查看
              </el-button>
            </div>
          </div>
        </div>
        <div class="total-size">
          总文件大小: {{ formatFileSize(fileStats.total_size) }}
        </div>
      </div>
      <div v-else class="no-files">
        <i class="fas fa-file-alt"></i>
        <p>暂无文件日志</p>
      </div>
    </div>

    <!-- 日志内容查看对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="`查看日志文件: ${selectedFile}`"
      width="80%"
      top="5vh"
    >
      <div class="log-content">
        <div class="content-header">
          <span>显示最近 {{ logContent.returned_lines }} 行 (共 {{ logContent.total_lines }} 行)</span>
          <el-input-number
            v-model="viewLines"
            :min="10"
            :max="1000"
            :step="10"
            size="small"
            @change="loadLogContent"
          />
        </div>
        <pre class="log-text">{{ logContent.content }}</pre>
      </div>
      <template #footer>
        <el-button @click="dialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Logger } from '@/utils/logger'
import { useApiStore } from '@/stores/api'

const apiStore = useApiStore()
const loading = ref(false)
const dialogVisible = ref(false)
const selectedFile = ref('')
const viewLines = ref(100)

// 本地日志统计
const localStats = ref({
  total: 0,
  debug: 0,
  info: 0,
  warn: 0,
  error: 0,
  lastHour: 0,
  today: 0
})

// 文件日志统计
const fileStats = ref<{
  files: Record<string, any>
  total_size: number
}>({
  files: {},
  total_size: 0
})

// 日志内容
const logContent = ref({
  filename: '',
  total_lines: 0,
  returned_lines: 0,
  content: ''
})

onMounted(() => {
  refreshStats()
})

// 刷新统计信息
const refreshStats = async () => {
  loading.value = true
  try {
    // 获取本地日志统计
    localStats.value = Logger.getLogStats()
    
    // 获取文件日志统计
    const response = await fetch(`${apiStore.baseURL}/v1/logs/frontend/stats`)
    if (response.ok) {
      fileStats.value = await response.json()
    }
  } catch (error) {
    console.error('Failed to refresh log stats:', error)
    ElMessage.error('刷新日志统计失败')
  } finally {
    loading.value = false
  }
}

// 下载本地日志
const downloadLocalLogs = () => {
  Logger.downloadLogs()
  ElMessage.success('日志下载已开始')
}

// 清除本地日志
const clearLocalLogs = () => {
  Logger.clearLogs()
  localStats.value = Logger.getLogStats()
  ElMessage.success('本地日志已清除')
}

// 查看日志文件
const viewLogFile = async (filename: string) => {
  selectedFile.value = filename
  dialogVisible.value = true
  await loadLogContent()
}

// 加载日志内容
const loadLogContent = async () => {
  try {
    const response = await fetch(`${apiStore.baseURL}/v1/logs/frontend/${selectedFile.value}?lines=${viewLines.value}`)
    if (response.ok) {
      logContent.value = await response.json()
    } else {
      ElMessage.error('加载日志文件失败')
    }
  } catch (error) {
    console.error('Failed to load log content:', error)
    ElMessage.error('加载日志文件失败')
  }
}

// 格式化文件大小
const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 格式化日期
const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleString('zh-CN')
}
</script>

<style scoped>
.log-management {
  padding: 20px;
}

.log-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.log-header h3 {
  margin: 0;
  color: #333;
}

.log-actions {
  display: flex;
  gap: 10px;
}

.log-section {
  margin-bottom: 30px;
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}

.log-section h4 {
  margin: 0 0 15px 0;
  color: #555;
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 15px;
}

.stat-item {
  background: white;
  padding: 15px;
  border-radius: 6px;
  text-align: center;
  border: 1px solid #eee;
}

.stat-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.stat-value.debug { color: #6c757d; }
.stat-value.info { color: #28a745; }
.stat-value.warn { color: #ffc107; }
.stat-value.error { color: #dc3545; }

.file-stats {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 15px;
  border-radius: 6px;
  border: 1px solid #eee;
}

.file-info h5 {
  margin: 0 0 5px 0;
  color: #333;
}

.file-details {
  display: flex;
  gap: 15px;
  font-size: 12px;
  color: #666;
}

.file-actions {
  display: flex;
  gap: 5px;
}

.total-size {
  margin-top: 15px;
  text-align: right;
  font-weight: bold;
  color: #555;
}

.no-files {
  text-align: center;
  padding: 40px;
  color: #999;
}

.no-files i {
  font-size: 48px;
  margin-bottom: 15px;
  display: block;
}

.log-content {
  max-height: 60vh;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.log-text {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 15px;
  border-radius: 4px;
  max-height: 50vh;
  overflow-y: auto;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 12px;
  line-height: 1.4;
  white-space: pre-wrap;
  word-break: break-all;
}
</style>