<template>
  <div class="int-root">
    <!-- Header -->
    <header class="int-hdr">
      <div class="int-hdr-l">
        <div class="int-live"></div>
        <span class="int-prog">{{ progressText }}</span>
        <span v-if="currentTopic" class="int-topic">{{ currentTopic }}</span>
      </div>
      <button v-if="!isCompleted" class="int-end" @click="endInterview" :disabled="loading">结束面试</button>
    </header>

    <!-- Chat -->
    <div class="chat-scroll" ref="chatScroll">
      <div class="chat-feed">
        <div v-for="(msg, idx) in chatMessages" :key="msg.id"
          class="msg-row" :class="isUser(msg) ? 'msg-right' : 'msg-left'"
          :style="{ animationDelay: `${idx * 0.03}s` }">
          <div class="msg-avatar" :class="isUser(msg) ? 'av-right' : 'av-left'">
            <svg v-if="!isUser(msg)" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#71717A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2.5" y="2.5" width="19" height="19" rx="5"/><circle cx="8.5" cy="10" r="1.5" fill="#71717A"/><circle cx="15.5" cy="10" r="1.5" fill="#71717A"/><path d="M8 16c1.8 2.2 5 2.6 7.5 1.5"/></svg>
            <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#FFF" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-8 8-8s8 3.6 8 8"/></svg>
          </div>
          <div class="msg-body">
            <div class="msg-bubble" :class="isUser(msg) ? 'bub-right' : 'bub-left'">
              <span class="whitespace-pre-wrap">{{ msg.content }}</span>
            </div>
            <div v-if="!isUser(msg) && msg.scores" class="score-inline">
              <div class="score-grid">
                <div v-for="d in scoreDims" :key="d.key" class="score-item">
                  <span class="score-lbl">{{ d.label }}</span>
                  <div class="score-track"><div class="score-bar" :style="{ width: `${(msg.scores?.[d.key] || 0) * 10}%`, background: scoreColor(msg.scores?.[d.key]) }"></div></div>
                  <span class="score-num" :style="{ color: scoreColor(msg.scores?.[d.key]) }">{{ msg.scores?.[d.key] || 0 }}</span>
                </div>
              </div>
              <p v-if="msg.scores?.comment" class="score-cmt">{{ msg.scores.comment }}</p>
            </div>
            <div class="msg-meta" :class="isUser(msg) ? 'meta-right' : ''">
              <span class="msg-time">{{ fmtTime(msg.created_at) }}</span>
            </div>
          </div>
        </div>

        <!-- Streaming -->
        <div v-if="streaming && streamText" class="msg-row msg-left in">
          <div class="msg-avatar av-left">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#71717A" stroke-width="1.5" stroke-linecap="round"><rect x="2.5" y="2.5" width="19" height="19" rx="5"/><circle cx="8.5" cy="10" r="1.5" fill="#71717A"/><circle cx="15.5" cy="10" r="1.5" fill="#71717A"/><path d="M8 16c1.8 2.2 5 2.6 7.5 1.5"/></svg>
          </div>
          <div class="msg-body">
            <div class="msg-bubble bub-left">{{ streamText }}<span class="cursor-blink"></span></div>
          </div>
        </div>

        <!-- Thinking -->
        <div v-if="loading && !streaming" class="msg-row msg-left in">
          <div class="msg-avatar av-left">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#71717A" stroke-width="1.5" stroke-linecap="round"><rect x="2.5" y="2.5" width="19" height="19" rx="5"/><circle cx="8.5" cy="10" r="1.5" fill="#71717A"/><circle cx="15.5" cy="10" r="1.5" fill="#71717A"/><path d="M8 16c1.8 2.2 5 2.6 7.5 1.5"/></svg>
          </div>
          <div class="msg-body">
            <div class="msg-bubble bub-left">
              <div class="thinking"><span></span><span></span><span></span></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Input -->
    <div v-if="!isCompleted" class="int-foot">
      <div class="int-input-box">
        <textarea ref="inputRef" v-model="inputText" :disabled="loading" placeholder="输入你的回答…" rows="1"
          @keydown="onKey" @input="onInput"></textarea>
        <button class="send-btn" :class="inputText.trim() && !loading ? 'send-on' : 'send-off'"
          :disabled="!inputText.trim() || loading" @click="send">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
        </button>
      </div>
      <div class="kbd-hint"><kbd>Enter</kbd> 发送 &nbsp;<kbd>Shift</kbd> + <kbd>Enter</kbd> 换行</div>
    </div>

    <!-- Finished -->
    <div v-if="isCompleted && !loading" class="fin-state">
      <div class="fin-icon">🎉</div>
      <h3>面试已结束</h3>
      <p>评估报告已生成</p>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'interview' })
