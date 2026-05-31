<template>
  <div style="max-width: 900px; margin: 0 auto;">
    <!-- ═══════════ HR 视图 ═══════════ -->
    <template v-if="isHR">
      <div style="text-align: center; padding: 40px 0 32px;">
        <div style="font-size: 44px; margin-bottom: 12px;">🏢</div>
        <h1 style="font-size: 28px; font-weight: 700; color: #18181B; letter-spacing: -0.025em; margin-bottom: 8px;">AI 面试管理</h1>
        <p style="font-size: 15px; color: #71717A; max-width: 500px; margin: 0 auto; line-height: 1.7;">
          创建岗位，邀请候选人，AI 自动完成面试并生成评估报告
        </p>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 28px;">
        <NuxtLink to="/jobs" style="background: linear-gradient(135deg, #5B5BED, #7C3AED); border-radius: 14px; padding: 28px; color: #FFF; text-decoration: none; box-shadow: 0 8px 24px rgba(91,91,237,0.2);">
          <div style="font-size: 32px; margin-bottom: 10px;">📋</div>
          <div style="font-size: 18px; font-weight: 700; margin-bottom: 4px;">岗位管理</div>
          <div style="font-size: 13px; opacity: 0.85;">创建岗位，生成邀请链接</div>
        </NuxtLink>
        <NuxtLink to="/interviews" style="background: linear-gradient(135deg, #10B981, #059669); border-radius: 14px; padding: 28px; color: #FFF; text-decoration: none; box-shadow: 0 8px 24px rgba(16,185,129,0.2);">
          <div style="font-size: 32px; margin-bottom: 10px;">📊</div>
          <div style="font-size: 18px; font-weight: 700; margin-bottom: 4px;">面试记录</div>
          <div style="font-size: 13px; opacity: 0.85;">查看候选人面试报告</div>
        </NuxtLink>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin-bottom: 24px;">
        <div v-for="s in hrStats" :key="s.label" style="background: #FFF; border: 1px solid #F0F0F3; border-radius: 12px; padding: 18px 20px;">
          <div style="font-size: 11px; color: #A1A1AA; text-transform: uppercase; letter-spacing: 0.04em; font-weight: 500; margin-bottom: 6px;">{{ s.label }}</div>
          <div style="font-size: 28px; font-weight: 700; color: #18181B;">{{ s.value }}</div>
        </div>
      </div>
    </template>

    <!-- ═══════════ 求职者视图 ═══════════ -->
    <template v-else>
      <div style="text-align: center; padding: 40px 0 32px;">
        <div style="font-size: 44px; margin-bottom: 12px;">🤖</div>
        <h1 style="font-size: 28px; font-weight: 700; color: #18181B; letter-spacing: -0.025em; margin-bottom: 8px;">AI 面试陪练</h1>
        <p style="font-size: 15px; color: #71717A; max-width: 500px; margin: 0 auto; line-height: 1.7;">
          模拟真实技术面试，根据目标岗位和你的简历，AI 面试官针对性提问、评分并给出改进建议。
        </p>
      </div>

      <div style="background: linear-gradient(135deg, #5B5BED, #7C3AED); border-radius: 16px; padding: 28px 32px; margin-bottom: 28px; color: #FFF; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 20px; box-shadow: 0 8px 32px rgba(91,91,237,0.25);">
        <div>
          <div style="font-size: 18px; font-weight: 700; margin-bottom: 6px;">开始一场模拟面试</div>
          <div style="font-size: 13px; opacity: 0.85;">粘贴目标岗位 JD，上传你的简历，AI 将模拟真实技术面试</div>
        </div>
        <div style="display: flex; gap: 12px; flex-wrap: wrap;">
          <NuxtLink to="/interviews/create" style="background: #FFF; color: #5B5BED; padding: 12px 24px; border-radius: 10px; font-weight: 600; font-size: 14px; text-decoration: none;display:inline-flex;align-items:center;gap:6px;box-shadow: 0 4px 12px rgba(0,0,0,0.1);">🚀 快速开始</NuxtLink>
          <NuxtLink to="/jobs" style="background: rgba(255,255,255,0.15); color: #FFF; padding: 12px 24px; border-radius: 10px; font-weight: 500; font-size: 14px; text-decoration: none;display:inline-flex;align-items:center;gap:6px;border:1px solid rgba(255,255,255,0.25);">管理目标岗位 →</NuxtLink>
        </div>
      </div>
    </template>

    <!-- 共用的面试记录列表 -->
    <div style="background: #FFF; border: 1px solid #F0F0F3; border-radius: 16px; padding: 24px 28px; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px;">
        <h2 style="font-size: 17px; font-weight: 600; color: #18181B;">{{ isHR ? '最近面试' : '最近练习' }}</h2>
        <NuxtLink to="/interviews" style="font-size: 13px; color: #5B5BED; text-decoration: none; font-weight: 500;">查看全部 →</NuxtLink>
      </div>
      <div v-if="!recent.length" style="text-align: center; padding: 40px; color: #A1A1AA;">
        <div style="font-size: 36px; margin-bottom: 10px;">{{ isHR ? '📋' : '📝' }}</div>
        <p style="font-size: 14px;">{{ isHR ? '还没有面试记录' : '还没有练习记录' }}</p>
      </div>
      <div v-else style="display: flex; flex-direction: column; gap: 8px;">
        <div v-for="iv in recent" :key="iv.id" style="display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; background: #F5F5F7; border-radius: 10px; gap: 12px;">
          <div style="display: flex; align-items: center; gap: 10px; min-width: 0;">
            <span :style="statusDot(normalize(iv.status))" style="width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0;"></span>
            <div style="min-width: 0;">
              <div style="font-size: 14px; font-weight: 500; color: #18181B; overflow: hidden; text-overflow: ellipsis;">{{ iv.job_title || '岗位 #'+iv.job_id }} · {{ iv.candidate_name || '候选人 #'+iv.candidate_id }}</div>
              <div style="font-size: 12px; color: #A1A1AA;">{{ fmtDate(iv.created_at) }}</div>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 8px; flex-shrink: 0;">
            <span :style="statusBadge(normalize(iv.status))" style="padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: 500;">{{ statusLabel(normalize(iv.status)) }}</span>
            <span v-if="iv.overall_score" style="font-size: 14px; font-weight: 700; color: #5B5BED;">{{ scoreAvg(iv.overall_score) }}</span>
            <NuxtLink :to="normalize(iv.status)==='completed'?`/reports/${iv.id}`:`/interviews/${iv.id}`" style="font-size: 12px; color: #5B5BED; text-decoration: none; font-weight: 500; flex-shrink: 0;">
              {{ normalize(iv.status)==='completed'?'报告':'继续' }}
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { $api } = useNuxtApp()
const recent = ref<any[]>([])
const hrStats = ref<any[]>([])
const skStats = ref<any[]>([])

