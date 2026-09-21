import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'
import { setUnauthorizedHandler } from './services/api'
import './assets/main.css'

const GUEST_ROUTES = ['login', 'register']

async function bootstrap() {
  const app = createApp(App)
  const pinia = createPinia()

  app.use(pinia)
  app.use(router)

  const auth = useAuthStore()

  setUnauthorizedHandler(() => {
    auth.logout()
    if (!GUEST_ROUTES.includes(router.currentRoute.value.name)) {
      router.push({ name: 'login' })
    }
  })

  if (auth.isAuthenticated) {
    await auth.fetchCurrentUser()
  }

  app.mount('#app')
}

bootstrap()
