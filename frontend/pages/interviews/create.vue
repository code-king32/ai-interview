<template>
  <div style="background: white; border-radius: 12px; box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05); padding: 24px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
      <h1 style="font-size: 24px; font-weight: bold; color: #1f2937;">开始模拟面试</h1>
      <button @click="cancel" style="background-color: #6b7280; color: white; padding: 8px 16px; border-radius: 8px; border: none; cursor: pointer;">取消</button>
    </div>

    <div style="max-width: 600px; margin: 0 auto;">
      <div style="margin-bottom: 24px;">
        <label style="display: block; font-size: 14px; font-weight: 500; color: #374151; margin-bottom: 8px;">选择目标岗位 *</label>
        <select v-model="selectedJobId" style="width: 100%; padding: 10px 12px; border: 1px solid #d1d5db; border-radius: 8px; font-size: 14px;">
          <option value="">请选择你要模拟的岗位</option>
          <option v-for="job in jobs" :key="job.id" :value="job.id">{{ job.title }}</option>
        </select>
        <div v-if="selectedJob" style="margin-top: 10px; padding: 10px 14px; background: #F5F5F7; border-radius: 8px; font-size: 13px; color: #6B7280; line-height: 1.6;">
          <div v-if="selectedJob.requirements"><strong>技能要求：</strong>{{ selectedJob.requirements.slice(0,200) }}</div>
        </div>
      </div>

      <div style="margin-bottom: 24px;">
        <label style="display: block; font-size: 14px; font-weight: 500; color: #374151; margin-bottom: 8px;">上传简历（选填，PDF/Word/TXT）</label>
        <input ref="fileInput" type="file" accept=".pdf,.docx,.doc,.txt" @change="onFileChange" style="width: 100%; padding: 10px 12px; border: 1px solid #d1d5db; border-radius: 8px; font-size: 14px;" />
        <p v-if="selectedFileName" style="font-size:12px;color:#10B981;margin-top:4px">已选择: {{ selectedFileName }}</p>
      </div>

      <div style="margin-bottom: 32px;">
        <label style="display: block; font-size: 14px; font-weight: 500; color: #374151; margin-bottom: 8px;">你的姓名</label>
        <input v-model="candidateName" placeholder="你的姓名" style="width: 100%; padding: 10px 12px; border: 1px solid #d1d5db; border-radius: 8px; font-size: 14px;" />
      </div>

      <div style="display: flex; justify-content: flex-end; gap: 16px;">
        <button @click="cancel" style="padding: 10px 20px; border: 1px solid #d1d5db; border-radius: 8px; background: white; cursor: pointer;">取消</button>
        <button @click="startInterview" :disabled="!selectedJobId || !candidateName.trim() || creating" style="background-color: #2563eb; color: white; padding: 10px 20px; border-radius: 8px; border: none; cursor: pointer; font-weight: 500;" :style="{ opacity: (!selectedJobId || !candidateName.trim()) ? 0.5 : 1 }">
          {{ creating ? '创建中...' : '🚀 开始模拟面试' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const router = useRouter()
const { $api } = useNuxtApp()

const jobs = ref<any[]>([])
const selectedJobId = ref('')
const selectedFileName = ref('')
const selectedFile = ref<File | null>(null)
const candidateName = ref('')
const creating = ref(false)
const fileInput = ref<HTMLInputElement>()

const selectedJob = computed(() => jobs.value.find(j => j.id === Number(selectedJobId.value)))

const fetchJobs = async () => {
  try { const data = (await $api.get('/jobs')).data; jobs.value = Array.isArray(data) ? data : [] }
  catch (err) { alert('无法连接后端服务') }
}

const onFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) { selectedFile.value = file; selectedFileName.value = file.name }
  else { selectedFile.value = null; selectedFileName.value = '' }
}

const startInterview = async () => {
  creating.value = true
  try {
    // 自动创建候选人
    const cRes = await $api.post('/candidates', { name: candidateName.value.trim() })
    const candidateId = cRes.data.id

    // 上传简历
    if (selectedFile.value) {
      const fd = new FormData(); fd.append('file', selectedFile.value)
      await $api.post(`/candidates/upload-resume/${candidateId}`, fd)
    }

    // 创建面试
    const ivRes = await $api.post('/interviews', { job_id: Number(selectedJobId.value), candidate_id: candidateId })
    router.push(`/interviews/${ivRes.data.id}`)
  } catch (e: any) { alert('创建失败：' + (e?.response?.data?.detail || '请重试')) }
  finally { creating.value = false }
}

const cancel = () => router.push('/interviews')

onMounted(fetchJobs)
</script>
