import { reactive, ref } from 'vue'
import { useAppointmentsStore } from '@/stores/appointments'
import { getApiErrorMessage } from '@/utils/apiError'

export function useAvailableSlots() {
  const store = useAppointmentsStore()

  const slots = ref([])
  const state = reactive({ loading: false, loaded: false, isOpen: true })
  const error = ref('')

  function reset() {
    slots.value = []
    state.loaded = false
    state.isOpen = true
  }

  async function load(date, serviceIds) {
    reset()
    error.value = ''
    if (!date || serviceIds.length === 0) return

    state.loading = true
    try {
      const result = await store.fetchAvailableSlots(date, serviceIds)
      slots.value = result.slots
      state.isOpen = result.is_open
      state.loaded = true
    } catch (err) {
      error.value = getApiErrorMessage(err, 'Não foi possível carregar os horários.')
    } finally {
      state.loading = false
    }
  }

  return { slots, state, error, load, reset }
}
