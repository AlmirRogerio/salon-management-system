<script setup>
import { computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()
const user = computed(() => auth.user)

function onLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <div class="admin-shell">
    <aside class="sidebar">
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
          <span class="nav-icon">◈</span>
          Painel
        </RouterLink>
        <RouterLink to="/admin/appointments">
          <span class="nav-icon">◔</span>
          Agendamentos
        </RouterLink>
        <RouterLink to="/admin/customers">
          <span class="nav-icon">◑</span>
          Clientes
        </RouterLink>
        <RouterLink to="/admin/services">
          <span class="nav-icon">✦</span>
          Serviços
        </RouterLink>
        <RouterLink to="/admin/business-hours">
          <span class="nav-icon">◷</span>
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
