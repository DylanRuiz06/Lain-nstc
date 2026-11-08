<template>
  <section class="card">
    <div class="page-header">
      <h1>{{ isEdit ? 'Editar especie' : 'Nueva especie' }}</h1>
    </div>

    <p v-if="generalError" class="error">{{ generalError }}</p>
    <p v-if="errors.__all__" class="error">{{ errors.__all__.join(' ') }}</p>

    <form @submit.prevent="submit">
      <fieldset>
        <legend>Datos generales</legend>

        <div class="field">
          <label for="common_name">Nombre común</label>
          <input id="common_name" v-model="form.common_name" type="text" required />
          <span v-if="errors.common_name" class="error">{{ errors.common_name.join(' ') }}</span>
        </div>

        <div class="field">
          <label for="scientific_name">Nombre científico</label>
          <input id="scientific_name" v-model="form.scientific_name" type="text" required />
          <span v-if="errors.scientific_name" class="error">{{ errors.scientific_name.join(' ') }}</span>
        </div>

        <div class="field">
          <label for="kind">Tipo</label>
          <select id="kind" v-model="form.kind" required>
            <option v-for="option in kindOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>
          <span v-if="errors.kind" class="error">{{ errors.kind.join(' ') }}</span>
        </div>
      </fieldset>

      <fieldset>
        <legend>Biotopo</legend>

        <div class="field">
          <label for="region">Región</label>
          <select id="region" v-model.number="form.region_id" required>
            <option value="" disabled>Selecciona una región</option>
            <option v-for="region in regions" :key="region.id" :value="region.id">
              {{ region.name }}
            </option>
          </select>
        </div>

        <div class="field">
          <label for="biotope">Biotopo</label>
          <select id="biotope" v-model.number="form.biotope_id" :disabled="!form.region_id" required>
            <option value="" disabled>Selecciona un biotopo</option>
            <option v-for="biotope in biotopes" :key="biotope.id" :value="biotope.id">
              {{ biotope.name }}
            </option>
          </select>
          <span v-if="errors.biotope" class="error">{{ errors.biotope.join(' ') }}</span>
        </div>
      </fieldset>

      <fieldset>
        <legend>Parámetros biológicos</legend>

        <div class="field">
          <label for="temp_min">Temperatura mínima (°C)</label>
          <input id="temp_min" v-model.number="form.temp_min" type="number" step="any" required />
          <span v-if="errors.temp_min" class="error">{{ errors.temp_min.join(' ') }}</span>
        </div>

        <div class="field">
          <label for="temp_max">Temperatura máxima (°C)</label>
          <input id="temp_max" v-model.number="form.temp_max" type="number" step="any" required />
          <span v-if="errors.temp_max" class="error">{{ errors.temp_max.join(' ') }}</span>
        </div>

        <div class="field">
          <label for="ph_min">pH mínimo</label>
          <input id="ph_min" v-model.number="form.ph_min" type="number" step="any" required />
          <span v-if="errors.ph_min" class="error">{{ errors.ph_min.join(' ') }}</span>
        </div>

        <div class="field">
          <label for="ph_max">pH máximo</label>
          <input id="ph_max" v-model.number="form.ph_max" type="number" step="any" required />
          <span v-if="errors.ph_max" class="error">{{ errors.ph_max.join(' ') }}</span>
        </div>

        <div class="field">
          <label for="gh_min">GH mínimo</label>
          <input id="gh_min" v-model.number="form.gh_min" type="number" step="any" required />
          <span v-if="errors.gh_min" class="error">{{ errors.gh_min.join(' ') }}</span>
        </div>

        <div class="field">
          <label for="gh_max">GH máximo</label>
          <input id="gh_max" v-model.number="form.gh_max" type="number" step="any" required />
          <span v-if="errors.gh_max" class="error">{{ errors.gh_max.join(' ') }}</span>
        </div>

        <div class="field">
          <label for="adult_size_cm">Tamaño adulto (cm)</label>
          <input id="adult_size_cm" v-model.number="form.adult_size_cm" type="number" step="any" required />
          <span v-if="errors.adult_size_cm" class="error">{{ errors.adult_size_cm.join(' ') }}</span>
        </div>

        <div class="field">
          <label for="min_tank_liters">Litros mínimos</label>
          <input id="min_tank_liters" v-model.number="form.min_tank_liters" type="number" step="1" required />
          <span v-if="errors.min_tank_liters" class="error">{{ errors.min_tank_liters.join(' ') }}</span>
        </div>

        <div class="field">
          <label for="min_group_size">Grupo mínimo</label>
          <input id="min_group_size" v-model.number="form.min_group_size" type="number" step="1" required />
          <span v-if="errors.min_group_size" class="error">{{ errors.min_group_size.join(' ') }}</span>
        </div>
      </fieldset>

      <fieldset>
        <legend>Comportamiento</legend>

        <div class="field">
          <label for="diet">Dieta</label>
          <select id="diet" v-model="form.diet" required>
            <option v-for="option in dietOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>
          <span v-if="errors.diet" class="error">{{ errors.diet.join(' ') }}</span>
        </div>

        <div class="field">
          <label for="temperament">Temperamento</label>
          <select id="temperament" v-model="form.temperament" required>
            <option v-for="option in temperamentOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>
          <span v-if="errors.temperament" class="error">{{ errors.temperament.join(' ') }}</span>
        </div>

        <div class="field">
          <label for="swim_zone">Zona de natación</label>
          <select id="swim_zone" v-model="form.swim_zone" required>
            <option v-for="option in swimZoneOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>
          <span v-if="errors.swim_zone" class="error">{{ errors.swim_zone.join(' ') }}</span>
        </div>

        <div class="checks">
          <label><input v-model="form.eats_plants" type="checkbox" /> Come plantas</label>
          <label><input v-model="form.fin_nipper" type="checkbox" /> Mordisquea aletas</label>
          <label><input v-model="form.territorial" type="checkbox" /> Territorial</label>
        </div>
      </fieldset>

      <div class="form-actions">
        <button type="submit" :disabled="saving">{{ saving ? 'Guardando…' : 'Guardar' }}</button>
        <router-link to="/species"><button type="button" class="btn-secondary">Cancelar</button></router-link>
      </div>
    </form>
  </section>
