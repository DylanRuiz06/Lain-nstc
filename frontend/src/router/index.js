import { createRouter, createWebHistory } from 'vue-router'
import { api } from '../api.js'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import UserListView from '../views/UserListView.vue'
import UserFormView from '../views/UserFormView.vue'

const routes = [
  { path: '/', redirect: '/users' },
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView },
  { path: '/users', component: UserListView, meta: { requiresAuth: true } },
  { path: '/users/create', component: UserFormView, meta: { requiresAuth: true } },
  { path: '/users/:id/edit', component: UserFormView, props: true, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Guardia global: si la ruta exige auth, comprobamos la sesión en Django.
// Si no hay sesión (403), redirigimos a /login.
router.beforeEach(async (to) => {
  if (!to.meta.requiresAuth) return true
  try {
    await api.me()
    return true
  } catch {
    return '/login'
  }
})

export default router
