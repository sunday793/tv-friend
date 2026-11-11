import { api } from './client'

export interface LoginResponse {
  access_token: string
  token_type: string
}

export const authApi = {
  login: async (username: string, password: string): Promise<LoginResponse> => {
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)

    const response = await api.post<LoginResponse>('/api/auth/login', formData)
    return response.data
  },
}