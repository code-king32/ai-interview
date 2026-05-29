<template>
  <div style="background: white; border-radius: 12px; box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05); padding: 24px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
      <h1 style="font-size: 24px; font-weight: bold;">面试报告</h1>
      <button @click="goBack" style="background-color: #6b7280; color: white; padding: 8px 16px; border-radius: 8px;">返回面试列表</button>
    </div>

    <div v-if="loading" style="text-align: center; padding: 60px;">加载中...</div>

    <div v-else-if="report">
      <!-- 基本信息卡片 -->
      <div style="background: #f9fafb; border-radius: 12px; padding: 20px; margin-bottom: 24px; display: flex; flex-wrap: wrap; gap: 24px;">
        <div><span style="color: #6b7280;">候选人：</span><strong>{{ report.candidate?.name || '-' }}</strong></div>
        <div><span style="color: #6b7280;">岗位：</span><strong>{{ report.job?.title || '-' }}</strong></div>
        <div><span style="color: #6b7280;">面试时间：</span><strong>{{ formatDate(report.generated_at) }}</strong></div>
        <div><span style="color: #6b7280;">总题数：</span><strong>{{ report.total_questions || 0 }}</strong></div>
      </div>

      <!-- 总体评分 -->
      <h2 style="font-size: 18px; font-weight: 600; margin: 24px 0 16px;">总体评分</h2>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px,1fr)); gap: 16px; margin-bottom: 24px;">
        <div style="background:#eff6ff; padding:16px; border-radius:12px; text-align:center">
          <div>技术能力</div>
          <div style="font-size:28px; font-weight:bold;">{{ report.overall_score?.technical || 0 }}</div>
        </div>
        <div style="background:#f0fdf4; padding:16px; border-radius:12px; text-align:center">
          <div>沟通表达</div>
          <div style="font-size:28px; font-weight:bold;">{{ report.overall_score?.communication || 0 }}</div>
        </div>
        <div style="background:#fef3c7; padding:16px; border-radius:12px; text-align:center">
          <div>学习潜力</div>
          <div style="font-size:28px; font-weight:bold;">{{ report.overall_score?.learning || 0 }}</div>
        </div>
        <div style="background:#fce7f3; padding:16px; border-radius:12px; text-align:center">
          <div>岗位匹配</div>
          <div style="font-size:28px; font-weight:bold;">{{ report.overall_score?.match || 0 }}</div>
        </div>
      </div>
      <div style="background:#f3f4f6; padding:16px; border-radius:12px; margin-bottom:24px;">
        <div><strong>录用建议：</strong>{{ report.overall_score?.recommendation || '待评估' }}</div>
        <div style="margin-top:8px;">{{ report.overall_score?.summary || '' }}</div>
      </div>

      <!-- 问答详情 -->
      <h2 style="font-size: 18px; font-weight: 600; margin: 24px 0 16px;">问答详情</h2>
      <div style="overflow-x: auto;">
        <table style="width:100%; border-collapse:collapse;">
          <thead style="background:#f9fafb;">
            <tr><th style="padding:12px;">#</th><th style="padding:12px;">问题</th><th style="padding:12px;">回答摘要</th><th style="padding:12px;">评分</th><th style="padding:12px;">评价</th></tr>
          </thead>
          <tbody>
            <tr v-for="d in report.question_details" :key="d.question_number" style="border-bottom:1px solid #e5e7eb;">
              <td style="padding:12px;">{{ d.question_number }}</td>
              <td style="padding:12px;">{{ d.question }}</td>
              <td style="padding:12px;">{{ d.answer || '-' }}</td>
              <td style="padding:12px;">{{ d.scores?.correctness || 0 }}/10</td>
              <td style="padding:12px;">{{ d.comment || '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-else style="text-align:center; padding:60px; color:#ef4444;">报告加载失败，请稍后重试。</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const { $api } = useNuxtApp()

const report = ref(null)
const loading = ref(true)

const formatDate = (dateStr) => dateStr ? new Date(dateStr).toLocaleString() : '-'
const goBack = () => router.push('/interviews')

// 模拟数据（后端就绪后删除此部分）
const getMockReport = (id) => ({
  candidate: { name: `候选人${id}` },
  job: { title: '示例岗位' },
  generated_at: new Date().toISOString(),
  total_questions: 5,
  overall_score: {
    technical: 8.2, communication: 7.5, learning: 8.0, match: 7.8,
    recommendation: '推荐', summary: '候选人表现良好，推荐录用。'
  },
  question_details: [
    { question_number: 1, question: '问题1', answer: '回答1', scores: { correctness: 8 }, comment: '不错' },
    { question_number: 2, question: '问题2', answer: '回答2', scores: { correctness: 7 }, comment: '中等' }
  ]
})

onMounted(async () => {
  loading.value = true
  try {
    const res = await $api.get(`/reports/${route.params.id}`)
    if (res.data.code === 0) report.value = res.data.data
    else report.value = getMockReport(route.params.id) // 后端未返回时使用模拟
  } catch (err) {
    console.warn(err)
    report.value = getMockReport(route.params.id) // 请求失败使用模拟
  } finally {
    loading.value = false
  }
})
</script>