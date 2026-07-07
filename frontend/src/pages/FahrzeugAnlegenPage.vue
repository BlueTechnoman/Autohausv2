<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  Plus, Edit2, Trash2, Save, X, ArrowLeft,
  ChevronDown, ChevronUp, AlertCircle, CheckCircle2,
  Car, Eye,
} from 'lucide-vue-next'
import NavBar    from '../components/NavBar.vue'
import AppFooter from '../components/AppFooter.vue'
import { apiFetch }  from '../services/api'
import { useAuth }   from '../composables/useAuth'
import { useFahrzeuge, mapApiToFahrzeug } from '../composables/useFahrzeuge'
import { formatPreis, formatKm, formatKraftstoff, formatGetriebe, KRAFTSTOFF_OPTIONS } from '../data/fahrzeuge'
import type { Fahrzeug } from '../data/fahrzeuge'

const router = useRouter()
const { user } = useAuth()
const { fahrzeuge, loading, laden } = useFahrzeuge()

const scrolled = ref(false)
const onScroll = () => { scrolled.value = window.scrollY > 24 }
onMounted(()  => { window.addEventListener('scroll', onScroll); laden() })
onUnmounted(() => window.removeEventListener('scroll', onScroll))

type FormMode = 'list' | 'create' | 'edit'
const mode        = ref<FormMode>('list')
const editId      = ref<number | null>(null)
const formLoading = ref(false)
const formError   = ref('')
const formSuccess = ref('')
const deleteId    = ref<number | null>(null)
const deleteLoading = ref(false)

const GETRIEBE_OPTS = [
  { value: 'manuell',       label: 'Schaltgetriebe' },
  { value: 'automatik',     label: 'Automatik' },
  { value: 'halbautomatik', label: 'Halbautomatik' },
]

const emptyForm = () => ({
  brand:        '',
  model:        '',
  year:         new Date().getFullYear(),
  mileage:      0,
  price:        '',
  status:       'available',
  kraftstoff:   'benzin',
  leistung:     '' as string | number,
  getriebe:     'manuell',
  farbe:        '',
  ez:           '',
  tueren:       4 as string | number,
  hu:           '',
  beschreibung: '',
  ausstattung:  '',
})

const form = ref(emptyForm())

