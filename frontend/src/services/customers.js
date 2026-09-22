import http from '@/services/api'

export const customersService = {
  list(params = {}) {
    return http.get('/admin/customers', { params }).then((res) => res.data)
  },
}

export default customersService
