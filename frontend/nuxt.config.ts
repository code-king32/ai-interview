export default defineNuxtConfig({
  ssr: false,
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  modules: ['@pinia/nuxt'],
  nitro: {
    output: {
      dir: 'dist'
    }
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || '/api'
    }
  }
})