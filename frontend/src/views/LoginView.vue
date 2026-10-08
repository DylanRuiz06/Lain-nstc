<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="onSubmit">
      <input v-model="username" placeholder="usuario" required />
      <input v-model="password" type="password" placeholder="contraseña" required />
      <button type="submit">Entrar</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
    <p>¿No tienes cuenta? <router-link to="/register">Regístrate</router-link></p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api.js'

const emit = defineEmits(['auth-change'])
const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

async function onSubmit() {
  error.value = ''
  try {
    await api.login({ username: username.value, password: password.value })
    emit('auth-change')
    router.push('/users')
  } catch (e) {
    error.value = e.message
  }
}
</script>
