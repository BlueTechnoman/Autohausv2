<!--
  FahrzeugDetailPage.vue – Einzelansicht eines Fahrzeugs
  ═══════════════════════════════════════════════════════
  Route: /fahrzeug/:id

  Datenladen:
    • API-Aufruf: GET /api/vehicles/{id}/
    • Enthält: alle Felder + Bilder (mit image_url) + Preisverlauf
    • Lädt via useFahrzeuge().ladenEinzel(id)

  Falls Fahrzeug nicht gefunden:
    • 404-Weiterleitung via router.replace('/404')
-->
<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  ChevronLeft, ChevronRight, ShoppingCart, Phone, Check, MessageSquare,
  Calendar, Gauge, Fuel, Settings2, Palette, DoorOpen,
  Wrench, Info, ArrowLeft,
} from 'lucide-vue-next'
import NavBar    from '../components/NavBar.vue'
import AppFooter from '../components/AppFooter.vue'
import { useFahrzeuge }    from '../composables/useFahrzeuge'
import { useCart }         from '../composables/useCart'
import { useNotification } from '../composables/useNotification'
import { formatKm, formatPreis } from '../data/fahrzeuge'
import type { Fahrzeug } from '../data/fahrzeuge'

const route  = useRoute()
const router = useRouter()
const { ladenEinzel }  = useFahrzeuge()
const { isInCart, toggle } = useCart()
const { show }             = useNotification()

// ── State ──────────────────────────────────────────────────────────────
const fahrzeug   = ref<Fahrzeug | null>(null)
const loading    = ref(true)
const fehler     = ref<string | null>(null)
const scrolled   = ref(false)
const activeImage= ref(0)

const onScroll = () => { scrolled.value = window.scrollY > 24 }
onMounted(()  => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))

// ── Fahrzeug laden ────────────────────────────────────────────────────
async function loadVehicle(id: number) {
  loading.value  = true
  fehler.value   = null
  activeImage.value = 0

  const result = await ladenEinzel(id)
  if (!result) {
    router.replace('/404')
    return
  }
  fahrzeug.value = result
  loading.value  = false
}

// Route-ID überwachen (falls Navigation zwischen Detailseiten)
watch(
  () => route.params.id,
  (newId) => { if (newId) loadVehicle(Number(newId)) },
  { immediate: true }
)

// ── Galerie ────────────────────────────────────────────────────────────
function prevImage() {
  if (!fahrzeug.value) return
  activeImage.value = (activeImage.value - 1 + fahrzeug.value.bilder.length) % fahrzeug.value.bilder.length
}
function nextImage() {
  if (!fahrzeug.value) return
  activeImage.value = (activeImage.value + 1) % fahrzeug.value.bilder.length
}

// ── Warenkorb ─────────────────────────────────────────────────────────
function handleCart() {
  if (!fahrzeug.value) return
  const added = toggle(fahrzeug.value)
  show(added
    ? `${fahrzeug.value.marke} ${fahrzeug.value.modell} zum Warenkorb hinzugefügt`
    : `${fahrzeug.value.marke} ${fahrzeug.value.modell} entfernt`)
}

// ── Specs-Tabelle ─────────────────────────────────────────────────────
const specs = computed(() => {
  if (!fahrzeug.value) return []
  const f = fahrzeug.value
  return [
    { icon: Calendar,  label: 'Erstzulassung', wert: f.ez || '–' },
    { icon: Gauge,     label: 'Kilometerstand', wert: formatKm(f.km) },
    { icon: Fuel,      label: 'Kraftstoff',    wert: f.kraftstoff || '–' },
    { icon: Settings2, label: 'Getriebe',      wert: f.getriebe || '–' },
    { icon: Info,      label: 'Leistung',      wert: f.leistung ? `${f.leistung} PS` : '–' },
    { icon: Palette,   label: 'Farbe',         wert: f.farbe || '–' },
    { icon: DoorOpen,  label: 'Türen',         wert: f.tueren ? `${f.tueren}-türig` : '–' },
    { icon: Wrench,    label: 'HU bis',        wert: f.hu || '–' },
  ]
})
</script>

