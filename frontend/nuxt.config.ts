export default defineNuxtConfig({
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],  // 确保这一行存在
  modules: ['@pinia/nuxt'],
  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000/api'
    }
  }
})