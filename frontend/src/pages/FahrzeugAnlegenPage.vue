<!--
  FahrzeugAnlegenPage.vue – Fahrzeug anlegen / bearbeiten
  ════════════════════════════════════════════════════════
  Route: /fahrzeug-anlegen (nur Admin + Employee)
  API:   POST /api/vehicles/     → neues Fahrzeug
         PATCH /api/vehicles/id/ → bestehendes bearbeiten
-->
<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Save, ArrowLeft } from 'lucide-vue-next'
import NavBar    from '../components/NavBar.vue'
import AppFooter from '../components/AppFooter.vue'
import { apiFetch } from '../services/api'
import { useAuth } from '../composables/useAuth'

const router = useRouter()
const { user } = useAuth()

const scrolled = ref(false)
const onScroll = () => { scrolled.value = window.scrollY > 24 }
onMounted(()  => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))

const loading = ref(false)
const error   = ref('')
const success  = ref(false)

// Formular-Felder
const form = ref({
  brand:        '',
  model:        '',
  year:         new Date().getFullYear(),
  mileage:      0,
  price:        '',
  status:       'available',
  kraftstoff:   '',
  leistung:     '',
  getriebe:     '',
  farbe:        '',
  ez:           '',
  tueren:       4,
  hu:           '',
  beschreibung: '',
  ausstattung:  '',  // kommagetrennt, wird in Array umgewandelt
})

function validate(): string | null {
  if (!form.value.brand.trim())  return 'Marke ist erforderlich.'
  if (!form.value.model.trim())  return 'Modell ist erforderlich.'
  if (!form.value.price)         return 'Preis ist erforderlich.'
  if (isNaN(Number(form.value.price))) return 'Preis muss eine Zahl sein.'
  if (/<[^>]+>/.test(form.value.brand + form.value.model)) return 'Ungültige Zeichen.'
  return null
}