<template>
  <NavBar :scrolled="scrolled" />

  <!-- Lade-Zustand -->
  <main v-if="loading" class="pt-16 min-h-screen bg-background">
    <div class="max-w-7xl mx-auto px-4 py-12 animate-pulse">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2 space-y-4">
          <div class="aspect-[16/10] bg-[#e2e8f0] rounded-xl" />
          <div class="h-32 bg-[#e2e8f0] rounded-xl" />
        </div>
        <div class="h-64 bg-[#e2e8f0] rounded-xl" />
      </div>
    </div>
  </main>

  <main v-else-if="fahrzeug" class="pt-16">

    <!-- Breadcrumb -->
    <div class="bg-white border-b border-[#1a2e5a]/8">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
        <nav class="flex items-center gap-2 text-xs text-[#8e9aaa]">
          <button @click="router.push('/')" class="hover:text-[#e85c1a] transition-colors">Startseite</button>
          <span>/</span>
          <button @click="router.push('/#fahrzeuge')" class="hover:text-[#e85c1a] transition-colors">Fahrzeuge</button>
          <span>/</span>
          <span class="text-[#1a2e5a] font-semibold">{{ fahrzeug.marke }} {{ fahrzeug.modell }}</span>
        </nav>
      </div>
    </div>

    <!-- Zurück -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6">
      <button
        @click="router.back()"
        class="flex items-center gap-1.5 text-sm text-[#8e9aaa] hover:text-[#1a2e5a] transition-colors mb-6"
      >
        <ArrowLeft :size="15" />
        Zurück zur Übersicht
      </button>
    </div>

    <!-- Haupt-Layout -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-16">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">

        <!-- Linke Spalte: Galerie + Details -->
        <div class="lg:col-span-2 space-y-6">

          <!-- Galerie -->
          <div class="bg-white rounded-xl border border-[#1a2e5a]/8 overflow-hidden shadow-sm">
            <div class="relative aspect-[16/10] bg-[#e2e8f0]">
              <img
                :src="fahrzeug.bilder[activeImage]"
                :alt="`${fahrzeug.marke} ${fahrzeug.modell}`"
                class="w-full h-full object-cover"
              />
              <div class="absolute top-4 left-4">
                <span class="bg-[#1a2e5a] text-white text-sm font-bold px-3 py-1.5 rounded">{{ fahrzeug.marke }}</span>
              </div>
              <div v-if="isInCart(fahrzeug.id)" class="absolute top-4 right-4">
                <span class="bg-[#e85c1a] text-white text-xs font-bold px-3 py-1.5 rounded flex items-center gap-1.5">
                  <Check :size="12" /> Vorgemerkt
                </span>
              </div>
              <button v-if="fahrzeug.bilder.length > 1" @click="prevImage"
                class="absolute left-3 top-1/2 -translate-y-1/2 w-10 h-10 bg-white/85 hover:bg-white rounded-full shadow flex items-center justify-center transition-colors">
                <ChevronLeft :size="18" class="text-[#1a2e5a]" />
              </button>
              <button v-if="fahrzeug.bilder.length > 1" @click="nextImage"
                class="absolute right-3 top-1/2 -translate-y-1/2 w-10 h-10 bg-white/85 hover:bg-white rounded-full shadow flex items-center justify-center transition-colors">
                <ChevronRight :size="18" class="text-[#1a2e5a]" />
              </button>
              <div class="absolute bottom-3 right-4 bg-black/50 text-white text-xs px-2.5 py-1 rounded-full">
                {{ activeImage + 1 }} / {{ fahrzeug.bilder.length }}
              </div>
            </div>
            <div v-if="fahrzeug.bilder.length > 1" class="flex gap-2 p-3">
              <button v-for="(bild, idx) in fahrzeug.bilder" :key="idx" @click="activeImage = idx"
                :class="['w-20 h-14 rounded overflow-hidden border-2 transition-colors',
                  activeImage === idx ? 'border-[#e85c1a]' : 'border-transparent hover:border-[#1a2e5a]/30']">
                <img :src="bild" class="w-full h-full object-cover" />
              </button>
            </div>
          </div>

          <!-- Beschreibung -->
          <div class="bg-white rounded-xl border border-[#1a2e5a]/8 p-7 shadow-sm">
            <h1 class="text-[#1a2e5a] font-bold text-2xl mb-1">{{ fahrzeug.marke }} {{ fahrzeug.modell }}</h1>
            <p class="text-[#8e9aaa] text-sm mb-6">Baujahr {{ fahrzeug.baujahr }} · {{ formatKm(fahrzeug.km) }}</p>
            <h2 class="text-[#1a2e5a] font-bold text-base mb-3">Beschreibung</h2>
            <p class="text-[#8e9aaa] text-sm leading-relaxed">{{ fahrzeug.beschreibung || 'Keine Beschreibung vorhanden.' }}</p>
          </div>

          <!-- Technische Daten -->
          <div class="bg-white rounded-xl border border-[#1a2e5a]/8 p-7 shadow-sm">
            <h2 class="text-[#1a2e5a] font-bold text-base mb-5">Technische Daten</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div v-for="spec in specs" :key="spec.label" class="bg-[#f8f9fa] rounded-lg p-4">
                <component :is="spec.icon" :size="16" class="text-[#e85c1a] mb-2" />
                <div class="text-[#8e9aaa] text-xs mb-1">{{ spec.label }}</div>
                <div class="text-[#1a2e5a] font-bold text-sm">{{ spec.wert }}</div>
              </div>
            </div>
          </div>

          <!-- Ausstattung -->
          <div v-if="fahrzeug.ausstattung.length > 0" class="bg-white rounded-xl border border-[#1a2e5a]/8 p-7 shadow-sm">
            <h2 class="text-[#1a2e5a] font-bold text-base mb-5">Ausstattung</h2>
            <ul class="grid grid-cols-1 md:grid-cols-2 gap-2.5">
              <li v-for="item in fahrzeug.ausstattung" :key="item" class="flex items-start gap-2.5 text-sm text-[#1a2e5a]">
                <span class="w-4 h-4 bg-[#e85c1a]/12 rounded-full flex items-center justify-center shrink-0 mt-0.5">
                  <Check :size="9" class="text-[#e85c1a]" />
                </span>
                {{ item }}
              </li>
            </ul>
          </div>

        </div>

        <!-- Rechte Spalte: Preis-Karte (sticky) -->
        <div>
          <div class="bg-white rounded-xl border border-[#1a2e5a]/8 p-6 shadow-sm sticky top-20">
            <div class="border-b border-[#1a2e5a]/8 pb-5 mb-5">
              <div class="text-[#8e9aaa] text-xs mb-1">Verkaufspreis (brutto)</div>
              <div class="text-[#1a2e5a] font-bold text-3xl">{{ formatPreis(fahrzeug.preis) }}</div>
              <div class="text-[#8e9aaa] text-xs mt-1">
                inkl. 19% MwSt. ({{ formatPreis(Math.round(fahrzeug.preis - fahrzeug.preis / 1.19)) }})
              </div>
            </div>

            <div class="space-y-2.5 mb-5 text-sm">
              <div class="flex justify-between"><span class="text-[#8e9aaa]">Baujahr</span><span class="text-[#1a2e5a] font-semibold">{{ fahrzeug.baujahr }}</span></div>
              <div class="flex justify-between"><span class="text-[#8e9aaa]">km-Stand</span><span class="text-[#1a2e5a] font-semibold">{{ formatKm(fahrzeug.km) }}</span></div>
              <div class="flex justify-between"><span class="text-[#8e9aaa]">Kraftstoff</span><span class="text-[#1a2e5a] font-semibold">{{ fahrzeug.kraftstoff || '–' }}</span></div>
              <div class="flex justify-between"><span class="text-[#8e9aaa]">Leistung</span><span class="text-[#1a2e5a] font-semibold">{{ fahrzeug.leistung ? fahrzeug.leistung + ' PS' : '–' }}</span></div>
            </div>

            <button
              @click="handleCart"
              :class="[
                'w-full flex items-center justify-center gap-2 font-bold py-3.5 rounded-lg text-sm transition-colors mb-3',
                isInCart(fahrzeug.id) ? 'bg-[#1a2e5a] text-white' : 'bg-[#e85c1a] hover:bg-[#d44e12] text-white',
              ]"
            >
              <Check v-if="isInCart(fahrzeug.id)" :size="16" />
              <ShoppingCart v-else :size="16" />
              {{ isInCart(fahrzeug.id) ? 'Im Warenkorb' : 'Vormerken' }}
            </button>

            <button v-if="isInCart(fahrzeug.id)" @click="router.push('/warenkorb')"
              class="w-full border border-[#1a2e5a] text-[#1a2e5a] hover:bg-[#1a2e5a] hover:text-white font-bold py-3.5 rounded-lg text-sm transition-colors mb-5">
              Zum Warenkorb
            </button>

            <div class="border-t border-[#1a2e5a]/8 pt-5 space-y-2">
              <a href="tel:+499211234567"
                class="flex items-center gap-2 bg-[#1a2e5a]/6 hover:bg-[#1a2e5a]/12 text-[#1a2e5a] font-semibold text-sm px-4 py-3 rounded-lg transition-colors w-full justify-center">
                <Phone :size="14" /> 0921 123 456
              </a>
              <!-- Anfrage-Button: öffnet Modal -->
              <button @click="anfrageOffen = true"
                class="flex items-center gap-2 border border-[#e85c1a] text-[#e85c1a] hover:bg-[#e85c1a] hover:text-white font-semibold text-sm px-4 py-3 rounded-lg transition-colors w-full justify-center">
                <MessageSquare :size="14" /> Fahrzeug anfragen
              </button>
            </div>
          </div>
        </div>

      </div>
    </div>
  </main>

  <AppFooter />

  <!-- Anfrage-Modal -->
  <div v-if="anfrageOffen" class="fixed inset-0 z-[200] flex items-center justify-center p-4 bg-black/40" @click.self="anfrageOffen = false">
    <div class="bg-white rounded-xl shadow-2xl max-w-md w-full p-6">
      <h2 class="text-[#1a2e5a] font-bold text-lg mb-1">Fahrzeug anfragen</h2>
      <p class="text-[#8e9aaa] text-sm mb-5">{{ fahrzeug?.marke }} {{ fahrzeug?.modell }}</p>

      <div v-if="anfrageErfolg" class="bg-green-50 border border-green-200 text-green-800 text-sm px-4 py-3 rounded-lg">
        ✓ Ihre Anfrage wurde gesendet. Wir melden uns bald bei Ihnen!
      </div>
      <template v-else>
        <div v-if="!isLoggedIn" class="bg-yellow-50 border border-yellow-200 text-yellow-800 text-sm px-4 py-3 rounded-lg mb-4">
          Bitte melden Sie sich an, um eine Anfrage zu stellen.
          <button @click="router.push('/login')" class="underline font-bold ml-1">Zum Login</button>
        </div>
        <template v-else>
          <textarea v-model="anfrageText" rows="4" placeholder="Ihre Nachricht zum Fahrzeug…"
            class="w-full px-3 py-2.5 border border-[#1a2e5a]/15 rounded-lg text-sm text-[#1a2e5a] focus:outline-none resize-none mb-4" />
          <div class="flex gap-3">
            <button @click="anfrageAbschicken" :disabled="anfrageLoading || !anfrageText.trim()"
              class="flex-1 bg-[#e85c1a] hover:bg-[#d44e12] disabled:opacity-60 text-white font-bold py-3 rounded-lg text-sm transition-colors">
              {{ anfrageLoading ? 'Wird gesendet…' : 'Anfrage senden' }}
            </button>
            <button @click="anfrageOffen = false" class="border border-[#1a2e5a]/20 text-[#1a2e5a] font-semibold px-4 py-3 rounded-lg text-sm hover:bg-[#1a2e5a]/5 transition-colors">
              Abbrechen
            </button>
          </div>
        </template>
      </template>
    </div>
  </div>
</template>
