<!--
  TerminePage.vue – Kalender & Termine
  ══════════════════════════════════════
  Route: /termine (nur für eingeloggte Nutzer)
  API:   GET  /api/appointments/     → eigene Termine (Kunde) oder alle (Admin/Employee)
         POST /api/appointments/     → neuen Termin anfragen
         PATCH /api/appointments/{id}/reply/ → Admin antwortet
-->
<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Calendar, Plus, X, Check, Clock, ChevronDown } from 'lucide-vue-next'
import NavBar    from '../components/NavBar.vue'
import AppFooter from '../components/AppFooter.vue'
import { useAuth } from '../composables/useAuth'
import { apiFetch } from '../services/api'

const router = useRouter()
const { user, isLoggedIn } = useAuth()

const scrolled = ref(false)
const onScroll = () => { scrolled.value = window.scrollY > 24 }
onMounted(()  => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))

interface Appointment {
  id:               number
  customer_name:    string
  vehicle_info:     string | null
  appointment_type: string
  type_display:     string
  appointment_date: string | null
  message:          string
  admin_reply:      string
  status:           string
  status_display:   string
  created_at:       string
}

const termine      = ref<Appointment[]>([])
const loading      = ref(true)
const error        = ref('')
const showForm     = ref(false)
const formLoading  = ref(false)
const formError    = ref('')

// Neuer Termin
const newType    = ref('consultation')
const newDate    = ref('')
const newMessage = ref('')

const TYPES = [
  { value: 'test_drive',   label: 'Probefahrt' },
  { value: 'consultation', label: 'Beratung' },
  { value: 'service',      label: 'Werkstatt' },
]

