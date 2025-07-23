<template>
  <div class="client-monitor-view">
    <h1>客户端监控</h1>
    <ClientStatus />
  </div>
</template>

<script setup lang="ts">
import ClientStatus from '@/components/ClientStatus.vue'
</script>

<style scoped>
.client-monitor-view {
  height: 100%;
}

h1 {
  margin: 0 0 20px 20px;
  font-size: 24px;
  font-weight: 500;
}
</style>