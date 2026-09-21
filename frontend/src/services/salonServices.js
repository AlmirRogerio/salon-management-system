import http from '@/services/api'

export const salonServicesService = {
  list() {
    return http.get('/services').then((res) => res.data)
  },

  listAll() {
    return http.get('/services/all').then((res) => res.data)
  },

  create(payload) {
    return http.post('/services', payload).then((res) => res.data)
  },

  update(id, payload) {
    return http.patch(`/services/${id}`, payload).then((res) => res.data)
  },
}

export default salonServicesService
