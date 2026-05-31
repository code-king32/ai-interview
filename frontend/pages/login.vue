<template>
  <div class="login-bg">
    <div class="login-card">
      <div class="brand-row">
        <div class="brand-icon">🤖</div>
        <h1>AI 面试平台</h1>
      </div>

      <!-- Step 1: 选择身份 -->
      <template v-if="step === 'role'">
        <p class="step-hint">请选择你的身份</p>
        <div class="role-cards">
          <button class="role-card" @click="selectRole('seeker')">
            <div class="role-icon-wrap seeker">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-8 8-8"/><path d="M16 3.13a4 4 0 010 7.75"/><path d="M21 21v-2a4 4 0 00-3-3.87"/></svg>
            </div>
            <div class="role-info">
              <h3>求职者</h3>
              <p>AI 模拟面试，针对性练习提升</p>
            </div>
            <span class="role-arrow">→</span>
          </button>
          <button class="role-card" @click="selectRole('hr')">
            <div class="role-icon-wrap hr">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
            </div>
            <div class="role-info">
              <h3>面试官 / HR</h3>
              <p>管理岗位，邀请候选人，查看报告</p>
            </div>
            <span class="role-arrow">→</span>
          </button>
        </div>
      </template>

      <!-- Step 2: 登录/注册 -->
      <template v-else>
        <div class="role-badge" :class="selectedRole">
          {{ selectedRole === 'seeker' ? '🧑‍💻 求职者' : '💼 面试官 / HR' }}
        </div>

        <div class="form-area">
          <div class="input-wrap">
            <input v-model="username" type="text" placeholder="用户名" />
          </div>
          <div class="input-wrap">
            <input v-model="password" type="password" placeholder="密码" />
          </div>
          <template v-if="isRegister">
            <div class="input-wrap">
              <input v-model="confirmPassword" type="password" placeholder="确认密码" />
            </div>
            <p class="note">注册后账号角色为「{{ selectedRole === 'seeker' ? '求职者' : '面试官/HR' }}」，不可更改</p>
          </template>
          <button class="submit-btn" :disabled="loading" @click="handleSubmit">
            {{ loading ? '处理中…' : (isRegister ? '注册并登录' : '登录') }}
          </button>
        </div>

        <div class="toggle-link">
          <a href="#" @click.prevent="goBack">← 重新选择身份</a>
          <span class="sep">|</span>
          <a href="#" @click.prevent="toggleMode">{{ isRegister ? '已有账号？去登录' : '没有账号？去注册' }}</a>
        </div>
      </template>

      <div v-if="error" class="error-msg">{{ error }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: false })
const router = useRouter()
const { $api } = useNuxtApp()

const step = ref<'role' | 'auth'>('role')
const selectedRole = ref('')
const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const isRegister = ref(false)
const loading = ref(false)
const error = ref('')

const selectRole = (role: string) => {
  selectedRole.value = role
  step.value = 'auth'
  isRegister.value = false
  username.value = ''
  password.value = ''
  confirmPassword.value = ''
  error.value = ''
}

const toggleMode = () => {
  isRegister.value = !isRegister.value
  error.value = ''
}

const goBack = () => {
  step.value = 'role'
  error.value = ''
}

const validate = (): boolean => {
  if (!username.value.trim()) { error.value = '请输入用户名'; return false }
  if (username.value.trim().length < 2) { error.value = '用户名至少2个字符'; return false }
  if (!password.value) { error.value = '请输入密码'; return false }
  if (password.value.length < 3) { error.value = '密码至少3个字符'; return false }
  if (isRegister.value && password.value !== confirmPassword.value) { error.value = '两次密码不一致'; return false }
  return true
}

