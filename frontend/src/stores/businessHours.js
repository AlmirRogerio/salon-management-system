import { defineStore } from 'pinia'
import businessHoursService from '@/services/businessHours'

export const useBusinessHoursStore = defineStore('businessHours', {
  state: () => ({
    days: [],
    loading: false,
    saving: false,
  }),

  actions: {
    async fetch() {
      this.loading = true
      try {
        this.days = await businessHoursService.list()
        return this.days
      } finally {
        this.loading = false
      }
    },

    async save(days) {
      this.saving = true
      try {
        this.days = await businessHoursService.update(days)
        return this.days
      } finally {
        this.saving = false
      }
    },
  },
})
