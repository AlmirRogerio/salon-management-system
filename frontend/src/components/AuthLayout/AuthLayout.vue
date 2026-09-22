<script setup>
import brandLogo from '@/assets/logo/cabeleleila-leila-logo-vetorizada.svg'

defineProps({
  title: { type: String, default: '' },
  subtitle: { type: String, default: '' },
})
</script>

<template>
  <div class="auth-page">
    <div class="auth-card">
      <header class="auth-header">
        <img
          class="auth-logo"
          :src="brandLogo"
          alt="Cabeleleila Leila — Salão de Beleza"
        >
        <h2
          v-if="title"
        >
          {{ title }}
        </h2>
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
