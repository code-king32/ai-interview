<template>
  <div style="background: white; border-radius: 12px; box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05); padding: 24px;">
    <!-- 头部 -->
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
      <h1 style="font-size: 24px; font-weight: bold; color: #1f2937;">面试记录</h1>
      <NuxtLink to="/interviews/create">
        <button style="background-color: #2563eb; color: white; padding: 8px 16px; border-radius: 8px; display: flex; align-items: center; gap: 8px; border: none; cursor: pointer; font-size: 16px;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 4v16m8-8H4" />
          </svg>
          添加面试
        </button>
      </NuxtLink>
    </div>

    <!-- 表格 -->
    <div style="overflow-x: auto;">
      <table style="width: 100%; border-collapse: collapse;">
        <thead style="background-color: #f9fafb;">
          <tr>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">ID</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">岗位名称</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">候选人</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">状态</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">综合评分</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">创建时间</th>
            <th style="padding: 16px 24px; text-align: left; font-size: 12px; font-weight: 500; color: #6b7280;">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="interview in interviews" :key="interview.id" style="border-bottom: 1px solid #e5e7eb;">
            <td style="padding: 20px 24px; white-space: nowrap; font-size: 14px; color: #111827;">{{ interview.id }}</td>
            <td style="padding: 20px 24px; white-space: nowrap; font-size: 14px; font-weight: 500; color: #111827;">{{ interview.job_title }}</td>
            <td style="padding: 20px 24px; white-space: nowrap; font-size: 14px; color: #6b7280;">{{ interview.candidate_name }}</td>
            <td style="padding: 20px 24px; white-space: nowrap;">
              <span :style="getStatusStyle(interview.status)" style="padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 500;">
                {{ getStatusText(interview.status) }}
              </span>
            </td>
            <td style="padding: 20px 24px; white-space: nowrap; font-size: 14px; font-weight: 500;">
              <span v-if="interview.status === 'completed' && interview.overall_score">{{ interview.overall_score }}/10</span>
              <span v-else>-</span>
            </td>
            <td style="padding: 20px 24px; white-space: nowrap; font-size: 14px; color: #6b7280;">{{ interview.created_at }}</td>
            <td style="padding: 20px 24px; white-space: nowrap; font-size: 14px;">
              <!-- 已完成 → 查看报告 -->
              <NuxtLink
                v-if="interview.status === 'completed'"
                :to="`/reports/${interview.id}`"
                style="color: #10b981; text-decoration: none;"
              >
                查看报告
              </NuxtLink>
              <!-- 进行中 → 继续面试 -->
              <NuxtLink
                v-else-if="interview.status === 'in_progress'"
                :to="`/interviews/${interview.id}`"
                style="color: #2563eb; text-decoration: none;"
              >
                继续面试
              </NuxtLink>
              <!-- 待开始 → 开始面试 -->
              <NuxtLink
                v-else-if="interview.status === 'pending'"
                :to="`/interviews/${interview.id}`"
                style="color: #2563eb; text-decoration: none;"
              >
                开始面试
              </NuxtLink>
              <!-- 其他状态默认显示进入（兜底） -->
              <NuxtLink v-else :to="`/interviews/${interview.id}`" style="color: #2563eb; text-decoration: none;">进入</NuxtLink>
            </td>
           </tr>
          <tr v-if="interviews.length === 0">
            <td colspan="7" style="padding: 32px; text-align: center; color: #6b7280;">暂无面试记录，点击“添加面试”创建</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 模拟数据（可根据需要调整）
const interviews = ref([
  {
    id: 1,
    job_title: '前端开发工程师',
    candidate_name: '张三',
    status: 'completed',
    overall_score: 8.5,
    created_at: '2025-03-15'
  },
  {
    id: 2,
    job_title: '后端开发工程师',
    candidate_name: '李四',
    status: 'in_progress',
    overall_score: null,
    created_at: '2025-03-16'
  },
  {
    id: 3,
    job_title: '全栈工程师',
    candidate_name: '王五',
    status: 'pending',
    overall_score: null,
    created_at: '2025-03-17'
  }
])

const getStatusStyle = (status) => {
  switch (status) {
    case 'completed': return { backgroundColor: '#d1fae5', color: '#065f46' }
    case 'in_progress': return { backgroundColor: '#dbeafe', color: '#1e40af' }
    case 'pending': return { backgroundColor: '#fed7aa', color: '#9a3412' }
    default: return { backgroundColor: '#f3f4f6', color: '#374151' }
  }
}

const getStatusText = (status) => {
  switch (status) {
    case 'completed': return '已完成'
    case 'in_progress': return '进行中'
    case 'pending': return '待开始'
    default: return status
  }
}
</script>