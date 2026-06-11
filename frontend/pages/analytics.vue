<template>
  <div style="padding:24px;max-width:1000px;margin:0 auto">
    <h1 style="font-size:24px;font-weight:700;color:#18181B;margin-bottom:6px">AI 评估仪表盘</h1>
    <p style="color:#A1A1AA;font-size:14px;margin-bottom:28px">实时追踪 AI 面试质量和效果</p>

    <div v-if="!loaded" style="text-align:center;padding:80px;color:#A1A1AA">加载中...</div>

    <template v-else>
      <!-- 面试质量总览 -->
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:24px">
        <div v-for="c in topCards" :key="c.label" style="background:#FFF;border:1px solid #F0F0F3;border-radius:14px;padding:20px;text-align:center">
          <div style="font-size:36px;margin-bottom:6px">{{ c.icon }}</div>
          <div style="font-size:26px;font-weight:700;color:#18181B">{{ c.value }}</div>
          <div style="font-size:12px;color:#A1A1AA;margin-top:4px">{{ c.label }}</div>
        </div>
      </div>

      <!-- 评分维度雷达图 + 分布 -->
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:24px">
        <!-- 雷达图 -->
        <div style="background:#FFF;border:1px solid #F0F0F3;border-radius:14px;padding:24px;text-align:center">
          <h3 style="font-size:15px;font-weight:600;margin-bottom:16px;text-align:left">评分维度总览</h3>
          <div ref="radarRef" style="display:flex;justify-content:center"></div>
          <p v-if="!hasScores" style="color:#A1A1AA;font-size:13px;padding:40px 0">暂无面试评分数据</p>
        </div>
        <!-- 分布柱状图 -->
        <div style="background:#FFF;border:1px solid #F0F0F3;border-radius:14px;padding:24px">
          <h3 style="font-size:15px;font-weight:600;margin-bottom:16px">评分分布</h3>
          <div v-if="!hasScores" style="color:#A1A1AA;font-size:13px;text-align:center;padding:40px 0">暂无数据</div>
          <div v-else v-for="d in dimLabels" :key="d.key" style="margin-bottom:14px">
            <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px">
              <span style="color:#71717A">{{ d.label }}</span>
              <span style="font-weight:600" :style="{color:d.color}">{{ avgScores[d.key] }} / 10</span>
            </div>
            <div style="height:6px;background:#F0F0F3;border-radius:3px;overflow:hidden">
              <div :style="{width:(avgScores[d.key]*10)+'%',height:'100%',background:d.color,borderRadius:'3px',transition:'width 1s ease'}"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 高频话题 + 最近面试 -->
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
        <div style="background:#FFF;border:1px solid #F0F0F3;border-radius:14px;padding:24px">
          <h3 style="font-size:15px;font-weight:600;margin-bottom:16px">高频考察话题</h3>
          <div v-if="!topTopics.length" style="color:#A1A1AA;font-size:13px;text-align:center;padding:20px">暂无数据</div>
          <div v-else style="display:flex;flex-wrap:wrap;gap:8px">
            <span v-for="t in topTopics" :key="t.topic" style="padding:6px 14px;background:rgba(91,91,237,0.06);color:#5B5BED;border-radius:20px;font-size:13px;font-weight:500">{{ t.topic }} <span style="opacity:0.5">×{{ t.count }}</span></span>
          </div>
        </div>
        <div style="background:#FFF;border:1px solid #F0F0F3;border-radius:14px;padding:24px">
          <h3 style="font-size:15px;font-weight:600;margin-bottom:16px">数据规模</h3>
          <div style="display:flex;flex-direction:column;gap:12px">
            <div v-for="d in dataSizeCards" :key="d.label" style="display:flex;justify-content:space-between;align-items:center">
              <span style="font-size:14px;color:#71717A">{{ d.label }}</span>
              <span style="font-size:16px;font-weight:700;color:#18181B">{{ d.value }}</span>
            </div>
          </div>
          <div v-if="promptVersions.length" style="margin-top:20px;padding-top:16px;border-top:1px solid #F0F0F3">
            <div style="font-size:12px;color:#A1A1AA;margin-bottom:8px">Prompt 版本使用</div>
            <div v-for="v in promptVersions" :key="v.version" style="display:flex;justify-content:space-between;font-size:13px;padding:4px 0">
              <span style="color:#71717A">{{ v.version }}</span>
              <span style="font-weight:600;color:#5B5BED">{{ v.count }} 次</span>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
