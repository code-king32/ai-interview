<template>
  <div style="background: white; border-radius: 12px; box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05); padding: 24px;">
    <!-- 头部：标题 + 右侧按钮 -->
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
      <h1 style="font-size: 24px; font-weight: bold; color: #1f2937;">候选人管理</h1>
      <button @click="openCreateModal" style="background-color: #2563eb; color: white; padding: 8px 16px; border-radius: 8px; display: flex; align-items: center; gap: 8px; border: none; cursor: pointer; font-size: 16px;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 4v16m8-8H4" />
        </svg>
        添加候选人
      </button>
    </div>

    <!-- 表格 -->
    <div style="overflow-x: auto;">
      <table style="width: 100%; border-collapse: collapse;">
        <thead style="background-color: #f9fafb;">
          <tr>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">ID</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">姓名</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">邮箱</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">电话</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">简历摘要</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">创建时间</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="candidate in candidates" :key="candidate.id" style="border-bottom: 1px solid #e5e7eb;">
            <td style="padding: 20px 24px; white-space: nowrap; font-size: 14px; color: #111827;">{{ candidate.id }}</td>
            <td style="padding: 20px 24px; white-space: nowrap; font-size: 14px; font-weight: 500; color: #111827;">{{ candidate.name }}</td>
            <td style="padding: 20px 24px; white-space: nowrap; font-size: 14px; color: #6b7280;">{{ candidate.email || '-' }}</td>
            <td style="padding: 20px 24px; white-space: nowrap; font-size: 14px; color: #6b7280;">{{ candidate.phone || '-' }}</td>
            <td style="padding: 20px 24px; font-size: 14px; color: #6b7280; max-width: 250px; overflow: hidden; text-overflow: ellipsis;">{{ candidate.resume_text || '-' }}</td>
            <td style="padding: 20px 24px; white-space: nowrap; font-size: 14px; color: #6b7280;">{{ candidate.created_at }}</td>
            <td style="padding: 20px 24px; white-space: nowrap; font-size: 14px;">
              <button @click="openEditModal(candidate)" style="color: #2563eb; margin-right: 12px; background: none; border: none; cursor: pointer;">编辑</button>
              <button @click="deleteCandidate(candidate.id)" style="color: #dc2626; background: none; border: none; cursor: pointer;">删除</button>
            </td>
          </tr>
          <tr v-if="candidates.length === 0">
            <td colspan="7" style="padding: 32px; text-align: center; color: #6b7280;">暂无候选人，点击“添加候选人”创建</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 创建/编辑弹窗 -->
    <div v-if="modalVisible" style="position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 50;">
      <div style="background: white; border-radius: 12px; width: 100%; max-width: 500px; padding: 24px;">
        <h2 style="font-size: 20px; font-weight: bold; margin-bottom: 16px;">{{ isEdit ? '编辑候选人' : '添加候选人' }}</h2>
        <div style="display: flex; flex-direction: column; gap: 16px;">
          <input v-model="form.name" placeholder="姓名 *" style="border: 1px solid #d1d5db; border-radius: 8px; padding: 8px 12px;" />
          <input v-model="form.email" placeholder="邮箱" style="border: 1px solid #d1d5db; border-radius: 8px; padding: 8px 12px;" />
          <input v-model="form.phone" placeholder="电话" style="border: 1px solid #d1d5db; border-radius: 8px; padding: 8px 12px;" />
          <textarea v-model="form.resume_text" rows="3" placeholder="简历摘要" style="border: 1px solid #d1d5db; border-radius: 8px; padding: 8px 12px;"></textarea>
          <div>
            <label style="display:block;font-size:14px;font-weight:500;color:#374151;margin-bottom:6px">上传简历（PDF / Word / TXT）</label>
            <input ref="fileInput" type="file" accept=".pdf,.docx,.doc,.txt" @change="handleFileChange"
              style="border: 1px solid #d1d5db; border-radius: 8px; padding: 8px 12px; width: 100%;" />
            <p v-if="selectedFile" style="font-size:12px;color:#10B981;margin-top:4px">已选择: {{ selectedFile.name }}</p>
            <p v-if="form.resume_text" style="font-size:12px;color:#6B7280;margin-top:4px">已解析简历文本 ({{ form.resume_text.length }}字)</p>
          </div>
        </div>
        <div style="display: flex; justify-content: flex-end; gap: 12px; margin-top: 24px;">
          <button @click="closeModal" style="padding: 8px 16px; border: 1px solid #d1d5db; border-radius: 8px;">取消</button>
          <button @click="submitForm" :disabled="uploading" style="background-color: #2563eb; color: white; padding: 8px 16px; border-radius: 8px; border: none; cursor:pointer" :style="{opacity: uploading?0.6:1}">{{ uploading ? '上传中…' : '保存' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { $api } = useNuxtApp()

const candidates = ref<any[]>([])
const modalVisible = ref(false)
const isEdit = ref(false)
const form = ref<any>({ id: null, name: '', email: '', phone: '', resume_text: '' })
const selectedFile = ref<File | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)
const uploading = ref(false)

const fetchCandidates = async () => {
  try {
    const res = await $api.get('/candidates')
    candidates.value = res.data.data?.items || res.data.data || []
  } catch (e) { console.error(e) }
}

const openCreateModal = () => {
  isEdit.value = false
  form.value = { id: null, name: '', email: '', phone: '', resume_text: '' }
  selectedFile.value = null
  modalVisible.value = true
}

const openEditModal = (candidate: any) => {
  isEdit.value = true
  form.value = { ...candidate }
  selectedFile.value = null
  modalVisible.value = true
}

const closeModal = () => { modalVisible.value = false }

const handleFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  selectedFile.value = target.files?.[0] || null
}

const submitForm = async () => {
  if (!form.value.name.trim()) return alert('请填写姓名')
  uploading.value = true
  try {
    let candidateId = form.value.id
    if (isEdit.value) {
      await $api.put(`/candidates/${candidateId}`, { name: form.value.name, email: form.value.email, phone: form.value.phone })
    } else {
      const body: any = { name: form.value.name }
      if (form.value.email) body.email = form.value.email
      if (form.value.phone) body.phone = form.value.phone
      const res = await $api.post('/candidates', body)
      candidateId = res.data.data.id
    }
    // 上传简历文件
    if (selectedFile.value && candidateId) {
      const fd = new FormData()
      fd.append('file', selectedFile.value)
      await $api.post(`/candidates/upload-resume/${candidateId}`, fd)
    }
    closeModal()
    await fetchCandidates()
  } catch (e) { alert('操作失败') }
  finally { uploading.value = false }
}

const deleteCandidate = async (id: number) => {
  if (!confirm('确定删除该候选人吗？')) return
  try { await $api.delete(`/candidates/${id}`); await fetchCandidates() }
  catch (e) { alert('删除失败') }
}

onMounted(fetchCandidates)
</script>