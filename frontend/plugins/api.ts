import axios from 'axios'

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()

  const api = axios.create({
    baseURL: config.public.apiBase,
    timeout: 60000,
  })

  // 请求拦截器：自动附加 role 参数 + ngrok 跳过警告
  api.interceptors.request.use((reqConfig) => {
    reqConfig.headers['ngrok-skip-browser-warning'] = 'true'
    let role = ''
    try {
      if (typeof window !== 'undefined') {
        role = localStorage.getItem('role') || ''
      }
    } catch (e) {}
    // SSR 回退：从 cookie 读取
    if (!role && typeof document !== 'undefined') {
      const match = document.cookie.match(/(?:^|;\s*)role=([^;]*)/)
      role = match ? match[1] : ''
    }
    if (role && reqConfig.url && !reqConfig.url!.includes('auth') && !reqConfig.url!.includes('invite')) {
      const sep = reqConfig.url!.includes('?') ? '&' : '?'
      reqConfig.url = `${reqConfig.url}${sep}role=${role}`
    }
    return reqConfig
  })

  // 响应拦截器：不再包装，直接透传
  api.interceptors.response.use(
    (response) => {
      if (response.status === 204) {
        response.data = { code: 0, message: 'success', data: null }
      }
      return response
    },
    (error) => {
      const detail = error.response?.data?.detail || error.message || '请求失败'
      return Promise.reject(error)
    },
  )

  return {
    provide: {
      api,
    },
  }
})
