<!--
  AnfragenPage.vue – Fahrzeuganfragen verwalten
  ══════════════════════════════════════════════
  Route: /anfragen (nur Admin + Employee)
  Zeigt alle Fahrzeuganfragen, Admin kann bestätigen/ablehnen/antworten.
-->
<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { Check, X, MessageSquare, Car } from 'lucide-vue-next'
import NavBar    from '../components/NavBar.vue'
import AppFooter from '../components/AppFooter.vue'
import { useAuth } from '../composables/useAuth'
import { apiFetch } from '../services/api'

const { user } = useAuth()

const scrolled = ref(false)
const onScroll = () => { scrolled.value = window.scrollY > 24 }
onMounted(()  => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))

interface Anfrage {
  id:             number
  customer_name:  string
  vehicle_info:   string | null
  type_display:   string
  message:        string
  admin_reply:    string
  status:         string
  status_display: string
  created_at:     string
}

const anfragen    = ref<Anfrage[]>([])
const loading     = ref(true)
const replyId     = ref<number | null>(null)
const replyText   = ref('')
const replyStatus = ref('confirmed')

async function laden() {
  loading.value = true
  try {
    anfragen.value = await apiFetch<Anfrage[]>('/api/appointments/?type=inquiry')
  } finally {
    loading.value = false
  }
}

async function antworten(id: number) {
  await apiFetch(`/api/appointments/${id}/reply/`, {
    method: 'PATCH',
    body: JSON.stringify({ admin_reply: replyText.value, status: replyStatus.value }),
  })
  replyId.value = null
  replyText.value = ''
  await laden()
}

const statusColor = (s: string) => ({
  pending:   'bg-yellow-100 text-yellow-800',
  confirmed: 'bg-green-100 text-green-800',
  rejected:  'bg-red-100 text-red-800',
  completed: 'bg-blue-100 text-blue-800',
}[s] ?? 'bg-gray-100 text-gray-600')

onMounted(laden)
</script>

<template>
  <NavBar :scrolled="scrolled" />
  <main class="pt-16 min-h-screen bg-background">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10">

      <h1 class="text-[#1a2e5a] font-bold text-2xl mb-2 flex items-center gap-2">
        <MessageSquare :size="22" class="text-[#e85c1a]" /> Anfragen verwalten
      </h1>
      <p class="text-[#8e9aaa] text-sm mb-8">Alle eingehenden Fahrzeuganfragen der Kunden</p>

      <div v-if="loading" class="space-y-3">
        <div v-for="n in 4" :key="n" class="bg-white rounded-xl h-24 animate-pulse border border-[#1a2e5a]/8" />
      </div>

      <div v-else-if="anfragen.length === 0" class="text-center py-20">
        <p class="text-[#1a2e5a] font-bold text-lg">Keine Anfragen vorhanden</p>
      </div>

      <div v-else class="space-y-4">
        <div v-for="a in anfragen" :key="a.id" class="bg-white rounded-xl border border-[#1a2e5a]/8 p-5 shadow-sm">

          <div class="flex items-start justify-between gap-4 flex-wrap mb-3">
            <div>
              <div class="flex items-center gap-2 mb-1">
                <span class="text-[#1a2e5a] font-bold text-sm">{{ a.customer_name }}</span>
                <span :class="['text-xs font-bold px-2 py-0.5 rounded-full', statusColor(a.status)]">
                  {{ a.status_display }}
                </span>
              </div>
              <p v-if="a.vehicle_info" class="text-[#e85c1a] text-xs font-semibold flex items-center gap-1">
                <Car :size="11" /> {{ a.vehicle_info }}
              </p>
              <p class="text-[#8e9aaa] text-xs">{{ new Date(a.created_at).toLocaleString('de-DE') }}</p>
            </div>
            <!-- Aktions-Buttons -->
            <div v-if="a.status === 'pending'" class="flex gap-2">
              <button @click="replyId = a.id; replyStatus = 'confirmed'"
                class="flex items-center gap-1.5 bg-green-500 hover:bg-green-600 text-white text-xs font-bold px-3 py-2 rounded-lg transition-colors">
                <Check :size="13" /> Bestätigen
              </button>
              <button @click="replyId = a.id; replyStatus = 'rejected'"
                class="flex items-center gap-1.5 bg-red-500 hover:bg-red-600 text-white text-xs font-bold px-3 py-2 rounded-lg transition-colors">
                <X :size="13" /> Ablehnen
              </button>
              <button @click="replyId = a.id; replyStatus = 'pending'"
                class="flex items-center gap-1.5 border border-[#1a2e5a]/20 text-[#1a2e5a] text-xs font-bold px-3 py-2 rounded-lg hover:bg-[#1a2e5a]/5 transition-colors">
                <MessageSquare :size="13" /> Antworten
              </button>
            </div>
          </div>

          <!-- Kundennachricht -->
          <div class="bg-[#f8f9fa] rounded-lg p-3 mb-3 text-sm text-[#1a2e5a]">{{ a.message }}</div>

          <!-- Bestehende Antwort -->
          <div v-if="a.admin_reply" class="bg-[#e85c1a]/5 border border-[#e85c1a]/20 rounded-lg p-3 text-sm text-[#1a2e5a] mb-3">
            <span class="text-[#e85c1a] font-bold text-xs">Ihre Antwort: </span>{{ a.admin_reply }}
          </div>

          <!-- Antwort-Formular -->
          <div v-if="replyId === a.id" class="border-t border-[#1a2e5a]/8 pt-4 mt-3">
            <select v-model="replyStatus" class="mb-3 px-3 py-2 border border-[#1a2e5a]/15 rounded-lg text-sm text-[#1a2e5a] focus:outline-none">
              <option value="confirmed">Bestätigen</option>
              <option value="rejected">Ablehnen</option>
              <option value="pending">Offen lassen</option>
            </select>
            <textarea v-model="replyText" rows="3" placeholder="Ihre Antwort an den Kunden..."
              class="w-full px-3 py-2.5 border border-[#1a2e5a]/15 rounded-lg text-sm text-[#1a2e5a] focus:outline-none resize-none mb-3" />
            <div class="flex gap-2">
              <button @click="antworten(a.id)"
                class="bg-[#e85c1a] hover:bg-[#d44e12] text-white font-bold px-4 py-2 rounded-lg text-sm transition-colors">
                Senden
              </button>
              <button @click="replyId = null"
                class="border border-[#1a2e5a]/20 text-[#1a2e5a] font-semibold px-4 py-2 rounded-lg text-sm hover:bg-[#1a2e5a]/5 transition-colors">
                Abbrechen
              </button>
            </div>
          </div>

        </div>
      </div>
    </div>
  </main>
  <AppFooter />
</template>
