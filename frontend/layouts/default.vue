<template>
  <div class="app-layout">
    <!-- 顶部栏 -->
    <header class="app-header">
      <div class="header-left">
        <span class="logo">🤖</span>
        <span class="title">AI 面试系统</span>
      </div>
      <div class="header-right">
        <span>管理员</span>
        <button @click="logout">退出登录</button>
      </div>
    </header>

    <div class="layout-body">
      <!-- 左侧菜单 -->
      <aside class="sidebar">
        <nav>
          <NuxtLink to="/" class="menu-item" :class="{ active: $route.path === '/' }">
            <span>📊</span> 主界面
          </NuxtLink>
          <NuxtLink to="/jobs" class="menu-item" :class="{ active: $route.path.startsWith('/jobs') }">
            <span>📋</span> 岗位管理
          </NuxtLink>
          <NuxtLink to="/candidates" class="menu-item" :class="{ active: $route.path.startsWith('/candidates') }">
            <span>👥</span> 候选人管理
          </NuxtLink>
          <NuxtLink to="/interviews" class="menu-item" :class="{ active: $route.path.startsWith('/interviews') }">
            <span>🎯</span> 面试记录
          </NuxtLink>
        </nav>
      </aside>

      <!-- 右侧内容区（白色背景） -->
      <main class="main-content">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
const router = useRouter()
const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
/* 整体布局 */
.app-layout {
  min-height: 100vh;
  background: #f3f4f6;
  display: flex;
  flex-direction: column;
}

/* 顶部栏 */
.app-header {
  height: 60px;
  background: white;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  position: sticky;
  top: 0;
  z-index: 10;
}
.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.logo {
  font-size: 28px;
}
.title {
  font-size: 20px;
  font-weight: bold;
  color: #1f2937;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
  color: #4b5563;
}
.header-right button {
  background: none;
  border: none;
  color: #ef4444;
  cursor: pointer;
}
.header-right button:hover {
  color: #dc2626;
}

/* 主体：左侧菜单 + 右侧内容 */
.layout-body {
  display: flex;
  flex: 1;
}

/* 左侧菜单 */
.sidebar {
  width: 240px;
  background: white;
  border-right: 1px solid #e5e7eb;
  height: calc(100vh - 60px);
  position: sticky;
  top: 60px;
  overflow-y: auto;
}
.sidebar nav {
  padding: 16px 0;
}
.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 20px;
  color: #4b5563;
  text-decoration: none;
  transition: all 0.2s;
}
.menu-item:hover {
  background: #f3f4f6;
  color: #2563eb;
}
.menu-item.active {
  background: #eff6ff;
  color: #2563eb;
  border-right: 3px solid #2563eb;
}
.menu-item span:first-child {
  font-size: 20px;
}

/* 右侧内容区：白色背景 */
.main-content {
  background-color: white;
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  height: calc(100vh - 60px);
}
</style>