// 格式化日期
export const formatDate = (dateStr: string): string => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

// 格式化时间（仅时间）
export const formatTime = (dateStr: string): string => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

// 格式化时长（分钟）
export const formatDuration = (minutes: number): string => {
  if (minutes < 60) return `${minutes}分钟`
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  return `${hours}小时${mins}分钟`
}

// 截断文本
export const truncateText = (text: string, maxLength: number): string => {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.slice(0, maxLength) + '...'
}