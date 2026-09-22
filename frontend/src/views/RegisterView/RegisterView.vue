<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getApiErrorMessage } from '@/utils/apiError'
import {
  validateName,
  validateEmail,
  validatePhone,
  validatePassword,
} from '@/utils/validators'
import { formatPhone, onlyDigits } from '@/utils/phone'
import AuthLayout from '@/components/AuthLayout/AuthLayout.vue'
import FormField from '@/components/FormField/FormField.vue'

const router = useRouter()
const auth = useAuthStore()

const form = reactive({ name: '', email: '', phone: '', password: '' })
const errors = reactive({ name: '', email: '', phone: '', password: '' })
const formError = ref('')

function validate() {
  errors.name = validateName(form.name)
  errors.email = validateEmail(form.email)
  errors.phone = validatePhone(form.phone)
  errors.password = validatePassword(form.password)
  return !errors.name && !errors.email && !errors.phone && !errors.password
}

async function onSubmit() {
  formError.value = ''
  if (!validate()) return

  try {
    await auth.register({
      name: form.name.trim(),
      email: form.email.trim(),
      phone: onlyDigits(form.phone),
      password: form.password,
    })
    router.push('/dashboard')
  } catch (err) {
    formError.value = getApiErrorMessage(err, 'Não foi possível concluir o cadastro.')
  }
}
</script>

<template>
  <AuthLayout
    subtitle="Cadastre-se para agendar seus serviços"
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
        id="name"
        v-model="form.name"
        label="Nome completo"
        autocomplete="name"
        placeholder="Maria da Silva"
        :error="errors.name"
        required
      />

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
        id="phone"
        v-model="form.phone"
        label="Telefone"
        type="tel"
        autocomplete="tel"
        placeholder="(11) 99999-9999"
        inputmode="numeric"
        maxlength="15"
        :formatter="formatPhone"
        :error="errors.phone"
        required
      />

      <FormField
        id="password"
        v-model="form.password"
        label="Senha"
        type="password"
        autocomplete="new-password"
        placeholder="Mínimo 8 caracteres"
        :error="errors.password"
        required
      />

      <button
        type="submit"
        class="submit-btn"
        :disabled="auth.loading"
      >
        {{ auth.loading ? 'Cadastrando...' : 'Cadastrar' }}
      </button>
    </form>

    <p class="switch">
      Já tem conta?
      <RouterLink to="/login">
        Entrar
      </RouterLink>
    </p>
  </AuthLayout>
</template>

<style scoped src="./RegisterView.css"></style>
