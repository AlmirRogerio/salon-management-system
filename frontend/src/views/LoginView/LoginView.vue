<script setup>
import { reactive, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getApiErrorMessage } from '@/utils/apiError'
import { validateEmail, validateRequired } from '@/utils/validators'
import AuthLayout from '@/components/AuthLayout/AuthLayout.vue'
import FormField from '@/components/FormField/FormField.vue'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const form = reactive({ email: '', password: '' })
const errors = reactive({ email: '', password: '' })
const formError = ref('')

function validate() {
  errors.email = validateEmail(form.email)
  errors.password = validateRequired(form.password, 'Informe sua senha.')
  return !errors.email && !errors.password
}

async function onSubmit() {
  formError.value = ''
  if (!validate()) return

  try {
    await auth.login({ email: form.email.trim(), password: form.password })
    const redirect = route.query.redirect || (auth.isAdmin ? '/admin' : '/dashboard')
    router.push(redirect)
  } catch (err) {
    formError.value = getApiErrorMessage(err, 'Não foi possível entrar. Tente novamente.')
  }
}
</script>

<template>
  <AuthLayout
    title="Entrar"
    subtitle="Acesse sua conta para agendar serviços"
  >
    <form
      novalidate
      @submit.prevent="onSubmit"
    >
      <p
        v-if="formError"
        class="form-error"
        role="alert"
      >
        {{ formError }}
      </p>

      <FormField
        id="email"
        v-model="form.email"
        label="E-mail"
        type="email"
        autocomplete="email"
        placeholder="voce@exemplo.com"
        :error="errors.email"
        required
      />

      <FormField
        id="password"
        v-model="form.password"
        label="Senha"
        type="password"
        autocomplete="current-password"
        placeholder="••••••••"
        :error="errors.password"
        required
      />

      <button
        type="submit"
        class="submit-btn"
        :disabled="auth.loading"
      >
        {{ auth.loading ? 'Entrando...' : 'Entrar' }}
      </button>
    </form>

    <p class="switch">
      Não tem conta?
      <RouterLink to="/register">
        Cadastre-se
      </RouterLink>
    </p>
  </AuthLayout>
</template>

<style scoped src="./LoginView.css"></style>
