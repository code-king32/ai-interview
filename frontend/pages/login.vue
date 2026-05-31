<template>
  <div class="login-bg">
    <div class="login-card">
      <div class="brand-row">
        <div class="brand-icon">🤖</div>
        <h1>AI 面试平台</h1>
      </div>

      <div class="form-area">
        <!-- 身份选择 -->
        <label class="fg-label">选择身份</label>
        <div class="role-row">
          <button class="role-btn" :class="{ active: role === 'seeker' }" @click="role = 'seeker'">
            <span class="rb-icon">🧑‍💻</span> 求职者
          </button>
          <button class="role-btn" :class="{ active: role === 'hr' }" @click="role = 'hr'">
            <span class="rb-icon">💼</span> 面试官/HR
          </button>
        </div>

        <!-- 用户名 -->
        <label class="fg-label">用户名</label>
        <input v-model="username" type="text" placeholder="请输入用户名" />

        <!-- 密码 -->
        <label class="fg-label">密码</label>
        <input v-model="password" type="password" placeholder="请输入密码" />

        <!-- 注册时确认密码 -->
        <template v-if="mode === 'register'">
          <label class="fg-label">确认密码</label>
          <input v-model="confirm" type="password" placeholder="再次输入密码" />
        </template>

        <p v-if="mode === 'register'" class="role-note">注：账号将注册为「{{ role === 'hr' ? '面试官/HR' : '求职者' }}」角色</p>
        <button class="submit-btn" :disabled="loading" @click="submit">
          {{ loading ? '...' : (mode === 'register' ? '注册' : '登录') }}
        </button>
      </div>

      <div class="toggle-link">
        {{ mode === 'login' ? '没有账号？' : '已有账号？' }}
        <a href="#" @click.prevent="mode = mode === 'login' ? 'register' : 'login'">{{ mode === 'login' ? '去注册' : '去登录' }}</a>
      </div>

      <div v-if="error" class="error-msg">{{ error }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: false })
const { $api } = useNuxtApp()

const role = ref('seeker')
const mode = ref<'login' | 'register'>('login')
const username = ref('')
const password = ref('')
const confirm = ref('')
const loading = ref(false)
const error = ref('')

// 兼容各种拦截器包装层级
const findUser = (d: any) => d?.data?.role ? d.data : d?.data?.data?.role ? d.data.data : d?.role ? d : null

const submit = async () => {
  error.value = ''
  const u = username.value.trim()
  const p = password.value
  if (!u) { error.value = '请输入用户名'; return }
  if (!p) { error.value = '请输入密码'; return }
  if (mode.value === 'register' && p !== confirm.value) { error.value = '两次密码不一致'; return }
  loading.value = true
  try {
    if (mode.value === 'register') {
      try {
        const r = await $api.post('/auth/register', { username: u, password: p, role: role.value })
        console.log('Register:', r.data)
      } catch (e: any) {
        if (e?.response?.data?.detail?.includes('已存在')) {
          error.value = '用户名已存在，请直接登录'
          loading.value = false
          return
        }
        throw e
      }
    }
    const r = await $api.post('/auth/login', { username: u, password: p })
    // auth 返回 {code, data: {username, role}}
    const user = r.data?.data || r.data
    console.log('user:', user)
    if (!user?.role) { error.value = '登录失败'; loading.value = false; return }
    if (user.role !== role.value) {
      error.value = `该账号是「${user.role === 'hr' ? '面试官/HR' : '求职者'}」账号，请切换身份后登录`
      loading.value = false
      return
    }
    localStorage.setItem('role', user.role)
    localStorage.setItem('token', 'ok')
    window.location.href = `/?role=${user.role}`
  } catch (e: any) {
    error.value = e?.response?.data?.detail || '请求失败'
    console.error(e)
  }
  finally { loading.value = false }
}
</script>

<style scoped>
.login-bg { min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 24px; background: radial-gradient(ellipse 60% 50% at 50% -20%, rgba(91,91,237,0.06) 0%, transparent 60%), #FAFAFA; }
.login-card { background: #FFF; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.06); padding: 36px; max-width: 440px; width: 100%; border: 1px solid #F0F0F3; }
.brand-row { text-align: center; margin-bottom: 28px; }
.brand-icon { width: 48px; height: 48px; background: linear-gradient(135deg, #5B5BED, #A78BFA); border-radius: 12px; display: inline-flex; align-items: center; justify-content: center; font-size: 24px; margin-bottom: 14px; box-shadow: 0 6px 20px rgba(91,91,237,0.2); }
.brand-row h1 { font-size: 24px; font-weight: 700; color: #18181B; }

.form-area { display: flex; flex-direction: column; gap: 10px; }
.fg-label { font-size: 12px; font-weight: 600; color: #71717A; text-transform: uppercase; letter-spacing: 0.04em; margin-top: 4px; }

.role-row { display: flex; gap: 10px; margin-bottom: 4px; }
.role-btn { flex: 1; padding: 12px; border: 1.5px solid #E8E8ED; border-radius: 10px; background: #FFF; cursor: pointer; font-size: 14px; font-family: inherit; font-weight: 500; color: #71717A; transition: all 0.2s; text-align: center; display: flex; align-items: center; justify-content: center; gap: 6px; }
.role-btn.active { border-color: #5B5BED; background: rgba(91,91,237,0.04); color: #5B5BED; }
.rb-icon { font-size: 16px; }

.form-area input { width: 100%; padding: 12px 14px; border: 1.5px solid #E8E8ED; border-radius: 10px; font-size: 15px; font-family: inherit; outline: none; color: #18181B; }
.form-area input:focus { border-color: #5B5BED; }

.submit-btn { width: 100%; padding: 12px; border-radius: 10px; border: none; background: #5B5BED; color: #FFF; font-size: 15px; font-weight: 600; cursor: pointer; font-family: inherit; margin-top: 8px; }
.submit-btn:hover:not(:disabled) { background: #4F4FE0; }
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.toggle-link { text-align: center; margin-top: 16px; font-size: 13px; color: #A1A1AA; }
.toggle-link a { color: #5B5BED; font-weight: 500; text-decoration: none; }
.error-msg { margin-top: 12px; padding: 10px 14px; background: #FEF2F2; color: #DC2626; border-radius: 8px; font-size: 13px; text-align: center; }
</style>
