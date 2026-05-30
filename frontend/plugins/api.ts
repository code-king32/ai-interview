import axios from 'axios'

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()

  const api = axios.create({
    baseURL: config.public.apiBase,
    timeout: 60000,
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
