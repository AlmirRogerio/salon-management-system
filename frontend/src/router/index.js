import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    redirect: '/dashboard',
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView/LoginView.vue'),
    meta: { guestOnly: true },
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/RegisterView/RegisterView.vue'),
    meta: { guestOnly: true },
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import('@/views/DashboardView/DashboardView.vue'),
    meta: { requiresAuth: true, customerOnly: true },
  },
  {
    path: '/appointments/new',
    name: 'new-appointment',
    component: () => import('@/views/NewAppointmentView/NewAppointmentView.vue'),
    meta: { requiresAuth: true, customerOnly: true },
  },
  {
    path: '/appointments',
    name: 'appointments',
    component: () => import('@/views/AppointmentsView/AppointmentsView.vue'),
    meta: { requiresAuth: true, customerOnly: true },
  },
  {
    path: '/admin',
    name: 'admin-dashboard',
    component: () => import('@/views/AdminDashboardView/AdminDashboardView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/appointments',
    name: 'admin-appointments',
    component: () => import('@/views/AdminAppointmentsView/AdminAppointmentsView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/business-hours',
    name: 'admin-business-hours',
    component: () => import('@/views/AdminBusinessHoursView/AdminBusinessHoursView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/services',
    name: 'admin-services',
    component: () => import('@/views/AdminServicesView/AdminServicesView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/customers',
    name: 'admin-customers',
    component: () => import('@/views/AdminCustomersView/AdminCustomersView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFoundView/NotFoundView.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (auth.isAuthenticated) {
    await auth.ensureHydrated()
  }

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.meta.requiresAdmin && !auth.isAdmin) {
    return { name: 'dashboard' }
  }

  if (to.meta.customerOnly && auth.isAdmin) {
    return { name: 'admin-dashboard' }
  }

  if (to.meta.guestOnly && auth.isAuthenticated) {
    return { name: auth.isAdmin ? 'admin-dashboard' : 'dashboard' }
  }

  return true
})

export default router
