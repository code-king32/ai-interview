export const useApi = () => {
  const { $api } = useNuxtApp()
  
  const get = async <T = any>(url: string, params?: any): Promise<T> => {
    const response = await $api.get(url, { params })
    if (response.data.code !== 0) {
      throw new Error(response.data.message)
    }
    return response.data.data
  }
  
  const post = async <T = any>(url: string, data?: any): Promise<T> => {
    const response = await $api.post(url, data)
    if (response.data.code !== 0) {
      throw new Error(response.data.message)
    }
    return response.data.data
  }
  
  const put = async <T = any>(url: string, data?: any): Promise<T> => {
    const response = await $api.put(url, data)
    if (response.data.code !== 0) {
      throw new Error(response.data.message)
    }
    return response.data.data
  }
  
  const del = async <T = any>(url: string): Promise<T> => {
    const response = await $api.delete(url)
    if (response.data.code !== 0) {
      throw new Error(response.data.message)
    }
    return response.data.data
  }
  
  return {
    get,
    post,
    put,
    delete: del
  }
}