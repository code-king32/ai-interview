import axios from 'axios'

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  
  const api = axios.create({
    baseURL: config.public.apiBase,
    timeout: 30000,
  })
  
  return {
    provide: {
      api
    }
  }
})