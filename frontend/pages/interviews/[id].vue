<template>
  <div class="h-screen flex flex-col bg-gray-100">
    <!-- 头部 -->
    <header class="bg-white shadow-sm px-6 py-4 flex justify-between items-center">
      <div>
        <h1 class="text-xl font-semibold">AI 智能面试</h1>
        <p class="text-sm text-gray-500">面试进行中</p>
      </div>
      <button @click="endInterview" class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600">
        结束面试
      </button>
    </header>

    <!-- 聊天区域 -->
    <div class="flex-1 overflow-y-auto p-6" ref="chatContainer">
      <div class="max-w-4xl mx-auto space-y-4">
        <div v-for="msg in messages" :key="msg.id" class="flex" 
             :class="msg.role === 'candidate' ? 'justify-end' : 'justify-start'">
          <div class="max-w-[70%] rounded-lg p-3" 
               :class="msg.role === 'candidate' ? 'bg-blue-500 text-white' : 'bg-white border'">
            <div class="whitespace-pre-wrap">{{ msg.content }}</div>
            <div class="text-xs mt-1" :class="msg.role === 'candidate' ? 'text-blue-100' : 'text-gray-400'">
              {{ formatTime(msg.created_at) }}
            </div>
          </div>
        </div>
        
        <div v-if="isLoading" class="flex justify-start">
          <div class="bg-white rounded-lg p-3">
            <div class="flex gap-1">
              <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>
              <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></span>
              <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="bg-white border-t p-4">
      <div class="max-w-4xl mx-auto flex gap-3">
        <textarea v-model="inputMessage" @keydown.ctrl.enter="sendMessage"
          placeholder="输入你的回答... (Ctrl+Enter 发送)"
          class="flex-1 border rounded-lg px-4 py-2 resize-none focus:outline-none focus:ring-2 focus:ring-purple-500"
          rows="3"></textarea>
        <button @click="sendMessage" :disabled="!inputMessage.trim()"
          class="px-6 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50">
          发送
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const route = useRoute()
const { $api } = useNuxtApp()

const messages = ref([])
const inputMessage = ref('')
const isLoading = ref(false)
const chatContainer = ref(null)

const formatTime = (isoString) => {
  if (!isoString) return ''
  const date = new Date(isoString)
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

const sendMessage = async () => {
  if (!inputMessage.value.trim()) return
  const content = inputMessage.value
  inputMessage.value = ''
  
  messages.value.push({
    id: Date.now(),
    role: 'candidate',
    content: content,
    created_at: new Date().toISOString()
  })
  scrollToBottom()
  
  isLoading.value = true
  
  try {
    const res = await $api.post(`/interviews/${route.params.id}/messages`, { content })
    if (res.data.code === 0 && res.data.data.ai_message) {
      messages.value.push(res.data.data.ai_message)
      scrollToBottom()
    }
  } catch (error) {
    console.error('发送失败:', error)
    alert('发送失败，请重试')
  } finally {
    isLoading.value = false
  }
}

const endInterview = async () => {
  if (confirm('确定要结束面试吗？')) {
    try {
      await $api.post(`/interviews/${route.params.id}/end`)
      alert('面试已结束')
      await navigateTo('/interviews')
    } catch (error) {
      console.error('结束失败:', error)
    }
  }
}

const loadMessages = async () => {
  try {
    const res = await $api.get(`/interviews/${route.params.id}`)
    if (res.data.code === 0) {
      messages.value = res.data.data.messages || []
      scrollToBottom()
    }
  } catch (error) {
    console.error('加载消息失败:', error)
  }
}

onMounted(loadMessages)
</script>

<style scoped>
@keyframes bounce {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-10px); }
}
.animate-bounce {
  animation: bounce 1s ease infinite;
}
</style>