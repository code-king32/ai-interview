<template>
  <div class="bg-white rounded-lg shadow p-4">
    <h3 class="font-semibold text-gray-800 mb-3">实时评分</h3>
    
    <div class="space-y-3">
      <div v-for="dimension in dimensions" :key="dimension.key" class="space-y-1">
        <div class="flex justify-between text-sm">
          <span class="text-gray-600">{{ dimension.label }}</span>
          <span class="font-medium" :class="getScoreColor(scores[dimension.key])">
            {{ scores[dimension.key] || 0 }}/10
          </span>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2">
          <div class="h-2 rounded-full transition-all duration-500"
               :class="getProgressColor(scores[dimension.key])"
               :style="{ width: `${((scores[dimension.key] || 0) / 10) * 100}%` }">
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="totalScore" class="mt-4 pt-3 border-t">
      <div class="flex justify-between items-center">
        <span class="font-semibold text-gray-800">综合得分</span>
        <span class="text-xl font-bold text-blue-600">{{ totalScore.toFixed(1) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Scores {
  correctness: number
  depth: number
  logic: number
  practice: number
}

const props = defineProps<{
  scores: Partial<Scores>
}>()

const dimensions = [
  { key: 'correctness', label: '正确性' },
  { key: 'depth', label: '深度' },
  { key: 'logic', label: '逻辑' },
  { key: 'practice', label: '实践' }
]

const totalScore = computed(() => {
  const values = Object.values(props.scores).filter(v => typeof v === 'number')
  if (values.length === 0) return null
  return values.reduce((a, b) => a + b, 0) / values.length
})

const getScoreColor = (score: number) => {
  if (score >= 8) return 'text-green-600'
  if (score >= 6) return 'text-yellow-600'
  return 'text-red-600'
}

const getProgressColor = (score: number) => {
  if (score >= 8) return 'bg-green-500'
  if (score >= 6) return 'bg-yellow-500'
  return 'bg-red-500'
}
</script>