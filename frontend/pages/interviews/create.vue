<template>
  <div style="background: white; border-radius: 12px; box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05); padding: 24px;">
    <!-- 头部 -->
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
      <h1 style="font-size: 24px; font-weight: bold; color: #1f2937;">添加面试</h1>
      <button @click="cancel" style="background-color: #6b7280; color: white; padding: 8px 16px; border-radius: 8px; border: none; cursor: pointer;">取消</button>
    </div>

    <div style="max-width: 600px; margin: 0 auto;">
      <div style="margin-bottom: 24px;">
        <label style="display: block; font-size: 14px; font-weight: 500; color: #374151; margin-bottom: 8px;">选择岗位 *</label>
        <select v-model="selectedJobId" style="width: 100%; padding: 10px 12px; border: 1px solid #d1d5db; border-radius: 8px; font-size: 14px;">
          <option value="">请选择岗位</option>
          <option v-for="job in jobs" :key="job.id" :value="job.id">{{ job.title }}</option>
        </select>
      </div>

      <div style="margin-bottom: 32px;">
        <label style="display: block; font-size: 14px; font-weight: 500; color: #374151; margin-bottom: 8px;">选择候选人 *</label>
        <select v-model="selectedCandidateId" style="width: 100%; padding: 10px 12px; border: 1px solid #d1d5db; border-radius: 8px; font-size: 14px;">
          <option value="">请选择候选人</option>
          <option v-for="candidate in candidates" :key="candidate.id" :value="candidate.id">{{ candidate.name }}</option>
        </select>
      </div>

      <div style="display: flex; justify-content: flex-end; gap: 16px;">
        <button @click="cancel" style="padding: 10px 20px; border: 1px solid #d1d5db; border-radius: 8px; background: white; cursor: pointer;">取消</button>
        <button @click="createInterview" :disabled="!selectedJobId || !selectedCandidateId" style="background-color: #2563eb; color: white; padding: 10px 20px; border-radius: 8px; border: none; cursor: pointer; font-weight: 500;" :style="{ opacity: (!selectedJobId || !selectedCandidateId) ? 0.5 : 1 }">
          开始面试
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const { $api } = useNuxtApp()

const jobs = ref([])
const candidates = ref([])
const selectedJobId = ref('')
const selectedCandidateId = ref('')

const fetchJobs = async () => {
  try {
    const res = await $api.get('/jobs')
    if (res.data.code === 0) jobs.value = res.data.data.items || []
  } catch (err) {
    console.warn('获取岗位失败，使用模拟数据', err)
    // 模拟数据（可选）
    jobs.value = [{ id: 1, title: '前端开发工程师' }, { id: 2, title: '后端开发工程师' }]
  }
}

const fetchCandidates = async () => {
  try {
    const res = await $api.get('/candidates')
    if (res.data.code === 0) candidates.value = res.data.data.items || []
  } catch (err) {
    console.warn('获取候选人失败，使用模拟数据', err)
    candidates.value = [{ id: 1, name: '张三' }, { id: 2, name: '李四' }]
  }
}

const createInterview = async () => {
  if (!selectedJobId.value || !selectedCandidateId.value) {
    alert('请选择岗位和候选人')
    return
  }
  try {
    const res = await $api.post('/interviews', {
      job_id: Number(selectedJobId.value),
      candidate_id: Number(selectedCandidateId.value)
    })
    if (res.data.code === 0) {
      router.push(`/interviews/${res.data.data.id}`)
    } else {
      alert('创建失败：' + (res.data.message || '未知错误'))
    }
  } catch (err) {
    console.error('创建失败', err)
    alert('创建失败，请确保后端服务已启动')
  }
}

const cancel = () => {
  router.push('/interviews')
}

onMounted(() => {
  fetchJobs()
  fetchCandidates()
})
</script>