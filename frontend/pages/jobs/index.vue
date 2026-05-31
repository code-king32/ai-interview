<template>
  <div style="padding:24px">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:24px">
      <h1 style="font-size:24px;font-weight:700;color:#18181B">岗位列表</h1>
      <button @click="openCreate" style="background:#5B5BED;color:#FFF;border:none;padding:10px 20px;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer">+ 添加岗位</button>
    </div>

    <div v-if="loading">加载中...</div>

    <div v-else-if="jobs.length === 0" style="text-align:center;padding:60px;color:#A1A1AA">
      <p>还没有岗位</p>
    </div>

    <table v-else style="width:100%;border-collapse:collapse">
      <thead style="background:#F5F5F7">
        <tr>
          <th style="padding:12px 16px;text-align:left;font-size:12px;color:#71717A">ID</th>
          <th style="padding:12px 16px;text-align:left;font-size:12px;color:#71717A">岗位名称</th>
          <th style="padding:12px 16px;text-align:left;font-size:12px;color:#71717A">描述</th>
          <th style="padding:12px 16px;text-align:left;font-size:12px;color:#71717A">技能要求</th>
          <th style="padding:12px 16px;text-align:left;font-size:12px;color:#71717A">操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="j in jobs" :key="j.id" style="border-bottom:1px solid #F0F0F3">
          <td style="padding:12px 16px;font-size:14px">{{ j.id }}</td>
          <td style="padding:12px 16px;font-size:14px;font-weight:500">{{ j.title }}</td>
          <td style="padding:12px 16px;font-size:13px;color:#71717A;max-width:250px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{{ j.description || '-' }}</td>
          <td style="padding:12px 16px;font-size:13px;color:#71717A;max-width:250px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{{ j.requirements || '-' }}</td>
          <td style="padding:12px 16px;font-size:13px;display:flex;gap:8px">
            <button @click="openInvite(j)" style="color:#10B981;background:none;border:none;cursor:pointer">邀请</button>
            <button @click="delJob(j.id)" style="color:#EF4444;background:none;border:none;cursor:pointer">删除</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 创建弹窗 -->
    <div v-if="modal" style="position:fixed;inset:0;background:rgba(0,0,0,0.5);display:flex;align-items:center;justify-content:center;z-index:50" @click.self="modal=false">
      <div style="background:#FFF;border-radius:12px;padding:24px;width:100%;max-width:500px">
        <h2 style="font-size:18px;font-weight:700;margin-bottom:16px">添加岗位</h2>
        <input v-model="form.title" placeholder="岗位名称" style="width:100%;padding:10px;border:1px solid #E8E8ED;border-radius:8px;margin-bottom:12px;font-size:14px" />
        <textarea v-model="form.description" placeholder="岗位描述" rows="3" style="width:100%;padding:10px;border:1px solid #E8E8ED;border-radius:8px;margin-bottom:12px;font-size:14px;resize:vertical"></textarea>
        <textarea v-model="form.requirements" placeholder="技能要求" rows="3" style="width:100%;padding:10px;border:1px solid #E8E8ED;border-radius:8px;margin-bottom:16px;font-size:14px;resize:vertical"></textarea>
        <div style="display:flex;gap:8px;justify-content:flex-end">
          <button @click="modal=false" style="padding:8px 16px;border:1px solid #E8E8ED;border-radius:8px;background:#FFF">取消</button>
          <button @click="createJob" style="padding:8px 20px;background:#5B5BED;color:#FFF;border:none;border-radius:8px">保存</button>
        </div>
      </div>
    </div>

    <!-- 邀请弹窗 -->
    <div v-if="inviteModal" style="position:fixed;inset:0;background:rgba(0,0,0,0.5);display:flex;align-items:center;justify-content:center;z-index:50" @click.self="inviteModal=false">
      <div style="background:#FFF;border-radius:12px;padding:24px;width:100%;max-width:480px">
        <h2 style="font-size:18px;font-weight:700;margin-bottom:4px">邀请候选⼈</h2>
        <p style="font-size:13px;color:#A1A1AA;margin-bottom:16px">{{ inviteJob?.title }}</p>
        <button v-if="!inviteLink" @click="genInvite" :disabled="genLoading" style="width:100%;padding:12px;background:#5B5BED;color:#FFF;border:none;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer">{{ genLoading?'生成中...':'生成邀请链接' }}</button>
        <div v-else>
          <input :value="inviteLink" readonly style="width:100%;padding:10px;border:1px solid #10B981;border-radius:8px;font-size:13px;color:#059669;background:#F0FDF4;margin-bottom:8px" @focus="$event.target.select()" />
          <div style="display:flex;gap:8px">
            <button @click="copyLink" style="flex:1;padding:10px;background:#10B981;color:#FFF;border:none;border-radius:8px;font-size:14px;cursor:pointer">{{ copied?'已复制':'复制链接' }}</button>
            <button @click="inviteModal=false" style="padding:10px 16px;border:1px solid #E8E8ED;border-radius:8px;background:#FFF;font-size:14px">关闭</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { $api } = useNuxtApp()

const jobs = ref<any[]>([])
const loading = ref(false)
const modal = ref(false)
const form = ref({ title:'', description:'', requirements:'' })
const inviteModal = ref(false)
const inviteJob = ref<any>(null)
const inviteLink = ref('')
const genLoading = ref(false)
const copied = ref(false)

const fetchJobs = async () => {
  loading.value = true
  try {
    const res = await $api.get('/jobs')
    const data = res.data
    // 兼容多种响应格式
    jobs.value = Array.isArray(data) ? data : Array.isArray(data?.data) ? data.data : Array.isArray(data?.data?.data) ? data.data.data : []
    console.log('Jobs loaded:', jobs.value.length)
  } catch(e) { console.error(e) }
  finally { loading.value = false }
}

const openCreate = () => { form.value = { title:'', description:'', requirements:'' }; modal.value = true }

const createJob = async () => {
  if (!form.value.title.trim()) return
  try {
    await $api.post('/jobs', form.value)
    modal.value = false
    await fetchJobs()
  } catch(e) { alert('创建失败') }
}

const delJob = async (id: number) => {
  if (!confirm('确定删除？')) return
  try { await $api.delete(`/jobs/${id}`); await fetchJobs() }
  catch(e) { alert('删除失败') }
}

const openInvite = (job: any) => { inviteJob.value = job; inviteLink.value = ''; inviteModal.value = true }

const genInvite = async () => {
  genLoading.value = true
  try {
    const res = await $api.post(`/jobs/${inviteJob.value.id}/invite`)
    inviteLink.value = window.location.origin + res.data.data.url
  } catch(e) { alert('生成失败') }
  finally { genLoading.value = false }
}

const copyLink = async () => { await navigator.clipboard.writeText(inviteLink.value); copied.value = true; setTimeout(()=>{copied.value=false},2000) }

onMounted(fetchJobs)
</script>
