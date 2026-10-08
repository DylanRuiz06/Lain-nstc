<template>
  <div>
    <h2>Usuarios</h2>
    <p><router-link to="/users/create">+ Crear usuario</router-link></p>
    <p v-if="error" class="error">{{ error }}</p>
    <table v-if="users.length">
      <thead>
        <tr><th>Usuario</th><th>Email</th><th>Acciones</th></tr>
      </thead>
      <tbody>
        <tr v-for="u in users" :key="u.id">
          <td>{{ u.username }}</td>
          <td>{{ u.email }}</td>
          <td class="actions">
            <router-link :to="`/users/${u.id}/edit`">Editar</router-link>
            <a href="#" class="danger" @click.prevent="remove(u)">Eliminar</a>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>Cargando o sin usuarios…</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api.js'

const users = ref([])
const error = ref('')
const router = useRouter()

async function load() {
  error.value = ''
  try {
    users.value = await api.listUsers()
  } catch (e) {
    if (e.message.includes('403')) router.push('/login')
    else error.value = e.message
  }
}

async function remove(u) {
  if (!confirm(`¿Eliminar a ${u.username}?`)) return
  try {
    await api.deleteUser(u.id)
    await load()
  } catch (e) {
    error.value = e.message
  }
}

onMounted(load)
</script>

<style scoped>
.danger { color: #b00020; cursor: pointer; }
</style>
