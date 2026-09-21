import { defineStore } from 'pinia'
import salonServicesService from '@/services/salonServices'

function sortByName(services) {
  return [...services].sort((a, b) => a.name.localeCompare(b.name, 'pt-BR'))
}

export const useAdminServicesStore = defineStore('adminServices', {
  state: () => ({
    services: [],
    loading: false,
    saving: false,
  }),

  actions: {
    async fetchAll() {
      this.loading = true
      try {
        this.services = await salonServicesService.listAll()
        return this.services
      } finally {
        this.loading = false
      }
    },

    async create(payload) {
      this.saving = true
      try {
        const created = await salonServicesService.create(payload)
        this.services = sortByName([...this.services, created])
        return created
      } finally {
        this.saving = false
      }
    },

    async update(id, payload) {
      this.saving = true
      try {
        const updated = await salonServicesService.update(id, payload)
        this.services = sortByName(
          this.services.map((item) => (item.id === updated.id ? updated : item))
        )
        return updated
      } finally {
        this.saving = false
      }
    },
  },
})
