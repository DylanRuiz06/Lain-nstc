<template>
  <div>
    <h2>{{ isEdit ? 'Editar usuario' : 'Crear usuario' }}</h2>
    <form @submit.prevent="onSubmit">
      <input v-model="username" placeholder="usuario" required />
      <input v-model="email" type="email" placeholder="email" />
      <input v-model="password" type="password"
        :placeholder="isEdit ? 'nueva contraseña (opcional)' : 'contraseña (mín. 8)'"
        :required="!isEdit" />
      <button type="submit">Guardar</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
    <p><router-link to="/users">Volver al listado</router-link></p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api.js'

const props = defineProps({ id: { type: String, default: null } })
const isEdit = computed(() => !!props.id)

const username = ref('')
const email = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

onMounted(async () => {
  if (!isEdit.value) return
  try {
    const u = await api.getUser(props.id)
    username.value = u.username
    email.value = u.email
  } catch (e) {
    error.value = e.message
  }
})

async function onSubmit() {
  error.value = ''
  try {
    if (isEdit.value) {
      await api.updateUser(props.id, { username: username.value, email: email.value, password: password.value })
    } else {
      await api.createUser({ username: username.value, email: email.value, password: password.value })
    }
    router.push('/users')
  } catch (e) {
    error.value = e.message
  }
}
</script>
