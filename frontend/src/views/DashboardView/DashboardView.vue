<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import brandSeal from '@/assets/logo/cabeleleila-mark-light.svg'
import AppLayout from '@/components/AppLayout/AppLayout.vue'

const auth = useAuthStore()
const firstName = computed(() => auth.user?.name?.trim().split(' ')[0] || 'cliente')
</script>

<template>
  <AppLayout>
    <section class="hero">
      <div>
        <p class="eyebrow">
          Seu momento de cuidado
        </p>
        <h1>Olá, {{ firstName }}.</h1>
        <p>
          Escolha seus serviços e encontre o melhor horário para você no Cabeleleila.
        </p>
        <RouterLink
          to="/appointments/new"
          class="hero-action"
        >
          Agendar um horário
        </RouterLink>
      </div>
      <div
        class="hero-detail"
        aria-hidden="true"
      >
        <img
          class="hero-seal"
          :src="brandSeal"
          alt=""
        >
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <div>
          <p class="eyebrow">
            Próximos passos
          </p>
          <h2>Como podemos ajudar?</h2>
        </div>
      </div>

      <div class="action-grid">
        <RouterLink
          to="/appointments/new"
          class="action-card"
        >
          <span class="icon">✦</span>
          <span>
            <strong>Novo agendamento</strong>
            <small>Escolha serviços, data e horário.</small>
          </span>
          <b>→</b>
        </RouterLink>

        <RouterLink
          to="/appointments"
          class="action-card"
        >
          <span class="icon">◷</span>
          <span>
            <strong>Meus agendamentos</strong>
            <small>Consulte, filtre ou reagende um horário.</small>
          </span>
          <b>→</b>
        </RouterLink>
      </div>
    </section>

    <section class="notice">
      <span class="notice-icon">i</span>
      <p>
        Precisa alterar um agendamento? Você pode reagendar pelo sistema até dois dias antes do horário marcado.
      </p>
    </section>
  </AppLayout>
</template>

<style scoped src="./DashboardView.css"></style>
