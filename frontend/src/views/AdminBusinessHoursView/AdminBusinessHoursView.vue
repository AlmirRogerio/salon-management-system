<script setup>
import { onMounted, ref } from 'vue'
import { useBusinessHoursStore } from '@/stores/businessHours'
import { getApiErrorMessage } from '@/utils/apiError'
import AdminLayout from '@/components/AdminLayout/AdminLayout.vue'

const store = useBusinessHoursStore()

const WEEKDAY_LABELS = [
  'Segunda-feira',
  'Terça-feira',
  'Quarta-feira',
  'Quinta-feira',
  'Sexta-feira',
  'Sábado',
  'Domingo',
]

const days = ref([])
const error = ref('')
const success = ref('')

function normalizeTime(value) {
  return value ? value.slice(0, 5) : '08:00'
}

onMounted(async () => {
  try {
    const data = await store.fetch()
    days.value = data.map((day) => ({
      weekday: day.weekday,
      is_open: day.is_open,
      open_time: normalizeTime(day.open_time),
      close_time: normalizeTime(day.close_time),
      slot_interval_minutes: day.slot_interval_minutes,
    }))
  } catch (err) {
    error.value = getApiErrorMessage(err, 'Não foi possível carregar o expediente.')
  }
})

function validate() {
  for (const day of days.value) {
    if (day.is_open && day.close_time <= day.open_time) {
      error.value = `${WEEKDAY_LABELS[day.weekday]}: o fechamento deve ser maior que a abertura.`
      return false
    }
    if (day.slot_interval_minutes < 1) {
      error.value = `${WEEKDAY_LABELS[day.weekday]}: intervalo inválido.`
      return false
    }
  }
  return true
}

async function onSave() {
  error.value = ''
  success.value = ''
  if (!validate()) return

  try {
    const payload = days.value.map((day) => ({
      weekday: day.weekday,
      is_open: day.is_open,
      open_time: `${day.open_time}:00`,
      close_time: `${day.close_time}:00`,
      slot_interval_minutes: Number(day.slot_interval_minutes),
    }))
    await store.save(payload)
    success.value = 'Expediente atualizado com sucesso.'
  } catch (err) {
    error.value = getApiErrorMessage(err, 'Não foi possível salvar o expediente.')
  }
}
</script>

<template>
  <AdminLayout>
    <h1>Expediente do salão</h1>
    <p class="subtitle">
      Configure os dias e horários de atendimento.
    </p>

    <p
      v-if="error"
      class="form-error"
      role="alert"
    >
      {{ error }}
    </p>
    <p
      v-if="success"
      class="form-success"
      role="status"
    >
      {{ success }}
    </p>

    <p
      v-if="store.loading"
      class="muted"
    >
      Carregando...
    </p>

    <form
      v-else
      @submit.prevent="onSave"
    >
      <ul class="days">
        <li
          v-for="day in days"
          :key="day.weekday"
          class="day"
        >
          <div class="day-header">
            <span class="day-name">{{ WEEKDAY_LABELS[day.weekday] }}</span>
            <label class="toggle">
              <input
                v-model="day.is_open"
                type="checkbox"
              >
              <span>{{ day.is_open ? 'Aberto' : 'Fechado' }}</span>
            </label>
          </div>

          <div
            v-if="day.is_open"
            class="day-fields"
          >
            <label>
              Abre
              <input
                v-model="day.open_time"
                type="time"
              >
            </label>
            <label>
              Fecha
              <input
                v-model="day.close_time"
                type="time"
              >
            </label>
            <label>
              Intervalo (min)
              <input
                v-model.number="day.slot_interval_minutes"
                type="number"
                min="1"
              >
            </label>
          </div>
        </li>
      </ul>

      <button
        type="submit"
        class="submit-btn"
        :disabled="store.saving"
      >
        {{ store.saving ? 'Salvando...' : 'Salvar expediente' }}
      </button>
    </form>
  </AdminLayout>
</template>

<style scoped src="./AdminBusinessHoursView.css"></style>
