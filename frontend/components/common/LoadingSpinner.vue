<template>
  <div class="flex flex-col items-center justify-center p-8">
    <div class="relative">
      <!-- 外层旋转圆环 -->
      <div class="w-12 h-12 border-4 border-gray-200 rounded-full"></div>
      <div class="absolute top-0 left-0 w-12 h-12 border-4 border-blue-500 rounded-full border-t-transparent animate-spin"></div>
    </div>
    <p class="mt-4 text-gray-500">{{ text || '加载中...' }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  text?: string
}>()
</script>

<style scoped>
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
.animate-spin {
  animation: spin 1s linear infinite;
}
</style>