const isHR = ref(false)
onMounted(() => { isHR.value = (localStorage.getItem('role') || '') === 'hr' })

const normalize = (s: string) => String(s || '').toLowerCase()
const statusDot = (s: string) => ({completed:{background:'#10B981'},in_progress:{background:'#5B5BED'},pending:{background:'#F59E0B'}})[s]||{background:'#D1D5DB'}
const statusBadge = (s: string) => ({completed:{background:'#D1FAE5',color:'#065F46'},in_progress:{background:'#DBEAFE',color:'#1E40AF'},pending:{background:'#FED7AA',color:'#9A3412'}})[s]||{}
const statusLabel = (s: string) => ({completed:'已完成',in_progress:'进行中',pending:'待开始'} as Record<string,string>)[s]||s
const fmtDate = (d: string) => d ? new Date(d).toLocaleDateString('zh-CN') : '-'
const scoreAvg = (s: any) => {
  if (typeof s === 'object') { const dims=['technical','communication','learning','match']; const vals=dims.map((d:string)=>Number(s[d])||0).filter((v:number)=>v>0); return vals.length?(vals.reduce((a:number,b:number)=>a+b,0)/vals.length).toFixed(1):'-' }
  return Number(s).toFixed(1)
}

onMounted(async () => {
  try {
    const [intRes, jobRes] = await Promise.all([$api.get('/interviews'),$api.get('/jobs')])
    const ints: any[] = intRes.data.data||[]
    const jobs: any[] = jobRes.data.data||[]
    const scored = ints.filter((i:any)=>i.overall_score)
    hrStats.value = [
      { label:'岗位数量', value:jobs.length },
      { label:'面试总数', value:ints.length },
      { label:'已完成', value:ints.filter((i:any)=>normalize(i.status)==='completed').length },
      { label:'待面试', value:ints.filter((i:any)=>normalize(i.status)==='pending').length },
    ]
    recent.value = ints.slice(-5).reverse()
  } catch(e) { console.error(e) }
})
</script>
