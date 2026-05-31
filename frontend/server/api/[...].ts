export default defineEventHandler(async (event) => {
  const path = event.path.replace(/^\/api/, '')
  const query = getQuery(event)
  const qs = Object.entries(query).length > 0
    ? '?' + new URLSearchParams(query as Record<string, string>).toString()
    : ''
  const target = `http://localhost:8000/api${path}${qs}`

  try {
    const body = event.method !== 'GET' && event.method !== 'HEAD'
      ? await readRawBody(event)
      : undefined

    const response = await fetch(target, {
      method: event.method,
      headers: {
        'Content-Type': event.headers.get('content-type') || 'application/json',
        Accept: event.headers.get('accept') || 'application/json',
      },
      body,
    })

    const text = await response.text()
    setResponseStatus(event, response.status)

    const ct = response.headers.get('content-type') || ''
    if (ct.includes('application/json')) {
      setHeader(event, 'content-type', 'application/json')
      return JSON.parse(text)
    }
    if (ct.includes('text/event-stream')) {
      setHeader(event, 'content-type', 'text/event-stream')
      return text
    }
    return text
  } catch (e) {
    setResponseStatus(event, 502)
    return { detail: 'Backend unavailable' }
  }
})
