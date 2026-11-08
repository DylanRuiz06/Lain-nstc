<template>
  <div class="app">
    <header v-if="showNav" class="topbar">
      <strong>Lain · Panel de catálogo</strong>
      <nav>
        <router-link to="/regions">Regiones</router-link>
        <router-link to="/biotopes">Biotopos</router-link>
        <router-link to="/species">Especies</router-link>
      </nav>
      <button class="btn-secondary" @click="onLogout">Cerrar sesión</button>
    </header>

    <main class="container">
      <router-view :key="$route.fullPath" />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from './api.js'
import { resetAuthCache } from './router/index.js'

const route = useRoute()
const router = useRouter()
const showNav = computed(() => Boolean(route.meta.requiresAuth))

async function onLogout() {
  try {
    await api.logout()
  } catch {
    // Si la sesión ya expiró, igual volvemos al login.
  }
  resetAuthCache()
  router.push('/login')
}
</script>

<style>
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  background: #f4f6f8;
  color: #1f2933;
}
.app { min-height: 100vh; }
.topbar {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 0.9rem 1.5rem;
  background: #123b4a;
  color: #fff;
}
.topbar strong { margin-right: auto; }
.topbar nav { display: flex; gap: 1rem; }
.topbar a { color: #cfe8ef; text-decoration: none; }
.topbar a.router-link-active { color: #fff; font-weight: 600; text-decoration: underline; }
.container { max-width: 1000px; margin: 1.5rem auto; padding: 0 1rem; }
.card {
  background: #fff;
  border: 1px solid #d9e2ec;
  border-radius: 8px;
  padding: 1.25rem;
}
.page-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}
.page-header h1 { margin: 0; font-size: 1.4rem; }
.page-header .spacer { margin-left: auto; }
form { display: flex; flex-direction: column; gap: 0.9rem; }
.field { display: flex; flex-direction: column; gap: 0.25rem; }
.field label { font-weight: 600; font-size: 0.9rem; }
.field input, .field select {
  padding: 0.45rem 0.55rem;
  border: 1px solid #bcccdc;
  border-radius: 4px;
  font-size: 1rem;
  background: #fff;
}
fieldset {
  border: 1px solid #d9e2ec;
  border-radius: 6px;
  padding: 0.9rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.75rem;
}
legend { padding: 0 0.35rem; font-weight: 600; }
.checks { display: flex; flex-wrap: wrap; gap: 1rem; align-items: center; }
.checks label { font-weight: 400; display: flex; align-items: center; gap: 0.35rem; }
.checks input { width: auto; }
.form-actions { display: flex; gap: 0.5rem; }
button {
  padding: 0.45rem 0.9rem;
  border: 1px solid #123b4a;
  border-radius: 4px;
  background: #123b4a;
  color: #fff;
  font-size: 0.95rem;
  cursor: pointer;
}
button:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-secondary { background: #fff; color: #123b4a; }
.btn-danger { background: #a61b1b; border-color: #a61b1b; }
.error { color: #b00020; font-size: 0.85rem; }
.table { width: 100%; border-collapse: collapse; background: #fff; }
.table th, .table td { border: 1px solid #d9e2ec; padding: 0.5rem 0.6rem; text-align: left; }
.table th { background: #eef3f7; }
.actions { display: flex; gap: 0.4rem; }
.muted { color: #627d98; }
</style>
