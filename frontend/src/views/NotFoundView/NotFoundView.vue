<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="notfound">
    <h1>404</h1>
    <p>Página não encontrada.</p>
    <RouterLink to="/">
      Voltar ao início
    </RouterLink>
  </div>
</template>

<style scoped src="./NotFoundView.css"></style>
