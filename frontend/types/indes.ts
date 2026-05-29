// 岗位类型
export interface Job {
  id: number
  title: string
  description: string
  requirements: string
  created_at: string
}

// 候选人类型
export interface Candidate {
  id: number
  name: string
  email: string | null
  phone: string | null
  resume_text: string | null
  resume_file_path: string | null
  created_at: string
}

// 消息类型
export interface Message {
  id: number
  interview_id: number
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

// 面试类型
export interface Interview {
  id: number
  job_id: number
  candidate_id: number
  status: 'pending' | 'in_progress' | 'completed'
  started_at: string | null
  completed_at: string | null
  overall_score: {
    technical: number
    communication: number
    learning: number
    match: number
    recommendation: string
    summary: string
  } | null
  messages?: Message[]
}

// 报告类型
export interface Report {
  interview_id: number
  job: Job
  candidate: Candidate
  overall_score: {
    technical: number
    communication: number
    learning: number
    match: number
    recommendation: string
    summary: string
  }
  question_details: Array<{
    question_number: number
    question: string
    answer: string
    scores: {
      correctness: number
      depth: number
      logic: number
      practice: number
    }
    comment: string
  }>
  total_questions: number
  duration: string
  generated_at: string
}

// API 响应类型
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}