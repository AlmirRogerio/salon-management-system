<script setup>
import { RouterLink } from 'vue-router'
import brandLogoDark from '@/assets/logo/cabeleleila-mark-dark.svg'
import AdminLayout from '@/components/AdminLayout/AdminLayout.vue'
</script>

<template>
  <AdminLayout>
    <section class="hero">
      <div>
        <p class="eyebrow">
          Visão geral
        </p>
        <h1>Gestão do salão, em um só lugar.</h1>
        <p class="intro">
          Organize sua operação, mantenha os serviços atualizados e defina quando o salão atende.
        </p>
      </div>
      <img
        class="hero-logo"
        :src="brandLogoDark"
        alt="Cabeleleila Leila — Salão de Beleza"
      >
    </section>

    <section class="quick-actions">
      <article class="action-card main-action">
        <span class="action-icon">◔</span>
        <div>
          <p class="action-label">
            Operação
          </p>
          <h2>Agendamentos</h2>
          <p>Confirme, reagende e gerencie o status de cada serviço.</p>
        </div>
        <RouterLink to="/admin/appointments">
          Gerenciar agendamentos
        </RouterLink>
      </article>

      <article class="action-card">
        <span class="action-icon">✦</span>
        <div>
          <p class="action-label">
            Catálogo
          </p>
          <h2>Serviços do salão</h2>
          <p>Cadastre, edite valores, duração e disponibilidade.</p>
        </div>
        <RouterLink to="/admin/services">
          Gerenciar serviços
        </RouterLink>
      </article>

      <article class="action-card">
        <span class="action-icon">◷</span>
        <div>
          <p class="action-label">
            Operação
          </p>
          <h2>Expediente</h2>
          <p>Configure os dias, horários e intervalos de atendimento.</p>
        </div>
        <RouterLink to="/admin/business-hours">
          Ajustar expediente
        </RouterLink>
      </article>
    </section>

    <section class="next-step">
      <p class="eyebrow">
        Em breve
      </p>
      <h2>Painel de desempenho</h2>
      <p>
        Uma próxima evolução trará o acompanhamento do desempenho semanal do salão — total de agendamentos,
        confirmações, conclusões e receita — em um painel dedicado.
      </p>
    </section>
  </AdminLayout>
</template>

<style scoped src="./AdminDashboardView.css"></style>
