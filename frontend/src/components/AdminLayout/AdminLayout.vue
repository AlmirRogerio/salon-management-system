<script setup>
import { computed, ref, watch } from 'vue'
import { RouterLink, useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const user = computed(() => auth.user)

const isSidebarOpen = ref(false)

function toggleSidebar() {
  isSidebarOpen.value = !isSidebarOpen.value
}

function closeSidebar() {
  isSidebarOpen.value = false
}

watch(
  () => route.fullPath,
  () => {
    isSidebarOpen.value = false
  },
)

function onLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <div class="admin-shell">
    <div
      class="sidebar-overlay"
      :class="{ 'is-visible': isSidebarOpen }"
      @click="closeSidebar"
    />

    <aside
      class="sidebar"
      :class="{ 'is-open': isSidebarOpen }"
    >
      <RouterLink
        to="/admin"
        class="brand"
      >
        <span>
          <strong>Cabeleleila</strong>
          <small>Gestão do salão</small>
        </span>
      </RouterLink>

      <nav class="nav">
        <p class="nav-label">
          Administração
        </p>
        <RouterLink to="/admin">
          <span class="nav-icon">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              aria-hidden="true"
            >
              <rect
                x="3"
                y="3"
                width="7"
                height="9"
                rx="1"
              />
              <rect
                x="14"
                y="3"
                width="7"
                height="5"
                rx="1"
              />
              <rect
                x="14"
                y="12"
                width="7"
                height="9"
                rx="1"
              />
              <rect
                x="3"
                y="16"
                width="7"
                height="5"
                rx="1"
              />
            </svg>
          </span>
          Painel
        </RouterLink>
        <RouterLink to="/admin/appointments">
          <span class="nav-icon">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              aria-hidden="true"
            >
              <rect
                x="3"
                y="4"
                width="18"
                height="18"
                rx="2"
              />
              <path d="M16 2v4" />
              <path d="M8 2v4" />
              <path d="M3 10h18" />
              <path d="m9 16 2 2 4-4" />
            </svg>
          </span>
          Agendamentos
        </RouterLink>
        <RouterLink to="/admin/customers">
          <span class="nav-icon">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              aria-hidden="true"
            >
              <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
              <circle
                cx="9"
                cy="7"
                r="4"
              />
              <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
              <path d="M16 3.13a4 4 0 0 1 0 7.75" />
            </svg>
          </span>
          Clientes
        </RouterLink>
        <RouterLink to="/admin/services">
          <span class="nav-icon">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              aria-hidden="true"
            >
              <path d="M14.5 8.5 21 2" />
              <path d="m8.5 8.5 7 7" />
              <circle
                cx="6"
                cy="6"
                r="3"
              />
              <circle
                cx="6"
                cy="18"
                r="3"
              />
              <path d="M8.12 8.12 12 12" />
              <path d="M14.8 14.8 21 21" />
            </svg>
          </span>
          Serviços
        </RouterLink>
        <RouterLink to="/admin/business-hours">
          <span class="nav-icon">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              aria-hidden="true"
            >
              <circle
                cx="12"
                cy="12"
                r="9"
              />
              <path d="M12 7v5l3 2" />
            </svg>
          </span>
          Expediente
        </RouterLink>
      </nav>

      <div class="sidebar-footer">
        <div class="profile">
          <span class="avatar">{{ user?.name?.slice(0, 1) || 'L' }}</span>
          <span class="profile-name">{{ user?.name || 'Administradora' }}</span>
        </div>
        <button
          class="logout-btn"
          @click="onLogout"
        >
          Sair da conta
        </button>
      </div>
    </aside>

    <div class="admin-content">
      <header class="topbar">
        <button
          class="menu-toggle"
          type="button"
          :aria-expanded="isSidebarOpen"
          aria-label="Abrir menu"
          @click="toggleSidebar"
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            aria-hidden="true"
          >
            <path d="M4 6h16" />
            <path d="M4 12h16" />
            <path d="M4 18h16" />
          </svg>
        </button>
        <div>
          <p class="eyebrow">
            Área administrativa
          </p>
          <p class="topbar-title">
            Cabeleleila Leila
          </p>
        </div>
      </header>

      <main class="page-content">
        <slot />
      </main>
    </div>
  </div>
</template>

<style scoped src="./AdminLayout.css"></style>