const route = useRoute()
const { $api } = useNuxtApp()

const interviewId = computed(() => Number(route.params.id))
const chatMessages = ref<any[]>([])
const loading = ref(false)
const streaming = ref(false)
const streamText = ref('')
const interviewStatus = ref('')
const latestScores = ref<any>(null)
const currentTopic = ref('')
const inputText = ref('')
const inputRef = ref<HTMLTextAreaElement>()
const chatScroll = ref<HTMLElement>()

const scoreDims = [{ key: 'correctness', label: '正确性' }, { key: 'depth', label: '深度' }, { key: 'logic', label: '逻辑' }, { key: 'practice', label: '实践' }]
const isCompleted = computed(() => interviewStatus.value === 'COMPLETED' || interviewStatus.value === 'completed')
const progressText = computed(() => {
  const n = chatMessages.value.filter(m => m.role === 'INTERVIEWER' || m.role === 'interviewer').length
  return n ? `第 ${n} 题` : '准备开始'
})
const isUser = (m: any) => m.role === 'CANDIDATE' || m.role === 'candidate' || m.role === 'user'
const fmtTime = (iso?: string) => iso ? new Date(iso).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }) : ''
const scoreColor = (s: number) => (s >= 8 ? '#10B981' : s >= 6 ? '#F59E0B' : '#EF4444')
const scrollDown = () => nextTick(() => { if (chatScroll.value) chatScroll.value.scrollTo({ top: chatScroll.value.scrollHeight, behavior: 'smooth' }) })

const send = () => {
  const t = inputText.value.trim()
  if (!t || loading.value) return
  sendMessage(t)
  inputText.value = ''
  if (inputRef.value) inputRef.value.style.height = 'auto'
}
const onInput = () => { const e = inputRef.value; if (e) { e.style.height = 'auto'; e.style.height = Math.min(e.scrollHeight, 76) + 'px' } }
const onKey = (e: KeyboardEvent) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send() } }

const sendMessage = async (content: string) => {
  chatMessages.value.push({ id: Date.now(), role: 'CANDIDATE', content, created_at: new Date().toISOString() })
  scrollDown()
  loading.value = true; streaming.value = true; streamText.value = ''
  let full = ''; let scores: any = null; let mid = 0
  try {
    const c = useRuntimeConfig()
    const r = await fetch(`${c.public.apiBase}/interviews/chat/stream`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ interview_id: interviewId.value, message: content }),
    })
    const reader = r.body?.getReader()
    if (!reader) throw new Error('No stream')
    const dec = new TextDecoder(); let buf = ''
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      buf += dec.decode(value, { stream: true })
      const parts = buf.split('\n\n'); buf = parts.pop() || ''
      for (const p of parts) {
        const line = p.trim(); if (!line) continue
        const js = line.startsWith('data: ') ? line.slice(6) : line
        try {
          const d = JSON.parse(js)
          if (d.type === 'token') { full += d.content || ''; streamText.value = full }
          else if (d.type === 'scores') { if (d.scores) { scores = d.scores; latestScores.value = d.scores } }
          else if (d.type === 'done') { mid = d.message_id || Date.now(); if (d.content) full = d.content }
        } catch { /* skip */ }
      }
    }
  } catch (e: any) {
    try {
      const fb = await $api.post('/interviews/chat-v2', { interview_id: interviewId.value, message: content })
      full = fb.data.assistant_response || ''; scores = fb.data.scores; mid = fb.data.message_id
      streamText.value = full
    } catch (e2: any) {
      const detail = e2?.response?.data?.detail || e2?.message || '未知错误'
      chatMessages.value.push({ id: Date.now()+1, role: 'INTERVIEWER', content: '⚠️ AI 响应失败：' + detail + '。请稍后重试。', scores: null, created_at: new Date().toISOString() })
    }
  } finally { streaming.value = false; loading.value = false }
  if (full) {
    chatMessages.value.push({ id: mid || Date.now() + 1, role: 'INTERVIEWER', content: full, scores, created_at: new Date().toISOString() })
    if (scores) latestScores.value = scores
    interviewStatus.value = 'IN_PROGRESS'
    scrollDown()
  }
  streamText.value = ''
}

