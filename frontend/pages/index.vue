<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <div class="bg-white rounded-lg shadow p-8">
      <h1 class="text-3xl font-bold text-gray-900">AI 智能面试系统</h1>
      <p class="text-gray-600 mt-4">欢迎使用 AI 驱动的技术面试平台</p>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
        <NuxtLink to="/jobs" class="block bg-blue-50 p-6 rounded-lg hover:bg-blue-100 transition-colors">
          <h2 class="text-xl font-semibold text-blue-600">📋 岗位管理</h2>
          <p class="text-gray-600 mt-2">创建和管理面试岗位</p>
        </NuxtLink>
        
        <NuxtLink to="/candidates" class="block bg-green-50 p-6 rounded-lg hover:bg-green-100 transition-colors">
          <h2 class="text-xl font-semibold text-green-600">👥 候选人管理</h2>
          <p class="text-gray-600 mt-2">添加和管理候选人信息</p>
        </NuxtLink>
        
        <NuxtLink to="/interviews" class="block bg-purple-50 p-6 rounded-lg hover:bg-purple-100 transition-colors">
          <h2 class="text-xl font-semibold text-purple-600">🎯 面试记录</h2>
          <p class="text-gray-600 mt-2">查看面试历史和报告</p>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>