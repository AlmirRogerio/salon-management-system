<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useAppointmentsStore } from '@/stores/appointments'
import { useAvailableSlots } from '@/composables/useAvailableSlots'
import { getApiErrorMessage } from '@/utils/apiError'
import {
  formatCurrency,
  formatDateTime,
  formatDuration,
  formatStatus,
} from '@/utils/format'
import AppLayout from '@/components/AppLayout/AppLayout.vue'
import SlotPicker from '@/components/SlotPicker/SlotPicker.vue'

const store = useAppointmentsStore()
const { slots, state: slotsState, load: loadSlots, reset: resetSlots } =
  useAvailableSlots()

const filters = reactive({ start: '', end: '' })
const error = ref('')
const expandedId = ref(null)
const rescheduling = reactive({
  id: null,
  date: '',
  selectedSlot: '',
  serviceIds: [],
  error: '',
})

async function load() {
  error.value = ''
  const params = {}
  if (filters.start) params.start = `${filters.start}T00:00:00`
  if (filters.end) params.end = `${filters.end}T23:59:59`
  try {
    await store.fetchAppointments(params)
  } catch (err) {
    error.value = getApiErrorMessage(err, 'Não foi possível carregar os agendamentos.')
  }
}

onMounted(load)

function clearFilters() {
  filters.start = ''
  filters.end = ''
  load()
}

function toggleDetail(id) {
  expandedId.value = expandedId.value === id ? null : id
}

function startReschedule(appointment) {
  rescheduling.id = appointment.id
  rescheduling.date = appointment.scheduled_at.slice(0, 10)
  rescheduling.selectedSlot = ''
  rescheduling.serviceIds = appointment.services.map((item) => item.service_id)
  rescheduling.error = ''
  loadRescheduleSlots()
}

function cancelReschedule() {
  rescheduling.id = null
  rescheduling.date = ''
  rescheduling.selectedSlot = ''
  rescheduling.serviceIds = []
  rescheduling.error = ''
  resetSlots()
}

async function loadRescheduleSlots() {
  rescheduling.selectedSlot = ''
  await loadSlots(rescheduling.date, rescheduling.serviceIds)
}

async function confirmReschedule(id) {
  rescheduling.error = ''
  if (!rescheduling.selectedSlot) {
    rescheduling.error = 'Escolha um horário disponível.'
    return
  }
  try {
    await store.rescheduleAppointment(id, rescheduling.selectedSlot)
    cancelReschedule()
  } catch (err) {
    rescheduling.error = getApiErrorMessage(err, 'Não foi possível reagendar.')
  }
}
</script>

<template>
  <AppLayout>
    <RouterLink
      to="/dashboard"
      class="back-link"
    >
      ← Voltar para o início
    </RouterLink>
    <div class="header">
      <h1>Meus agendamentos</h1>
      <RouterLink
        to="/appointments/new"
        class="new-btn"
      >
        Novo agendamento
      </RouterLink>
    </div>

    <form
      class="filters"
      @submit.prevent="load"
    >
      <label>
        De
        <input
          v-model="filters.start"
          type="date"
        >
      </label>
      <label>
        Até
        <input
          v-model="filters.end"
          type="date"
        >
      </label>
      <button
        type="submit"
        class="filter-btn"
      >
        Filtrar
      </button>
      <button
        type="button"
        class="filter-btn ghost"
        @click="clearFilters"
      >
        Limpar
      </button>
    </form>

    <p
      v-if="error"
      class="form-error"
      role="alert"
    >
      {{ error }}
    </p>
    <p
      v-if="store.loadingAppointments"
      class="muted"
    >
      Carregando...
    </p>

    <p
      v-else-if="!store.appointments.length"
      class="muted empty"
    >
      Nenhum agendamento encontrado.
    </p>

    <ul
      v-else
      class="list"
    >
      <li
        v-for="appt in store.appointments"
        :key="appt.id"
        class="card"
      >
        <div
          class="card-head"
          @click="toggleDetail(appt.id)"
        >
          <div>
            <p class="date">
              {{ formatDateTime(appt.scheduled_at) }}
            </p>
            <p class="meta">
              {{ appt.services.length }} serviço(s) ·
              {{ formatCurrency(appt.total_price) }} ·
              {{ formatDuration(appt.total_duration_minutes) }}
            </p>
          </div>
          <span
            class="status"
            :class="`status-${appt.status}`"
          >
            {{ formatStatus(appt.status) }}
          </span>
        </div>

        <div
          v-if="expandedId === appt.id"
          class="card-body"
        >
          <ul class="service-lines">
            <li
              v-for="item in appt.services"
              :key="item.id"
            >
              <span>{{ item.service_name }}</span>
              <span class="muted">
                {{ formatCurrency(item.price) }} · {{ formatDuration(item.duration_minutes) }} ·
                {{ formatStatus(item.status) }}
              </span>
            </li>
          </ul>

          <p
            v-if="appt.notes"
            class="notes"
          >
            Observações: {{ appt.notes }}
          </p>

          <div
            v-if="rescheduling.id === appt.id"
            class="reschedule"
          >
            <label class="reschedule-date">
              Nova data
              <input
                v-model="rescheduling.date"
                type="date"
                @change="loadRescheduleSlots"
              >
            </label>

            <SlotPicker
              :slots="slots"
              :state="slotsState"
              :selected="rescheduling.selectedSlot"
              :has-query="Boolean(rescheduling.date)"
              @select="rescheduling.selectedSlot = $event"
            >
              <template #empty-query>
                Escolha uma data para ver os horários disponíveis.
              </template>
            </SlotPicker>

            <div class="reschedule-actions">
              <button
                class="filter-btn"
                :disabled="store.submitting"
                @click="confirmReschedule(appt.id)"
              >
                Salvar
              </button>
              <button
                class="filter-btn ghost"
                @click="cancelReschedule"
              >
                Cancelar
              </button>
            </div>
            <p
              v-if="rescheduling.error"
              class="field-error"
            >
              {{ rescheduling.error }}
            </p>
          </div>

          <div
            v-else
            class="card-actions"
          >
            <button
              v-if="appt.can_reschedule"
              class="filter-btn"
              @click="startReschedule(appt)"
            >
              Reagendar
            </button>
            <p
              v-else
              class="muted phone-note"
            >
              Alterações a menos de 2 dias só por telefone.
            </p>
          </div>
        </div>
      </li>
    </ul>
  </AppLayout>
</template>

<style scoped src="./AppointmentsView.css"></style>
