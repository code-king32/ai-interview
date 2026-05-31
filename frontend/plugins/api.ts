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

  // 响应拦截器：统一包装为 { code, message, data }
  api.interceptors.response.use(
    (response) => {
      // 204 No Content 直接返回
      if (response.status === 204) {
        response.data = { code: 0, message: 'success', data: null }
        return response
      }
      // auth 接口自身已返回 {code, data}，跳过包装
      const url = response.config.url || ''
      if (url.includes('/auth/')) return response
      // 空响应
      if (!response.data) {
        response.data = { code: 0, message: 'success', data: null }
        return response
      }
      response.data = { code: 0, message: 'success', data: response.data }
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
