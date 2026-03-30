import { useEffect, useRef, useState } from 'react'
import { createWorldScene } from '../three/WorldScene'
import { connectWorldSocket } from '../services/ws'

export default function WorldPage() {
  const containerRef = useRef(null)
  const [selection, setSelection] = useState(null)

  useEffect(() => {
    const saved = localStorage.getItem('codecity_world')
    if (!saved || !containerRef.current) return
    const data = JSON.parse(saved)

    const cleanupScene = createWorldScene(containerRef.current, data.world, setSelection)

    const socket = connectWorldSocket(data.username, () => {})
    const interval = setInterval(() => {
      socket.send(JSON.stringify({ type: 'position', timestamp: Date.now() }))
    }, 1000)

    return () => {
      clearInterval(interval)
      socket.close()
      cleanupScene()
    }
  }, [])

  return (
    <div className="grid grid-cols-4 h-[calc(100vh-65px)]">
      <div ref={containerRef} className="col-span-3" />
      <aside className="bg-white p-4 border-l overflow-auto">
        <h2 className="font-semibold text-xl">Explorer Panel</h2>
        {!selection && <p className="text-slate-500 mt-3">Click homes and buildings to inspect details.</p>}
        {selection && <pre className="mt-3 text-xs whitespace-pre-wrap">{JSON.stringify(selection.payload, null, 2)}</pre>}
      </aside>
    </div>
  )
}
