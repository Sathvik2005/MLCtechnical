import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { generateWorld } from '../services/api'

export default function HomePage() {
  const navigate = useNavigate()
  const [github, setGithub] = useState('')
  const [leetcode, setLeetcode] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setLoading(true)
    try {
      const data = await generateWorld(github, leetcode)
      localStorage.setItem('codecity_world', JSON.stringify(data))
      navigate('/world')
    } catch (err) {
      alert(`Failed: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-xl mx-auto mt-20 bg-white p-8 rounded-2xl shadow">
      <h1 className="text-3xl font-semibold">Welcome to CodeCity Life</h1>
      <p className="mt-2 text-slate-600">Enter your GitHub + LeetCode usernames to generate your living dev world.</p>
      <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
        <input className="w-full border rounded p-3" value={github} onChange={e => setGithub(e.target.value)} placeholder="GitHub username" required />
        <input className="w-full border rounded p-3" value={leetcode} onChange={e => setLeetcode(e.target.value)} placeholder="LeetCode username" required />
        <button className="w-full bg-primary py-3 rounded font-medium" disabled={loading}>{loading ? 'Generating...' : 'Build My City'}</button>
      </form>
    </div>
  )
}
