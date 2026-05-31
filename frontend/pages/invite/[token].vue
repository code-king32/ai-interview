<template>
  <div class="invite-bg">
    <!-- Step 1: 填写信息 -->
    <div v-if="step === 'form'" class="invite-card animate-fade">
      <div class="brand-row">
        <div class="brand-icon">🤖</div>
        <h1>AI 技术面试</h1>
        <p v-if="job">岗位：{{ job.title }}</p>
      </div>

      <div class="form-area">
        <div class="input-group">
          <label>你的姓名 *</label>
          <input v-model="name" type="text" placeholder="请输入姓名" />
        </div>
        <div class="input-group">
          <label>邮箱（选填）</label>
          <input v-model="email" type="email" placeholder="用于接收面试结果通知" />
        </div>
        <div class="input-group">
          <label>上传简历（PDF / Word / TXT）</label>
          <div class="upload-zone" @click="fileInput?.click()" @dragover.prevent @drop.prevent="onDrop">
            <input ref="fileInput" type="file" accept=".pdf,.docx,.doc,.txt" @change="onFileChange" hidden />
            <div v-if="!selectedFile" class="upload-placeholder">
              <span class="upload-icon">📂</span>
              <span>点击或拖拽简历文件到此处</span>
            </div>
            <div v-else class="upload-done">
              <span>✅</span> {{ selectedFile.name }}
            </div>
          </div>
        </div>
        <button class="start-btn" :disabled="!name.trim() || starting" @click="startInterview">
          {{ starting ? '准备中...' : '🚀 开始面试' }}
        </button>
        <p class="hint-text">面试将通过 AI 进行，请认真回答每个问题。</p>
      </div>

      <div v-if="error" class="error-msg">{{ error }}</div>
    </div>

    <!-- Step 2: 面试完成 -->
    <div v-else-if="step === 'done'" class="invite-card animate-fade">
      <div class="done-icon">🎉</div>
      <h2>面试已完成</h2>
      <p>感谢你的参与！HR 将查看你的面试报告并尽快联系你。</p>
    </div>

    <!-- Step 3: 错误 -->
    <div v-else-if="step === 'error'" class="invite-card animate-fade">
      <div class="done-icon">😕</div>
      <h2>{{ error }}</h2>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: false })
const route = useRoute()
const { $api } = useNuxtApp()

const step = ref<'form' | 'done' | 'error'>('form')
const job = ref<any>(null)
const name = ref('')
const email = ref('')
const selectedFile = ref<File | null>(null)
const fileInput = ref<HTMLInputElement>()
const starting = ref(false)
const error = ref('')

const token = computed(() => route.params.token as string)

const onFileChange = (e: Event) => {
  const f = (e.target as HTMLInputElement).files?.[0]
  if (f) selectedFile.value = f
}
const onDrop = (e: DragEvent) => {
  const f = e.dataTransfer?.files?.[0]
  if (f) selectedFile.value = f
}

const startInterview = async () => {
  starting.value = true
  error.value = ''
  try {
    const fd = new FormData()
    fd.append('name', name.value.trim())
    if (email.value) fd.append('email', email.value)
    if (selectedFile.value) fd.append('resume', selectedFile.value)

    const res = await $api.post(`/invite/${token.value}/start`, fd, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    const iid = res.data.data.interview_id
    // 跳转到面试页（使用 interview 布局）
    window.location.href = `/interviews/${iid}`
  } catch (e: any) {
    error.value = e?.response?.data?.detail || '启动面试失败'
    if (error.value.includes('已被使用')) step.value = 'error'
  }
  finally { starting.value = false }
}

onMounted(async () => {
  try {
    const res = await $api.get(`/invite/${token.value}`)
    job.value = res.data.data?.job
  } catch (e: any) {
    step.value = 'error'
    error.value = e?.response?.data?.detail || '邀请链接无效'
  }
})
</script>

<style scoped>
.invite-bg {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: radial-gradient(ellipse 60% 50% at 50% -20%, rgba(91,91,237,0.04) 0%, transparent 60%), #FAFAFA;
}
.invite-card {
  background: #FFF;
  border-radius: 20px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04), 0 10px 40px rgba(0,0,0,0.06);
  padding: 40px;
  max-width: 500px;
  width: 100%;
  border: 1px solid #F0F0F3;
  text-align: center;
}
.animate-fade { animation: fadeIn 0.4s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }

.brand-row { margin-bottom: 28px; }
.brand-icon {
  width: 52px; height: 52px;
  background: linear-gradient(135deg, #5B5BED, #A78BFA);
  border-radius: 14px; display: inline-flex; align-items: center; justify-content: center;
  font-size: 26px; margin-bottom: 14px;
  box-shadow: 0 8px 24px rgba(91,91,237,0.2);
}
.brand-row h1 { font-size: 24px; font-weight: 700; color: #18181B; letter-spacing: -0.02em; margin-bottom: 4px; }
.brand-row p { font-size: 14px; color: #A1A1AA; }

.form-area { text-align: left; }
.input-group { margin-bottom: 18px; }
.input-group label { display: block; font-size: 13px; font-weight: 600; color: #374151; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.03em; }
.input-group input {
  width: 100%; padding: 12px 14px; border: 1.5px solid #E8E8ED; border-radius: 10px;
  font-size: 15px; font-family: inherit; outline: none; transition: border-color 0.2s; color: #18181B;
}
.input-group input:focus { border-color: #5B5BED; }

.upload-zone {
  border: 2px dashed #E8E8ED; border-radius: 10px; padding: 24px;
  cursor: pointer; text-align: center; transition: all 0.2s;
}
.upload-zone:hover { border-color: #5B5BED; background: rgba(91,91,237,0.02); }
.upload-placeholder { display: flex; flex-direction: column; align-items: center; gap: 8px; color: #A1A1AA; font-size: 14px; }
.upload-icon { font-size: 28px; }
.upload-done { color: #10B981; font-size: 14px; }

.start-btn {
  width: 100%; padding: 14px; border-radius: 10px; border: none;
  background: linear-gradient(135deg, #5B5BED, #7C3AED); color: #FFF; font-size: 16px;
  font-weight: 600; cursor: pointer; font-family: inherit; margin-top: 8px;
  box-shadow: 0 4px 16px rgba(91,91,237,0.25);
  transition: all 0.2s;
}
.start-btn:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 6px 24px rgba(91,91,237,0.3); }
.start-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.hint-text { text-align: center; font-size: 12px; color: #D4D4D8; margin-top: 12px; }

.done-icon { font-size: 56px; margin-bottom: 16px; }
.invite-card h2 { font-size: 22px; font-weight: 700; color: #18181B; margin-bottom: 8px; }
.invite-card p { color: #71717A; font-size: 15px; line-height: 1.6; }

.error-msg { margin-top: 14px; padding: 10px 14px; background: #FEF2F2; color: #DC2626; border-radius: 8px; font-size: 13px; }
</style>
