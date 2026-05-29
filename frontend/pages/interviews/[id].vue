<template>
  <div style="background: white; border-radius: 12px; box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05); padding: 24px;">
    <!-- 头部 -->
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
      <div>
        <h1 style="font-size: 24px; font-weight: bold; color: #1f2937;">AI 智能面试</h1>
        <p style="color: #6b7280; margin-top: 4px;">{{ interviewInfo }}</p>
      </div>
      <button
        v-if="status !== 'completed'"
        @click="endInterview"
        style="background-color: #ef4444; color: white; padding: 8px 16px; border-radius: 8px; border: none; cursor: pointer;"
      >
        结束面试
      </button>
    </div>

    <!-- 聊天区域 -->
    <div ref="chatContainer" style="height: 500px; overflow-y: auto; background: #f9fafb; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
      <div v-for="msg in messages" :key="msg.id" style="margin-bottom: 16px; display: flex;" :class="{ 'justify-end': msg.role === 'candidate' }">
        <div
          :style="msg.role === 'interviewer'
            ? { background: 'white', border: '1px solid #e5e7eb', padding: '12px 16px', borderRadius: '12px', maxWidth: '70%', color: '#1f2937' }
            : { background: '#2563eb', padding: '12px 16px', borderRadius: '12px', maxWidth: '70%', color: 'white' }"
        >
          <div style="font-size: 14px; white-space: pre-wrap;">{{ msg.content }}</div>
          <div style="font-size: 12px; margin-top: 4px; opacity: 0.7;">{{ formatTime(msg.created_at) }}</div>
        </div>
      </div>
      <div v-if="isLoading" style="display: flex; justify-content: flex-start;">
        <div style="background: white; border: 1px solid #e5e7eb; padding: 12px 16px; border-radius: 12px;">
          <span>AI 正在思考...</span>
        </div>
      </div>
    </div>

    <!-- 输入区域（仅进行中） -->
    <div v-if="status === 'in_progress'" style="display: flex; gap: 12px;">
      <textarea
        v-model="inputMessage"
        @keydown.ctrl.enter="sendMessage"
        placeholder="输入你的回答... (Ctrl+Enter 发送)"
        style="flex: 1; border: 1px solid #d1d5db; border-radius: 8px; padding: 12px; resize: none; font-size: 14px;"
        rows="3"
      ></textarea>
      <button
        @click="sendMessage"
        :disabled="!inputMessage.trim()"
        style="background-color: #2563eb; color: white; padding: 0 24px; border-radius: 8px; border: none; cursor: pointer; font-size: 16px;"
      >
        发送
      </button>
    </div>

    <!-- 面试已完成提示 -->
    <div v-if="status === 'completed'" style="text-align: center; padding: 20px; background: #f0fdf4; border-radius: 8px;">
      <p style="color: #166534;">面试已完成！</p>
      <NuxtLink :to="`/reports/${route.params.id}`" style="color: #2563eb; margin-top: 8px; display: inline-block;">查看报告 →</NuxtLink>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const { $api } = useNuxtApp()

const messages = ref([])
const status = ref('pending')
const isLoading = ref(false)
const inputMessage = ref('')
const chatContainer = ref(null)
const interviewInfo = ref('加载中...')

const formatTime = (iso) => iso ? new Date(iso).toLocaleTimeString() : ''

const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  })
}

// 发送消息
const sendMessage = async () => {
  if (!inputMessage.value.trim()) return
  const content = inputMessage.value
  inputMessage.value = ''

  messages.value.push({
    id: Date.now(),
    role: 'candidate',
    content,
    created_at: new Date().toISOString()
  })
  scrollToBottom()

  isLoading.value = true
  try {
    const res = await $api.post(`/interviews/${route.params.id}/messages`, { content })
    if (res.data.code === 0 && res.data.data.ai_message) {
      messages.value.push(res.data.data.ai_message)
    } else {
      // 模拟回复
      messages.value.push({
        id: Date.now(),
        role: 'interviewer',
        content: '感谢您的回答，我们继续下一个问题。',
        created_at: new Date().toISOString()
      })
    }
    scrollToBottom()
  } catch (err) {
    console.error('发送失败', err)
    alert('发送失败，请重试')
  } finally {
    isLoading.value = false
  }
}

// 结束面试（重点修改）
const endInterview = async () => {
  if (confirm('确定要结束面试吗？')) {
    try {
      await $api.post(`/interviews/${route.params.id}/end`)
      // 成功后跳转到面试记录页面
      await router.push('/interviews')
    } catch (err) {
      console.error('结束失败', err)
      alert('结束失败，即将返回面试记录页面')
      // 即使失败也跳转，让用户刷新列表（后端未就绪时可模拟）
      await router.push('/interviews')
    }
  }
}

// 加载面试信息
const loadInterview = async () => {
  try {
    const res = await $api.get(`/interviews/${route.params.id}`)
    if (res.data.code === 0) {
      const data = res.data.data
      status.value = data.status
      messages.value = data.messages || []
      const jobRes = await $api.get(`/jobs/${data.job_id}`)
      const candidateRes = await $api.get(`/candidates/${data.candidate_id}`)
      interviewInfo.value = `${jobRes.data.data.title} · ${candidateRes.data.data.name}`
      scrollToBottom()
    } else {
      // 模拟数据（后端未就绪）
      status.value = 'in_progress'
      messages.value = [
        { id: 1, role: 'interviewer', content: '您好，欢迎参加面试。请先简单介绍一下自己。', created_at: new Date().toISOString() }
      ]
      interviewInfo.value = '示例岗位 · 候选人'
      scrollToBottom()
    }
  } catch (err) {
    console.warn('后端未就绪，使用模拟数据', err)
    status.value = 'in_progress'
    messages.value = [
      { id: 1, role: 'interviewer', content: '您好，欢迎参加面试。请先简单介绍一下自己。', created_at: new Date().toISOString() }
    ]
    interviewInfo.value = '示例岗位 · 候选人'
    scrollToBottom()
  }
}

onMounted(loadInterview)
</script>