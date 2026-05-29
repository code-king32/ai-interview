<template>
  <div style="background: white; border-radius: 12px; box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05); padding: 24px;">
    <!-- 头部：标题 + 右侧按钮（使用 flex 布局） -->
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
      <h1 style="font-size: 24px; font-weight: bold; color: #1f2937;">岗位管理</h1>
      <button @click="openCreateModal" style="background-color: #2563eb; color: white; padding: 8px 16px; border-radius: 8px; display: flex; align-items: center; gap: 8px; border: none; cursor: pointer; font-size: 16px;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 4v16m8-8H4" />
        </svg>
        创建岗位
      </button>
    </div>

    <!-- 表格：使用内联样式保证行间距 -->
    <div style="overflow-x: auto;">
      <table style="width: 100%; border-collapse: collapse;">
        <thead style="background-color: #f9fafb;">
          <tr>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">ID</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">岗位名称</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">岗位描述</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">技术要求</th>
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
            <td colspan="6" style="padding: 32px; text-align: center; color: #6b7280;">暂无数据，点击“创建岗位”添加</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 弹窗（代码未变，略） -->
    <div v-if="modalVisible" style="position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 50;">
      <div style="background: white; border-radius: 12px; width: 100%; max-width: 500px; padding: 24px;">
        <h2 style="font-size: 20px; font-weight: bold; margin-bottom: 16px;">{{ isEdit ? '编辑岗位' : '创建岗位' }}</h2>
        <div style="display: flex; flex-direction: column; gap: 16px;">
          <input v-model="form.title" placeholder="岗位名称" style="border: 1px solid #d1d5db; border-radius: 8px; padding: 8px 12px;" />
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

<script setup>
import { ref } from 'vue'

const jobs = ref([
  { id: 1, title: '前端开发工程师', description: '负责公司前端架构设计，优化性能', requirements: 'Vue3, React, TypeScript, Webpack', created_at: '2025-01-01' },
  { id: 2, title: '后端开发工程师', description: '负责后端API开发，数据库设计', requirements: 'Python, FastAPI, PostgreSQL, Redis', created_at: '2025-01-02' }
])

const modalVisible = ref(false)
const isEdit = ref(false)
const form = ref({ id: null, title: '', description: '', requirements: '' })

const openCreateModal = () => {
  isEdit.value = false
  form.value = { id: null, title: '', description: '', requirements: '' }
  modalVisible.value = true
}
const openEditModal = (job) => {
  isEdit.value = true
  form.value = { ...job }
  modalVisible.value = true
}
const closeModal = () => { modalVisible.value = false }
const submitForm = () => {
  if (!form.value.title.trim()) return alert('请填写岗位名称')
  if (isEdit.value) {
    const index = jobs.value.findIndex(j => j.id === form.value.id)
    if (index !== -1) jobs.value[index] = { ...form.value }
    alert('更新成功')
  } else {
    const newId = jobs.value.length ? Math.max(...jobs.value.map(j => j.id)) + 1 : 1
    jobs.value.push({ id: newId, ...form.value, created_at: new Date().toISOString().slice(0,10) })
    alert('创建成功')
  }
  closeModal()
}
const deleteJob = (id) => {
  if (confirm('确定删除该岗位吗？')) {
    jobs.value = jobs.value.filter(j => j.id !== id)
    alert('删除成功')
  }
}
</script>