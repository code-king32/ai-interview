<template>
  <div style="background: white; border-radius: 12px; box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05); padding: 24px;">
    <!-- 头部：标题 + 右侧按钮（使用 flex 布局） -->
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
      <h1 style="font-size: 24px; font-weight: bold; color: #1f2937;">目标岗位</h1>
      <button @click="openCreateModal" style="background-color: #2563eb; color: white; padding: 8px 16px; border-radius: 8px; display: flex; align-items: center; gap: 8px; border: none; cursor: pointer; font-size: 16px;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 4v16m8-8H4"/></svg>
        添加目标岗位
      </button>
    </div>

    <!-- 表格：使用内联样式保证行间距 -->
    <div style="overflow-x: auto;">
      <table style="width: 100%; border-collapse: collapse;">
        <thead style="background-color: #f9fafb;">
          <tr>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">ID</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">目标岗位</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">岗位描述</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">技能要求</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">创建时间</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="job in jobs" :key="job.id" style="border-bottom: 1px solid #e5e7eb;">
            <td style="padding: 20px 24px; white-space: nowrap; font-size: 14px; color: #111827;">{{ job.id }}</td>
            <td style="padding: 20px 24px; white-space: nowrap; font-size: 14px; font-weight: 500; color: #111827;">{{ job.title }}</td>
            <td style="padding: 20px 24px; font-size: 14px; color: #6b7280; max-width: 200px; overflow: hidden; text-overflow: ellipsis;">{{ job.description || '-' }}</td>
            <td style="padding: 20px 24px; font-size: 14px; color: #6b7280; max-width: 200px; overflow: hidden; text-overflow: ellipsis;">{{ job.requirements || '-' }}</td>
            <td style="padding: 20px 24px; white-space: nowrap; font-size: 14px; color: #6b7280;">{{ job.created_at }}</td>
            <td style="padding: 20px 24px; white-space: nowrap; font-size: 14px;">
              <button @click="openEditModal(job)" style="color: #2563eb; margin-right: 12px; background: none; border: none; cursor: pointer;">编辑</button>
              <button @click="deleteJob(job.id)" style="color: #dc2626; background: none; border: none; cursor: pointer;">删除</button>
            </td>
          </tr>
          <tr v-if="jobs.length === 0">
            <td colspan="6" style="padding: 32px; text-align: center; color: #6b7280;">还没有目标岗位，添加一个开始针对性练习</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 弹窗（代码未变，略） -->
    <div v-if="modalVisible" style="position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 50;">
      <div style="background: white; border-radius: 12px; width: 100%; max-width: 500px; padding: 24px;">
        <h2 style="font-size: 20px; font-weight: bold; margin-bottom: 16px;">{{ isEdit ? '编辑目标' : '添加岗位' }}</h2>
        <div style="display: flex; flex-direction: column; gap: 16px;">
          <input v-model="form.title" placeholder="目标岗位名" style="border: 1px solid #d1d5db; border-radius: 8px; padding: 8px 12px;" />
          <textarea v-model="form.description" rows="3" placeholder="岗位描述" style="border: 1px solid #d1d5db; border-radius: 8px; padding: 8px 12px;"></textarea>
          <textarea v-model="form.requirements" rows="3" placeholder="技术要求" style="border: 1px solid #d1d5db; border-radius: 8px; padding: 8px 12px;"></textarea>
        </div>
        <div style="display: flex; justify-content: flex-end; gap: 12px; margin-top: 24px;">
          <button @click="closeModal" style="padding: 8px 16px; border: 1px solid #d1d5db; border-radius: 8px;">取消</button>
          <button @click="submitForm" style="background-color: #2563eb; color: white; padding: 8px 16px; border-radius: 8px; border: none;">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { $api } = useNuxtApp()

const jobs = ref<any[]>([])
const modalVisible = ref(false)
const isEdit = ref(false)
const form = ref<any>({ id: null, title: '', description: '', requirements: '' })

const fetchJobs = async () => {
  try {
    const res = await $api.get('/jobs')
    jobs.value = res.data.data?.items || res.data.data || []
  } catch (e) { console.error(e) }
}

const openCreateModal = () => {
  isEdit.value = false
  form.value = { id: null, title: '', description: '', requirements: '' }
  modalVisible.value = true
}
const openEditModal = (job: any) => {
  isEdit.value = true
  form.value = { ...job }
  modalVisible.value = true
}
const closeModal = () => { modalVisible.value = false }

const submitForm = async () => {
  if (!form.value.title.trim()) return alert('请填写目标岗位名')
  try {
    if (isEdit.value) {
      await $api.put(`/jobs/${form.value.id}`, { title: form.value.title, description: form.value.description, requirements: form.value.requirements })
    } else {
      await $api.post('/jobs', { title: form.value.title, description: form.value.description, requirements: form.value.requirements })
    }
    closeModal()
    await fetchJobs()
  } catch (e) { alert('操作失败，请确保后端服务已启动') }
}

const deleteJob = async (id) => {
  if (!confirm('确定删除该目标吗？')) return
  try {
    await $api.delete(`/jobs/${id}`)
    await fetchJobs()
  } catch (e) { alert('删除失败') }
}

onMounted(fetchJobs)
</script>