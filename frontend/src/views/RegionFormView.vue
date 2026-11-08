<template>
  <section class="card">
    <div class="page-header">
      <h1>{{ isEdit ? 'Editar región' : 'Nueva región' }}</h1>
    </div>

    <p v-if="generalError" class="error">{{ generalError }}</p>

    <form @submit.prevent="submit">
      <div class="field">
        <label for="name">Nombre</label>
        <input id="name" v-model="form.name" type="text" required />
        <span v-if="errors.name" class="error">{{ errors.name.join(' ') }}</span>
      </div>

      <div class="form-actions">
        <button type="submit" :disabled="saving">{{ saving ? 'Guardando…' : 'Guardar' }}</button>
        <router-link to="/regions"><button type="button" class="btn-secondary">Cancelar</button></router-link>
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
const form = reactive({ name: '' })
const errors = ref({})
const generalError = ref('')
const saving = ref(false)

onMounted(async () => {
  if (!isEdit.value) return
  try {
    const region = await api.getRegion(props.id)
    form.name = region.name
  } catch (err) {
    generalError.value = err.message
  }
})

async function submit() {
  errors.value = {}
  generalError.value = ''
  saving.value = true
  try {
    if (isEdit.value) {
      await api.updateRegion(props.id, { name: form.name })
    } else {
      await api.createRegion({ name: form.name })
    }
    router.push('/regions')
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