async function ladeDaten() {
  loading.value = true
  error.value   = ''
  try {
    termine.value = await apiFetch<Appointment[]>('/api/appointments/')
  } catch (e: any) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

async function terminAnfragen() {
  if (!newMessage.value.trim()) { formError.value = 'Bitte eine Nachricht eingeben.'; return }
  formLoading.value = true
  formError.value   = ''
  try {
    await apiFetch('/api/appointments/', {
      method: 'POST',
      body: JSON.stringify({
        appointment_type: newType.value,
        appointment_date: newDate.value || null,
        message:          newMessage.value,
        status:           'pending',
      }),
    })
    showForm.value   = false
    newMessage.value = ''
    newDate.value    = ''
    await ladeDaten()
  } catch (e: any) {
    formError.value = e.message
  } finally {
    formLoading.value = false
  }
}

const statusColor = (s: string) => ({
  pending:   'bg-yellow-100 text-yellow-800',
  confirmed: 'bg-green-100 text-green-800',
  rejected:  'bg-red-100 text-red-800',
  completed: 'bg-blue-100 text-blue-800',
  cancelled: 'bg-gray-100 text-gray-600',
}[s] ?? 'bg-gray-100 text-gray-600')

onMounted(() => { if (isLoggedIn.value) ladeDaten() })
</script>

<template>
  <NavBar :scrolled="scrolled" />
  <main class="pt-16 min-h-screen bg-background">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">

      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-[#1a2e5a] font-bold text-2xl flex items-center gap-2">
            <Calendar :size="22" class="text-[#e85c1a]" /> Termine & Anfragen
          </h1>
          <p class="text-[#8e9aaa] text-sm mt-1">
            {{ user?.role === 'customer' ? 'Ihre persönlichen Termine' : 'Alle Kundenanfragen' }}
          </p>
        </div>
        <button
          v-if="user?.role === 'customer'"
          @click="showForm = !showForm"
          class="flex items-center gap-2 bg-[#e85c1a] hover:bg-[#d44e12] text-white font-bold px-4 py-2.5 rounded-lg text-sm transition-colors"
        >
          <Plus :size="15" /> Termin anfragen
        </button>
      </div>

      <!-- Anfrageformular -->
      <div v-if="showForm" class="bg-white border border-[#1a2e5a]/10 rounded-xl p-6 mb-6 shadow-sm">
        <h2 class="text-[#1a2e5a] font-bold text-base mb-4">Neuen Termin anfragen</h2>
        <div v-if="formError" class="bg-red-50 border border-red-200 text-red-700 text-sm px-4 py-3 rounded-lg mb-4">{{ formError }}</div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label class="block text-xs font-bold text-[#1a2e5a] uppercase tracking-wider mb-2">Art</label>
            <select v-model="newType" class="w-full px-3 py-2.5 border border-[#1a2e5a]/15 rounded-lg text-sm text-[#1a2e5a] focus:outline-none">
              <option v-for="t in TYPES" :key="t.value" :value="t.value">{{ t.label }}</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-bold text-[#1a2e5a] uppercase tracking-wider mb-2">Wunschdatum (optional)</label>
            <input v-model="newDate" type="datetime-local"
              class="w-full px-3 py-2.5 border border-[#1a2e5a]/15 rounded-lg text-sm text-[#1a2e5a] focus:outline-none" />
          </div>
        </div>
        <div class="mb-4">
          <label class="block text-xs font-bold text-[#1a2e5a] uppercase tracking-wider mb-2">Nachricht *</label>
          <textarea v-model="newMessage" rows="3" placeholder="Ihre Nachricht an uns..."
            class="w-full px-3 py-2.5 border border-[#1a2e5a]/15 rounded-lg text-sm text-[#1a2e5a] focus:outline-none resize-none" />
        </div>
        <div class="flex gap-3">
          <button @click="terminAnfragen" :disabled="formLoading"
            class="bg-[#e85c1a] hover:bg-[#d44e12] disabled:opacity-60 text-white font-bold px-5 py-2.5 rounded-lg text-sm transition-colors">
            {{ formLoading ? 'Wird gesendet…' : 'Anfrage senden' }}
          </button>
          <button @click="showForm = false" class="border border-[#1a2e5a]/20 text-[#1a2e5a] font-semibold px-5 py-2.5 rounded-lg text-sm hover:bg-[#1a2e5a]/5 transition-colors">
            Abbrechen
          </button>
        </div>
      </div>

      <!-- Lade-State -->
      <div v-if="loading" class="space-y-3">
        <div v-for="n in 3" :key="n" class="bg-white rounded-xl h-20 animate-pulse border border-[#1a2e5a]/8" />
      </div>

      <!-- Fehler -->
      <div v-else-if="error" class="text-center py-16 text-red-500 text-sm">{{ error }}</div>

      <!-- Leer -->
      <div v-else-if="termine.length === 0" class="text-center py-20">
        <Calendar :size="36" class="text-[#1a2e5a]/20 mx-auto mb-4" />
        <p class="text-[#1a2e5a] font-bold text-lg">Keine Termine vorhanden</p>
        <p class="text-[#8e9aaa] text-sm">Stellen Sie eine Anfrage über den Button oben.</p>
      </div>

      <!-- Terminliste -->
      <div v-else class="space-y-4">
        <div v-for="t in termine" :key="t.id" class="bg-white rounded-xl border border-[#1a2e5a]/8 p-5 shadow-sm">
          <div class="flex items-start justify-between gap-4 flex-wrap">
            <div class="flex-1">
              <div class="flex items-center gap-2 flex-wrap mb-1">
                <span class="text-[#1a2e5a] font-bold text-sm">{{ t.type_display }}</span>
                <span :class="['text-xs font-bold px-2 py-0.5 rounded-full', statusColor(t.status)]">
                  {{ t.status_display }}
                </span>
              </div>
              <p v-if="t.vehicle_info" class="text-[#e85c1a] text-xs font-semibold mb-1">🚗 {{ t.vehicle_info }}</p>
              <p v-if="t.customer_name && user?.role !== 'customer'" class="text-[#8e9aaa] text-xs mb-1">Kunde: {{ t.customer_name }}</p>
              <p v-if="t.appointment_date" class="text-[#8e9aaa] text-xs flex items-center gap-1">
                <Clock :size="11" /> {{ new Date(t.appointment_date).toLocaleString('de-DE') }}
              </p>
              <p v-if="t.message" class="text-[#8e9aaa] text-sm mt-2 bg-[#f8f9fa] rounded p-2">{{ t.message }}</p>
              <p v-if="t.admin_reply" class="text-[#1a2e5a] text-sm mt-2 bg-[#e85c1a]/5 border border-[#e85c1a]/20 rounded p-2">
                <span class="font-bold text-[#e85c1a] text-xs">Antwort: </span>{{ t.admin_reply }}
              </p>
            </div>
            <span class="text-[#8e9aaa] text-xs">{{ new Date(t.created_at).toLocaleDateString('de-DE') }}</span>
          </div>
        </div>
      </div>

    </div>
  </main>
  <AppFooter />
</template>
