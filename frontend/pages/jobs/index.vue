<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900">岗位管理</h1>
      <button @click="openModal" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
        创建岗位
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center py-8 text-gray-500">
      加载中...
    </div>

    <!-- 岗位列表 -->
    <div v-else class="bg-white rounded-lg shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">岗位名称</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">岗位描述</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">创建时间</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="job in jobs" :key="job.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ job.id }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ job.title }}</td>
            <td class="px-6 py-4 text-sm text-gray-500 max-w-md truncate">{{ job.description || '-' }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(job.created_at) }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <button @click="confirmDelete(job)" class="text-red-600 hover:text-red-900">删除</button>
            </td>
          </tr>
          <tr v-if="jobs.length === 0">
            <td colspan="5" class="px-6 py-8 text-center text-gray-500">
              暂无岗位，点击"创建岗位"添加
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 创建岗位弹窗 -->
    <div v-if="modalOpen" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <!-- 背景遮罩 -->
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="closeModal"></div>

        <!-- 弹窗内容 -->
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mt-3 text-center sm:mt-0 sm:text-left w-full">
                <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                  创建岗位
                </h3>
                <div class="mt-4 space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">岗位名称 *</label>
                    <input
                      v-model="form.title"
                      type="text"
                      class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="请输入岗位名称"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">岗位描述</label>
                    <textarea
                      v-model="form.description"
                      rows="3"
                      class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="请输入岗位描述"
                    ></textarea>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">技术要求</label>
                    <textarea
                      v-model="form.requirements"
                      rows="3"
                      class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="请输入技术要求"
                    ></textarea>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              @click="createJob"
              :disabled="!form.title"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto text-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              创建
            </button>
            <button
              @click="closeModal"
              type="button"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:ml-3 sm:w-auto text-sm"
            >
              取消
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const { $api } = useNuxtApp()

// 状态
const jobs = ref([])
const loading = ref(false)
const modalOpen = ref(false)
const form = ref({
  title: '',
  description: '',
  requirements: ''
})

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

// 打开弹窗
const openModal = () => {
  form.value = { title: '', description: '', requirements: '' }
  modalOpen.value = true
}

// 关闭弹窗
const closeModal = () => {
  modalOpen.value = false
}

// 获取岗位列表
const fetchJobs = async () => {
  loading.value = true
  try {
    const res = await $api.get('/jobs')
    if (res.data.code === 0) {
      jobs.value = res.data.data.items || []
    }
  } catch (error) {
    console.error('获取岗位失败:', error)
  } finally {
    loading.value = false
  }
}

// 创建岗位
const createJob = async () => {
  if (!form.value.title) {
    alert('请填写岗位名称')
    return
  }
  
  try {
    const res = await $api.post('/jobs', {
      title: form.value.title,
      description: form.value.description,
      requirements: form.value.requirements
    })
    if (res.data.code === 0) {
      closeModal()
      await fetchJobs()
      alert('创建成功')
    }
  } catch (error) {
    console.error('创建失败:', error)
    alert('创建失败，请确保后端服务已启动')
  }
}

// 确认删除
const confirmDelete = (job) => {
  if (confirm(`确定要删除岗位"${job.title}"吗？`)) {
    deleteJob(job.id)
  }
}

// 删除岗位
const deleteJob = async (id) => {
  try {
    const res = await $api.delete(`/jobs/${id}`)
    if (res.data.code === 0) {
      await fetchJobs()
      alert('删除成功')
    }
  } catch (error) {
    console.error('删除失败:', error)
    alert('删除失败')
  }
}

// 初始化
onMounted(() => {
  fetchJobs()
})
</script>