const handleSubmit = async () => {
  error.value = ''
  if (!validate()) return
  loading.value = true
  try {
    if (isRegister.value) {
      // 注册
      try {
        await $api.post('/auth/register', { username: username.value.trim(), password: password.value, role: selectedRole.value })
      } catch (e: any) {
        const detail = e?.response?.data?.detail || ''
        if (detail.includes('已存在')) {
          error.value = '该用户名已被注册，请直接登录'
          loading.value = false
          return
        }
        throw e
      }
    }
    // 登录
    const res = await $api.post('/auth/login', { username: username.value.trim(), password: password.value })
    const user = res.data.data
    if (user.role !== selectedRole.value) {
      error.value = `该账号是「${user.role === 'hr' ? '面试官/HR' : '求职者'}」账号，请返回选择正确的身份`
      loading.value = false
      return
    }
    localStorage.setItem('role', user.role)
    localStorage.setItem('token', 'ok')
    localStorage.setItem('user', JSON.stringify({ id: user.id, username: user.username }))
    document.cookie = `role=${user.role};path=/;max-age=86400`
    // Nuxt 跨组件状态，layout 立即可用
    useState('user-role').value = user.role
    router.push('/')
  } catch (e: any) {
    error.value = e?.response?.data?.detail || '登录失败，请重试'
  }
  finally { loading.value = false }
}

onMounted(() => {
  localStorage.clear()
  document.cookie = 'role=;path=/;max-age=0'
})
</script>

<style scoped>
.login-bg {
  min-height: 100vh;
  display: flex; align-items: center; justify-content: center; padding: 24px;
  background: radial-gradient(ellipse 60% 50% at 50% -20%, rgba(91,91,237,0.06) 0%, transparent 60%), #FAFAFA;
}
.login-card {
  background: #FFF; border-radius: 20px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04), 0 10px 40px rgba(0,0,0,0.06);
  padding: 36px; max-width: 520px; width: 100%; border: 1px solid #F0F0F3; min-height: 380px;
}
.brand-row { text-align: center; margin-bottom: 28px; }
.brand-icon {
  width: 48px; height: 48px; background: linear-gradient(135deg, #5B5BED, #A78BFA);
  border-radius: 12px; display: inline-flex; align-items: center; justify-content: center;
  font-size: 24px; margin-bottom: 14px; box-shadow: 0 6px 20px rgba(91,91,237,0.2);
}
.brand-row h1 { font-size: 24px; font-weight: 700; color: #18181B; }
.step-hint { text-align: center; font-size: 14px; color: #A1A1AA; margin-bottom: 20px; }

.role-cards { display: flex; flex-direction: column; gap: 10px; }
.role-card {
  display: flex; align-items: center; gap: 14px;
  padding: 18px 20px; border: 1.5px solid #F0F0F3; border-radius: 12px;
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

.role-badge {
  text-align: center; padding: 8px 16px; border-radius: 20px; font-size: 13px; font-weight: 500; margin-bottom: 20px;
}
.role-badge.seeker { background: rgba(16,185,129,0.08); color: #059669; }
.role-badge.hr { background: rgba(91,91,237,0.08); color: #5B5BED; }

.form-area { display: flex; flex-direction: column; gap: 12px; }
.input-wrap input {
  width: 100%; padding: 12px 14px; border: 1.5px solid #E8E8ED; border-radius: 10px;
  font-size: 15px; font-family: inherit; outline: none; transition: border-color 0.2s; color: #18181B;
}
.input-wrap input:focus { border-color: #5B5BED; }
.note { font-size: 12px; color: #A1A1AA; text-align: center; }

.submit-btn {
  width: 100%; padding: 12px; border-radius: 10px; border: none;
  background: #5B5BED; color: #FFF; font-size: 15px; font-weight: 600;
  cursor: pointer; font-family: inherit; transition: all 0.2s;
}
.submit-btn:hover:not(:disabled) { background: #4F4FE0; }
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.toggle-link { text-align: center; margin-top: 18px; font-size: 13px; color: #A1A1AA; display: flex; justify-content: center; gap: 10px; }
.toggle-link a { color: #5B5BED; font-weight: 500; text-decoration: none; }
.toggle-link a:hover { text-decoration: underline; }
.toggle-link .sep { color: #E8E8ED; }

.error-msg { margin-top: 12px; padding: 10px 14px; background: #FEF2F2; color: #DC2626; border-radius: 8px; font-size: 13px; text-align: center; }
</style>
