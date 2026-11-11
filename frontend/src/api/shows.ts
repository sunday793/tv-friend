import { api } from './client'

export interface Media {
  external_id: string
  title: string
  type: string
  year: number | null
  poster_url: string | null
  overview: string | null
}

export interface WatchlistItem {
  id: number
  status: string
  rating: number | null
  show: Media
}

export const showsApi = {
  search: async (query: string): Promise<Media[]> => {
    const response = await api.get<Media[]>('/api/shows/search', {
      params: { query },
    })
    return response.data
  },

  getWatchlist: async (): Promise<WatchlistItem[]> => {
    const response = await api.get<WatchlistItem[]>('/api/shows/watchlist')
    return response.data
  },

  addToWatchlist: async (external_id: string): Promise<WatchlistItem> => {
    const response = await api.post<WatchlistItem>('/api/shows/watchlist', {
      external_id,
    })
    return response.data
  },
}