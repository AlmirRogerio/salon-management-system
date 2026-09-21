import { defineStore } from 'pinia'
import adminAppointmentsService from '@/services/adminAppointments'

export const useAdminAppointmentsStore = defineStore('adminAppointments', {
  state: () => ({
    appointments: [],
    loading: false,
    updatingId: null,
  }),

  actions: {
    async fetchAll(params = {}) {
      this.loading = true
      try {
        this.appointments = await adminAppointmentsService.list(params)
        return this.appointments
      } finally {
        this.loading = false
      }
    },

    _replace(updated) {
      this.appointments = this.appointments.map((item) =>
        item.id === updated.id ? updated : item
      )
    },

    async confirm(id) {
      this.updatingId = id
      try {
        this._replace(await adminAppointmentsService.confirm(id))
      } finally {
        this.updatingId = null
      }
    },

    async cancel(id) {
      this.updatingId = id
      try {
        this._replace(await adminAppointmentsService.cancel(id))
      } finally {
        this.updatingId = null
      }
    },

    async complete(id) {
      this.updatingId = id
      try {
        this._replace(await adminAppointmentsService.complete(id))
      } finally {
        this.updatingId = null
      }
    },

    async reschedule(id, scheduledAt) {
      this.updatingId = id
      try {
        this._replace(await adminAppointmentsService.reschedule(id, scheduledAt))
      } finally {
        this.updatingId = null
      }
    },

    async updateServiceStatus(id, serviceRowId, status) {
      this.updatingId = id
      try {
        this._replace(
          await adminAppointmentsService.updateServiceStatus(
            id,
            serviceRowId,
            status
          )
        )
      } finally {
        this.updatingId = null
      }
    },
  },
})
