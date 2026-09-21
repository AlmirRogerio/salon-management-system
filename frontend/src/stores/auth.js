import { defineStore } from 'pinia'
import authService from '@/services/auth'
import { getToken, setToken, clearToken } from '@/services/token'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: getToken(),
    loading: false,
  }),

  getters: {
    isAuthenticated: (state) => Boolean(state.token),
    isAdmin: (state) => state.user?.role === 'admin',
  },

  actions: {
    _setSession({ access_token, user }) {
      this.token = access_token
      this.user = user
      setToken(access_token)
    },

    async register(payload) {
      this.loading = true
      try {
        const data = await authService.register(payload)
        this._setSession(data)
        return data.user
      } finally {
        this.loading = false
      }
    },

    async login(credentials) {
      this.loading = true
      try {
        const data = await authService.login(credentials)
        this._setSession(data)
        return data.user
      } finally {
        this.loading = false
      }
    },

    async fetchCurrentUser() {
      if (!this.token) return null
      try {
        this.user = await authService.me()
        return this.user
      } catch {
        this.logout()
        return null
      }
    },

    logout() {
      this.user = null
      this.token = null
      clearToken()
    },
  },
})
