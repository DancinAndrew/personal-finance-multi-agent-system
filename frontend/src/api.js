const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'

export async function fetchDefaultRun() {
  const response = await fetch(`${API_BASE}/api/demo/default-run`)
  return parseJsonResponse(response)
}

export async function createResearchRun(payload) {
  const response = await fetch(`${API_BASE}/api/research-runs`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  })
  return parseJsonResponse(response)
}

async function parseJsonResponse(response) {
  const data = await response.json()
  if (!response.ok) {
    throw new Error(data.error || `Request failed with ${response.status}`)
  }
  return data
}
