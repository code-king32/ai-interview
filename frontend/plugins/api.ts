import axios from 'axios'

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()

  const api = axios.create({
    baseURL: config.public.apiBase,
    timeout: 60000,
  })

  // 请求拦截器：自动附加 role 参数
  api.interceptors.request.use((reqConfig) => {
    let role = ''
    try {
      if (typeof window !== 'undefined') {
        role = localStorage.getItem('role') || ''
      }
    } catch (e) {}
    if (role && reqConfig.url && !reqConfig.url!.startsWith('/api/auth') && !reqConfig.url!.startsWith('/api/invite')) {
      const sep = reqConfig.url!.includes('?') ? '&' : '?'
      reqConfig.url = `${reqConfig.url}${sep}role=${role}`
    }
    return reqConfig
  })

  // 响应拦截器：统一包装为 { code, message, data }
  api.interceptors.response.use(
    (response) => {
      // 204 No Content 或其他空响应直接返回
      if (response.status === 204 || !response.data) {
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
