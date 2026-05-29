import { defineStore } from 'pinia'

interface Job {
  id: number
  title: string
  description: string
  requirements: string
  created_at: string
}

export const useJobStore = defineStore('job', {
  state: () => ({
    jobs: [] as Job[],
    loading: false
  }),
  
  actions: {
    async fetchJobs() {
      this.loading = true
      try {
        const { $api } = useNuxtApp()
        const res = await $api.get('/jobs')
        if (res.data.code === 0) {
          this.jobs = res.data.data.items || []
        }
      } catch (error) {
        console.error('获取岗位失败:', error)
      } finally {
        this.loading = false
      }
    },
    
    async createJob(data: { title: string; description: string; requirements: string }) {
      try {
        const { $api } = useNuxtApp()
        const res = await $api.post('/jobs', data)
        if (res.data.code === 0) {
          await this.fetchJobs()
          return res.data.data
        }
      } catch (error) {
        console.error('创建岗位失败:', error)
        throw error
      }
    },
    
    async deleteJob(id: number) {
      try {
        const { $api } = useNuxtApp()
        const res = await $api.delete(`/jobs/${id}`)
        if (res.data.code === 0) {
          await this.fetchJobs()
          return true
        }
      } catch (error) {
        console.error('删除岗位失败:', error)
        throw error
      }
    }
  }
})