async function speichern() {
  const err = validate()
  if (err) { error.value = err; return }

  loading.value = true
  error.value   = ''

  try {
    const payload = {
      ...form.value,
      leistung:    form.value.leistung ? Number(form.value.leistung) : null,
      ausstattung: form.value.ausstattung
        ? form.value.ausstattung.split(',').map(s => s.trim()).filter(Boolean)
        : [],
    }
    await apiFetch('/api/vehicles/', { method: 'POST', body: JSON.stringify(payload) })
    success.value = true
    setTimeout(() => router.push('/'), 2000)
  } catch (e: any) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

const inputCls = 'w-full px-3 py-2.5 border border-[#1a2e5a]/15 rounded-lg text-sm text-[#1a2e5a] focus:outline-none focus:ring-2 focus:ring-[#1a2e5a]/20 bg-white'
</script>

<template>
  <NavBar :scrolled="scrolled" />
  <main class="pt-16 min-h-screen bg-background">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-10">

      <button @click="router.back()" class="flex items-center gap-1.5 text-sm text-[#8e9aaa] hover:text-[#1a2e5a] mb-6 transition-colors">
        <ArrowLeft :size="15" /> Zurück
      </button>

      <h1 class="text-[#1a2e5a] font-bold text-2xl mb-1">Fahrzeug anlegen</h1>
      <p class="text-[#8e9aaa] text-sm mb-8">Nur für Mitarbeiter und Administratoren</p>

      <!-- Erfolgsmeldung -->
      <div v-if="success" class="bg-green-50 border border-green-200 text-green-800 px-5 py-4 rounded-xl mb-6 font-semibold text-sm">
        ✓ Fahrzeug wurde erfolgreich angelegt. Sie werden weitergeleitet…
      </div>

      <!-- Fehlermeldung -->
      <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-5 py-4 rounded-xl mb-6 text-sm">{{ error }}</div>

      <div class="bg-white rounded-xl border border-[#1a2e5a]/8 p-7 shadow-sm space-y-6">

        <!-- Basisdaten -->
        <div>
          <h2 class="text-[#1a2e5a] font-bold text-sm uppercase tracking-wider mb-4">Basisdaten</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-[#8e9aaa] uppercase tracking-wider mb-2">Marke *</label>
              <input v-model="form.brand" type="text" placeholder="z.B. BMW" :class="inputCls" />
            </div>
            <div>
              <label class="block text-xs font-bold text-[#8e9aaa] uppercase tracking-wider mb-2">Modell *</label>
              <input v-model="form.model" type="text" placeholder="z.B. 3er Touring" :class="inputCls" />
            </div>
            <div>
              <label class="block text-xs font-bold text-[#8e9aaa] uppercase tracking-wider mb-2">Baujahr</label>
              <input v-model.number="form.year" type="number" min="1990" :max="new Date().getFullYear()" :class="inputCls" />
            </div>
            <div>
              <label class="block text-xs font-bold text-[#8e9aaa] uppercase tracking-wider mb-2">Kilometerstand</label>
              <input v-model.number="form.mileage" type="number" min="0" placeholder="48200" :class="inputCls" />
            </div>
            <div>
              <label class="block text-xs font-bold text-[#8e9aaa] uppercase tracking-wider mb-2">Preis (€) *</label>
              <input v-model="form.price" type="text" placeholder="32900.00" :class="inputCls" />
            </div>
            <div>
              <label class="block text-xs font-bold text-[#8e9aaa] uppercase tracking-wider mb-2">Status</label>
              <select v-model="form.status" :class="inputCls">
                <option value="available">Verfügbar</option>
                <option value="reserved">Reserviert</option>
                <option value="sold">Verkauft</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Details -->
        <div class="border-t border-[#1a2e5a]/8 pt-6">
          <h2 class="text-[#1a2e5a] font-bold text-sm uppercase tracking-wider mb-4">Details</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-[#8e9aaa] uppercase tracking-wider mb-2">Kraftstoff</label>
              <select v-model="form.kraftstoff" :class="inputCls">
                <option value="">- bitte wählen -</option>
                <option>Benzin</option><option>Diesel</option>
                <option>Elektro</option><option>Hybrid</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold text-[#8e9aaa] uppercase tracking-wider mb-2">Leistung (PS)</label>
              <input v-model="form.leistung" type="number" placeholder="190" :class="inputCls" />
            </div>
            <div>
              <label class="block text-xs font-bold text-[#8e9aaa] uppercase tracking-wider mb-2">Getriebe</label>
              <select v-model="form.getriebe" :class="inputCls">
                <option value="">- bitte wählen -</option>
                <option>Automatik</option><option>Schaltgetriebe</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-bold text-[#8e9aaa] uppercase tracking-wider mb-2">Farbe</label>
              <input v-model="form.farbe" type="text" placeholder="Alpinweiß" :class="inputCls" />
            </div>
            <div>
              <label class="block text-xs font-bold text-[#8e9aaa] uppercase tracking-wider mb-2">Erstzulassung</label>
              <input v-model="form.ez" type="text" placeholder="03/2021" :class="inputCls" />
            </div>
            <div>
              <label class="block text-xs font-bold text-[#8e9aaa] uppercase tracking-wider mb-2">Türen</label>
              <input v-model.number="form.tueren" type="number" min="2" max="5" :class="inputCls" />
            </div>
            <div>
              <label class="block text-xs font-bold text-[#8e9aaa] uppercase tracking-wider mb-2">HU bis</label>
              <input v-model="form.hu" type="text" placeholder="03/2026" :class="inputCls" />
            </div>
          </div>
        </div>

        <!-- Beschreibung + Ausstattung -->
        <div class="border-t border-[#1a2e5a]/8 pt-6">
          <h2 class="text-[#1a2e5a] font-bold text-sm uppercase tracking-wider mb-4">Beschreibung & Ausstattung</h2>
          <div class="mb-4">
            <label class="block text-xs font-bold text-[#8e9aaa] uppercase tracking-wider mb-2">Beschreibung</label>
            <textarea v-model="form.beschreibung" rows="4" placeholder="Fahrzeugbeschreibung…" :class="inputCls + ' resize-none'" />
          </div>
          <div>
            <label class="block text-xs font-bold text-[#8e9aaa] uppercase tracking-wider mb-2">Ausstattung (kommagetrennt)</label>
            <input v-model="form.ausstattung" type="text" placeholder="Navi, Ledersitze, Panoramadach" :class="inputCls" />
            <p class="text-[#8e9aaa] text-xs mt-1">Mehrere Einträge mit Komma trennen</p>
          </div>
        </div>

        <!-- Speichern -->
        <div class="border-t border-[#1a2e5a]/8 pt-6">
          <button @click="speichern" :disabled="loading"
            class="flex items-center gap-2 bg-[#e85c1a] hover:bg-[#d44e12] disabled:opacity-60 text-white font-bold px-6 py-3 rounded-lg text-sm transition-colors">
            <Save :size="15" />
            {{ loading ? 'Wird gespeichert…' : 'Fahrzeug speichern' }}
          </button>
        </div>

      </div>
    </div>
  </main>
  <AppFooter />
</template>
