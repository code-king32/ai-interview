import { defineStore } from 'pinia'

interface Candidate {
  id: number
  name: string
  email: string | null
  phone: string | null
  resume_text: string | null
  created_at: string
}

export const useCandidateStore = defineStore('candidate', {
  state: () => ({
    candidates: [] as Candidate[],
    loading: false,
    total: 0
  }),
  
  actions: {
    async fetchCandidates(page = 1, pageSize = 10) {
      this.loading = true
      try {
        const { $api } = useNuxtApp()
        const res = await $api.get('/candidates', { 
          params: { page, page_size: pageSize } 
        })
        if (res.data.code === 0) {
          this.candidates = res.data.data.items || []
          this.total = res.data.data.total
        }
      } catch (error) {
        console.error('获取候选人失败:', error)
      } finally {
        this.loading = false
      }
    },
    
    async createCandidate(formData: FormData) {
      try {
        const { $api } = useNuxtApp()
        const res = await $api.post('/candidates', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        if (res.data.code === 0) {
          await this.fetchCandidates()
          return res.data.data
        }
      } catch (error) {
        console.error('创建候选人失败:', error)
        throw error
      }
    },
    
    async deleteCandidate(id: number) {
      try {
        const { $api } = useNuxtApp()
        const res = await $api.delete(`/candidates/${id}`)
        if (res.data.code === 0) {
          await this.fetchCandidates()
          return true
        }
      } catch (error) {
        console.error('删除候选人失败:', error)
        throw error
      }
    }
  }
})