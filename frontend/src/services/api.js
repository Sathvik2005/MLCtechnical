const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:10000'

export async function generateWorld(githubUsername, leetcodeUsername) {
  const response = await fetch(`${API_URL}/generate-world`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ github_username: githubUsername, leetcode_username: leetcodeUsername }),
  })
  if (!response.ok) {
    throw new Error(await response.text())
  }
  return response.json()
}

export async function fetchWorld(username) {
  const response = await fetch(`${API_URL}/world/${username}`)
  if (!response.ok) throw new Error('World fetch failed')
  return response.json()
}

export { API_URL }
