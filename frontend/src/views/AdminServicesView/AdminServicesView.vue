<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useAdminServicesStore } from '@/stores/services'
import { getApiErrorMessage } from '@/utils/apiError'
import { formatCurrency, formatDuration } from '@/utils/format'
import AdminLayout from '@/components/AdminLayout/AdminLayout.vue'

const store = useAdminServicesStore()

const error = ref('')
const success = ref('')

const form = reactive({
  id: null,
  name: '',
  description: '',
  price: '',
  duration_minutes: '',
  active: true,
})

const fieldErrors = reactive({
  name: '',
  description: '',
  price: '',
  duration_minutes: '',
})

onMounted(async () => {
  try {
    await store.fetchAll()
  } catch (err) {
    error.value = getApiErrorMessage(err, 'Não foi possível carregar os serviços.')
  }
})

function resetForm() {
  form.id = null
  form.name = ''
  form.description = ''
  form.price = ''
  form.duration_minutes = ''
  form.active = true
  clearFieldErrors()
}

function clearFieldErrors() {
  fieldErrors.name = ''
  fieldErrors.description = ''
  fieldErrors.price = ''
  fieldErrors.duration_minutes = ''
}

function startEdit(service) {
  form.id = service.id
  form.name = service.name
  form.description = service.description
  form.price = String(service.price)
  form.duration_minutes = String(service.duration_minutes)
  form.active = service.active
  clearFieldErrors()
  error.value = ''
  success.value = ''
}

function validate() {
  clearFieldErrors()
  let valid = true

  if (!form.name.trim()) {
    fieldErrors.name = 'Informe o nome.'
    valid = false
  }
  if (!form.description.trim()) {
    fieldErrors.description = 'Informe a descrição.'
    valid = false
  }
  const price = Number(form.price)
  if (form.price === '' || Number.isNaN(price) || price < 0) {
    fieldErrors.price = 'Informe um preço válido.'
    valid = false
  }
  const duration = Number(form.duration_minutes)
  if (
    form.duration_minutes === '' ||
    !Number.isInteger(duration) ||
    duration < 1
  ) {
    fieldErrors.duration_minutes = 'Informe uma duração válida (min. 1).'
    valid = false
  }

  return valid
}

async function onSubmit() {
  error.value = ''
  success.value = ''
  if (!validate()) return

  const payload = {
    name: form.name.trim(),
    description: form.description.trim(),
    price: Number(form.price),
    duration_minutes: Number(form.duration_minutes),
    active: form.active,
  }

  try {
    if (form.id) {
      await store.update(form.id, payload)
      success.value = 'Serviço atualizado com sucesso.'
    } else {
      await store.create(payload)
      success.value = 'Serviço cadastrado com sucesso.'
    }
    resetForm()
  } catch (err) {
    error.value = getApiErrorMessage(err, 'Não foi possível salvar o serviço.')
  }
}
</script>

<template>
  <AdminLayout>
    <h1>Serviços</h1>
    <p class="subtitle">
      Cadastre e edite os serviços oferecidos pelo salão.
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

    <form
      class="service-form"
      novalidate
      @submit.prevent="onSubmit"
    >
      <h2>{{ form.id ? 'Editar serviço' : 'Novo serviço' }}</h2>

      <label class="field">
        Nome
        <input
          v-model="form.name"
          type="text"
          maxlength="150"
        >
        <span
          v-if="fieldErrors.name"
          class="field-error"
        >{{ fieldErrors.name }}</span>
      </label>

      <label class="field">
        Descrição
        <textarea
          v-model="form.description"
          rows="2"
        />
        <span
          v-if="fieldErrors.description"
          class="field-error"
        >{{ fieldErrors.description }}</span>
      </label>

      <div class="row">
        <label class="field">
          Preço (R$)
          <input
            v-model="form.price"
            type="number"
            min="0"
            step="0.01"
          >
          <span
            v-if="fieldErrors.price"
            class="field-error"
          >{{ fieldErrors.price }}</span>
        </label>

        <label class="field">
          Duração (min)
          <input
            v-model="form.duration_minutes"
            type="number"
            min="1"
            step="1"
          >
          <span
            v-if="fieldErrors.duration_minutes"
            class="field-error"
          >{{ fieldErrors.duration_minutes }}</span>
        </label>

        <label class="toggle">
          <input
            v-model="form.active"
            type="checkbox"
          >
          <span>{{ form.active ? 'Ativo' : 'Inativo' }}</span>
        </label>
      </div>

      <div class="form-actions">
        <button
          type="submit"
          class="submit-btn"
          :disabled="store.saving"
        >
          {{ store.saving ? 'Salvando...' : form.id ? 'Salvar alterações' : 'Cadastrar serviço' }}
        </button>
        <button
          v-if="form.id"
          type="button"
          class="ghost-btn"
          @click="resetForm"
        >
          Cancelar edição
        </button>
      </div>
    </form>

    <p
      v-if="store.loading"
      class="muted"
    >
      Carregando...
    </p>
    <p
      v-else-if="!store.services.length"
      class="muted empty"
    >
      Nenhum serviço cadastrado.
    </p>
    <ul
      v-else
      class="list"
    >
      <li
        v-for="service in store.services"
        :key="service.id"
        class="card"
        :class="{ inactive: !service.active }"
      >
        <div class="card-info">
          <div class="card-title">
            <span class="name">{{ service.name }}</span>
            <span
              v-if="!service.active"
              class="badge"
            >Inativo</span>
          </div>
          <p class="desc">
            {{ service.description }}
          </p>
          <p class="meta">
            {{ formatCurrency(service.price) }} · {{ formatDuration(service.duration_minutes) }}
          </p>
        </div>
        <button
          type="button"
          class="edit-btn"
          @click="startEdit(service)"
        >
          Editar
        </button>
      </li>
    </ul>
  </AdminLayout>
</template>

<style scoped src="./AdminServicesView.css"></style>
