<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useCustomersStore } from '@/stores/customers'
import { getApiErrorMessage } from '@/utils/apiError'
import { formatDateTime } from '@/utils/format'
import { formatPhone } from '@/utils/phone'
import AdminLayout from '@/components/AdminLayout/AdminLayout.vue'

const store = useCustomersStore()

const filters = reactive({ search: '' })
const error = ref('')

async function load() {
  error.value = ''
  const params = {}
  if (filters.search.trim()) params.search = filters.search.trim()
  try {
    await store.fetchAll(params)
  } catch (err) {
    error.value = getApiErrorMessage(err, 'Não foi possível carregar os clientes.')
  }
}

onMounted(load)

function clearFilters() {
  filters.search = ''
  load()
}
</script>

<template>
  <AdminLayout>
    <h1>Clientes</h1>
    <p class="subtitle">
      Consulte os clientes cadastrados e o histórico de agendamentos.
    </p>

    <form
      class="filters"
      @submit.prevent="load"
    >
      <label>
        Buscar
        <input
          v-model="filters.search"
          type="search"
          placeholder="Nome, e-mail ou telefone"
        >
      </label>
      <button
        type="submit"
        class="filter-btn"
      >
        Buscar
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
      v-if="store.loading"
      class="muted"
    >
      Carregando...
    </p>
    <p
      v-else-if="!store.customers.length"
      class="muted empty"
    >
      Nenhum cliente encontrado.
    </p>

    <div
      v-else
      class="table-wrap"
    >
      <table class="table">
        <thead>
          <tr>
            <th>Nome</th>
            <th>Contato</th>
            <th class="num">
              Agendamentos
            </th>
            <th>Último agendamento</th>
            <th>Cliente desde</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="customer in store.customers"
            :key="customer.id"
          >
            <td data-label="Nome">
              <span class="name">{{ customer.name }}</span>
            </td>
            <td data-label="Contato">
              <span class="contact-phone">{{ formatPhone(customer.phone) }}</span>
              <span class="contact-email">{{ customer.email }}</span>
            </td>
            <td
              class="num"
              data-label="Agendamentos"
            >
              {{ customer.appointments_count }}
            </td>
            <td data-label="Último agendamento">
              {{ customer.last_appointment_at ? formatDateTime(customer.last_appointment_at) : '—' }}
            </td>
            <td data-label="Cliente desde">
              {{ formatDateTime(customer.created_at) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </AdminLayout>
</template>

<style scoped src="./AdminCustomersView.css"></style>
