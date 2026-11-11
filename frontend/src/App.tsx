import { Routes, Route, Navigate, Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from './store/auth'
import Login from './pages/Login'

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const token = useAuthStore((state) => state.token)
  if (!token) return <Navigate to="/login" replace />
  return <>{children}</>
}

function Home() {
  const logout = useAuthStore((state) => state.logout)
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-gray-900 p-8">
      <header className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-white">Мой список</h1>
        <button 
          onClick={handleLogout}
          className="text-gray-400 hover:text-white transition"
        >
          Выйти
        </button>
      </header>
      <div className="text-gray-400">
        Скоро здесь появится поиск и список сериалов!
      </div>
    </div>
  )
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route 
        path="/" 
        element={
          <ProtectedRoute>
            <Home />
          </ProtectedRoute>
        } 
      />
    </Routes>
  )
}

export default App