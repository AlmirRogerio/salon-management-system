import http from '@/services/api'

export const businessHoursService = {
  list() {
    return http.get('/business-hours').then((res) => res.data)
  },

  update(days) {
    return http.put('/business-hours', { days }).then((res) => res.data)
  },
}

export default businessHoursService
