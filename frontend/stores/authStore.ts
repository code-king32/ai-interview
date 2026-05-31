import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
  // 初始化时直接从 localStorage 读取
  const storedRole = typeof window !== 'undefined' ? (localStorage.getItem('role') || '') : ''
  const storedUser = typeof window !== 'undefined' ? (localStorage.getItem('user') || '{}') : '{}'
  let storedName = ''
  try { storedName = JSON.parse(storedUser).username || '' } catch {}
  console.log('[authStore] init: role="' + storedRole + '" isHR=' + (storedRole === 'hr'))

  const role = ref(storedRole)
  const username = ref(storedName)
  const isHR = computed(() => role.value === 'hr')
  const isLoggedIn = computed(() => !!role.value && role.value !== '')

  const login = (r: string, name: string) => {
    role.value = r
    username.value = name
    localStorage.setItem('role', r)
    localStorage.setItem('token', 'ok')
    localStorage.setItem('user', JSON.stringify({ username: name }))
  }

  const logout = () => {
    role.value = ''
    username.value = ''
    localStorage.clear()
  }

  return { role, username, isHR, isLoggedIn, login, logout }
})
