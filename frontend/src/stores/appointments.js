import { defineStore } from 'pinia'
import salonServicesService from '@/services/salonServices'
import appointmentsService from '@/services/appointments'

export const useAppointmentsStore = defineStore('appointments', {
  state: () => ({
    services: [],
    appointments: [],
    loadingServices: false,
    loadingAppointments: false,
    submitting: false,
  }),

  actions: {
    async fetchServices() {
      this.loadingServices = true
      try {
        this.services = await salonServicesService.list()
        return this.services
      } finally {
        this.loadingServices = false
      }
    },

    async fetchAppointments(params = {}) {
      this.loadingAppointments = true
      try {
        this.appointments = await appointmentsService.list(params)
        return this.appointments
      } finally {
        this.loadingAppointments = false
      }
    },

    async createAppointment(payload) {
      this.submitting = true
      try {
        const created = await appointmentsService.create(payload)
        this.appointments = [created, ...this.appointments]
        return created
      } finally {
        this.submitting = false
      }
    },

    getWeekSuggestion(targetDate) {
      return appointmentsService.weekSuggestion(targetDate)
    },

    fetchAvailableSlots(date, serviceIds) {
      return appointmentsService.availableSlots(date, serviceIds)
    },

    async rescheduleAppointment(id, scheduledAt) {
      this.submitting = true
      try {
        const updated = await appointmentsService.reschedule(id, scheduledAt)
        this.appointments = this.appointments.map((item) =>
          item.id === updated.id ? updated : item
        )
        return updated
      } finally {
        this.submitting = false
      }
    },
  },
})
