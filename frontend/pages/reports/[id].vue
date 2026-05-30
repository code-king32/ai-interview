<template>
  <div class="rpt-page">
    <div v-if="loading" class="rpt-loading">
      <div class="spinner"></div>
      <p>加载评估报告中…</p>
    </div>

    <div v-else-if="error" class="rpt-error">
      <div class="rpt-error-icon">😕</div>
      <p>{{ error }}</p>
      <NuxtLink to="/interviews" class="back-link">← 返回面试列表</NuxtLink>
    </div>

    <template v-else-if="report">
      <!-- Header -->
      <div class="rpt-header">
        <h1>面试评估报告</h1>
        <div class="rpt-meta">
          <span>{{ report.candidate?.name || '候选人' }}</span><span class="dot"></span>
          <span>{{ report.job?.title || '岗位' }}</span><span class="dot"></span>
          <span>{{ fmtDate(report.generated_at) }}</span><span class="dot"></span>
          <span>共 {{ report.total_questions || 0 }} 题</span>
        </div>
      </div>

      <!-- Score Hero -->
      <div class="score-hero">
        <div class="ring-wrap" id="ringWrap"></div>
        <div class="score-info">
          <div class="score-badge" :class="badgeClass">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
            {{ ratingLabel }}
          </div>
          <p class="summary-text">{{ report.overall_score?.summary || '暂无综合评语' }}</p>
          <p class="summary-hint">本报告由 AI 智能面试系统自动生成</p>
        </div>
      </div>

      <!-- Dimension Details -->
      <div v-if="report.dimension_details" class="detail-card">
        <h3>能力维度分析</h3>
        <div class="dim-list">
          <div v-for="(d, k) in report.dimension_details" :key="k" class="dim-item">
            <div class="dim-head">
              <span class="dim-name">{{ dimLabel(String(k)) }}</span>
              <span class="dim-score">{{ d.score }}</span>
            </div>
            <p class="dim-summary">{{ d.summary }}</p>
            <div class="dim-tags">
              <span v-for="s in d.strengths" :key="s" class="tag tag-good">+ {{ s }}</span>
              <span v-for="w in d.weaknesses" :key="w" class="tag tag-warn">- {{ w }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Key Q&A -->
      <div v-if="report.key_questions_summary?.length" class="detail-card">
        <h3>关键问答</h3>
        <div class="qa-list">
          <div v-for="(q, idx) in report.key_questions_summary" :key="idx" class="qa-item">
            <div class="qa-num">{{ idx + 1 }}</div>
            <div class="qa-body">
              <p class="qa-q">{{ q.question }}</p>
              <p class="qa-a">{{ q.key_takeaway }}</p>
            </div>
            <span class="qa-quality" :class="qualityClass(q.answer_quality)">{{ q.answer_quality || '-' }}</span>
          </div>
        </div>
      </div>

      <!-- Next Steps -->
      <div v-if="report.next_steps" class="next-steps">
        <div class="ns-icon">💡</div>
        <h3>下一步建议</h3>
        <p>{{ report.next_steps }}</p>
      </div>

      <!-- 完整对话记录 -->
      <div v-if="report.conversation?.length" class="conv-card">
        <h3>完整面试对话</h3>
        <div class="conv-list">
          <div v-for="(msg, idx) in report.conversation" :key="idx" class="conv-msg" :class="msg.role === '面试官' ? 'conv-ai' : 'conv-user'">
            <div class="conv-head">
              <span class="conv-role">{{ msg.role }}</span>
              <span v-if="msg.question_number" class="conv-qnum">第 {{ msg.question_number }} 题</span>
            </div>
            <p class="conv-text">{{ msg.content }}</p>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="rpt-actions">
        <button class="btn-primary" onclick="window.print()">下载报告</button>
        <NuxtLink to="/interviews" class="btn-secondary">返回列表</NuxtLink>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const { $api } = useNuxtApp()
const report = ref<any>(null)
const loading = ref(true)
const error = ref<string | null>(null)

const fmtDate = (d: string) => d ? new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' }) : '-'
const dimLabel = (k: string) => ({ technical: '技术能力', communication: '沟通表达', learning: '学习潜力', match: '岗位匹配' })[k] || k
const qualityClass = (q: string) => ({ '优秀': 'qa-good', '良好': 'qa-ok', '一般': 'qa-warn', '较差': 'qa-bad' })[q] || ''

const overallScore = computed(() => {
  const os = report.value?.overall_score
  if (!os) return 0
  return Math.round((os.technical || 0) + (os.communication || 0) + (os.learning || 0) + (os.match || 0)) / 4
})
const ratingLabel = computed(() => {
  const s = overallScore.value
  if (s >= 90) return '卓越'
  if (s >= 80) return '优秀'
  if (s >= 70) return '良好'
  return '一般'
})
const badgeClass = computed(() => {
  const s = overallScore.value
  if (s >= 80) return 'badge-great'
  if (s >= 70) return 'badge-good'
  return 'badge-ok'
})

onMounted(async () => {
  try {
    const res = await $api.get(`/reports/${route.params.id}`)
    report.value = res.data.data
    nextTick(() => drawRing(overallScore.value))
  } catch (e: any) {
    console.error('报告加载失败:', e)
    const detail = e?.response?.data?.detail || e?.message || '请求失败'
    const status = e?.response?.status || ''
    error.value = `加载报告失败 (${status}: ${detail})`
  }
  finally { loading.value = false }
})

function drawRing(score: number) {
  const el = document.getElementById('ringWrap')
  if (!el) return
  const r = 72, circ = 2 * Math.PI * r, target = circ - (circ * score) / 100
  el.innerHTML = `
    <svg width="168" height="168" viewBox="0 0 168 168">
      <defs><linearGradient id="rGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#5B5BED"/><stop offset="100%" stop-color="#10B981"/></linearGradient></defs>
      <circle cx="84" cy="84" r="${r}" fill="none" stroke="#F0F0F3" stroke-width="10"/>
      <circle cx="84" cy="84" r="${r}" fill="none" stroke="url(#rGrad)" stroke-width="10" stroke-linecap="round" stroke-dasharray="${circ}" stroke-dashoffset="${circ}" id="ringArc" style="transition:stroke-dashoffset 1.4s cubic-bezier(0.16,1,0.3,1)"/>
    </svg>
    <div class="ring-center"><div class="ring-score">${score}</div><div class="ring-unit">/ 100</div></div>`
  requestAnimationFrame(() => {
    const a = document.getElementById('ringArc')
    if (a) a.setAttribute('stroke-dashoffset', String(target))
  })
}
</script>

<style scoped>
/* Page */
.rpt-page { max-width: 780px; margin: 0 auto; padding: 40px 24px }
.rpt-loading, .rpt-error { text-align: center; padding: 80px 24px }
.spinner { width: 36px; height: 36px; border: 3px solid #E8E8ED; border-top-color: #5B5BED; border-radius: 50%; animation: spin .8s linear infinite; margin: 0 auto 16px }
@keyframes spin { to { transform: rotate(360deg) } }
.rpt-loading p { color: #A1A1AA; font-size: 14px }
.rpt-error-icon { font-size: 48px; margin-bottom: 12px }
.rpt-error p { color: #EF4444; margin-bottom: 16px }
.back-link { color: #5B5BED; font-size: 14px; font-weight: 500; text-decoration: none }
.back-link:hover { text-decoration: underline }

/* Header */
.rpt-header { text-align: center; margin-bottom: 36px }
.rpt-header h1 { font-size: 28px; font-weight: 700; letter-spacing: -0.025em; background: linear-gradient(135deg, #18181B, #3F3F46); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 4px }
.rpt-meta { font-size: 14px; color: #71717A; display: flex; align-items: center; justify-content: center; gap: 10px }
.dot { width: 3px; height: 3px; border-radius: 50%; background: #E8E8ED }

/* Score Hero */
.score-hero { display: flex; align-items: center; gap: 40px; flex-wrap: wrap; justify-content: center; background: #FFF; border: 1px solid #F0F0F3; border-radius: 20px; padding: 36px 40px; box-shadow: 0 4px 6px rgba(0,0,0,0.03), 0 2px 4px rgba(0,0,0,0.02); margin-bottom: 24px }
.ring-wrap { position: relative; width: 168px; height: 168px; flex-shrink: 0 }
.ring-wrap :deep(svg) { display: block; transform: rotate(-90deg) }
.ring-center { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center }
.ring-score { font-size: 46px; font-weight: 700; letter-spacing: -0.03em; line-height: 1; color: #18181B }
.ring-unit { font-size: 13px; color: #A1A1AA; margin-top: 3px }
.score-info { flex: 1; min-width: 220px }
.score-badge { display: inline-flex; align-items: center; gap: 6px; padding: 5px 13px; border-radius: 9999px; font-size: 13px; font-weight: 600; margin-bottom: 16px }
.badge-great { background: rgba(16,185,129,0.08); color: #10B981 }
.badge-good { background: rgba(91,91,237,0.06); color: #5B5BED }
.badge-ok { background: rgba(245,158,11,0.08); color: #F59E0B }
.summary-text { font-size: 15px; color: #71717A; line-height: 1.7 }
.summary-hint { font-size: 13px; color: #A1A1AA; margin-top: 8px }

/* Detail Card */
.detail-card { background: #FFF; border: 1px solid #F0F0F3; border-radius: 20px; padding: 28px 32px; box-shadow: 0 1px 2px rgba(0,0,0,0.03); margin-bottom: 16px }
.detail-card h3 { font-size: 17px; font-weight: 600; color: #18181B; margin-bottom: 20px; letter-spacing: -0.01em }

/* Dimensions */
.dim-list { display: flex; flex-direction: column; gap: 12px }
.dim-item { border: 1px solid #F0F0F3; border-radius: 12px; padding: 16px 20px }
.dim-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px }
.dim-name { font-size: 14px; font-weight: 600; color: #18181B }
.dim-score { font-size: 22px; font-weight: 700; color: #5B5BED }
.dim-summary { font-size: 13px; color: #71717A; line-height: 1.6; margin-bottom: 8px }
.dim-tags { display: flex; flex-wrap: wrap; gap: 6px }
.tag { font-size: 11px; padding: 3px 8px; border-radius: 9999px; font-weight: 500 }
.tag-good { background: rgba(16,185,129,0.06); color: #059669 }
.tag-warn { background: rgba(245,158,11,0.06); color: #D97706 }

/* Q&A */
.qa-list { display: flex; flex-direction: column; gap: 8px }
.qa-item { display: flex; align-items: flex-start; gap: 12px; padding: 14px 16px; background: #F5F5F7; border-radius: 12px }
.qa-num { width: 28px; height: 28px; border-radius: 8px; background: rgba(91,91,237,0.06); color: #5B5BED; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; flex-shrink: 0 }
.qa-body { flex: 1; min-width: 0 }
.qa-q { font-size: 13px; font-weight: 500; color: #18181B; margin-bottom: 4px }
.qa-a { font-size: 12px; color: #A1A1AA }
.qa-quality { font-size: 11px; padding: 2px 8px; border-radius: 9999px; font-weight: 500; flex-shrink: 0 }
.qa-good { background: rgba(16,185,129,0.06); color: #10B981 }
.qa-ok { background: rgba(91,91,237,0.06); color: #5B5BED }
.qa-warn { background: rgba(245,158,11,0.06); color: #F59E0B }
.qa-bad { background: rgba(239,68,68,0.06); color: #EF4444 }

/* Next Steps */
.next-steps { background: linear-gradient(135deg, rgba(91,91,237,0.02), rgba(16,185,129,0.02)); border: 1px solid rgba(91,91,237,0.08); border-radius: 20px; padding: 28px 32px; text-align: center; margin-bottom: 24px }
.ns-icon { font-size: 28px; margin-bottom: 8px }
.next-steps h3 { font-size: 16px; font-weight: 600; color: #18181B; margin-bottom: 6px }
.next-steps p { font-size: 14px; color: #71717A; line-height: 1.7 }

/* Actions */
/* Conversation */
.conv-card { background: #FFF; border: 1px solid #F0F0F3; border-radius: 20px; padding: 28px 32px; box-shadow: 0 1px 2px rgba(0,0,0,0.03); margin-bottom: 16px }
.conv-card h3 { font-size: 17px; font-weight: 600; color: #18181B; margin-bottom: 20px; letter-spacing: -0.01em }
.conv-list { display: flex; flex-direction: column; gap: 10px }
.conv-msg { padding: 14px 18px; border-radius: 12px }
.conv-ai { background: #F5F5F7; border-left: 3px solid #5B5BED }
.conv-user { background: #F0FDF4; border-left: 3px solid #10B981 }
.conv-head { display: flex; align-items: center; gap: 10px; margin-bottom: 6px }
.conv-role { font-size: 12px; font-weight: 600; color: #71717A }
.conv-qnum { font-size: 11px; color: #5B5BED; font-weight: 500 }
.conv-text { font-size: 14px; color: #3F3F46; line-height: 1.65; white-space: pre-wrap }

.rpt-actions { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap }
.btn-primary { display: inline-flex; align-items: center; justify-content: center; height: 48px; padding: 0 24px; border-radius: 10px; font-size: 15px; font-weight: 500; font-family: inherit; border: none; cursor: pointer; background: #5B5BED; color: #FFF; box-shadow: 0 4px 16px rgba(91,91,237,0.2); transition: all 0.2s; text-decoration: none; min-width: 160px }
.btn-primary:hover { background: #4F4FE0; transform: translateY(-1px); box-shadow: 0 6px 20px rgba(91,91,237,0.28) }
.btn-secondary { display: inline-flex; align-items: center; justify-content: center; height: 48px; padding: 0 24px; border-radius: 10px; font-size: 15px; font-weight: 500; font-family: inherit; border: 1px solid #E8E8ED; cursor: pointer; background: #FFF; color: #18181B; text-decoration: none; min-width: 160px; transition: all 0.2s }
.btn-secondary:hover { background: #F5F5F7; border-color: #D4D4D8 }

@media (max-width: 640px) { .score-hero { flex-direction: column; gap: 28px; padding: 28px } .ring-wrap { width: 140px; height: 140px } .ring-score { font-size: 38px } }
</style>
