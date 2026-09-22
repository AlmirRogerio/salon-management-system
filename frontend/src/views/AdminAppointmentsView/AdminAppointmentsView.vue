<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useAdminAppointmentsStore } from '@/stores/adminAppointments'
import { useAvailableSlots } from '@/composables/useAvailableSlots'
import { getApiErrorMessage } from '@/utils/apiError'
import {
  formatCurrency,
  formatDateTime,
  formatDuration,
  formatStatus,
} from '@/utils/format'
import AdminLayout from '@/components/AdminLayout/AdminLayout.vue'
import SlotPicker from '@/components/SlotPicker/SlotPicker.vue'
import ConfirmDialog from '@/components/ConfirmDialog/ConfirmDialog.vue'

const store = useAdminAppointmentsStore()
const { slots, state: slotsState, load: loadSlots, reset: resetSlots } =
  useAvailableSlots()

const STATUS_OPTIONS = [
  { value: 'pending', label: 'Pendente' },
  { value: 'confirmed', label: 'Confirmado' },
  { value: 'completed', label: 'Concluído' },
  { value: 'canceled', label: 'Cancelado' },
]

const SERVICE_STATUS_OPTIONS = [
  { value: 'pending', label: 'Pendente' },
  { value: 'in_progress', label: 'Em andamento' },
  { value: 'completed', label: 'Concluído' },
  { value: 'canceled', label: 'Cancelado' },
]

const filters = reactive({ start: '', end: '', status: '' })
const error = ref('')
const success = ref('')
const expandedId = ref(null)

const dialog = reactive({
  open: false,
  title: '',
  message: '',
  confirmLabel: 'Confirmar',
  variant: 'primary',
  busy: false,
  action: null,
})

function openDialog({ title, message, confirmLabel, variant, action }) {
  dialog.title = title
  dialog.message = message
  dialog.confirmLabel = confirmLabel ?? 'Confirmar'
  dialog.variant = variant ?? 'primary'
  dialog.action = action
  dialog.busy = false
  dialog.open = true
}

function closeDialog() {
  if (dialog.busy) return
  dialog.open = false
  dialog.action = null
}

async function runDialogAction() {
  if (!dialog.action) return
  dialog.busy = true
  try {
    await dialog.action()
    dialog.open = false
    dialog.action = null
  } finally {
    dialog.busy = false
  }
}

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
  if (filters.status) params.statuses = [filters.status]
  try {
    await store.fetchAll(params)
  } catch (err) {
    error.value = getApiErrorMessage(err, 'Não foi possível carregar os agendamentos.')
  }
}

onMounted(load)

function clearFilters() {
  filters.start = ''
  filters.end = ''
  filters.status = ''
  load()
}

function toggleDetail(id) {
  expandedId.value = expandedId.value === id ? null : id
}

function flashSuccess(message) {
  success.value = message
  window.setTimeout(() => {
    if (success.value === message) success.value = ''
  }, 3000)
}

async function onConfirm(appt) {
  error.value = ''
  try {
    await store.confirm(appt.id)
    flashSuccess('Agendamento confirmado.')
  } catch (err) {
    error.value = getApiErrorMessage(err, 'Não foi possível confirmar.')
  }
}

function onCancel(appt) {
  openDialog({
    title: 'Cancelar agendamento',
    message: 'Deseja realmente cancelar este agendamento? Esta ação não pode ser desfeita.',
    confirmLabel: 'Cancelar agendamento',
    variant: 'danger',
    action: async () => {
      error.value = ''
      try {
        await store.cancel(appt.id)
        flashSuccess('Agendamento cancelado.')
      } catch (err) {
        error.value = getApiErrorMessage(err, 'Não foi possível cancelar.')
      }
    },
  })
}

