<template>
  <div style="background: white; border-radius: 12px; box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05); padding: 24px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
      <h1 style="font-size: 24px; font-weight: bold; color: #1f2937;">面试记录</h1>
      <NuxtLink to="/interviews/create" style="text-decoration:none">
        <button style="background-color: #2563eb; color: white; padding: 8px 16px; border-radius: 8px; display: flex; align-items: center; gap: 8px; border: none; cursor: pointer; font-size: 16px;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 4v16m8-8H4"/></svg>
          添加面试
        </button>
      </NuxtLink>
    </div>

    <div v-if="loading" style="text-align:center;padding:60px;color:#9CA3AF">加载中…</div>

    <div v-else style="overflow-x: auto;">
      <table style="width: 100%; border-collapse: collapse;">
        <thead style="background-color: #f9fafb;">
          <tr>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">ID</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">岗位</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">候选人</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">状态</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">评分</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">时间</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="iv in interviews" :key="iv.id" style="border-bottom: 1px solid #e5e7eb;">
            <td style="padding: 20px 24px; white-space: nowrap; font-size: 14px; color: #111827;">{{ iv.id }}</td>
            <td style="padding: 20px 24px; white-space: nowrap; font-size: 14px;font-weight:500;color:#111827;">{{ iv.job_title || '岗位#'+iv.job_id }}</td>
            <td style="padding: 20px 24px; white-space: nowrap; font-size: 14px; color: #6b7280;">{{ iv.candidate_name || '候选人#'+iv.candidate_id }}</td>
            <td style="padding: 20px 24px; white-space: nowrap;">
              <span :style="statusStyle(normalizeStatus(iv.status))" style="padding:4px 12px;border-radius:20px;font-size:12px;font-weight:500;">
                {{ statusLabel(normalizeStatus(iv.status)) }}
              </span>
            </td>
            <td style="padding: 20px 24px; white-space: nowrap; font-size: 14px; font-weight: 500;">
              <span v-if="iv.overall_score">{{ scoreDisplay(iv.overall_score) }}</span>
              <span v-else style="color:#D1D5DB">-</span>
            </td>
            <td style="padding: 20px 24px; white-space: nowrap; font-size: 14px; color: #6b7280;">{{ fmtDate(iv.created_at) }}</td>
            <td style="padding: 20px 24px; white-space: nowrap; font-size: 14px; display:flex;gap:12px;align-items:center;">
              <NuxtLink v-if="normalizeStatus(iv.status) === 'completed'" :to="`/reports/${iv.id}`" style="color:#10b981;text-decoration:none;font-weight:500">报告</NuxtLink>
              <NuxtLink v-else :to="`/interviews/${iv.id}`" style="color:#2563eb;text-decoration:none;font-weight:500">{{ normalizeStatus(iv.status)==='in_progress'?'继续':'进入' }}</NuxtLink>
              <button @click="deleteInterview(iv)" style="color:#EF4444;background:none;border:none;cursor:pointer;font-size:12px">删除</button>
            </td>
          </tr>
          <tr v-if="interviews.length === 0">
            <td colspan="7" style="padding:32px;text-align:center;color:#6b7280;">暂无面试记录</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
const { $api } = useNuxtApp()
const interviews = ref<any[]>([])
const loading = ref(true)

// Normalize status to lowercase
const normalizeStatus = (s: string) => String(s || '').toLowerCase()

const statusStyle = (s: string) => {
  const m: Record<string,any> = {completed:{backgroundColor:'#d1fae5',color:'#065f46'},in_progress:{backgroundColor:'#dbeafe',color:'#1e40af'},pending:{backgroundColor:'#fed7aa',color:'#9a3412'}}
  return m[s] || {backgroundColor:'#f3f4f6',color:'#374151'}
}
const statusLabel = (s: string) => ({completed:'已完成',in_progress:'进行中',pending:'待开始'} as Record<string,string>)[s] || s
const scoreDisplay = (s: any) => {
  if (!s) return '-'
  if (typeof s === 'object') return ((s.overall || s.technical || 0) as number).toFixed(1)
  return Number(s).toFixed(1)
}
const fmtDate = (d: string) => d ? new Date(d).toLocaleDateString('zh-CN') : '-'

const fetchInterviews = async () => {
  loading.value = true
  try { interviews.value = (await $api.get('/interviews')).data.data || [] }
  catch (e) { console.error(e) }
  finally { loading.value = false }
}

const deleteInterview = async (iv: any) => {
  if (!confirm(`确定删除面试 #${iv.id}（${iv.job_title || iv.job_id} - ${iv.candidate_name || iv.candidate_id}）吗？`)) return
  try { await $api.delete(`/interviews/${iv.id}`); await fetchInterviews() }
  catch (e) { alert('删除失败') }
}

onMounted(fetchInterviews)
</script>
