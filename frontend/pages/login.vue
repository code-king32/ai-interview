<template>
  <div class="login-bg">
    <div class="login-card">
      <!-- Brand -->
      <div class="brand-row">
        <div class="brand-icon">🤖</div>
        <h1>AI 面试平台</h1>
        <p>选择你的身份，开始智能面试之旅</p>
      </div>

      <!-- 身份选择卡片 -->
      <div class="role-cards">
        <button class="role-card" @click="login('seeker')">
          <div class="role-icon-wrap seeker">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-8 8-8"/>
              <path d="M16 3.13a4 4 0 010 7.75"/><path d="M21 21v-2a4 4 0 00-3-3.87"/>
            </svg>
          </div>
          <div class="role-info">
            <h3>我是求职者</h3>
            <p>上传简历，设置目标岗位<br>AI 模拟面试，针对性提升</p>
          </div>
          <span class="role-arrow">→</span>
        </button>

        <button class="role-card" @click="login('hr')">
          <div class="role-icon-wrap hr">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>
            </svg>
          </div>
          <div class="role-info">
            <h3>我是面试官 / HR</h3>
            <p>管理岗位和候选人<br>发起 AI 面试，查看评估报告</p>
          </div>
          <span class="role-arrow">→</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: false })

const router = useRouter()

const login = (role: 'seeker' | 'hr') => {
  localStorage.setItem('role', role)
  localStorage.setItem('token', 'mock-token')
  router.push('/')
}
</script>

<style scoped>
.login-bg {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background:
    radial-gradient(ellipse 60% 50% at 50% -20%, rgba(91,91,237,0.06) 0%, transparent 60%),
    #FAFAFA;
}

.login-card {
  background: #FFF;
  border-radius: 20px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04), 0 10px 40px rgba(0,0,0,0.06);
  padding: 40px;
  max-width: 560px;
  width: 100%;
  border: 1px solid #F0F0F3;
}

.brand-row {
  text-align: center;
  margin-bottom: 36px;
}
.brand-icon {
  width: 52px; height: 52px;
  background: linear-gradient(135deg, #5B5BED, #A78BFA);
  border-radius: 14px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  margin-bottom: 16px;
  box-shadow: 0 8px 24px rgba(91,91,237,0.25);
}
.brand-row h1 {
  font-size: 26px;
  font-weight: 700;
  color: #18181B;
  letter-spacing: -0.02em;
  margin-bottom: 6px;
}
.brand-row p {
  font-size: 14px;
  color: #A1A1AA;
}

.role-cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.role-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 22px;
  border: 1.5px solid #F0F0F3;
  border-radius: 14px;
  background: #FFF;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.16,1,0.3,1);
  text-align: left;
  font-family: inherit;
}
.role-card:hover {
  border-color: #5B5BED;
  box-shadow: 0 4px 20px rgba(91,91,237,0.1);
  transform: translateY(-2px);
}

.role-icon-wrap {
  width: 48px; height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.role-icon-wrap.seeker {
  background: rgba(16,185,129,0.08);
  color: #10B981;
}
.role-icon-wrap.hr {
  background: rgba(91,91,237,0.08);
  color: #5B5BED;
}

.role-info {
  flex: 1;
  min-width: 0;
}
.role-info h3 {
  font-size: 16px;
  font-weight: 600;
  color: #18181B;
  margin-bottom: 4px;
  letter-spacing: -0.01em;
}
.role-info p {
  font-size: 13px;
  color: #A1A1AA;
  line-height: 1.5;
}

.role-arrow {
  font-size: 18px;
  color: #D4D4D8;
  flex-shrink: 0;
  transition: all 0.2s;
}
.role-card:hover .role-arrow {
  color: #5B5BED;
  transform: translateX(4px);
}

@media (max-width: 480px) {
  .login-card { padding: 28px 20px; }
  .role-card { padding: 16px; gap: 12px; }
}
</style>
