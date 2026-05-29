// middleware/auth.ts
export default defineNuxtRouteMiddleware((to, from) => {
  // 只在客户端执行
  if (process.client) {
    // 如果是登录页面，直接放行
    if (to.path === '/login') {
      return
    }
    
    // 检查是否已登录
    const token = localStorage.getItem('token')
    if (!token) {
      return navigateTo('/login')
    }
  }
})