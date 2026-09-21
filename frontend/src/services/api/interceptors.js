import { getToken } from '@/services/token'

let onUnauthorized = null

export function setUnauthorizedHandler(handler) {
  onUnauthorized = handler
}

function attachRequestInterceptor(client) {
  client.interceptors.request.use((config) => {
    const token = getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  })
}

function attachResponseInterceptor(client) {
  client.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401 && onUnauthorized) {
        onUnauthorized()
      }
      return Promise.reject(error)
    }
  )
}

export function registerInterceptors(client) {
  attachRequestInterceptor(client)
  attachResponseInterceptor(client)
}
