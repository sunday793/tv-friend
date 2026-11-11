import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/auth'
import { showsApi, type Media, type WatchlistItem } from '../api/shows'
import MediaCard from '../components/MediaCard'

export default function Home() {
  const [query, setQuery] = useState('')
  const [searchResults, setSearchResults] = useState<Media[]>([])
  const [watchlist, setWatchlist] = useState<WatchlistItem[]>([])
  const [loading, setLoading] = useState(false)
  const [searching, setSearching] = useState(false)

  const logout = useAuthStore((state) => state.logout)
  const navigate = useNavigate()

  useEffect(() => {
    loadWatchlist()
  }, [])

  const loadWatchlist = async () => {
    setLoading(true)
    try {
      const data = await showsApi.getWatchlist()
      setWatchlist(data)
    } catch (e) {
      console.error('Ошибка загрузки списка', e)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return

    setSearching(true)
    try {
      const data = await showsApi.search(query)
      setSearchResults(data)
    } catch (e) {
      console.error('Ошибка поиска', e)
    } finally {
      setSearching(false)
    }
  }

  const handleAdd = async (external_id: string) => {
    try {
      const newItem = await showsApi.addToWatchlist(external_id)
      setWatchlist([newItem, ...watchlist])
    } catch (e) {
      console.error(e)
      alert('Ошибка при добавлении. Возможно, фильм уже в списке.')
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const isInWatchlist = (external_id: string) => {
    return watchlist.some((item) => item.show.external_id === external_id)
  }

  return (
    <div className="min-h-screen bg-gray-900 pb-12">
      {/* Шапка */}
      <header className="bg-gray-800 p-4 sticky top-0 z-10 shadow-md flex justify-between items-center">
        <h1 className="text-2xl font-bold text-white">TV Friend</h1>
        <button onClick={handleLogout} className="text-gray-400 hover:text-white transition">
          Выйти
        </button>
      </header>

      <main className="max-w-6xl mx-auto px-4 mt-8">
        {/* Строка поиска */}
        <form onSubmit={handleSearch} className="flex gap-2 mb-8">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Найти фильм или сериал..."
            className="flex-1 px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-blue-500 outline-none"
          />
          <button
            type="submit"
            disabled={searching}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition disabled:opacity-50"
          >
            {searching ? 'Поиск...' : 'Искать'}
          </button>
        </form>

        {/* Результаты поиска */}
        {searchResults.length > 0 && (
          <section className="mb-12">
            <h2 className="text-xl font-semibold text-white mb-4">Результаты поиска</h2>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
              {searchResults.map((media) => (
                <MediaCard
                  key={media.external_id}
                  media={media}
                  onAdd={handleAdd}
                  isAdded={isInWatchlist(media.external_id)}
                />
              ))}
            </div>
          </section>
        )}

        {/* Мой список */}
        <section>
          <h2 className="text-xl font-semibold text-white mb-4">Мой список</h2>
          {loading ? (
            <p className="text-gray-400">Загрузка...</p>
          ) : watchlist.length === 0 ? (
            <p className="text-gray-400">Список пока пуст. Найдите что-нибудь через поиск!</p>
          ) : (
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
              {watchlist.map((item) => (
                <MediaCard key={item.id} media={item.show} />
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  )
}