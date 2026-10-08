<template>
  <div>
    <h2>Registro</h2>
    <form @submit.prevent="onSubmit">
      <input v-model="username" placeholder="usuario" required />
      <input v-model="email" type="email" placeholder="email" required />
      <input v-model="password" type="password" placeholder="contraseña (mín. 8)" required />
      <input v-model="password2" type="password" placeholder="confirmar pacontraseña" required />
      <button type="submit">Crear cuenta</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
    <p>¿Ya tienes cuenta? <router-link to="/login">Entra aquí</router-link></p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api.js'

const username = ref('')
const email = ref('')
const password = ref('')
const password2 = ref('')
const error = ref('')
const router = useRouter()

async function onSubmit() {
  error.value = ''
  if (password.value !== password2.value) {
    error.value = 'Las contraseñas no coinciden.'
    return
  }
  try {
    await api.register({ username: username.value, email: email.value, password: password.value, password2: password2.value })
    router.push('/login')
  } catch (e) {
    error.value = e.message
  }
}
</script>