</template>

<script setup>
import { computed, nextTick, onMounted, reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api.js'

const props = defineProps({
  id: { type: String, default: null },
})

const router = useRouter()
const isEdit = computed(() => props.id !== null)

const kindOptions = [
  { value: 'fish', label: 'Pez' },
  { value: 'invertebrate', label: 'Invertebrado' },
  { value: 'plant', label: 'Planta' },
  { value: 'amphibian', label: 'Anfibio' },
]
const dietOptions = [
  { value: 'herbivore', label: 'Herbívoro' },
  { value: 'carnivore', label: 'Carnívoro' },
  { value: 'omnivore', label: 'Omnívoro' },
]
const temperamentOptions = [
  { value: 'peaceful', label: 'Pacífico' },
  { value: 'semi_aggressive', label: 'Semiagresivo' },
  { value: 'aggressive', label: 'Agresivo' },
]
const swimZoneOptions = [
  { value: 'top', label: 'Superior' },
  { value: 'middle', label: 'Media' },
  { value: 'bottom', label: 'Inferior' },
]

const form = reactive({
  common_name: '',
  scientific_name: '',
  kind: 'fish',
  temp_min: '',
  temp_max: '',
  ph_min: '',
  ph_max: '',
  gh_min: '',
  gh_max: '',
  adult_size_cm: '',
  min_tank_liters: '',
  min_group_size: '',
  diet: 'omnivore',
  temperament: 'peaceful',
  swim_zone: 'middle',
  eats_plants: false,
  fin_nipper: false,
  territorial: false,
  region_id: '',
  biotope_id: '',
})

const regions = ref([])
const biotopes = ref([])
const errors = ref({})
const generalError = ref('')
const saving = ref(false)
const initializing = ref(false)

const SPECIES_KEYS = [
  'common_name', 'scientific_name', 'kind',
  'temp_min', 'temp_max', 'ph_min', 'ph_max', 'gh_min', 'gh_max',
  'adult_size_cm', 'min_tank_liters', 'min_group_size',
  'diet', 'temperament', 'swim_zone',
  'eats_plants', 'fin_nipper', 'territorial',
]

function fillForm(data) {
  for (const key of SPECIES_KEYS) {
    if (data[key] !== undefined) form[key] = data[key]
  }
  form.region_id = data.region_id
  form.biotope_id = data.biotope_id
}

onMounted(async () => {
  try {
    regions.value = await api.listRegions()
    if (!isEdit.value) return

    initializing.value = true
    const species = await api.getSpecies(props.id)
    fillForm(species)

    // Dejamos que el watch vea el cambio programático sin borrar el biotopo
    // y después cargamos los biotopos de la región antes de seleccionarlo.
    await nextTick()
    biotopes.value = await api.biotopesByRegion(species.region_id)
    form.biotope_id = species.biotope_id
  } catch (err) {
    generalError.value = err.message
  } finally {
    initializing.value = false
  }
})

// El usuario cambia la región: se limpia el biotopo y se recargan sus opciones.
watch(
  () => form.region_id,
  async (regionId) => {
    if (initializing.value) return
    form.biotope_id = ''
    biotopes.value = []
    if (!regionId) return
    try {
      biotopes.value = await api.biotopesByRegion(regionId)
    } catch (err) {
      generalError.value = err.message
    }
  },
)

async function submit() {
  errors.value = {}
  generalError.value = ''
  saving.value = true

  const payload = { biotope_id: form.biotope_id, region_id: form.region_id }
  for (const key of SPECIES_KEYS) payload[key] = form[key]

  try {
    if (isEdit.value) {
      await api.updateSpecies(props.id, payload)
    } else {
      await api.createSpecies(payload)
    }
    router.push('/species')
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
