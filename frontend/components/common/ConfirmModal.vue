<template>
  <div v-if="visible" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 w-full max-w-md">
      <h3 class="text-xl font-semibold mb-2">{{ title }}</h3>
      <p class="text-gray-600 mb-6">{{ message }}</p>
      <div class="flex justify-end gap-3">
        <button @click="onCancel" class="px-4 py-2 border rounded-lg hover:bg-gray-50">
          {{ cancelText }}
        </button>
        <button @click="onConfirm" class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600">
          {{ confirmText }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  visible: boolean
  title?: string
  message?: string
  confirmText?: string
  cancelText?: string
}>(), {
  title: '确认操作',
  message: '确定要执行此操作吗？',
  confirmText: '确定',
  cancelText: '取消'
})

const emit = defineEmits<{
  confirm: []
  cancel: []
}>()

const onConfirm = () => emit('confirm')
const onCancel = () => emit('cancel')
</script>