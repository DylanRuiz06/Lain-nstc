<template>
  <div class="container">
    <header v-if="showHeader" class="topbar">
    <button @click="onLogout">Cerrar sesión</button>
    </header>

    <router-view :key="$route.fullPath" @auth-change="refresh" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { api } from './api.js'

const user = ref(null)
const router = useRouter()
const route = useRoute()

const showHeader = computed(() => route.path.startsWith('/users'))

async function refresh() {
  try {
    user.value = await api.me()
  } catch {
    user.value = null
  }
}

async function onLogout() {
  try {
    await api.logout()
  } finally {
    user.value = null
    router.push('/login')
  }
}

onMounted(refresh)
watch(() => route.path, refresh)
</script>

<style>
body { font-family: sans-serif; margin: 0; background: #f4f4f4; }
.container { max-width: 700px; margin: 2rem auto; background: #fff; padding: 1.5rem; border-radius: 8px; }
nav { display: flex; gap: 1rem; align-items: right; margin-bottom: 1.5rem; }
.topbar { display: flex; gap: 1rem; align-items: right; margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid #ddd; }
.topbar strong { margin-right: auto; }
form { display: flex; flex-direction: column; gap: 0.6rem; }
input { padding: 0.5rem; font-size: 1rem; }
button { padding: 0.5rem 1rem; cursor: pointer; margin: 0 0 0 auto}
.error { color: #b00020; }
table { width: 100%; border-collapse: collapse; }
td, th { border: 1px solid #ddd; padding: 0.5rem; text-align: left; }
.actions { display: flex; gap: 0.5rem; }
</style>