function onComplete(appt) {
  const isFuture = new Date(appt.scheduled_at).getTime() > Date.now()
  openDialog({
    title: 'Concluir agendamento',
    message: isFuture
      ? 'Este agendamento está marcado para uma data futura. Ao concluir agora, o horário será remarcado para o intervalo disponível anterior mais próximo do momento atual, dentro do horário de funcionamento. Deseja continuar?'
      : 'Deseja concluir este agendamento?',
    confirmLabel: 'Concluir',
    variant: 'primary',
    action: async () => {
      error.value = ''
      try {
        await store.complete(appt.id)
        flashSuccess('Agendamento concluído.')
      } catch (err) {
        error.value = getApiErrorMessage(err, 'Não foi possível concluir.')
      }
    },
  })
}

async function onServiceStatusChange(appt, item, event) {
  error.value = ''
  const newStatus = event.target.value
  try {
    await store.updateServiceStatus(appt.id, item.id, newStatus)
    flashSuccess('Status do serviço atualizado.')
  } catch (err) {
    error.value = getApiErrorMessage(err, 'Não foi possível atualizar o serviço.')
  }
}

const isFinal = (appt) =>
  appt.status === 'completed' || appt.status === 'canceled'

function startReschedule(appt) {
  rescheduling.id = appt.id
  rescheduling.date = appt.scheduled_at.slice(0, 10)
  rescheduling.selectedSlot = ''
  rescheduling.serviceIds = appt.services.map((item) => item.service_id)
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
    await store.reschedule(id, rescheduling.selectedSlot)
    cancelReschedule()
    flashSuccess('Agendamento reagendado.')
  } catch (err) {
    rescheduling.error = getApiErrorMessage(err, 'Não foi possível reagendar.')
  }
}
</script>

<template>
  <AdminLayout>
    <h1>Agendamentos</h1>
    <p class="subtitle">
      Acompanhe, confirme e gerencie os agendamentos recebidos.
    </p>

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
      <label>
        Status
        <select v-model="filters.status">
          <option value="">
            Todos
          </option>
          <option
            v-for="opt in STATUS_OPTIONS"
            :key="opt.value"
            :value="opt.value"
          >
            {{ opt.label }}
          </option>
        </select>
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
            <p class="customer">
              {{ appt.customer_name }}
              <span class="phone">· {{ appt.customer_phone }}</span>
            </p>
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
              <div class="service-info">
                <span class="service-name">{{ item.service_name }}</span>
                <span class="muted">
                  {{ formatCurrency(item.price) }} · {{ formatDuration(item.duration_minutes) }}
                </span>
              </div>
              <label class="service-status">
                <span class="sr-only">Status do serviço</span>
                <select
                  :value="item.status"
                  :disabled="isFinal(appt) || store.updatingId === appt.id"
                  @change="onServiceStatusChange(appt, item, $event)"
                >
                  <option
                    v-for="opt in SERVICE_STATUS_OPTIONS"
                    :key="opt.value"
                    :value="opt.value"
                  >
                    {{ opt.label }}
                  </option>
                </select>
              </label>
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
                :disabled="store.updatingId === appt.id"
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
            v-else-if="!isFinal(appt)"
            class="card-actions"
          >
            <button
              v-if="appt.status === 'pending'"
              class="action-btn confirm"
              :disabled="store.updatingId === appt.id"
              @click="onConfirm(appt)"
            >
              Confirmar
            </button>
            <button
              v-if="appt.status === 'confirmed'"
              class="action-btn confirm"
              :disabled="store.updatingId === appt.id"
              @click="onComplete(appt)"
            >
              Concluir
            </button>
            <button
              class="action-btn"
              :disabled="store.updatingId === appt.id"
              @click="startReschedule(appt)"
            >
              Reagendar
            </button>
            <button
              class="action-btn danger"
              :disabled="store.updatingId === appt.id"
              @click="onCancel(appt)"
            >
              Cancelar
            </button>
          </div>
        </div>
      </li>
    </ul>

    <ConfirmDialog
      :open="dialog.open"
      :title="dialog.title"
      :message="dialog.message"
      :confirm-label="dialog.confirmLabel"
      :variant="dialog.variant"
      :busy="dialog.busy"
      @confirm="runDialogAction"
      @cancel="closeDialog"
    />
  </AdminLayout>
</template>

<style scoped src="./AdminAppointmentsView.css"></style>
