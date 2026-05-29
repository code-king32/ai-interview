<template>
  <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; overflow-x: hidden;">
    <div class="w-full max-w-md px-4" style="box-sizing: border-box;">
      <div style="background: rgba(255, 255, 255, 0.08); backdrop-filter: blur(12px); border-radius: 1.5rem; padding: 2rem; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); border: 1px solid rgba(255, 255, 255, 0.15); box-sizing: border-box; width: 100%;">
        
        <!-- 图标和标题同一行居中 -->
        <div style="display: flex; align-items: center; justify-content: center; gap: 12px; margin-bottom: 8px;">
          <div style="width: 44px; height: 44px; background: linear-gradient(135deg, #3b82f6, #2563eb); border-radius: 14px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
            <span style="font-size: 24px;">🤖</span>
          </div>
          <h1 style="color: white; font-size: 28px; font-weight: 700; letter-spacing: -0.5px;">AI 面试平台</h1>
        </div>
        
        <p style="color: #9ca3af; text-align: center; font-size: 14px; margin-top: 4px; margin-bottom: 32px;">智能面试 · 精准评估</p>

        <!-- 用户名输入框 -->
        <div style="margin-bottom: 20px; width: 100%;">
          <input 
            v-model="username"
            type="text"
            style="width: 100%; padding: 12px 16px; background: rgba(255, 255, 255, 0.12); border: 1px solid rgba(255, 255, 255, 0.25); border-radius: 12px; color: white; font-size: 16px; outline: none; transition: all 0.2s; box-sizing: border-box;"
            placeholder="用户名"
            @focus="e => e.target.style.borderColor = '#3b82f6'"
            @blur="e => e.target.style.borderColor = 'rgba(255,255,255,0.25)'"
            @keyup.enter="handleLogin"
          />
        </div>

        <!-- 密码输入框 -->
        <div style="margin-bottom: 28px; width: 100%;">
          <div style="position: relative; width: 100%;">
            <input 
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              style="width: 100%; padding: 12px 40px 12px 16px; background: rgba(255, 255, 255, 0.12); border: 1px solid rgba(255, 255, 255, 0.25); border-radius: 12px; color: white; font-size: 16px; outline: none; transition: all 0.2s; box-sizing: border-box;"
              placeholder="密码"
              @focus="e => e.target.style.borderColor = '#3b82f6'"
              @blur="e => e.target.style.borderColor = 'rgba(255,255,255,0.25)'"
              @keyup.enter="handleLogin"
            />
            <button
              type="button"
              @click="showPassword = !showPassword"
              style="position: absolute; right: 12px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer; color: #9ca3af; display: flex; align-items: center; padding: 0;"
            >
              <svg v-if="!showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" width="20" height="20">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" width="20" height="20">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
              </svg>
            </button>
          </div>
        </div>

        <!-- 登录按钮 -->
        <button
          @click="handleLogin"
          :disabled="loading"
          style="width: 100%; background: #2563eb; color: white; padding: 12px; border-radius: 12px; font-weight: 600; font-size: 16px; border: none; cursor: pointer; transition: all 0.2s; box-sizing: border-box;"
          @mouseenter="e => e.target.style.background = '#1d4ed8'"
          @mouseleave="e => e.target.style.background = '#2563eb'"
        >
          <span v-if="!loading">登录</span>
          <span v-else class="flex items-center justify-center gap-2">
            <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24" width="20" height="20">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="white" stroke-width="4" />
              <path class="opacity-75" fill="white" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            登录中...
          </span>
        </button>

        <!-- 默认账号提示 -->
        <div style="margin-top: 24px; text-align: center;">
          <p style="color: #6b7280; font-size: 12px;">默认账号：admin / 123456</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: false })

const router = useRouter()
const username = ref('')
const password = ref('')
const loading = ref(false)
const showPassword = ref(false)

const handleLogin = async () => {
  if (!username.value || !password.value) {
    alert('请输入用户名和密码')
    return
  }
  loading.value = true
  setTimeout(() => {
    if (username.value === 'admin' && password.value === '123456') {
      localStorage.setItem('token', 'mock-token')
      localStorage.setItem('user', JSON.stringify({ username: username.value }))
      router.push('/')
    } else {
      alert('用户名或密码错误')
    }
    loading.value = false
  }, 800)
}
</script>

<style scoped>
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.animate-spin {
  animation: spin 1s linear infinite;
}
</style>