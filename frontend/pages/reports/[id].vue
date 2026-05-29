<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <div class="bg-white rounded-lg shadow p-6">
      <!-- 加载状态 -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
        <p class="text-gray-500 mt-4">加载报告中...</p>
      </div>

      <!-- 报告内容 -->
      <div v-else-if="report">
        <!-- 标题 -->
        <div class="text-center mb-8">
          <h1 class="text-3xl font-bold text-gray-900">面试报告</h1>
          <p class="text-gray-500 mt-2">
            {{ report.candidate?.name }} - {{ report.job?.title }}
          </p>
          <p class="text-gray-400 text-sm">生成时间：{{ formatDate(report.generated_at) }}</p>
        </div>

        <!-- 总体评分 -->
        <div class="mb-8">
          <h2 class="text-xl font-semibold mb-4">总体评分</h2>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="text-center p-4 bg-blue-50 rounded-lg">
              <div class="text-2xl font-bold text-blue-600">{{ report.overall_score?.technical || 0 }}</div>
              <div class="text-sm text-gray-600">技术能力</div>
            </div>
            <div class="text-center p-4 bg-green-50 rounded-lg">
              <div class="text-2xl font-bold text-green-600">{{ report.overall_score?.communication || 0 }}</div>
              <div class="text-sm text-gray-600">沟通表达</div>
            </div>
            <div class="text-center p-4 bg-purple-50 rounded-lg">
              <div class="text-2xl font-bold text-purple-600">{{ report.overall_score?.learning || 0 }}</div>
              <div class="text-sm text-gray-600">学习潜力</div>
            </div>
            <div class="text-center p-4 bg-orange-50 rounded-lg">
              <div class="text-2xl font-bold text-orange-600">{{ report.overall_score?.match || 0 }}</div>
              <div class="text-sm text-gray-600">岗位匹配</div>
            </div>
          </div>
          
          <div class="mt-4 p-4 rounded-lg" :class="getRecommendationClass(report.overall_score?.recommendation)">
            <div class="font-semibold">录用建议：{{ report.overall_score?.recommendation || '待评估' }}</div>
            <div class="text-gray-700 mt-2">{{ report.overall_score?.summary || '暂无评价' }}</div>
          </div>
        </div>

        <!-- 问答详情 -->
        <div>
          <h2 class="text-xl font-semibold mb-4">问答详情</h2>
          <div class="space-y-4">
            <div v-for="detail in report.question_details" :key="detail.question_number" class="border rounded-lg p-4">
              <div class="font-semibold text-purple-600">第 {{ detail.question_number }} 题</div>
              <div class="mt-2"><span class="font-medium">问题：</span>{{ detail.question }}</div>
              <div class="mt-2"><span class="font-medium">回答：</span>{{ detail.answer || '无回答' }}</div>
              <div class="mt-2 flex flex-wrap gap-3 text-sm">
                <span class="text-gray-600">正确性: {{ detail.scores?.correctness || 0 }}/10</span>
                <span class="text-gray-600">深度: {{ detail.scores?.depth || 0 }}/10</span>
                <span class="text-gray-600">逻辑: {{ detail.scores?.logic || 0 }}/10</span>
                <span class="text-gray-600">实践: {{ detail.scores?.practice || 0 }}/10</span>
              </div>
              <div v-if="detail.comment" class="mt-2 text-gray-600 text-sm bg-gray-50 p-2 rounded">
                {{ detail.comment }}
              </div>
            </div>
          </div>
        </div>

        <!-- 面试信息 -->
        <div class="mt-8 pt-4 border-t text-center text-sm text-gray-400">
          <p>总题数：{{ report.total_questions || 0 }} 题 | 时长：{{ report.duration || '未知' }}</p>
        </div>
      </div>

      <!-- 错误状态 -->
      <div v-else-if="error" class="text-center py-12">
        <p class="text-red-500">{{ error }}</p>
        <NuxtLink to="/interviews" class="text-purple-500 hover:underline mt-4 inline-block">
          返回面试列表
        </NuxtLink>
      </div>

      <!-- 按钮 -->
      <div class="mt-8 flex justify-center gap-4">
        <button @click="$router.back()" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
          返回
        </button>
        <NuxtLink to="/interviews" class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700">
          面试列表
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
const route = useRoute()
const { $api } = useNuxtApp()

const report = ref(null)
const loading = ref(true)
const error = ref(null)

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}

const getRecommendationClass = (recommendation) => {
  const classes = {
    '强烈推荐': 'bg-green-50 border border-green-200',
    '推荐': 'bg-blue-50 border border-blue-200',
    '保留': 'bg-yellow-50 border border-yellow-200',
    '不推荐': 'bg-red-50 border border-red-200'
  }
  return classes[recommendation] || 'bg-gray-50'
}

const loadReport = async () => {
  loading.value = true
  error.value = null
  
  try {
    const res = await $api.get(`/reports/${route.params.id}`)
    if (res.data.code === 0) {
      report.value = res.data.data
    } else {
      error.value = res.data.message || '加载报告失败'
    }
  } catch (err) {
    console.error('加载报告失败:', err)
    error.value = '无法连接到服务器，请确保后端服务已启动'
  } finally {
    loading.value = false
  }
}

onMounted(loadReport)
</script>