import { Link, Route, Routes } from 'react-router-dom'
import HomePage from './pages/HomePage'
import WorldPage from './pages/WorldPage'
import ProfilePage from './pages/ProfilePage'

export default function App() {
  return (
    <div className="min-h-screen">
      <nav className="flex gap-4 p-4 bg-white/80 backdrop-blur sticky top-0 z-10 border-b">
        <Link to="/" className="font-semibold">CodeCity Life</Link>
        <Link to="/world">World</Link>
        <Link to="/profile">Profile</Link>
      </nav>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/world" element={<WorldPage />} />
        <Route path="/profile" element={<ProfilePage />} />
      </Routes>
    </div>
  )
}
