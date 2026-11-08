<template>
  <section>
    <div class="page-header">
      <h1>Regiones</h1>
      <div class="spacer"></div>
      <router-link to="/regions/new"><button>Nueva región</button></router-link>
    </div>

    <p v-if="error" class="error">{{ error }}</p>

    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="region in regions" :key="region.id">
          <td>{{ region.id }}</td>
          <td>{{ region.name }}</td>
          <td class="actions">
            <router-link :to="`/regions/${region.id}/edit`"><button>Editar</button></router-link>
            <button class="btn-danger" @click="remove(region)">Eliminar</button>
          </td>
        </tr>
        <tr v-if="!loading && regions.length === 0">
          <td colspan="3" class="muted">No hay regiones.</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { api } from '../api.js'

const regions = ref([])
const error = ref('')
const loading = ref(false)

async function load() {
  loading.value = true
  error.value = ''
  try {
    regions.value = await api.listRegions()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

async function remove(region) {
  if (!window.confirm(`¿Eliminar la región "${region.name}"?`)) return
  error.value = ''
  try {
    await api.deleteRegion(region.id)
    await load()
  } catch (err) {
    error.value = err.message
  }
}

onMounted(load)
</script>
