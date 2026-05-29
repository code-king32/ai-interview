<template>
  <div>
    <div class="welcome-section">
      <h1>欢迎使用 AI 面试系统</h1>
      <p>您好，管理员</p>
    </div>

    <!-- 统计卡片：4列网格 -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-info">
          <div class="stat-label">岗位数量</div>
          <div class="stat-number">{{ jobCount }}</div>
        </div>
        <div class="stat-icon">📋</div>
      </div>
      <div class="stat-card">
        <div class="stat-info">
          <div class="stat-label">候选人</div>
          <div class="stat-number">{{ candidateCount }}</div>
        </div>
        <div class="stat-icon">👥</div>
      </div>
      <div class="stat-card">
        <div class="stat-info">
          <div class="stat-label">面试场次</div>
          <div class="stat-number">{{ interviewCount }}</div>
        </div>
        <div class="stat-icon">🎯</div>
      </div>
      <div class="stat-card">
        <div class="stat-info">
          <div class="stat-label">平均评分</div>
          <div class="stat-number">{{ avgScore }}</div>
        </div>
        <div class="stat-icon">⭐</div>
      </div>
    </div>

    <!-- 功能卡片 -->
    <div class="feature-grid">
      <div class="feature-card">
        <div class="feature-icon">📋</div>
        <h3>岗位管理</h3>
        <p>创建和管理面试岗位，定义技术要求</p>
        <NuxtLink to="/jobs" class="feature-link">去管理 →</NuxtLink>
      </div>
      <div class="feature-card">
        <div class="feature-icon">👥</div>
        <h3>候选人管理</h3>
        <p>管理候选人信息，上传简历文档</p>
        <NuxtLink to="/candidates" class="feature-link">去管理 →</NuxtLink>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <h3>面试记录</h3>
        <p>查看面试历史，获取详细报告</p>
        <NuxtLink to="/interviews" class="feature-link">去查看 →</NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useJobStore } from '~/stores/jobStore'
import { useCandidateStore } from '~/stores/candidateStore'

const { $api } = useNuxtApp()
const jobStore = useJobStore()
const candidateStore = useCandidateStore()

const jobCount = ref(0)
const candidateCount = ref(0)
const interviewCount = ref(0)
const avgScore = ref(0)

const fetchStats = async () => {
  await jobStore.fetchJobs(1, 1)
  jobCount.value = jobStore.total

  await candidateStore.fetchCandidates(1, 1)
  candidateCount.value = candidateStore.total

  try {
    const res = await $api.get('/interviews', { params: { page: 1, page_size: 100 } })
    if (res.data.code === 0) {
      const items = res.data.data.items || []
      interviewCount.value = items.length
      const scores = items.filter(i => i.overall_score).map(i => i.overall_score)
      if (scores.length) {
        avgScore.value = (scores.reduce((a, b) => a + b, 0) / scores.length).toFixed(1)
      }
    }
  } catch (error) {
    console.error('获取面试数据失败', error)
  }
}

onMounted(fetchStats)
</script>

<style scoped>
.welcome-section {
  margin-bottom: 28px;
}
.welcome-section h1 {
  font-size: 24px;
  font-weight: bold;
  color: #1f2937;
}
.welcome-section p {
  color: #6b7280;
  margin-top: 4px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 40px;
}
.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-left: 4px solid #3b82f6;
}
.stat-card .stat-label {
  color: #6b7280;
  font-size: 14px;
}
.stat-card .stat-number {
  font-size: 28px;
  font-weight: bold;
  color: #1f2937;
}
.stat-card .stat-icon {
  font-size: 32px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}
.feature-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  transition: 0.2s;
}
.feature-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.feature-icon {
  width: 48px;
  height: 48px;
  background: #eff6ff;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  margin-bottom: 16px;
}
.feature-card h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #1f2937;
}
.feature-card p {
  color: #6b7280;
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 16px;
}
.feature-link {
  color: #3b82f6;
  text-decoration: none;
  font-size: 14px;
}
.feature-link:hover {
  text-decoration: underline;
}
</style>