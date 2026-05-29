import { defineStore } from 'pinia'

interface Message {
  id: number
  role: 'interviewer' | 'candidate' | 'system'
  content: string
  question_number?: number
  scores?: {
    correctness: number
    depth: number
    logic: number
    practice: number
    comment?: string
  } | null
  created_at: string
}

interface Interview {
  id: number
  job_id: number
  candidate_id: number
  status: 'pending' | 'in_progress' | 'completed'
  started_at: string | null
  completed_at: string | null
  overall_score: any
}

export const useInterviewStore = defineStore('interview', {
  state: () => ({
    currentInterview: null as Interview | null,
    messages: [] as Message[],
    isLoading: false,
    isStreaming: false,
    streamContent: '',
    currentQuestionNumber: 1
  }),
  
  getters: {
    canSendMessage: (state) => 
      !state.isLoading && 
      !state.isStreaming && 
      state.currentInterview?.status === 'in_progress'
  },
  
  actions: {
    setCurrentInterview(interview: Interview) {
      this.currentInterview = interview
    },
    
    addMessage(message: Message) {
      this.messages.push(message)
    },
    
    setLoading(loading: boolean) {
      this.isLoading = loading
    },
    
    setStreaming(streaming: boolean) {
      this.isStreaming = streaming
    },
    
    appendStreamContent(content: string) {
      this.streamContent += content
    },
    
    clearStreamContent() {
      this.streamContent = ''
    },
    
    finishStream() {
      if (this.streamContent) {
        this.addMessage({
          id: Date.now(),
          role: 'interviewer',
          content: this.streamContent,
          created_at: new Date().toISOString(),
          question_number: this.currentQuestionNumber
        })
        this.streamContent = ''
        this.currentQuestionNumber++
      }
      this.isStreaming = false
    },
    
    reset() {
      this.currentInterview = null
      this.messages = []
      this.streamContent = ''
      this.currentQuestionNumber = 1
    }
  }
})