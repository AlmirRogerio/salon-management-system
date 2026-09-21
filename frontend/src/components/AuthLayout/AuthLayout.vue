<script setup>
import brandMark from '@/assets/logo/cabeleleila-mark-light.svg'

defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
})
</script>

<template>
  <div class="auth-page">
    <div class="auth-card">
      <header class="auth-header">
        <img
          class="auth-mark"
          :src="brandMark"
          alt="Cabeleleila Leila — Salão de Beleza"
        >
        <p class="brand-name">
          <span>Cabeleleila</span>
          <strong>Leila</strong>
        </p>
        <h2>{{ title }}</h2>
        <p
          v-if="subtitle"
          class="subtitle"
        >
          {{ subtitle }}
        </p>
      </header>
      <slot />
    </div>
  </div>
</template>

<style scoped src="./AuthLayout.css"></style>
