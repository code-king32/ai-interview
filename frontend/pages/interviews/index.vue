<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900">面试记录</h1>
      <NuxtLink to="/interviews/create" class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg">
        开始新面试
      </NuxtLink>
    </div>

    <div v-if="loading" class="text-center py-8 text-gray-500">
      加载中...
    </div>

    <div v-else class="bg-white rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">岗位名称</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">候选人</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">状态</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">综合评分</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">创建时间</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">操作</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="item in interviews" :key="item.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ item.id }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ item.job_title || '-' }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ item.candidate_name || '-' }}</td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="getStatusClass(item.status)" class="px-2 py-1 rounded-full text-xs">
                {{ getStatusText(item.status) }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <span v-if="item.overall_score" class="font-medium text-blue-600">{{ item.overall_score }}/10</span>
              <span v-else class="text-gray-400">-</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(item.created_at) }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <NuxtLink :to="`/interviews/${item.id}`" class="text-blue-600 hover:text-blue-900 mr-3">
                进入
              </NuxtLink>
              <NuxtLink v-if="item.status === 'completed'" :to="`/reports/${item.id}`" class="text-green-600 hover:text-green-900">
                报告
              </NuxtLink>
            </td>
          </tr>
          <tr v-if="interviews.length === 0">
            <td colspan="7" class="px-6 py-8 text-center text-gray-500">
              暂无面试记录，点击"开始新面试"创建
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
const { $api } = useNuxtApp()
const interviews = ref([])
const loading = ref(false)

const getStatusClass = (status) => {
  const classes = {
    pending: 'bg-yellow-100 text-yellow-800',
    in_progress: 'bg-blue-100 text-blue-800',
    completed: 'bg-green-100 text-green-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getStatusText = (status) => {
  const texts = {
    pending: '待开始',
    in_progress: '进行中',
    completed: '已完成'
  }
  return texts[status] || status
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}

const fetchInterviews = async () => {
  loading.value = true
  try {
    const res = await $api.get('/interviews')
    if (res.data.code === 0) {
      interviews.value = res.data.data.items || []
    }
  } catch (error) {
    console.error('获取面试列表失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchInterviews)
</script>