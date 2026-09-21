import apiClient from './client'
import { registerInterceptors, setUnauthorizedHandler } from './interceptors'

registerInterceptors(apiClient)

export { apiClient, setUnauthorizedHandler }
export default apiClient
