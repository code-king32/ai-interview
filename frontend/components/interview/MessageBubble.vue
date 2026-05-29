<template>
  <div class="flex" :class="isUser ? 'justify-end' : 'justify-start'">
    <div class="flex gap-3 max-w-[70%]" :class="isUser ? 'flex-row-reverse' : ''">
      <!-- 头像 -->
      <div class="w-8 h-8 rounded-full flex items-center justify-center text-white text-sm flex-shrink-0"
           :class="isUser ? 'bg-green-500' : 'bg-blue-500'">
        {{ isUser ? '我' : 'AI' }}
      </div>
      
      <!-- 消息内容 -->
      <div class="rounded-lg shadow-sm p-4" :class="isUser ? 'bg-blue-500 text-white' : 'bg-white'">
        <div class="whitespace-pre-wrap">{{ message.content }}</div>
        
        <!-- 评分显示（仅 AI 消息） -->
        <div v-if="!isUser && message.scores" class="mt-3 pt-2 border-t border-gray-100">
          <div class="text-xs font-medium text-gray-600 mb-1">本题评分：</div>
          <div class="grid grid-cols-4 gap-2 text-xs">
            <div><span class="text-gray-500">正确性：</span><span class="font-medium">{{ message.scores.correctness }}/10</span></div>
            <div><span class="text-gray-500">深度：</span><span class="font-medium">{{ message.scores.depth }}/10</span></div>
            <div><span class="text-gray-500">逻辑：</span><span class="font-medium">{{ message.scores.logic }}/10</span></div>
            <div><span class="text-gray-500">实践：</span><span class="font-medium">{{ message.scores.practice }}/10</span></div>
          </div>
          <div v-if="message.scores.comment" class="text-xs text-gray-500 mt-1">
            {{ message.scores.comment }}
          </div>
        </div>
        
        <!-- 时间戳 -->
        <div class="text-xs mt-2" :class="isUser ? 'text-blue-100' : 'text-gray-400'">
          {{ formatTime(message.created_at) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Message {
  id: number
  role: 'interviewer' | 'candidate' | 'system'
  content: string
  scores?: {
    correctness: number
    depth: number
    logic: number
    practice: number
    comment?: string
  } | null
  created_at: string
}

const props = defineProps<{
  message: Message
}>()

const isUser = computed(() => props.message.role === 'candidate')

const formatTime = (isoString: string) => {
  const date = new Date(isoString)
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}
</script>