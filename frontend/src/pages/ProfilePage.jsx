export default function ProfilePage() {
  const saved = localStorage.getItem('codecity_world')
  const data = saved ? JSON.parse(saved) : null

  return (
    <div className="max-w-3xl mx-auto mt-10 bg-white rounded-2xl p-6 shadow">
      <h1 className="text-2xl font-semibold">Resident Profile</h1>
      {!data && <p className="mt-3 text-slate-500">Generate your world first.</p>}
      {data && (
        <div className="mt-4 space-y-4">
          <p><b>Username:</b> {data.username}</p>
          <p><b>Problems solved:</b> {data.profile.problems_solved}</p>
          <p><b>Top skills:</b> {data.profile.skills.join(', ')}</p>
          <h2 className="font-semibold">Mentor Insights</h2>
          <pre className="text-xs bg-slate-100 p-3 rounded">{JSON.stringify(data.insights, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}
