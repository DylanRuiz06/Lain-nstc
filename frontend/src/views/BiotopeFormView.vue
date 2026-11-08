<template>
  <section class="card">
    <div class="page-header">
      <h1>{{ isEdit ? 'Editar biotopo' : 'Nuevo biotopo' }}</h1>
    </div>

    <p v-if="generalError" class="error">{{ generalError }}</p>

    <form @submit.prevent="submit">
      <div class="field">
        <label for="name">Nombre</label>
        <input id="name" v-model="form.name" type="text" required />
        <span v-if="errors.name" class="error">{{ errors.name.join(' ') }}</span>
      </div>

      <div class="field">
        <label for="region">Región</label>
        <select id="region" v-model.number="form.region_id" required>
          <option value="" disabled>Selecciona una región</option>
          <option v-for="region in regions" :key="region.id" :value="region.id">
            {{ region.name }}
          </option>
        </select>
        <span v-if="errors.region" class="error">{{ errors.region.join(' ') }}</span>
      </div>

      <div class="form-actions">
        <button type="submit" :disabled="saving">{{ saving ? 'Guardando…' : 'Guardar' }}</button>
        <router-link to="/biotopes"><button type="button" class="btn-secondary">Cancelar</button></router-link>
      </div>
    </form>
  </section>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api.js'

const props = defineProps({
  id: { type: String, default: null },
})

const router = useRouter()
const isEdit = computed(() => props.id !== null)
const form = reactive({ name: '', region_id: '' })
const regions = ref([])
const errors = ref({})
const generalError = ref('')
const saving = ref(false)

onMounted(async () => {
  try {
    const [regionList, biotope] = await Promise.all([
      api.listRegions(),
      isEdit.value ? api.getBiotope(props.id) : Promise.resolve(null),
    ])
    regions.value = regionList
    if (biotope) {
      form.name = biotope.name
      form.region_id = biotope.region_id
    }
  } catch (err) {
    generalError.value = err.message
  }
})

async function submit() {
  errors.value = {}
  generalError.value = ''
  saving.value = true
  const payload = { name: form.name, region_id: form.region_id }
  try {
    if (isEdit.value) {
      await api.updateBiotope(props.id, payload)
    } else {
      await api.createBiotope(payload)
    }
    router.push('/biotopes')
  } catch (err) {
    if (err.data && err.data.errors) {
      errors.value = err.data.errors
    } else {
      generalError.value = err.message
    }
  } finally {
    saving.value = false
  }
}
</script>
