import { defineStore } from 'pinia'
import customersService from '@/services/customers'

export const useCustomersStore = defineStore('customers', {
  state: () => ({
    customers: [],
    loading: false,
  }),

  actions: {
    async fetchAll(params = {}) {
      this.loading = true
      try {
        this.customers = await customersService.list(params)
        return this.customers
      } finally {
        this.loading = false
      }
    },
  },
})