const endInterview = async () => {
  if (!confirm('确定要结束本次面试吗？AI 将生成评估报告。')) return
  try { await $api.post(`/interviews/${interviewId.value}/end-v2`); interviewStatus.value = 'COMPLETED'; await navigateTo(`/reports/${interviewId.value}`) }
  catch (e: any) { alert('结束失败：' + (e?.response?.data?.detail || '请重试')) }
}

const load = async () => {
  try {
    const [ir, mr] = await Promise.all([$api.get(`/interviews/${interviewId.value}`), $api.get(`/interviews/${interviewId.value}/messages`)])
    interviewStatus.value = ir.data.status || ''
    const msgData = mr.data; chatMessages.value = (Array.isArray(msgData) ? msgData : []).map((m: any) => ({ ...m, role: m.role === 'CANDIDATE' || m.role === 'INTERVIEWER' ? m.role : String(m.role || '').toUpperCase() }))
    for (let i = chatMessages.value.length - 1; i >= 0; i--) { if (chatMessages.value[i].scores) { latestScores.value = chatMessages.value[i].scores; break } }
    const ai = chatMessages.value.filter((m: any) => m.role === 'INTERVIEWER')
    if (ai.length && ai[ai.length - 1].scores?.topic) currentTopic.value = ai[ai.length - 1].scores.topic
    scrollDown()
  } catch (e) { console.error(e) }
}

onMounted(load)
</script>

