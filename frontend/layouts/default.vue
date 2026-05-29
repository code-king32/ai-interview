<template>
  <div class="min-h-screen bg-gray-100">
    <nav class="bg-white shadow-md sticky top-0 z-40">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex space-x-8">
            <NuxtLink to="/" class="flex items-center text-gray-800 hover:text-blue-600 font-semibold">
              🤖 AI 面试系统
            </NuxtLink>
            <NuxtLink to="/jobs" class="flex items-center text-gray-600 hover:text-blue-600">
              岗位管理
            </NuxtLink>
            <NuxtLink to="/candidates" class="flex items-center text-gray-600 hover:text-green-600">
              候选人
            </NuxtLink>
            <NuxtLink to="/interviews" class="flex items-center text-gray-600 hover:text-purple-600">
              面试记录
            </NuxtLink>
          </div>
        </div>
      </div>
    </nav>
    
    <main>
      <slot />
    </main>
  </div>
</template>