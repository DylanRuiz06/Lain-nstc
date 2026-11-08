<template>
  <div class="card login-card">
    <h1>Lain · Panel</h1>
    <p class="muted">Acceso solo para administradores.</p>

    <form @submit.prevent="submit">
      <div class="field">
        <label for="username">Usuario</label>
        <input id="username" v-model="username" type="text" required autocomplete="username" />
      </div>
      <div class="field">
        <label for="password">Contraseña</label>
        <input id="password" v-model="password" type="password" required autocomplete="current-password" />
      </div>

      <p v-if="error" class="error">{{ error }}</p>

      <button type="submit" :disabled="loading">{{ loading ? 'Entrando…' : 'Entrar' }}</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '../api.js'
import { resetAuthCache } from '../router/index.js'

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const router = useRouter()
const route = useRoute()

async function submit() {
  error.value = ''
  loading.value = true
  try {
    await api.login({ username: username.value, password: password.value })
    resetAuthCache()
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/regions'
    router.push(redirect)
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-card { max-width: 380px; margin: 3rem auto; }
h1 { margin-top: 0; }
</style>
