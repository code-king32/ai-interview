<template>
  <div style="padding:24px;max-width:1000px;margin:0 auto">
    <h1 style="font-size:24px;font-weight:700;color:#18181B;margin-bottom:24px">AI 评估仪表盘</h1>

    <!-- 概览卡片 -->
    <div v-if="overview" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin-bottom:28px">
      <div v-for="s in overviewCards" :key="s.label" style="background:#FFF;border:1px solid #F0F0F3;border-radius:14px;padding:20px 22px;box-shadow:0 1px 2px rgba(0,0,0,0.03)">
        <div style="font-size:11px;color:#A1A1AA;text-transform:uppercase;letter-spacing:0.04em;font-weight:500;margin-bottom:8px">{{ s.label }}</div>
        <div style="font-size:28px;font-weight:700;color:#18181B">{{ s.value }}</div>
      </div>
    </div>

    <!-- 评分分布 -->
    <div v-if="distribution" style="background:#FFF;border:1px solid #F0F0F3;border-radius:14px;padding:24px;margin-bottom:20px;box-shadow:0 1px 2px rgba(0,0,0,0.03)">
      <h2 style="font-size:17px;font-weight:600;margin-bottom:20px">评分分布</h2>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px">
        <div v-for="(dist, dim) in distribution" :key="dim" style="text-align:center">
          <div style="font-size:13px;font-weight:600;color:#71717A;margin-bottom:12px">{{ dimLabel(dim) }}</div>
          <div v-for="(count, range) in dist" :key="range" style="display:flex;justify-content:space-between;margin-bottom:6px;font-size:12px">
            <span style="color:#A1A1AA">{{ range }}</span>
            <div style="flex:1;margin:0 8px;background:#F0F0F3;border-radius:2px;height:6px;align-self:center;overflow:hidden">
              <div :style="{width:maxBar(count)+'%',height:'100%',background:barColor(range),borderRadius:'2px'}"></div>
            </div>
            <span style="color:#18181B;font-weight:600">{{ count }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 高频话题 -->
    <div v-if="dataStats?.top_topics?.length" style="background:#FFF;border:1px solid #F0F0F3;border-radius:14px;padding:24px;margin-bottom:20px;box-shadow:0 1px 2px rgba(0,0,0,0.03)">
      <h2 style="font-size:17px;font-weight:600;margin-bottom:16px">高频考察话题</h2>
      <div style="display:flex;flex-wrap:wrap;gap:8px">
        <span v-for="t in dataStats.top_topics.slice(0,15)" :key="t.topic" style="padding:6px 14px;background:rgba(91,91,237,0.06);color:#5B5BED;border-radius:20px;font-size:13px;font-weight:500">
          {{ t.topic }} ({{ t.count }})
        </span>
      </div>
    </div>

    <!-- Prompt 版本 -->
    <div v-if="dataStats?.prompt_versions?.length" style="background:#FFF;border:1px solid #F0F0F3;border-radius:14px;padding:24px;box-shadow:0 1px 2px rgba(0,0,0,0.03)">
      <h2 style="font-size:17px;font-weight:600;margin-bottom:16px">Prompt 版本分布</h2>
      <div v-for="v in dataStats.prompt_versions" :key="v.version" style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #F0F0F3;font-size:14px">
        <span style="color:#18181B;font-weight:500">{{ v.version }}</span>
        <span style="color:#5B5BED;font-weight:600">{{ v.count }} 次</span>
      </div>
    </div>

    <div v-if="!overview" style="text-align:center;padding:60px;color:#A1A1AA">加载中...</div>
  </div>
</template>

<script setup lang="ts">
const { $api } = useNuxtApp()

const overview = ref<any>(null)
const distribution = ref<any>(null)
const dataStats = ref<any>(null)

const overviewCards = computed(() => {
  if (!overview.value) return []
  const d = overview.value
  return [
    { label:'总面试数', value:d.total_interviews },
    { label:'已完成', value:d.completed_interviews },
    { label:'完成率', value:d.completion_rate },
    { label:'平均消息', value:d.avg_messages_per_interview },
  ]
})

const dimLabel = (d: string) => ({correctness:'正确性',depth:'深度',logic:'逻辑',practice:'实践'} as any)[d]||d
const barColor = (r: string) => r === '8-10' ? '#10B981' : r === '6-7' ? '#5B5BED' : r === '4-5' ? '#F59E0B' : '#EF4444'
const maxBar = (count: number) => Math.min(100, count * 10)

onMounted(async () => {
  try {
    const [o, dist, stats] = await Promise.all([
      $api.get('/analytics/overview'),
      $api.get('/analytics/scores/distribution'),
      $api.get('/analytics/dataset/stats'),
    ])
    overview.value = o.data
    distribution.value = dist.data
    dataStats.value = stats.data
  } catch(e) { console.error(e) }
})
</script>
