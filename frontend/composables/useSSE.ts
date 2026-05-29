export interface SSEMessage {
  type: 'token' | 'scores' | 'done' | 'error'
  data: any
}

export const useSSE = () => {
  const isConnected = ref(false)
  const eventSource = ref<EventSource | null>(null)
  
  const connect = (url: string, onMessage: (message: SSEMessage) => void) => {
    eventSource.value = new EventSource(url)
    
    eventSource.value.onopen = () => {
      isConnected.value = true
      console.log('SSE 连接已建立')
    }
    
    eventSource.value.addEventListener('token', (event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data)
        onMessage({ type: 'token', data })
      } catch (e) {
        console.error('解析 token 事件失败:', e)
      }
    })
    
    eventSource.value.addEventListener('scores', (event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data)
        onMessage({ type: 'scores', data })
      } catch (e) {
        console.error('解析 scores 事件失败:', e)
      }
    })
    
    eventSource.value.addEventListener('done', (event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data)
        onMessage({ type: 'done', data })
      } catch (e) {
        console.error('解析 done 事件失败:', e)
      }
    })
    
    eventSource.value.addEventListener('error', (event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data)
        onMessage({ type: 'error', data })
      } catch (e) {
        console.error('解析 error 事件失败:', e)
      }
    })
    
    eventSource.value.onerror = (error) => {
      console.error('SSE 连接错误:', error)
      isConnected.value = false
      onMessage({ 
        type: 'error', 
        data: { code: 40008, message: 'SSE 连接断开' } 
      })
    }
    
    return () => disconnect()
  }
  
  const disconnect = () => {
    if (eventSource.value) {
      eventSource.value.close()
      eventSource.value = null
      isConnected.value = false
    }
  }
  
  return {
    connect,
    disconnect,
    isConnected
  }
}