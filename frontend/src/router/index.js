import { createRouter, createWebHistory } from 'vue-router'
import { api } from '../api.js'
import LoginView from '../views/LoginView.vue'
import RegionsView from '../views/RegionsView.vue'
import RegionFormView from '../views/RegionFormView.vue'
import BiotopesView from '../views/BiotopesView.vue'
import BiotopeFormView from '../views/BiotopeFormView.vue'
import SpeciesView from '../views/SpeciesView.vue'
import SpeciesFormView from '../views/SpeciesFormView.vue'

const routes = [
  { path: '/', redirect: '/species' },
  { path: '/login', component: LoginView },
  { path: '/regions', component: RegionsView, meta: { requiresAuth: true } },
  { path: '/regions/new', component: RegionFormView, meta: { requiresAuth: true } },
  { path: '/regions/:id/edit', component: RegionFormView, props: true, meta: { requiresAuth: true } },
  { path: '/biotopes', component: BiotopesView, meta: { requiresAuth: true } },
  { path: '/biotopes/new', component: BiotopeFormView, meta: { requiresAuth: true } },
  { path: '/biotopes/:id/edit', component: BiotopeFormView, props: true, meta: { requiresAuth: true } },
  { path: '/species', component: SpeciesView, meta: { requiresAuth: true } },
  { path: '/species/new', component: SpeciesFormView, meta: { requiresAuth: true } },
  { path: '/species/:id/edit', component: SpeciesFormView, props: true, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// El guard solo mejora la experiencia. La seguridad real está en Django:
// cada endpoint de administración responde 401 sin sesión y 403 si no es staff.
let authPromise = null

export function resetAuthCache() {
  authPromise = null
}

function checkAuth() {
  if (!authPromise) {
    authPromise = api.me().then(() => true).catch(() => false)
  }
  return authPromise
}

router.beforeEach(async (to) => {
  if (to.meta.requiresAuth && !(await checkAuth())) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }
  if (to.path === '/login' && (await checkAuth())) {
    return '/species'
  }
  return true
})

export default router
