import http from '@/services/api'

export const authService = {
  register(payload) {
    return http.post('/auth/register', payload).then((res) => res.data)
  },

  login(credentials) {
    return http.post('/auth/login', credentials).then((res) => res.data)
  },

  me() {
    return http.get('/auth/me').then((res) => res.data)
  },
}

export default authService