const { $api } = useNuxtApp()

const loaded = ref(false)
const hasScores = computed(() => Object.values(avgScores.value).some(v => v > 0))
const avgScores = ref({correctness:0,depth:0,logic:0,practice:0})
const interviewCount = ref(0)
const completedCount = ref(0)
const topTopics = ref<any[]>([])
const promptVersions = ref<any[]>([])
const radarRef = ref<HTMLElement>()

const dimLabels = [
  {key:'correctness',label:'正确性',color:'#10B981'},
  {key:'depth',label:'深度',color:'#5B5BED'},
  {key:'logic',label:'逻辑性',color:'#F59E0B'},
  {key:'practice',label:'实践',color:'#EF4444'},
]

const topCards = computed(() => [
  {icon:'🎯',value:interviewCount.value,label:'总面试数'},
  {icon:'✅',value:completedCount.value,label:'已完成'},
  {icon:'💬',value:avgScores.value.correctness?avgScores.value.correctness.toFixed(1):'-',label:'平均正确性'},
  {icon:'📊',value:hasScores.value?overallAvg.value.toFixed(1):'-',label:'综合评分'},
])

const overallAvg = computed(() => {
  const vals = Object.values(avgScores.value).filter(v=>v>0)
  return vals.length ? vals.reduce((a,b)=>a+b,0)/vals.length : 0
})

const dataSizeCards = computed(() => [
  {label:'累计消息数',value:topCards.value[0].value},
  {label:'评分记录数',value:hasScores.value?'有数据':'无'},
  {label:'Prompt 版本数',value:promptVersions.value.length||'-'},
  {label:'平均回答长度',value:'-' },
])

onMounted(async () => {
  try {
    const [o,d,s] = await Promise.all([
      $api.get('/analytics/overview'),
      $api.get('/analytics/scores/distribution'),
      $api.get('/analytics/dataset/stats'),
    ])
    const overview = o.data
    interviewCount.value = overview.total_interviews||0
    completedCount.value = overview.completed_interviews||0
    avgScores.value = overview.avg_scores||{correctness:0,depth:0,logic:0,practice:0}
    topTopics.value = s.data?.top_topics||[]
    promptVersions.value = s.data?.prompt_versions||[]
    // 画雷达图
    nextTick(() => drawRadar())
  } catch(e) { console.error(e) }
  finally { loaded.value = true }
})

const drawRadar = () => {
  if (!hasScores.value || !radarRef.value) return
  const dims = dimLabels.map(d => ({...d, score: avgScores.value[d.key]}))
  const n = dims.length, size = 200, cx = size/2, cy = size/2, r = 80
  const pt = (i:number, rad:number) => {
    const a = 2*Math.PI*i/n - Math.PI/2
    return {x:cx+rad*Math.cos(a), y:cy+rad*Math.sin(a)}
  }
  let grid='', axes=''
  for(let l=1;l<=4;l++){const ps=Array.from({length:n},(_,i)=>pt(i,r*l/4));grid+=`<polygon points="${ps.map(p=>p.x+','+p.y).join(' ')}" fill="none" stroke="#F0F0F3" stroke-width="1"/>`}
  for(let i=0;i<n;i++){const p=pt(i,r);axes+=`<line x1="${cx}" y1="${cy}" x2="${p.x}" y2="${p.y}" stroke="#F0F0F3" stroke-width="1"/>`}
  const dp = dims.map((d,i)=>pt(i,r*d.score/10))
  const poly = dp.map(p=>p.x+','+p.y).join(' ')
  const dots = dp.map(p=>`<circle cx="${p.x}" cy="${p.y}" r="3" fill="#5B5BED"/>`).join('')
  let labels=''
  dims.forEach((d,i)=>{const p=pt(i,r+18);labels+=`<text x="${p.x}" y="${p.y}" text-anchor="middle" fill="#71717A" font-size="11">${d.label}</text>`})
  radarRef.value.innerHTML = `<svg width="${size}" height="${size}">${grid}${axes}<polygon points="${poly}" fill="rgba(91,91,237,0.1)" stroke="#5B5BED" stroke-width="2"/>${dots}${labels}</svg>`
}
</script>
