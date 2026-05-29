<template>
  <div class="flex flex-col h-full bg-gray-50">
    <!-- 消息列表 -->
    <div class="flex-1 overflow-y-auto p-4 space-y-4" ref="messageContainer">
      <MessageBubble v-for="msg in messages" :key="msg.id" :message="msg" />
      
      <!-- 流式输出 -->
      <div v-if="isStreaming && streamContent" class="flex justify-start gap-3">
        <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white text-sm">
          AI
        </div>
        <div class="bg-white rounded-lg shadow-sm p-4 max-w-[70%]">
          <div class="whitespace-pre-wrap">
            {{ streamContent }}
            <span class="inline-block w-2 h-4 bg-blue-500 animate-pulse ml-1"></span>
          </div>
        </div>
      </div>
      
      <!-- 加载中 -->
      <div v-if="isLoading && !isStreaming" class="flex justify-start gap-3">
        <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white text-sm">
          AI
        </div>
        <div class="bg-white rounded-lg shadow-sm p-4">
          <div class="flex gap-1">
            <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>
            <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></span>
            <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 输入区域 -->
    <div v-if="canSend" class="bg-white border-t p-4">
      <div class="flex gap-3">
        <textarea v-model="inputMessage" @keydown.ctrl.enter="send"
          :placeholder="placeholder"
          class="flex-1 border rounded-lg px-4 py-3 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
          rows="3" :disabled="disabled">
        </textarea>
        <button @click="send" :disabled="!inputMessage.trim() || disabled"
          class="px-6 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 transition-colors">
          发送
        </button>
      </div>
      <div class="text-xs text-gray-400 mt-2 text-center">
        💡 提示：回答越详细具体，AI 面试官评分越准确
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import MessageBubble from './MessageBubble.vue'

interface Message {
  id: number
  role: 'interviewer' | 'candidate' | 'system'
  content: string
  scores?: any
  created_at: string
}

const props = defineProps<{
  messages: Message[]
  isStreaming?: boolean
  isLoading?: boolean
  streamContent?: string
  canSend?: boolean
  disabled?: boolean
  placeholder?: string
}>()

const emit = defineEmits<{
  send: [content: string]
}>()

const inputMessage = ref('')
const messageContainer = ref<HTMLElement>()

const send = () => {
  if (!inputMessage.value.trim()) return
  emit('send', inputMessage.value)
  inputMessage.value = ''
}

watch(() => props.messages.length, () => {
  nextTick(() => {
    if (messageContainer.value) {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight
    }
  })
})
</script>