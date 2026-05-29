<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <div class="bg-white rounded-lg shadow p-6">
      <h1 class="text-2xl font-bold mb-6">开始新面试</h1>
      
      <form @submit.prevent="createInterview" class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">选择岗位 *</label>
          <select v-model="selectedJobId" class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500" required>
            <option value="">请选择岗位</option>
            <option v-for="job in jobs" :key="job.id" :value="job.id">
              {{ job.title }}
            </option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">选择候选人 *</label>
          <select v-model="selectedCandidateId" class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500" required>
            <option value="">请选择候选人</option>
            <option v-for="candidate in candidates" :key="candidate.id" :value="candidate.id">
              {{ candidate.name }} - {{ candidate.email || '无邮箱' }}
            </option>
          </select>
        </div>
        
        <div class="flex gap-3 pt-4">
          <button type="button" @click="$router.back()" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
            取消
          </button>
          <button type="submit" :disabled="!selectedJobId || !selectedCandidateId" 
                  class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50">
            开始面试
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
const router = useRouter()
const { $api } = useNuxtApp()

const jobs = ref([])
const candidates = ref([])
const selectedJobId = ref('')
const selectedCandidateId = ref('')

const fetchJobs = async () => {
  const res = await $api.get('/jobs')
  if (res.data.code === 0) {
    jobs.value = res.data.data.items || []
  }
}

const fetchCandidates = async () => {
  const res = await $api.get('/candidates')
  if (res.data.code === 0) {
    candidates.value = res.data.data.items || []
  }
}

const createInterview = async () => {
  try {
    const res = await $api.post('/interviews', {
      job_id: Number(selectedJobId.value),
      candidate_id: Number(selectedCandidateId.value)
    })
    if (res.data.code === 0) {
      router.push(`/interviews/${res.data.data.id}`)
    }
  } catch (error) {
    console.error('创建失败:', error)
    alert('创建失败，请确保后端服务已启动')
  }
}

onMounted(() => {
  fetchJobs()
  fetchCandidates()
})
</script>