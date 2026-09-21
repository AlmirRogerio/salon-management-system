<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAppointmentsStore } from '@/stores/appointments'
import { useAvailableSlots } from '@/composables/useAvailableSlots'
import { getApiErrorMessage } from '@/utils/apiError'
import { formatCurrency, formatDuration, formatDateTime } from '@/utils/format'
import AppLayout from '@/components/AppLayout/AppLayout.vue'
import SlotPicker from '@/components/SlotPicker/SlotPicker.vue'

const router = useRouter()
const store = useAppointmentsStore()
const { slots, state: slotsState, error: slotsError, load: loadAvailableSlots, reset: resetSlots } =
  useAvailableSlots()

const form = reactive({
  date: '',
  selectedSlot: '',
  serviceIds: [],
  notes: '',
})

const formError = ref('')
const fieldErrors = reactive({ date: '', selectedSlot: '', serviceIds: '' })
const suggestion = ref(null)

const services = computed(() => store.services)

const selectedServices = computed(() =>
  services.value.filter((s) => form.serviceIds.includes(s.id))
)

const totalPrice = computed(() =>
  selectedServices.value.reduce((sum, s) => sum + Number(s.price), 0)
)

const totalDuration = computed(() =>
  selectedServices.value.reduce((sum, s) => sum + Number(s.duration_minutes), 0)
)

const hasSlotQuery = computed(
  () => Boolean(form.date) && form.serviceIds.length > 0
)

onMounted(async () => {
  try {
    await store.fetchServices()
  } catch (err) {
    formError.value = getApiErrorMessage(err, 'Não foi possível carregar os serviços.')
  }
})

function toggleService(id) {
  const index = form.serviceIds.indexOf(id)
  if (index === -1) {
    form.serviceIds.push(id)
    return
  }
  form.serviceIds.splice(index, 1)
}

async function loadSlots() {
  form.selectedSlot = ''
  await loadAvailableSlots(form.date, form.serviceIds)
  if (slotsError.value) {
    formError.value = slotsError.value
  }
}

async function checkWeekSuggestion() {
  suggestion.value = null
  if (!form.date) return
  try {
    const result = await store.getWeekSuggestion(`${form.date}T12:00:00`)
    if (result.has_suggestion) {
      suggestion.value = result
    }
  } catch {
    suggestion.value = null
  }
}

function onDateChange() {
  checkWeekSuggestion()
  loadSlots()
}

function applySuggestion() {
  if (!suggestion.value?.suggested_date) return
  form.date = suggestion.value.suggested_date.slice(0, 10)
  suggestion.value = null
  loadSlots()
}

watch(
  () => form.serviceIds.slice(),
  () => {
    if (!form.date) {
      resetSlots()
      return
    }
    loadSlots()
  }
)

function validate() {
  fieldErrors.date = ''
  fieldErrors.selectedSlot = ''
  fieldErrors.serviceIds = ''

  if (form.serviceIds.length === 0) {
    fieldErrors.serviceIds = 'Selecione ao menos um serviço.'
  }
  if (!form.date) {
    fieldErrors.date = 'Escolha uma data.'
  }
  if (!form.selectedSlot) {
    fieldErrors.selectedSlot = 'Escolha um horário disponível.'
  }

  return !fieldErrors.date && !fieldErrors.selectedSlot && !fieldErrors.serviceIds
}

async function onSubmit() {
  formError.value = ''
  if (!validate()) return

  try {
    await store.createAppointment({
      scheduled_at: form.selectedSlot,
      service_ids: form.serviceIds,
      notes: form.notes.trim() || null,
    })
    router.push('/appointments')
  } catch (err) {
    formError.value = getApiErrorMessage(err, 'Não foi possível criar o agendamento.')
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
    <h1>Novo agendamento</h1>

    <p
      v-if="formError"
      class="form-error"
      role="alert"
    >
      {{ formError }}
    </p>

    <form
      novalidate
      @submit.prevent="onSubmit"
    >
      <section class="block">
        <h2>Serviços</h2>
        <p
          v-if="fieldErrors.serviceIds"
          class="field-error"
        >
          {{ fieldErrors.serviceIds }}
        </p>
        <p
          v-if="store.loadingServices"
          class="muted"
        >
          Carregando serviços...
        </p>

        <ul
          v-else
          class="service-list"
        >
          <li
            v-for="service in services"
            :key="service.id"
          >
            <label
              class="service-item"
              :class="{ selected: form.serviceIds.includes(service.id) }"
            >
              <input
                type="checkbox"
                :checked="form.serviceIds.includes(service.id)"
                @change="toggleService(service.id)"
              >
              <span class="service-info">
                <span class="service-name">{{ service.name }}</span>
                <span class="service-desc">{{ service.description }}</span>
              </span>
              <span class="service-meta">
                {{ formatCurrency(service.price) }} · {{ formatDuration(service.duration_minutes) }}
              </span>
            </label>
          </li>
        </ul>
      </section>

      <section class="block">
        <h2>Data</h2>
        <input
          v-model="form.date"
          type="date"
          class="input"
          @change="onDateChange"
        >
        <p
          v-if="fieldErrors.date"
          class="field-error"
        >
          {{ fieldErrors.date }}
        </p>

        <div
          v-if="suggestion"
          class="suggestion"
          role="status"
        >
          <p>
            Você já tem um agendamento nesta semana em
            <strong>{{ formatDateTime(suggestion.suggested_date) }}</strong>.
            Deseja agendar no mesmo dia?
          </p>
          <button
            type="button"
            class="link-btn"
            @click="applySuggestion"
          >
            Usar o mesmo dia
          </button>
        </div>
      </section>

      <section class="block">
        <h2>Horário</h2>
        <SlotPicker
          :slots="slots"
          :state="slotsState"
          :selected="form.selectedSlot"
          :has-query="hasSlotQuery"
          @select="form.selectedSlot = $event"
        />
        <p
          v-if="fieldErrors.selectedSlot"
          class="field-error"
        >
          {{ fieldErrors.selectedSlot }}
        </p>
      </section>

      <section class="block">
        <h2>Observações (opcional)</h2>
        <textarea
          v-model="form.notes"
          class="input"
          rows="3"
          maxlength="500"
          placeholder="Alguma preferência ou observação?"
        />
      </section>

      <div
        v-if="form.serviceIds.length"
        class="summary"
      >
        <span>Total: <strong>{{ formatCurrency(totalPrice) }}</strong></span>
        <span>Duração estimada: <strong>{{ formatDuration(totalDuration) }}</strong></span>
      </div>

      <button
        type="submit"
        class="submit-btn"
        :disabled="store.submitting"
      >
        {{ store.submitting ? 'Agendando...' : 'Confirmar agendamento' }}
      </button>
    </form>
  </AppLayout>
</template>

<style scoped src="./NewAppointmentView.css"></style>
