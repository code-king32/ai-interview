<template>
  <div class="login-bg">
    <div class="login-card">
      <!-- Brand -->
      <div class="brand-row">
        <div class="brand-icon">🤖</div>
        <h1>AI 面试平台</h1>
        <p>{{ isRegister ? '创建账号开始使用' : '选择身份或登录已有账号' }}</p>
      </div>

      <!-- 快速入口（登录模式） -->
      <div v-if="!isRegister" class="role-cards">
        <button class="role-card" @click="quickLogin('seeker')">
          <div class="role-icon-wrap seeker">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-8 8-8"/><path d="M16 3.13a4 4 0 010 7.75"/><path d="M21 21v-2a4 4 0 00-3-3.87"/></svg>
          </div>
          <div class="role-info">
            <h3>我是求职者</h3>
            <p>上传简历，AI 模拟面试</p>
          </div>
          <span class="role-arrow">→</span>
        </button>

        <button class="role-card" @click="quickLogin('hr')">
          <div class="role-icon-wrap hr">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
          </div>
          <div class="role-info">
            <h3>我是面试官 / HR</h3>
            <p>管理岗位，评估候选人</p>
          </div>
          <span class="role-arrow">→</span>
        </button>
      </div>

      <div class="divider"><span>或使用账号登录</span></div>

      <!-- 表单 -->
      <div class="form-area">
        <div class="input-wrap">
          <input v-model="username" type="text" placeholder="用户名" @keyup.enter="handleSubmit" />
        </div>
        <div class="input-wrap">
          <input v-model="password" type="password" placeholder="密码" @keyup.enter="handleSubmit" />
        </div>
        <div v-if="isRegister" class="input-wrap">
          <select v-model="role" class="role-select">
            <option value="seeker">我是求职者</option>
            <option value="hr">我是面试官 / HR</option>
          </select>
        </div>
        <button class="submit-btn" :disabled="loading" @click="handleSubmit">
          {{ loading ? '处理中…' : (isRegister ? '注册' : '登录') }}
        </button>
      </div>

      <div class="toggle-link">
        {{ isRegister ? '已有账号？' : '没有账号？' }}
        <a href="#" @click.prevent="isRegister = !isRegister">{{ isRegister ? '去登录' : '去注册' }}</a>
      </div>

      <div v-if="error" class="error-msg">{{ error }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: false })
const router = useRouter()
const { $api } = useNuxtApp()

const username = ref('')
const password = ref('')
const role = ref('seeker')
const isRegister = ref(false)
const loading = ref(false)
const error = ref('')

// 快速免密登录
const quickLogin = (r: string) => {
  localStorage.setItem('role', r)
  localStorage.setItem('token', 'guest')
  router.push('/')
}

const handleSubmit = async () => {
  error.value = ''
  if (!username.value || !password.value) {
    error.value = '请输入用户名和密码'
    return
  }
  loading.value = true
  try {
    if (isRegister.value) {
      await $api.post('/auth/register', { username: username.value, password: password.value, role: role.value })
    }
    const res = await $api.post('/auth/login', { username: username.value, password: password.value })
    const user = res.data.data
    localStorage.setItem('role', user.role)
    localStorage.setItem('token', 'mock-token')
    localStorage.setItem('user', JSON.stringify({ id: user.id, username: user.username }))
    router.push('/')
  } catch (e: any) {
    error.value = e?.response?.data?.detail || '请求失败'
  }
  finally { loading.value = false }
}

onMounted(() => {
  localStorage.removeItem('token')
  localStorage.removeItem('role')
})
</script>

<style scoped>
.login-bg {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: radial-gradient(ellipse 60% 50% at 50% -20%, rgba(91,91,237,0.06) 0%, transparent 60%), #FAFAFA;
}
.login-card {
  background: #FFF;
  border-radius: 20px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04), 0 10px 40px rgba(0,0,0,0.06);
  padding: 36px;
  max-width: 520px;
  width: 100%;
  border: 1px solid #F0F0F3;
}

.brand-row { text-align: center; margin-bottom: 32px; }
.brand-icon {
  width: 48px; height: 48px;
  background: linear-gradient(135deg, #5B5BED, #A78BFA);
  border-radius: 12px; display: inline-flex; align-items: center; justify-content: center;
  font-size: 24px; margin-bottom: 14px;
  box-shadow: 0 6px 20px rgba(91,91,237,0.2);
}
.brand-row h1 { font-size: 24px; font-weight: 700; color: #18181B; letter-spacing: -0.02em; margin-bottom: 4px; }
.brand-row p { font-size: 14px; color: #A1A1AA; }

.role-cards { display: flex; flex-direction: column; gap: 10px; }
.role-card {
  display: flex; align-items: center; gap: 14px;
  padding: 16px 20px; border: 1.5px solid #F0F0F3; border-radius: 12px;
  background: #FFF; cursor: pointer; text-align: left; font-family: inherit;
  transition: all 0.25s cubic-bezier(0.16,1,0.3,1);
}
.role-card:hover { border-color: #5B5BED; box-shadow: 0 4px 16px rgba(91,91,237,0.08); transform: translateY(-1px); }
.role-icon-wrap { width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.role-icon-wrap.seeker { background: rgba(16,185,129,0.08); color: #10B981; }
.role-icon-wrap.hr { background: rgba(91,91,237,0.08); color: #5B5BED; }
.role-info { flex: 1; }
.role-info h3 { font-size: 15px; font-weight: 600; color: #18181B; margin-bottom: 2px; }
.role-info p { font-size: 12px; color: #A1A1AA; }
.role-arrow { font-size: 16px; color: #D4D4D8; }

.divider {
  display: flex; align-items: center; gap: 14px; margin: 24px 0;
  color: #D4D4D8; font-size: 12px;
}
.divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: #F0F0F3; }

.form-area { display: flex; flex-direction: column; gap: 12px; }
.input-wrap input, .role-select {
  width: 100%; padding: 12px 14px; border: 1.5px solid #E8E8ED; border-radius: 10px;
  font-size: 15px; font-family: inherit; outline: none;
  transition: border-color 0.2s;
  color: #18181B; background: #FFF;
}
.input-wrap input:focus, .role-select:focus { border-color: #5B5BED; }
.role-select { cursor: pointer; }

.submit-btn {
  width: 100%; padding: 12px; border-radius: 10px; border: none;
  background: #5B5BED; color: #FFF; font-size: 15px; font-weight: 600;
  cursor: pointer; font-family: inherit; transition: all 0.2s;
}
.submit-btn:hover:not(:disabled) { background: #4F4FE0; }
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.toggle-link { text-align: center; margin-top: 18px; font-size: 13px; color: #A1A1AA; }
.toggle-link a { color: #5B5BED; font-weight: 500; text-decoration: none; }
.toggle-link a:hover { text-decoration: underline; }

.error-msg { margin-top: 12px; padding: 10px 14px; background: #FEF2F2; color: #DC2626; border-radius: 8px; font-size: 13px; text-align: center; }
</style>
