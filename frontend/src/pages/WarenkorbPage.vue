<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  ShoppingCart, Trash2, Check, ArrowRight, ArrowLeft,
  User, MapPin, Calendar, Phone, FileText, AlertCircle,
  CheckCircle2, Car, Lock,
} from 'lucide-vue-next'
import NavBar    from '../components/NavBar.vue'
import AppFooter from '../components/AppFooter.vue'
import { useCart }         from '../composables/useCart'
import { useAuth }         from '../composables/useAuth'
import { apiFetch }        from '../services/api'
import { formatKm, formatPreis } from '../data/fahrzeuge'

const router = useRouter()
const { cartItems, cartTotal, cartTotalFormatted, remove, clear } = useCart()
const { isLoggedIn } = useAuth()

const scrolled = ref(false)
const onScroll = () => { scrolled.value = window.scrollY > 24 }
onMounted(()  => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))

const step = ref<1 | 2 | 3>(1)

const STEPS = [
  { nr: 1, label: 'Warenkorb' },
  { nr: 2, label: 'Ihre Daten' },
  { nr: 3, label: 'Bestätigung' },
]

const form = ref({
  vorname:    '',
  nachname:   '',
  email:      '',
  telefon:    '',
  strasse:    '',
  hausnr:     '',
  plz:        '',
  ort:        '',
  abholDatum: '',
  anmerkung:  '',
  datenschutz: false,
})

const formErrors     = ref<Record<string, string>>({})
const bestellnummer  = ref('')
const submitLoading  = ref(false)
const apiError       = ref('')

const minDatum = computed(() => {
  const d = new Date()
  let added = 0
  while (added < 3) {
    d.setDate(d.getDate() + 1)
    const day = d.getDay()
    if (day !== 0 && day !== 6) added++
  }
  return d.toISOString().split('T')[0]
})

const mwstBetrag = computed(() => Math.round(cartTotal.value - cartTotal.value / 1.19))
const nettoPreis = computed(() => cartTotal.value - mwstBetrag.value)

function isValidEmail(e: string) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e) }
function isValidPlz(plz: string) { return /^\d{5}$/.test(plz) }

function validateForm(): boolean {
  const errors: Record<string, string> = {}
  const f = form.value

  if (!f.vorname.trim())   errors.vorname    = 'Vorname ist erforderlich.'
  if (!f.nachname.trim())  errors.nachname   = 'Nachname ist erforderlich.'
  if (!f.email.trim())     errors.email      = 'E-Mail ist erforderlich.'
  else if (!isValidEmail(f.email)) errors.email = 'Bitte gültige E-Mail-Adresse eingeben.'
  if (!f.strasse.trim())   errors.strasse    = 'Straße ist erforderlich.'
  if (!f.hausnr.trim())    errors.hausnr     = 'Hausnummer ist erforderlich.'
  if (!f.plz.trim())       errors.plz        = 'PLZ ist erforderlich.'
  else if (!isValidPlz(f.plz)) errors.plz   = 'PLZ muss 5-stellig sein.'
  if (!f.ort.trim())       errors.ort        = 'Ort ist erforderlich.'
  if (!f.abholDatum)       errors.abholDatum = 'Bitte Abholdatum angeben.'
  if (!f.datenschutz)      errors.datenschutz = 'Bitte stimmen Sie der Datenschutzerklärung zu.'

  formErrors.value = errors
  return Object.keys(errors).length === 0
}

