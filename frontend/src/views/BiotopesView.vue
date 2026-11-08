<template>
  <section>
    <div class="page-header">
      <h1>Biotopos</h1>
      <div class="spacer"></div>
      <router-link to="/biotopes/new"><button>Nuevo biotopo</button></router-link>
    </div>

    <p v-if="error" class="error">{{ error }}</p>

    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Región</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="biotope in biotopes" :key="biotope.id">
          <td>{{ biotope.id }}</td>
          <td>{{ biotope.name }}</td>
          <td>{{ biotope.region_name }}</td>
          <td class="actions">
            <router-link :to="`/biotopes/${biotope.id}/edit`"><button>Editar</button></router-link>
            <button class="btn-danger" @click="remove(biotope)">Eliminar</button>
          </td>
        </tr>
        <tr v-if="!loading && biotopes.length === 0">
          <td colspan="4" class="muted">No hay biotopos.</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { api } from '../api.js'

const biotopes = ref([])
const error = ref('')
const loading = ref(false)

async function load() {
  loading.value = true
  error.value = ''
  try {
    biotopes.value = await api.listBiotopes()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

async function remove(biotope) {
  if (!window.confirm(`¿Eliminar el biotopo "${biotope.name}"?`)) return
  error.value = ''
  try {
    await api.deleteBiotope(biotope.id)
    await load()
  } catch (err) {
    error.value = err.message
  }
}

onMounted(load)
</script>
