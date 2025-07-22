<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1>小新RPA在线平台</h1>
        <p>管理员登录</p>
      </div>
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        status-icon
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            size="large"
            prefix-icon="User"
            clearable
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            prefix-icon="Lock"
            show-password
            clearable
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        
        <el-form-item>
          <el-checkbox v-model="rememberMe" label="记住登录状态" />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="authStore.isLoading"
            @click="handleLogin"
            class="login-button"
          >
            {{ authStore.isLoading ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// 表单引用
const loginFormRef = ref<FormInstance>()

// 表单数据
const loginForm = reactive({
  username: '',
  password: ''
})

// 记住登录状态
const rememberMe = ref(false)

// 表单验证规则
const loginRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度应为3-50个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ]
}

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    // 验证表单
    const valid = await loginFormRef.value.validate()
    if (!valid) return
    
    // 执行登录
    const success = await authStore.login(loginForm)
    
    if (success) {
      // 登录成功，跳转到首页
      router.push('/')
    }
  } catch (error) {
    console.error('登录过程中出现错误:', error)
  }
}

// 页面挂载时的处理
onMounted(() => {
  // 如果已经登录，直接跳转到首页
  if (authStore.isLoggedIn) {
    router.push('/')
  }
  
  // 从localStorage读取记住的用户名
  const rememberedUsername = localStorage.getItem('remembered_username')
  if (rememberedUsername) {
    loginForm.username = rememberedUsername
    rememberMe.value = true
  }
})

// 监听记住登录状态的变化
import { watch } from 'vue'
watch(rememberMe, (newValue) => {
  if (newValue) {
    localStorage.setItem('remembered_username', loginForm.username)
  } else {
    localStorage.removeItem('remembered_username')
  }
})
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  background: white;
  border-radius: 12px;
  padding: 40px 30px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h1 {
  color: #2c3e50;
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.login-header p {
  color: #7f8c8d;
  font-size: 14px;
  margin: 0;
}

.login-form {
  width: 100%;
}

.login-form .el-form-item {
  margin-bottom: 20px;
}

.login-button {
  width: 100%;
  height: 45px;
  font-size: 16px;
  font-weight: 500;
}

:deep(.el-input__wrapper) {
  padding: 12px 15px;
}

:deep(.el-checkbox__label) {
  font-size: 14px;
  color: #606266;
}

@media (max-width: 480px) {
  .login-card {
    margin: 0 10px;
    padding: 30px 20px;
  }
  
  .login-header h1 {
    font-size: 20px;
  }
}
</style>