function openCreate() {
  form.value  = emptyForm()
  editId.value = null
  formError.value   = ''
  formSuccess.value = ''
  mode.value  = 'create'
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function openEdit(f: Fahrzeug) {
  form.value = {
    brand:        f.marke,
    model:        f.modell,
    year:         f.baujahr,
    mileage:      f.km,
    price:        String(f.preis),
    status:       f.status,
    kraftstoff:   f.kraftstoff,
    leistung:     f.leistung || '',
    getriebe:     f.getriebe,
    farbe:        f.farbe,
    ez:           f.ez,
    tueren:       f.tueren || 4,
    hu:           f.hu,
    beschreibung: f.beschreibung,
    ausstattung:  f.ausstattung.join(', '),
  }
  editId.value      = f.id
  formError.value   = ''
  formSuccess.value = ''
  mode.value        = 'edit'
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function validate(): string | null {
  if (!form.value.brand.trim())  return 'Marke ist erforderlich.'
  if (!form.value.model.trim())  return 'Modell ist erforderlich.'
  if (!form.value.price)         return 'Preis ist erforderlich.'
  if (isNaN(Number(form.value.price))) return 'Preis muss eine Zahl sein.'
  if (Number(form.value.price) <= 0)   return 'Preis muss größer als 0 sein.'
  if (/<[^>]+>/.test(form.value.brand + form.value.model + form.value.beschreibung)) {
    return 'Ungültige Zeichen (HTML-Tags nicht erlaubt).'
  }
  return null
}

async function speichern() {
  const err = validate()
  if (err) { formError.value = err; return }

  formLoading.value = true
  formError.value   = ''
  formSuccess.value = ''

  const payload = {
    brand:        form.value.brand.trim(),
    model:        form.value.model.trim(),
    year:         Number(form.value.year),
    mileage:      Number(form.value.mileage),
    price:        form.value.price,
    status:       form.value.status,
    kraftstoff:   form.value.kraftstoff,
    getriebe:     form.value.getriebe,
    leistung:     form.value.leistung ? Number(form.value.leistung) : null,
    farbe:        form.value.farbe,
    ez:           form.value.ez,
    tueren:       form.value.tueren ? Number(form.value.tueren) : null,
    hu:           form.value.hu,
    beschreibung: form.value.beschreibung,
    ausstattung:  form.value.ausstattung
      ? form.value.ausstattung.toString().split(',').map(s => s.trim()).filter(Boolean)
      : [],
  }

  try {
    if (mode.value === 'create') {
      await apiFetch('/api/vehicles/', { method: 'POST', body: JSON.stringify(payload) })
      formSuccess.value = 'Fahrzeug erfolgreich angelegt.'
    } else {
      await apiFetch(`/api/vehicles/${editId.value}/`, { method: 'PATCH', body: JSON.stringify(payload) })
      formSuccess.value = 'Fahrzeug erfolgreich aktualisiert.'
    }
    await laden()
    setTimeout(() => { mode.value = 'list'; formSuccess.value = '' }, 1500)
  } catch (e: unknown) {
    formError.value = e instanceof Error ? e.message : 'Fehler beim Speichern.'
  } finally {
    formLoading.value = false
  }
}

async function loeschen(id: number) {
  deleteLoading.value = true
  try {
    await apiFetch(`/api/vehicles/${id}/`, { method: 'DELETE' })
    deleteId.value = null
    await laden()
  } catch (e: unknown) {
    alert(e instanceof Error ? e.message : 'Fehler beim Löschen.')
  } finally {
    deleteLoading.value = false
  }
}

async function statusAendern(id: number, newStatus: string) {
  try {
    await apiFetch(`/api/vehicles/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify({ status: newStatus }),
    })
    await laden()
  } catch (e: unknown) {
    alert(e instanceof Error ? e.message : 'Fehler beim Statuswechsel.')
  }
}

const statusOptions = [
  { value: 'available', label: 'Verfügbar',  cls: 'bg-green-100 text-green-800' },
  { value: 'reserved',  label: 'Reserviert', cls: 'bg-yellow-100 text-yellow-800' },
  { value: 'sold',      label: 'Verkauft',   cls: 'bg-red-100 text-red-800' },
]
function statusCls(s: string) {
  return statusOptions.find(o => o.value === s)?.cls ?? 'bg-gray-100 text-gray-600'
}
function statusLabel(s: string) {
  return statusOptions.find(o => o.value === s)?.label ?? s
}

const inputCls = 'w-full px-3 py-2.5 border border-[#1a2e5a]/15 rounded-lg text-sm text-[#1a2e5a] focus:outline-none focus:ring-2 focus:ring-[#1a2e5a]/20 bg-white'
</script>

<template>
  <NavBar :scrolled="scrolled" />
  <main class="pt-16 min-h-screen bg-background">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">

      <!-- Header -->
      <div class="flex items-center justify-between mb-8 flex-wrap gap-4">
        <div>
          <h1 class="text-[#1a2e5a] font-bold text-2xl flex items-center gap-2">
            <Car :size="22" class="text-[#e85c1a]" /> Fahrzeugverwaltung
          </h1>
          <p class="text-[#8e9aaa] text-sm mt-1">
            Mitarbeiter: {{ user?.username }} · {{ fahrzeuge.length }} Fahrzeuge
          </p>
        </div>
        <button v-if="mode === 'list'" @click="openCreate"
          class="flex items-center gap-2 bg-[#e85c1a] hover:bg-[#d44e12] text-white font-bold px-5 py-2.5 rounded-lg text-sm transition-colors">
          <Plus :size="16" /> Fahrzeug anlegen
        </button>
        <button v-else @click="mode = 'list'"
          class="flex items-center gap-2 border border-[#1a2e5a]/20 text-[#1a2e5a] hover:bg-[#1a2e5a]/5 font-semibold px-5 py-2.5 rounded-lg text-sm transition-colors">
          <ArrowLeft :size="15" /> Zurück zur Liste
        </button>
      </div>

      <!-- ── Formular: Anlegen / Bearbeiten ── -->
      <div v-if="mode !== 'list'" class="bg-white rounded-xl border border-[#1a2e5a]/8 p-7 shadow-sm mb-8">
        <h2 class="text-[#1a2e5a] font-bold text-lg mb-6">
          {{ mode === 'create' ? 'Neues Fahrzeug anlegen' : 'Fahrzeug bearbeiten' }}
        </h2>

        <div v-if="formSuccess" class="bg-green-50 border border-green-200 rounded-lg px-5 py-4 mb-5 flex gap-3">
          <CheckCircle2 :size="18" class="text-green-600 shrink-0" />
          <p class="text-green-800 font-semibold text-sm">{{ formSuccess }}</p>
        </div>
        <div v-if="formError" class="bg-red-50 border border-red-200 rounded-lg px-5 py-4 mb-5 flex gap-3">
          <AlertCircle :size="18" class="text-red-600 shrink-0" />
          <p class="text-red-700 text-sm">{{ formError }}</p>
        </div>

        <div class="space-y-6">

          <!-- Basisdaten -->
          <div>
            <h3 class="text-[#1a2e5a] text-xs font-bold uppercase tracking-wider mb-4">Basisdaten</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label class="block text-xs font-bold text-[#8e9aaa] uppercase tracking-wider mb-2">Marke *</label>
                <input v-model="form.brand" type="text" placeholder="BMW" :class="inputCls" />
              </div>
              <div class="md:col-span-2">
                <label class="block text-xs font-bold text-[#8e9aaa] uppercase tracking-wider mb-2">Modell *</label>
                <input v-model="form.model" type="text" placeholder="3er Touring 320d" :class="inputCls" />
              </div>
              <div>
                <label class="block text-xs font-bold text-[#8e9aaa] uppercase tracking-wider mb-2">Baujahr</label>
                <input v-model.number="form.year" type="number" min="1900" :max="new Date().getFullYear() + 1" :class="inputCls" />
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

          <!-- Technische Details -->
          <div class="border-t border-[#1a2e5a]/8 pt-6">
            <h3 class="text-[#1a2e5a] text-xs font-bold uppercase tracking-wider mb-4">Technische Details</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label class="block text-xs font-bold text-[#8e9aaa] uppercase tracking-wider mb-2">Kraftstoff</label>
                <select v-model="form.kraftstoff" :class="inputCls">
                  <option v-for="k in KRAFTSTOFF_OPTIONS.filter(o => o.value)" :key="k.value" :value="k.value">{{ k.label }}</option>
                </select>
              </div>
              <div>
                <label class="block text-xs font-bold text-[#8e9aaa] uppercase tracking-wider mb-2">Getriebe</label>
                <select v-model="form.getriebe" :class="inputCls">
                  <option v-for="g in GETRIEBE_OPTS" :key="g.value" :value="g.value">{{ g.label }}</option>
                </select>
              </div>
              <div>
                <label class="block text-xs font-bold text-[#8e9aaa] uppercase tracking-wider mb-2">Leistung (PS)</label>
                <input v-model="form.leistung" type="number" placeholder="190" :class="inputCls" />
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
                <input v-model.number="form.tueren" type="number" min="1" max="8" :class="inputCls" />
              </div>
              <div>
                <label class="block text-xs font-bold text-[#8e9aaa] uppercase tracking-wider mb-2">HU bis</label>
                <input v-model="form.hu" type="text" placeholder="03/2026" :class="inputCls" />
              </div>
            </div>
          </div>

          <!-- Beschreibung & Ausstattung -->
          <div class="border-t border-[#1a2e5a]/8 pt-6">
            <h3 class="text-[#1a2e5a] text-xs font-bold uppercase tracking-wider mb-4">Beschreibung & Ausstattung</h3>
            <div class="mb-4">
              <label class="block text-xs font-bold text-[#8e9aaa] uppercase tracking-wider mb-2">Beschreibung</label>
              <textarea v-model="form.beschreibung" rows="4" placeholder="Fahrzeugbeschreibung …" :class="inputCls + ' resize-none'" />
            </div>
            <div>
              <label class="block text-xs font-bold text-[#8e9aaa] uppercase tracking-wider mb-2">Ausstattung (kommagetrennt)</label>
              <input v-model="form.ausstattung" type="text" placeholder="Navi, Ledersitze, Panoramadach" :class="inputCls" />
              <p class="text-[#8e9aaa] text-xs mt-1">Mehrere Einträge mit Komma trennen</p>
            </div>
          </div>

          <!-- Speichern -->
          <div class="border-t border-[#1a2e5a]/8 pt-6 flex gap-3">
            <button @click="speichern" :disabled="formLoading"
              class="flex items-center gap-2 bg-[#e85c1a] hover:bg-[#d44e12] disabled:opacity-60 text-white font-bold px-6 py-3 rounded-lg text-sm transition-colors">
              <Save :size="15" /> {{ formLoading ? 'Wird gespeichert…' : 'Fahrzeug speichern' }}
            </button>
            <button @click="mode = 'list'"
              class="flex items-center gap-2 border border-[#1a2e5a]/20 text-[#1a2e5a] hover:bg-[#1a2e5a]/5 font-semibold px-6 py-3 rounded-lg text-sm transition-colors">
              <X :size="15" /> Abbrechen
            </button>
          </div>

        </div>
      </div>

      <!-- ── Fahrzeugliste ── -->
      <div v-if="mode === 'list'">

        <div v-if="loading" class="space-y-3">
          <div v-for="n in 5" :key="n" class="bg-white rounded-xl h-20 animate-pulse border border-[#1a2e5a]/8" />
        </div>

        <div v-else-if="fahrzeuge.length === 0" class="text-center py-20 bg-white rounded-xl border border-[#1a2e5a]/8">
          <p class="text-[#1a2e5a] font-bold text-lg mb-2">Noch keine Fahrzeuge vorhanden</p>
          <p class="text-[#8e9aaa] text-sm">Legen Sie das erste Fahrzeug über den Button oben an.</p>
        </div>

        <div v-else class="space-y-3">
          <div v-for="f in fahrzeuge" :key="f.id"
            class="bg-white rounded-xl border border-[#1a2e5a]/8 shadow-sm overflow-hidden">
            <div class="flex items-center gap-4 p-4">

              <!-- Fahrzeugbild -->
              <div class="w-20 h-14 shrink-0 rounded-lg overflow-hidden bg-[#e2e8f0]">
                <img :src="f.bild" :alt="f.modell" class="w-full h-full object-cover" />
              </div>

              <!-- Info -->
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 flex-wrap">
                  <span class="text-[#1a2e5a] font-bold text-sm">{{ f.marke }} {{ f.modell }}</span>
                  <span :class="['text-xs font-bold px-2 py-0.5 rounded-full', statusCls(f.status)]">
                    {{ statusLabel(f.status) }}
                  </span>
                </div>
                <p class="text-[#8e9aaa] text-xs mt-0.5">
                  {{ f.baujahr }} · {{ formatKm(f.km) }} · {{ formatKraftstoff(f.kraftstoff) }}
                </p>
              </div>

              <!-- Preis -->
              <div class="text-right shrink-0 hidden sm:block">
                <div class="text-[#1a2e5a] font-bold">{{ formatPreis(f.preis) }}</div>
              </div>

              <!-- Aktionen -->
              <div class="flex items-center gap-2 shrink-0">

                <!-- Status ändern -->
                <select
                  :value="f.status"
                  @change="statusAendern(f.id, ($event.target as HTMLSelectElement).value)"
                  class="text-xs border border-[#1a2e5a]/15 rounded-lg px-2 py-1.5 text-[#1a2e5a] bg-white focus:outline-none hidden md:block"
                >
                  <option value="available">Verfügbar</option>
                  <option value="reserved">Reserviert</option>
                  <option value="sold">Verkauft</option>
                </select>

                <!-- Detail ansehen -->
                <button @click="$router.push(`/fahrzeug/${f.id}`)"
                  class="w-8 h-8 rounded-full border border-[#1a2e5a]/15 hover:bg-[#1a2e5a]/5 flex items-center justify-center transition-colors"
                  title="Detailseite">
                  <Eye :size="14" class="text-[#1a2e5a]" />
                </button>

                <!-- Bearbeiten -->
                <button @click="openEdit(f)"
                  class="w-8 h-8 rounded-full bg-[#1a2e5a]/8 hover:bg-[#1a2e5a]/15 flex items-center justify-center transition-colors"
                  title="Bearbeiten">
                  <Edit2 :size="14" class="text-[#1a2e5a]" />
                </button>

                <!-- Löschen -->
                <button @click="deleteId = f.id"
                  class="w-8 h-8 rounded-full bg-red-50 hover:bg-red-100 flex items-center justify-center transition-colors"
                  title="Löschen">
                  <Trash2 :size="14" class="text-red-600" />
                </button>

              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </main>

  <!-- Lösch-Bestätigungs-Dialog -->
  <div v-if="deleteId !== null" class="fixed inset-0 z-[200] flex items-center justify-center p-4 bg-black/40"
    @click.self="deleteId = null">
    <div class="bg-white rounded-xl shadow-2xl max-w-sm w-full p-6">
      <h2 class="text-[#1a2e5a] font-bold text-lg mb-2">Fahrzeug löschen?</h2>
      <p class="text-[#8e9aaa] text-sm mb-6">
        Diese Aktion kann nicht rückgängig gemacht werden. Das Fahrzeug wird dauerhaft aus der Datenbank entfernt.
      </p>
      <div class="flex gap-3">
        <button @click="loeschen(deleteId!)" :disabled="deleteLoading"
          class="flex-1 bg-red-600 hover:bg-red-700 disabled:opacity-60 text-white font-bold py-2.5 rounded-lg text-sm transition-colors">
          {{ deleteLoading ? 'Wird gelöscht…' : 'Ja, löschen' }}
        </button>
        <button @click="deleteId = null"
          class="flex-1 border border-[#1a2e5a]/20 text-[#1a2e5a] font-semibold py-2.5 rounded-lg text-sm hover:bg-[#1a2e5a]/5 transition-colors">
          Abbrechen
        </button>
      </div>
    </div>
  </div>

  <AppFooter />
</template>