function goToStep2() {
  if (cartItems.value.length === 0) return
  step.value = 2
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

async function submitOrder() {
  if (!validateForm()) return

  if (!isLoggedIn.value) {
    apiError.value = 'Sie müssen angemeldet sein, um eine Anfrage zu stellen.'
    return
  }

  submitLoading.value = true
  apiError.value      = ''

  try {
    // POST /api/sales/checkout/ → Backend legt Sale-Einträge an
    // und gibt order_number zurück. Alle Fahrzeuge werden auf "reserved" gesetzt.
    const result = await apiFetch<{ order_number: string }>('/api/sales/checkout/', {
      method: 'POST',
      body: JSON.stringify({
        vehicle_ids: cartItems.value.map(f => f.id),
        phone: form.value.telefon || '',
      }),
    })

    bestellnummer.value = result.order_number
    step.value = 3
    clear()
    window.scrollTo({ top: 0, behavior: 'smooth' })

  } catch (e: unknown) {
    apiError.value = e instanceof Error ? e.message : 'Fehler beim Senden der Anfrage.'
  } finally {
    submitLoading.value = false
  }
}

const inputCls = (err: boolean) => [
  'w-full px-3.5 py-3 border rounded-lg text-sm text-[#1a2e5a] placeholder-[#8e9aaa]/60',
  'focus:outline-none focus:ring-2 focus:ring-[#1a2e5a]/20 transition-colors bg-white',
  err ? 'border-red-400 bg-red-50' : 'border-[#1a2e5a]/15',
].join(' ')
</script>

<template>
  <NavBar :scrolled="scrolled" />

  <main class="pt-16 min-h-screen bg-background">

    <div class="bg-white border-b border-[#1a2e5a]/8">
      <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <nav class="flex items-center gap-2 text-xs text-[#8e9aaa] font-medium mb-4 tracking-wide">
          <button @click="router.push('/')" class="hover:text-[#e85c1a] transition-colors">Startseite</button>
          <span class="text-[#8e9aaa]/50">/</span>
          <span class="text-[#1a2e5a] font-semibold">Warenkorb</span>
        </nav>
        <h1 class="text-[#1a2e5a] font-bold text-2xl">Ihr Warenkorb</h1>
      </div>
    </div>

    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

      <!-- Schritt-Indikator -->
      <div class="flex items-center gap-0 mb-10">
        <template v-for="(s, idx) in STEPS" :key="s.nr">
          <div class="flex items-center gap-2">
            <div :class="[
              'w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition-colors',
              step === s.nr ? 'bg-[#e85c1a] text-white'
              : step > s.nr ? 'bg-[#1a2e5a] text-white'
              : 'bg-[#1a2e5a]/10 text-[#8e9aaa]',
            ]">
              <Check v-if="step > s.nr" :size="14" />
              <span v-else>{{ s.nr }}</span>
            </div>
            <span :class="['text-sm font-semibold hidden sm:block', step === s.nr ? 'text-[#1a2e5a]' : 'text-[#8e9aaa]']">
              {{ s.label }}
            </span>
          </div>
          <div v-if="idx < STEPS.length - 1" :class="['flex-1 h-px mx-4', step > s.nr ? 'bg-[#1a2e5a]' : 'bg-[#1a2e5a]/12']" />
        </template>
      </div>

      <!-- SCHRITT 1: Warenkorb-Übersicht -->
      <div v-if="step === 1">
        <div v-if="cartItems.length === 0" class="text-center py-24">
          <div class="w-20 h-20 bg-[#1a2e5a]/6 rounded-full flex items-center justify-center mx-auto mb-6">
            <ShoppingCart :size="36" class="text-[#1a2e5a]/30" />
          </div>
          <h2 class="text-[#1a2e5a] font-bold text-xl mb-3">Ihr Warenkorb ist leer</h2>
          <p class="text-[#8e9aaa] text-sm mb-8">Sie haben noch keine Fahrzeuge vorgemerkt.</p>
          <button @click="router.push('/#fahrzeuge')"
            class="inline-flex items-center gap-2 bg-[#e85c1a] hover:bg-[#d44e12] text-white font-bold px-8 py-4 rounded transition-colors">
            <Car :size="16" /> Fahrzeuge entdecken
          </button>
        </div>

        <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div class="lg:col-span-2 space-y-4">
            <div v-for="f in cartItems" :key="f.id"
              class="bg-white rounded-xl border border-[#1a2e5a]/8 overflow-hidden shadow-sm flex gap-0">
              <div class="w-28 sm:w-40 shrink-0 bg-[#e2e8f0] cursor-pointer" @click="router.push(`/fahrzeug/${f.id}`)">
                <img :src="f.bild" :alt="`${f.marke} ${f.modell}`" class="w-full h-full object-cover" />
              </div>
              <div class="flex-1 p-4 flex flex-col justify-between">
                <div>
                  <div class="text-[#8e9aaa] text-xs font-bold uppercase tracking-wide mb-0.5">{{ f.marke }}</div>
                  <h3 @click="router.push(`/fahrzeug/${f.id}`)"
                    class="text-[#1a2e5a] font-bold text-base mb-1 cursor-pointer hover:text-[#e85c1a] transition-colors">
                    {{ f.modell }}
                  </h3>
                  <p class="text-[#8e9aaa] text-xs">{{ f.baujahr }} · {{ formatKm(f.km) }} · {{ f.kraftstoff }}</p>
                </div>
                <div class="flex items-center justify-between mt-3">
                  <span class="text-[#1a2e5a] font-bold text-xl">{{ formatPreis(f.preis) }}</span>
                  <button @click="remove(f.id)"
                    class="flex items-center gap-1.5 text-xs text-[#8e9aaa] hover:text-[#e85c1a] transition-colors">
                    <Trash2 :size="13" /> Entfernen
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl border border-[#1a2e5a]/8 p-6 shadow-sm self-start sticky top-20">
            <h2 class="text-[#1a2e5a] font-bold text-base mb-5">Zusammenfassung</h2>
            <div class="space-y-3 mb-4">
              <div v-for="f in cartItems" :key="f.id" class="flex justify-between text-sm">
                <span class="text-[#8e9aaa] truncate mr-2">{{ f.modell }}</span>
                <span class="text-[#1a2e5a] font-semibold shrink-0">{{ formatPreis(f.preis) }}</span>
              </div>
            </div>
            <div class="border-t border-[#1a2e5a]/8 pt-4 space-y-2 mb-5">
              <div class="flex justify-between text-sm">
                <span class="text-[#8e9aaa]">Nettobetrag</span>
                <span class="text-[#1a2e5a]">{{ formatPreis(nettoPreis) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-[#8e9aaa]">MwSt. (19 %)</span>
                <span class="text-[#1a2e5a]">{{ formatPreis(mwstBetrag) }}</span>
              </div>
            </div>
            <div class="flex justify-between items-baseline border-t border-[#1a2e5a]/8 pt-4 mb-6">
              <span class="text-[#1a2e5a] font-bold">Gesamt (brutto)</span>
              <span class="text-[#1a2e5a] font-bold text-2xl">{{ cartTotalFormatted }}</span>
            </div>

            <!-- Login-Hinweis wenn nicht eingeloggt -->
            <div v-if="!isLoggedIn" class="bg-yellow-50 border border-yellow-200 rounded-lg px-4 py-3 mb-4 flex gap-2.5">
              <Lock :size="14" class="text-yellow-600 shrink-0 mt-0.5" />
              <p class="text-yellow-800 text-xs">
                Für die Anfrage ist ein Konto erforderlich.
                <button @click="router.push('/login?redirect=/warenkorb')"
                  class="underline font-bold ml-1">Jetzt anmelden</button>
              </p>
            </div>

            <button @click="goToStep2"
              class="w-full bg-[#e85c1a] hover:bg-[#d44e12] text-white font-bold py-3.5 rounded-lg text-sm flex items-center justify-center gap-2 transition-colors">
              Weiter <ArrowRight :size="15" />
            </button>
            <button @click="router.push('/#fahrzeuge')"
              class="w-full mt-3 text-sm text-[#8e9aaa] hover:text-[#1a2e5a] py-2 transition-colors">
              Weitere Fahrzeuge ansehen
            </button>
          </div>
        </div>
      </div>

      <!-- SCHRITT 2: Kundendaten-Formular -->
      <div v-else-if="step === 2">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div class="lg:col-span-2 space-y-5">

            <!-- API-Fehler -->
            <div v-if="apiError" class="bg-red-50 border border-red-200 rounded-xl px-5 py-4 flex gap-3">
              <AlertCircle :size="18" class="text-red-600 shrink-0" />
              <div>
                <p class="text-red-800 font-bold text-sm">Fehler</p>
                <p class="text-red-700 text-xs mt-1">{{ apiError }}</p>
                <button v-if="!isLoggedIn" @click="router.push('/login?redirect=/warenkorb')"
                  class="text-[#e85c1a] text-xs font-bold underline mt-2 block">Jetzt anmelden →</button>
              </div>
            </div>

            <!-- Persönliche Daten -->
            <div class="bg-white rounded-xl border border-[#1a2e5a]/8 p-6 shadow-sm">
              <div class="flex items-center gap-2.5 mb-5">
                <div class="w-8 h-8 bg-[#1a2e5a] rounded flex items-center justify-center shrink-0">
                  <User :size="14" class="text-white" />
                </div>
                <h2 class="text-[#1a2e5a] font-bold text-base">Persönliche Daten</h2>
              </div>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-[#1a2e5a] text-xs font-bold uppercase tracking-wider mb-1.5">Vorname *</label>
                  <input v-model="form.vorname" type="text" placeholder="Max" :class="inputCls(!!formErrors.vorname)" />
                  <p v-if="formErrors.vorname" class="text-red-600 text-xs mt-1">{{ formErrors.vorname }}</p>
                </div>
                <div>
                  <label class="block text-[#1a2e5a] text-xs font-bold uppercase tracking-wider mb-1.5">Nachname *</label>
                  <input v-model="form.nachname" type="text" placeholder="Mustermann" :class="inputCls(!!formErrors.nachname)" />
                  <p v-if="formErrors.nachname" class="text-red-600 text-xs mt-1">{{ formErrors.nachname }}</p>
                </div>
                <div>
                  <label class="block text-[#1a2e5a] text-xs font-bold uppercase tracking-wider mb-1.5">E-Mail *</label>
                  <input v-model="form.email" type="email" placeholder="max@beispiel.de" :class="inputCls(!!formErrors.email)" />
                  <p v-if="formErrors.email" class="text-red-600 text-xs mt-1">{{ formErrors.email }}</p>
                </div>
                <div>
                  <label class="block text-[#1a2e5a] text-xs font-bold uppercase tracking-wider mb-1.5">
                    Telefon <span class="font-normal text-[#8e9aaa] normal-case tracking-normal">(optional)</span>
                  </label>
                  <input v-model="form.telefon" type="tel" placeholder="+49 89 ..."
                    class="w-full px-3.5 py-3 border border-[#1a2e5a]/15 rounded-lg text-sm text-[#1a2e5a] placeholder-[#8e9aaa]/60 focus:outline-none focus:ring-2 focus:ring-[#1a2e5a]/20 transition-colors bg-white" />
                </div>
              </div>
            </div>

            <!-- Rechnungsadresse -->
            <div class="bg-white rounded-xl border border-[#1a2e5a]/8 p-6 shadow-sm">
              <div class="flex items-center gap-2.5 mb-5">
                <div class="w-8 h-8 bg-[#1a2e5a] rounded flex items-center justify-center shrink-0">
                  <MapPin :size="14" class="text-white" />
                </div>
                <h2 class="text-[#1a2e5a] font-bold text-base">Rechnungsadresse</h2>
              </div>
              <div class="grid grid-cols-1 sm:grid-cols-4 gap-4">
                <div class="sm:col-span-3">
                  <label class="block text-[#1a2e5a] text-xs font-bold uppercase tracking-wider mb-1.5">Straße *</label>
                  <input v-model="form.strasse" type="text" placeholder="Musterstraße" :class="inputCls(!!formErrors.strasse)" />
                  <p v-if="formErrors.strasse" class="text-red-600 text-xs mt-1">{{ formErrors.strasse }}</p>
                </div>
                <div>
                  <label class="block text-[#1a2e5a] text-xs font-bold uppercase tracking-wider mb-1.5">Nr. *</label>
                  <input v-model="form.hausnr" type="text" placeholder="12a" :class="inputCls(!!formErrors.hausnr)" />
                  <p v-if="formErrors.hausnr" class="text-red-600 text-xs mt-1">{{ formErrors.hausnr }}</p>
                </div>
                <div>
                  <label class="block text-[#1a2e5a] text-xs font-bold uppercase tracking-wider mb-1.5">PLZ *</label>
                  <input v-model="form.plz" type="text" placeholder="95444" maxlength="5" :class="inputCls(!!formErrors.plz)" />
                  <p v-if="formErrors.plz" class="text-red-600 text-xs mt-1">{{ formErrors.plz }}</p>
                </div>
                <div class="sm:col-span-3">
                  <label class="block text-[#1a2e5a] text-xs font-bold uppercase tracking-wider mb-1.5">Ort *</label>
                  <input v-model="form.ort" type="text" placeholder="Bayreuth" :class="inputCls(!!formErrors.ort)" />
                  <p v-if="formErrors.ort" class="text-red-600 text-xs mt-1">{{ formErrors.ort }}</p>
                </div>
              </div>
            </div>

            <!-- Abholdatum -->
            <div class="bg-white rounded-xl border border-[#1a2e5a]/8 p-6 shadow-sm">
              <div class="flex items-center gap-2.5 mb-5">
                <div class="w-8 h-8 bg-[#1a2e5a] rounded flex items-center justify-center shrink-0">
                  <Calendar :size="14" class="text-white" />
                </div>
                <div>
                  <h2 class="text-[#1a2e5a] font-bold text-base">Gewünschtes Abholdatum</h2>
                  <p class="text-[#8e9aaa] text-xs mt-0.5">Frühestes Datum: 3 Werktage ab heute</p>
                </div>
              </div>
              <div>
                <label class="block text-[#1a2e5a] text-xs font-bold uppercase tracking-wider mb-1.5">Abholdatum *</label>
                <input v-model="form.abholDatum" type="date" :min="minDatum" :class="inputCls(!!formErrors.abholDatum)" />
                <p v-if="formErrors.abholDatum" class="text-red-600 text-xs mt-1">{{ formErrors.abholDatum }}</p>
              </div>
            </div>

            <!-- Anmerkungen -->
            <div class="bg-white rounded-xl border border-[#1a2e5a]/8 p-6 shadow-sm">
              <div class="flex items-center gap-2.5 mb-5">
                <div class="w-8 h-8 bg-[#1a2e5a] rounded flex items-center justify-center shrink-0">
                  <FileText :size="14" class="text-white" />
                </div>
                <h2 class="text-[#1a2e5a] font-bold text-base">Anmerkungen <span class="font-normal text-[#8e9aaa] text-sm">(optional)</span></h2>
              </div>
              <textarea v-model="form.anmerkung" rows="3" placeholder="Besondere Wünsche, Fragen oder Hinweise ..."
                class="w-full px-3.5 py-3 border border-[#1a2e5a]/15 rounded-lg text-sm text-[#1a2e5a] placeholder-[#8e9aaa]/60 focus:outline-none focus:ring-2 focus:ring-[#1a2e5a]/20 transition-colors bg-white resize-none" />
            </div>

            <!-- Datenschutz -->
            <div :class="['bg-white rounded-xl border p-5 shadow-sm', formErrors.datenschutz ? 'border-red-300' : 'border-[#1a2e5a]/8']">
              <label class="flex items-start gap-3 cursor-pointer">
                <input v-model="form.datenschutz" type="checkbox" class="w-4 h-4 accent-[#e85c1a] mt-0.5 cursor-pointer shrink-0" />
                <span class="text-sm text-[#8e9aaa] leading-relaxed">
                  Ich habe die
                  <a href="/datenschutz" target="_blank" class="text-[#e85c1a] underline">Datenschutzerklärung</a>
                  gelesen und stimme der Verarbeitung meiner Daten zur Abwicklung meiner Anfrage zu. *
                </span>
              </label>
              <p v-if="formErrors.datenschutz" class="text-red-600 text-xs mt-2 ml-7">{{ formErrors.datenschutz }}</p>
            </div>

            <p class="text-[#8e9aaa] text-xs">* Pflichtfelder</p>

            <div class="flex gap-3">
              <button @click="step = 1"
                class="flex items-center gap-2 border border-[#1a2e5a]/20 text-[#1a2e5a] hover:bg-[#1a2e5a]/5 font-semibold px-6 py-3 rounded-lg text-sm transition-colors">
                <ArrowLeft :size="14" /> Zurück
              </button>
              <button @click="submitOrder" :disabled="submitLoading"
                class="flex-1 flex items-center justify-center gap-2 bg-[#e85c1a] hover:bg-[#d44e12] disabled:opacity-60 text-white font-bold py-3.5 rounded-lg text-sm transition-colors">
                {{ submitLoading ? 'Wird gesendet…' : 'Anfrage absenden' }}
                <ArrowRight v-if="!submitLoading" :size="15" />
              </button>
            </div>

          </div>

          <!-- Rechte Spalte -->
          <div class="bg-white rounded-xl border border-[#1a2e5a]/8 p-6 shadow-sm self-start sticky top-20">
            <h3 class="text-[#1a2e5a] font-bold text-sm mb-4">Ihre Anfrage</h3>
            <div class="space-y-3 mb-4">
              <div v-for="f in cartItems" :key="f.id" class="flex gap-3">
                <img :src="f.bild" :alt="f.modell" class="w-14 h-10 object-cover rounded" />
                <div>
                  <div class="text-[#1a2e5a] font-semibold text-xs">{{ f.marke }} {{ f.modell }}</div>
                  <div class="text-[#8e9aaa] text-xs">{{ formatPreis(f.preis) }}</div>
                </div>
              </div>
            </div>
            <div class="border-t border-[#1a2e5a]/8 pt-4 flex justify-between">
              <span class="text-[#1a2e5a] font-bold text-sm">Gesamt</span>
              <span class="text-[#1a2e5a] font-bold text-sm">{{ cartTotalFormatted }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- SCHRITT 3: Bestätigung -->
      <div v-else-if="step === 3">
        <div class="max-w-2xl mx-auto text-center">
          <div class="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <CheckCircle2 :size="40" class="text-green-600" />
          </div>
          <h2 class="text-[#1a2e5a] font-bold text-2xl mb-2">Anfrage erfolgreich gesendet!</h2>
          <p class="text-[#8e9aaa] text-base mb-2">Ihre Bestellnummer:</p>
          <div class="bg-[#1a2e5a] text-white font-bold text-xl px-6 py-3 rounded-lg inline-block mb-8">
            {{ bestellnummer }}
          </div>

          <div class="bg-white border border-[#1a2e5a]/8 rounded-xl p-6 shadow-sm text-left mb-6">
            <h3 class="text-[#1a2e5a] font-bold text-base mb-4 flex items-center gap-2">
              <Phone :size="16" class="text-[#e85c1a]" /> Was passiert als nächstes?
            </h3>
            <ol class="space-y-3 mb-6">
              <li class="flex gap-3 text-sm text-[#8e9aaa]">
                <span class="w-6 h-6 bg-[#e85c1a]/12 text-[#e85c1a] font-bold rounded-full flex items-center justify-center shrink-0 text-xs">1</span>
                Wir bestätigen Ihre Anfrage per E-Mail innerhalb von 1–2 Werktagen.
              </li>
              <li class="flex gap-3 text-sm text-[#8e9aaa]">
                <span class="w-6 h-6 bg-[#e85c1a]/12 text-[#e85c1a] font-bold rounded-full flex items-center justify-center shrink-0 text-xs">2</span>
                Unser Team kontaktiert Sie zur finalen Abstimmung des Abholtermins.
              </li>
              <li class="flex gap-3 text-sm text-[#8e9aaa]">
                <span class="w-6 h-6 bg-[#e85c1a]/12 text-[#e85c1a] font-bold rounded-full flex items-center justify-center shrink-0 text-xs">3</span>
                Das Fahrzeug wird für Sie reserviert und zur Abholung vorbereitet.
              </li>
            </ol>
            <div class="bg-[#f8f9fa] rounded-lg p-5">
              <h4 class="text-[#1a2e5a] font-bold text-sm mb-3 flex items-center gap-2">
                <MapPin :size="14" class="text-[#e85c1a]" /> Abholadresse
              </h4>
              <p class="text-[#8e9aaa] text-sm leading-relaxed">
                AutoHaus Müller GmbH<br />
                Amselstraße 1B<br />
                95444 Bayreuth<br /><br />
                <strong class="text-[#1a2e5a]">Öffnungszeiten:</strong><br />
                Mo – Fr: 09:00 – 18:30 Uhr<br />
                Samstag: 10:00 – 16:00 Uhr<br />
                Sonntag: Geschlossen
              </p>
              <a href="tel:+499211234567" class="flex items-center gap-2 mt-4 text-sm font-semibold text-[#e85c1a] hover:underline">
                <Phone :size="13" /> 0921 123 456
              </a>
            </div>
          </div>

          <button @click="router.push('/')"
            class="bg-[#e85c1a] hover:bg-[#d44e12] text-white font-bold px-8 py-4 rounded-lg transition-colors">
            Zurück zur Startseite
          </button>
        </div>
      </div>

    </div>
  </main>

  <AppFooter />
</template>
