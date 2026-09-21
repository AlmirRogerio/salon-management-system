import http from '@/services/api'

export const adminAppointmentsService = {
  list(params = {}) {
    return http
      .get('/admin/appointments', {
        params,
        paramsSerializer: {
          indexes: null,
        },
      })
      .then((res) => res.data)
  },

  getById(id) {
    return http.get(`/admin/appointments/${id}`).then((res) => res.data)
  },

  confirm(id) {
    return http
      .patch(`/admin/appointments/${id}/confirm`)
      .then((res) => res.data)
  },

  cancel(id) {
    return http
      .patch(`/admin/appointments/${id}/cancel`)
      .then((res) => res.data)
  },

  complete(id) {
    return http
      .patch(`/admin/appointments/${id}/complete`)
      .then((res) => res.data)
  },

  reschedule(id, scheduledAt) {
    return http
      .patch(`/admin/appointments/${id}/reschedule`, {
        scheduled_at: scheduledAt,
      })
      .then((res) => res.data)
  },

  updateServiceStatus(id, serviceRowId, status) {
    return http
      .patch(`/admin/appointments/${id}/services/${serviceRowId}`, { status })
      .then((res) => res.data)
  },
}

export default adminAppointmentsService
