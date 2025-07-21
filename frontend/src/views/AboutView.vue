<template>
  <div class="about">
    <el-container>
      <el-header height="60px">
        <div class="header-content">
          <h1>关于小新RPA</h1>
          <el-button @click="$router.push('/')" type="primary">返回首页</el-button>
        </div>
      </el-header>
      <el-main>
        <el-card>
          <template #header>
            <span>平台介绍</span>
          </template>
          <p>小新RPA在线平台是一个基于前后端分离架构的自动化流程管理系统。</p>
          <p>主要功能包括：</p>
          <ul>
            <li>可视化流程设计</li>
            <li>自动化任务执行</li>
            <li>实时监控和报告</li>
            <li>用户权限管理</li>
            <li>多租户支持</li>
          </ul>
        </el-card>
        
        <el-card style="margin-top: 20px">
          <template #header>
            <span>技术栈</span>
          </template>
          <el-row :gutter="20">
            <el-col :span="12">
              <h3>前端</h3>
              <el-tag style="margin: 2px">Vue 3</el-tag>
              <el-tag style="margin: 2px">TypeScript</el-tag>
              <el-tag style="margin: 2px">Element Plus</el-tag>
              <el-tag style="margin: 2px">Vite</el-tag>
            </el-col>
            <el-col :span="12">
              <h3>后端</h3>
              <el-tag style="margin: 2px">FastAPI</el-tag>
              <el-tag style="margin: 2px">SQLAlchemy</el-tag>
              <el-tag style="margin: 2px">PostgreSQL</el-tag>
              <el-tag style="margin: 2px">Redis</el-tag>
            </el-col>
          </el-row>
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
// Vue 3 Composition API setup
</script>

<style scoped>
.about {
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
</style>