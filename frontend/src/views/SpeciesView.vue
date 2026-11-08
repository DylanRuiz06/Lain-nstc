<template>
  <section>
    <div class="page-header">
      <h1>Especies</h1>
      <div class="spacer"></div>
      <router-link to="/species/new"><button>Nueva especie</button></router-link>
    </div>

    <p v-if="error" class="error">{{ error }}</p>

    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre común</th>
          <th>Nombre científico</th>
          <th>Tipo</th>
          <th>Biotopo</th>
          <th>Región</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="species in speciesList" :key="species.id">
          <td>{{ species.id }}</td>
          <td>{{ species.common_name }}</td>
          <td><em>{{ species.scientific_name }}</em></td>
          <td>{{ kindLabel(species.kind) }}</td>
          <td>{{ species.biotope_name }}</td>
          <td>{{ species.region_name }}</td>
          <td class="actions">
            <router-link :to="`/species/${species.id}/edit`"><button>Editar</button></router-link>
            <button class="btn-danger" @click="remove(species)">Eliminar</button>
          </td>
        </tr>
        <tr v-if="!loading && speciesList.length === 0">
          <td colspan="7" class="muted">No hay especies.</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { api } from '../api.js'

const speciesList = ref([])
const error = ref('')
const loading = ref(false)

const KIND_LABELS = {
  fish: 'Pez',
  invertebrate: 'Invertebrado',
  plant: 'Planta',
  amphibian: 'Anfibio',
}

function kindLabel(kind) {
  return KIND_LABELS[kind] || kind
}

async function load() {
  loading.value = true
  error.value = ''
  try {
    speciesList.value = await api.listSpecies()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

async function remove(species) {
  if (!window.confirm(`¿Eliminar la especie "${species.common_name}"?`)) return
  error.value = ''
  try {
    await api.deleteSpecies(species.id)
    await load()
  } catch (err) {
    error.value = err.message
  }
}

onMounted(load)
</script>