<style scoped>
/* ── Root ── */
.int-root { display: flex; flex-direction: column; height: 100%; background: #FFF }

/* ── Header ── */
.int-hdr { display: flex; align-items: center; justify-content: space-between; height: 56px; padding: 0 24px; flex-shrink: 0; background: rgba(255,255,255,0.85); backdrop-filter: saturate(180%) blur(12px); border-bottom: 1px solid #F0F0F3; z-index: 10 }
.int-hdr-l { display: flex; align-items: center; gap: 13px }
.int-live { position: relative; width: 9px; height: 9px }
.int-live::before { content: ''; position: absolute; inset: -3px; border-radius: 50%; background: #10B981; animation: liveRing 2s cubic-bezier(0.4,0,0.2,1) infinite }
.int-live::after { content: ''; position: absolute; inset: 0; border-radius: 50%; background: #10B981 }
@keyframes liveRing { 0%,100% { transform: scale(1); opacity: .3 } 50% { transform: scale(2.2); opacity: 0 } }
.int-prog { font-size: 13px; font-weight: 600; color: #18181B; letter-spacing: -0.005em }
.int-topic { font-size: 11px; font-weight: 500; padding: 3px 10px; border-radius: 9999px; background: rgba(91,91,237,0.06); color: #5B5BED; letter-spacing: 0.01em }
.int-end { font-size: 13px; color: #71717A; padding: 6px 12px; border-radius: 6px; border: none; background: transparent; cursor: pointer; font-family: inherit; transition: all .2s }
.int-end:hover { color: #EF4444; background: rgba(239,68,68,0.06) }

/* ── Chat ── */
.chat-scroll { flex: 1; overflow-y: auto; padding: 36px 24px; background: radial-gradient(ellipse 50% 50% at 50% 0%, rgba(91,91,237,0.01) 0%, transparent 70%), #FFF; scroll-behavior: smooth }
.chat-feed { max-width: 720px; margin: 0 auto; display: flex; flex-direction: column; gap: 28px }

/* ── Messages ── */
.msg-row { display: flex; gap: 11px; max-width: 72% }
.msg-left { align-self: flex-start }
.msg-right { align-self: flex-end; flex-direction: row-reverse }
.in { animation: msgIn .5s cubic-bezier(0.34,1.56,0.64,1) both }
@keyframes msgIn { 0% { opacity: 0; transform: translateY(20px) scale(.92) } 60% { transform: translateY(-2px) scale(1.01) } 100% { opacity: 1; transform: translateY(0) scale(1) } }

.msg-avatar { width: 34px; height: 34px; border-radius: 10px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; margin-top: 1px }
.av-left { background: #F5F5F7; border: 1px solid #F0F0F3; box-shadow: 0 0 0 1px rgba(0,0,0,0.03) }
.av-right { background: linear-gradient(135deg, #5B5BED, #A78BFA); box-shadow: 0 4px 12px rgba(91,91,237,0.22) }

.msg-body { min-width: 0; display: flex; flex-direction: column }
.msg-bubble { padding: 13px 17px; font-size: 14.5px; line-height: 1.62; letter-spacing: -0.005em; word-break: break-word }
.bub-left { background: #F5F5F7; color: #1F2937; border-radius: 3px 14px 14px 14px }
.bub-right { background: #5B5BED; color: #FFF; border-radius: 14px 3px 14px 14px }

/* ── Score inline ── */
.score-inline { margin-top: 6px; padding: 10px 12px; background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 10px }
.score-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 5px 10px }
.score-item { display: flex; align-items: center; gap: 6px }
.score-lbl { font-size: 10.5px; color: #71717A; min-width: 30px }
.score-track { flex: 1; height: 3.5px; background: #FDE68A; border-radius: 2px; overflow: hidden }
.score-bar { height: 100%; border-radius: 2px; transition: width .6s cubic-bezier(0.16,1,0.3,1) }
.score-num { font-size: 10.5px; font-weight: 700; min-width: 16px; text-align: right }
.score-cmt { font-size: 11px; color: #71717A; margin-top: 6px; padding-top: 6px; border-top: 1px solid #FDE68A; font-style: italic }

/* ── Meta ── */
.msg-meta { display: flex; align-items: center; gap: 6px; margin-top: 4px; padding: 0 5px }
.meta-right { justify-content: flex-end }
.msg-time { font-size: 10.5px; color: #D4D4D8 }

/* ── Cursor ── */
.cursor-blink { display: inline-block; width: 1.5px; height: 15px; background: #71717A; margin-left: 1px; vertical-align: text-bottom; animation: blink .75s step-end infinite }
@keyframes blink { 50% { opacity: 0 } }

/* ── Thinking ── */
.thinking { display: flex; gap: 5px; padding: 5px 0 }
.thinking span { width: 7px; height: 7px; border-radius: 50%; background: #D4D4D8; animation: think 1.2s cubic-bezier(0.65,0,0.35,1) infinite }
.thinking span:nth-child(2) { animation-delay: .18s } .thinking span:nth-child(3) { animation-delay: .36s }
@keyframes think { 0%,60%,100% { transform: translateY(0); opacity: .3 } 30% { transform: translateY(-9px); opacity: 1 } }

/* ── Input ── */
.int-foot { padding: 16px 24px 20px; border-top: 1px solid #F0F0F3; background: #FFF; flex-shrink: 0 }
.int-input-box { max-width: 720px; margin: 0 auto; display: flex; align-items: flex-end; gap: 10px; background: #F5F5F7; border: 1.5px solid #E8E8ED; border-radius: 12px; padding: 8px 8px 8px 18px; transition: all .25s cubic-bezier(0.16,1,0.3,1) }
.int-input-box:focus-within { border-color: #5B5BED; background: #FFF; box-shadow: 0 0 0 5px rgba(91,91,237,0.06) }
.int-input-box textarea { flex: 1; border: none; background: transparent; font-size: 15px; font-family: inherit; line-height: 1.5; resize: none; outline: none; max-height: 76px; padding: 5px 0; color: #18181B; letter-spacing: -0.005em }
.int-input-box textarea::placeholder { color: #A1A1AA }
.send-btn { width: 40px; height: 40px; border-radius: 10px; flex-shrink: 0; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all .25s cubic-bezier(0.16,1,0.3,1) }
.send-on { background: #5B5BED; color: #FFF; box-shadow: 0 2px 10px rgba(91,91,237,0.22) }
.send-on:hover { background: #4F4FE0; transform: scale(1.07); box-shadow: 0 4px 16px rgba(91,91,237,0.28) }
.send-off { background: #EEEEF2; color: #A1A1AA; cursor: not-allowed; box-shadow: none }
.kbd-hint { text-align: center; font-size: 11px; color: #D4D4D8; margin-top: 10px }
.kbd-hint kbd { display: inline-flex; align-items: center; min-width: 18px; height: 18px; padding: 0 5px; border-radius: 4px; border: 1px solid #E8E8ED; background: #FFF; font-family: inherit; font-size: 10.5px; color: #71717A; box-shadow: 0 1px 0 #E8E8ED }

/* ── Finished ── */
.fin-state { border-top: 1px solid #F0F0F3; padding: 40px 24px; text-align: center; background: #FFF }
.fin-icon { font-size: 40px; margin-bottom: 12px }
.fin-state h3 { font-size: 16px; font-weight: 600; color: #18181B; margin-bottom: 4px }
.fin-state p { font-size: 13px; color: #71717A }
</style>
