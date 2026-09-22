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
  <div class="app-shell">
    <header class="topbar">
      <RouterLink
        to="/dashboard"
        class="brand"
      >
        <span>
          <strong>Cabeleleila</strong>
          <small>Salão da Leila</small>
        </span>
      </RouterLink>

      <div class="topbar-right">
        <div class="user-info">
          <span class="avatar">{{ user?.name?.slice(0, 1) || 'C' }}</span>
          <span class="welcome">Olá, {{ user?.name || 'cliente' }}</span>
        </div>
        <button
          class="logout-btn"
          aria-label="Sair da conta"
          @click="onLogout"
        >
          Sair
        </button>
      </div>
    </header>

    <main class="content">
      <slot />
    </main>
  </div>
</template>

<style scoped src="./AppLayout.css"></style>
