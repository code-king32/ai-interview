<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900">候选人管理</h1>
      <button @click="openModal" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg">
        + 添加候选人
      </button>
    </div>

    <div v-if="loading" class="text-center py-8 text-gray-500">
      加载中...
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="candidate in candidates" :key="candidate.id" class="bg-white rounded-lg shadow p-6">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h3 class="text-lg font-semibold">{{ candidate.name }}</h3>
            <p class="text-gray-500 text-sm">{{ candidate.email || '无邮箱' }}</p>
          </div>
          <button @click="deleteCandidate(candidate.id)" class="text-red-500">删除</button>
        </div>
        <div class="text-sm text-gray-600">{{ candidate.resume_text || '无简历' }}</div>
        <div class="text-xs text-gray-400 mt-4">{{ new Date(candidate.created_at).toLocaleDateString() }}</div>
      </div>
      
      <div v-if="candidates.length === 0" class="col-span-full text-center py-12 bg-white rounded-lg">
        暂无候选人
      </div>
    </div>

    <!-- 添加弹窗 -->
    <div v-if="modalOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">添加候选人</h2>
        <div class="space-y-3">
          <input v-model="form.name" placeholder="姓名" class="w-full border rounded px-3 py-2">
          <input v-model="form.email" placeholder="邮箱" class="w-full border rounded px-3 py-2">
          <input v-model="form.phone" placeholder="电话" class="w-full border rounded px-3 py-2">
          <input type="file" @change="handleFileUpload" accept=".pdf,.docx,.doc,.txt" class="w-full border rounded px-3 py-2">
        </div>
        <div class="flex justify-end gap-3 mt-6">
          <button @click="closeModal" class="px-4 py-2 border rounded">取消</button>
          <button @click="createCandidate" class="px-4 py-2 bg-green-600 text-white rounded">创建</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const { $api } = useNuxtApp()
const candidates = ref([])
const loading = ref(false)
const modalOpen = ref(false)
const form = ref({ name: '', email: '', phone: '', resume: null })

const fetchCandidates = async () => {
  loading.value = true
  try {
    const res = await $api.get('/candidates')
    if (res.data.code === 0) {
      candidates.value = res.data.data.items || []
    }
  } catch (error) {
    console.error('获取失败:', error)
  } finally {
    loading.value = false
  }
}

const openModal = () => {
  form.value = { name: '', email: '', phone: '', resume: null }
  modalOpen.value = true
}

const closeModal = () => {
  modalOpen.value = false
}

const handleFileUpload = (e) => {
  form.value.resume = e.target.files[0]
}

const createCandidate = async () => {
  if (!form.value.name) {
    alert('请填写姓名')
    return
  }
  const fd = new FormData()
  fd.append('name', form.value.name)
  if (form.value.email) fd.append('email', form.value.email)
  if (form.value.phone) fd.append('phone', form.value.phone)
  if (form.value.resume) fd.append('resume', form.value.resume)
  
  try {
    await $api.post('/candidates', fd)
    closeModal()
    fetchCandidates()
    alert('创建成功')
  } catch (error) {
    alert('创建失败')
  }
}

const deleteCandidate = async (id) => {
  if (confirm('确定删除？')) {
    await $api.delete(`/candidates/${id}`)
    fetchCandidates()
  }
}

onMounted(fetchCandidates)
</script>