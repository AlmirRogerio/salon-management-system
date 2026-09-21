import http from '@/services/api'

export const appointmentsService = {
  create(payload) {
    return http.post('/appointments', payload).then((res) => res.data)
  },

  list(params = {}) {
    return http.get('/appointments', { params }).then((res) => res.data)
  },

  getById(id) {
    return http.get(`/appointments/${id}`).then((res) => res.data)
  },

  weekSuggestion(targetDate) {
    return http
      .get('/appointments/week-suggestion', {
        params: { target_date: targetDate },
      })
      .then((res) => res.data)
  },

  availableSlots(date, serviceIds) {
    return http
      .get('/appointments/available-slots', {
        params: { date, service_ids: serviceIds },
        paramsSerializer: {
          indexes: null,
        },
      })
      .then((res) => res.data)
  },

  reschedule(id, scheduledAt) {
    return http
      .patch(`/appointments/${id}`, { scheduled_at: scheduledAt })
      .then((res) => res.data)
  },
}

export default appointmentsService
