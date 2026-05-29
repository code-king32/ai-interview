// utils/validator.ts
// 验证邮箱
export const isValidEmail = (email: string): boolean => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return regex.test(email)
}

// 验证手机号（中国）
export const isValidPhone = (phone: string): boolean => {
  const regex = /^1[3-9]\d{9}$/
  return regex.test(phone)
}

// 验证 URL
export const isValidUrl = (url: string): boolean => {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

// 验证非空 ✅ 修复版本
export const isNotEmpty = (value: string): boolean => {
  return Boolean(value && value.trim().length > 0)
}