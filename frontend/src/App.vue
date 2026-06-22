<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import {
  Phone, MapPin, Clock, ShoppingCart, Info, Menu, X,
  Check, ChevronDown, Fuel, Calendar, Gauge,
} from 'lucide-vue-next'

// ── Typen ────────────────────────────────────────────────────────────
interface Fahrzeug {
  id: number
  marke: string
  modell: string
  baujahr: number
  km: number
  kraftstoff: string
  preis: number
  bild: string
}

// ── Daten ────────────────────────────────────────────────────────────
const FAHRZEUGE: Fahrzeug[] = [
  {
    id: 1,
    marke: 'BMW',
    modell: '3er Touring 320d',
    baujahr: 2021,
    km: 48200,
    kraftstoff: 'Diesel',
    preis: 32900,
    bild: 'https://images.unsplash.com/photo-1569021476330-3545605d7062?w=800&h=500&fit=crop&auto=format',
  },
  {
    id: 2,
    marke: 'Volkswagen',
    modell: 'Golf 8 GTI',
    baujahr: 2022,
    km: 21500,
    kraftstoff: 'Benzin',
    preis: 38500,
    bild: 'https://images.unsplash.com/photo-1565786089437-496904c48734?w=800&h=500&fit=crop&auto=format',
  },
  {
    id: 3,
    marke: 'Volkswagen',
    modell: 'Passat Variant 2.0 TDI',
    baujahr: 2020,
    km: 67800,
    kraftstoff: 'Diesel',
    preis: 24900,
    bild: 'https://images.unsplash.com/photo-1572811298797-9eecadf6cb24?w=800&h=500&fit=crop&auto=format',
  },
  {
    id: 4,
    marke: 'Mercedes-Benz',
    modell: 'C 220 d Avantgarde',
    baujahr: 2021,
    km: 39100,
    kraftstoff: 'Diesel',
    preis: 41200,
    bild: 'https://images.unsplash.com/photo-1624085568108-36410cfe4d24?w=800&h=500&fit=crop&auto=format',
  },
  {
    id: 5,
    marke: 'BMW',
    modell: 'X3 xDrive20d M Sport',
    baujahr: 2022,
    km: 29400,
    kraftstoff: 'Diesel',
    preis: 47800,
    bild: 'https://images.unsplash.com/photo-1691111375360-81227c67d093?w=800&h=500&fit=crop&auto=format',
  },
  {
    id: 6,
    marke: 'Audi',
    modell: 'A4 Avant 35 TDI',
    baujahr: 2020,
    km: 55600,
    kraftstoff: 'Diesel',
    preis: 28900,
    bild: 'https://images.unsplash.com/photo-1585390062628-be8608aa7d83?w=800&h=500&fit=crop&auto=format',
  },
]

const MARKEN = ['Alle Marken', 'Audi', 'BMW', 'Mercedes-Benz', 'Volkswagen']
const KRAFTSTOFFE = ['Alle', 'Benzin', 'Diesel', 'Elektro', 'Hybrid']
const MAX_PREISE = [
  { label: 'Alle Preise', value: 100000 },
  { label: 'bis 25.000 €', value: 25000 },
  { label: 'bis 30.000 €', value: 30000 },
  { label: 'bis 40.000 €', value: 40000 },
  { label: 'bis 50.000 €', value: 50000 },
]

const NAV_LINKS: [string, string][] = [
  ['fahrzeuge', 'Fahrzeuge'],
  ['ueber-uns', 'Über uns'],
  ['kontakt', 'Kontakt'],
]

const STATS: [string, string][] = [
  ['80+', 'Fahrzeuge im Bestand'],
  ['15 J.', 'Erfahrung'],
  ['4,9 ★', 'Kundenbewertung'],
]

const OEFFNUNGSZEITEN: [string, string][] = [
  ['Mo – Fr', '09:00 – 18:30'],
  ['Samstag', '10:00 – 16:00'],
  ['Sonntag', 'Geschlossen'],
]

const UEBER_UNS_PUNKTE = [
  'TÜV-geprüfte Fahrzeuge',
  'Finanzierungsberatung vor Ort',
  'Inzahlungnahme Ihres Altfahrzeugs',
  '12 Monate Gebrauchtwagengarantie',
]

// ── Hilfsfunktionen ──────────────────────────────────────────────────
function formatKm(km: number): string {
  return km.toLocaleString('de-DE') + ' km'
}

function formatPreis(preis: number): string {
  return preis.toLocaleString('de-DE') + ' €'
}

// ── State (reaktiv) ──────────────────────────────────────────────────
const mobileMenuOpen = ref(false)
const scrolled       = ref(false)
const cart           = ref<number[]>([])
const markeFilter    = ref('Alle Marken')
const kraftstoffFilter = ref('Alle')
const maxPreis       = ref(100000)
const notification   = ref({ text: '', visible: false })

// ── Computed ─────────────────────────────────────────────────────────
const filteredFahrzeuge = computed(() =>
  FAHRZEUGE.filter((f) => {
    if (markeFilter.value !== 'Alle Marken' && f.marke !== markeFilter.value) return false
    if (kraftstoffFilter.value !== 'Alle' && f.kraftstoff !== kraftstoffFilter.value) return false
    if (f.preis > maxPreis.value) return false
    return true
  })
)

const hasActiveFilters = computed(() =>
  markeFilter.value !== 'Alle Marken' ||
  kraftstoffFilter.value !== 'Alle' ||
  maxPreis.value !== 100000
)

// ── Scroll-Listener ───────────────────────────────────────────────────
const onScroll = () => { scrolled.value = window.scrollY > 24 }
onMounted(() => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))

// ── Methoden ──────────────────────────────────────────────────────────
let notifTimeout: ReturnType<typeof setTimeout> | null = null

function showNotification(text: string) {
  if (notifTimeout) clearTimeout(notifTimeout)
  notification.value = { text, visible: true }
  notifTimeout = setTimeout(() => {
    notification.value = { ...notification.value, visible: false }
  }, 2800)
}

function toggleCart(fahrzeug: Fahrzeug) {
  const inCart = cart.value.includes(fahrzeug.id)
  showNotification(
    inCart
      ? `${fahrzeug.marke} ${fahrzeug.modell} entfernt`
      : `${fahrzeug.marke} ${fahrzeug.modell} zum Warenkorb hinzugefügt`
  )
  cart.value = inCart
    ? cart.value.filter((id) => id !== fahrzeug.id)
    : [...cart.value, fahrzeug.id]
}

function scrollTo(id: string) {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
  mobileMenuOpen.value = false
}

function resetFilters() {
  markeFilter.value    = 'Alle Marken'
  kraftstoffFilter.value = 'Alle'
  maxPreis.value       = 100000
}
</script>

<template>
  <div class="min-h-screen bg-background">

    <!-- ── Toast-Notification ─────────────────────────────────── -->
    <div
      :class="[
        'fixed top-20 right-4 z-50 transition-all duration-300',
        notification.visible
          ? 'opacity-100 translate-y-0'
          : 'opacity-0 -translate-y-2 pointer-events-none',
      ]"
    >
      <div class="bg-[#0F2044] text-white text-sm font-medium px-4 py-3 rounded shadow-xl flex items-center gap-2.5">
        <Check :size="14" class="text-green-400 shrink-0" />
        {{ notification.text }}
      </div>
    </div>

    <!-- ── Navigation ─────────────────────────────────────────── -->
    <nav
      :class="[
        'fixed top-0 inset-x-0 z-40 transition-all duration-200',
        scrolled ? 'bg-white shadow-md' : 'bg-white border-b border-[#0F2044]/8',
      ]"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">

          <!-- Logo -->
          <button @click="scrollTo('hero')" class="flex items-center gap-2.5">
            <div class="w-8 h-8 bg-[#0F2044] rounded flex items-center justify-center shrink-0">
              <span class="text-white font-bold text-xs tracking-tight">AH</span>
            </div>
            <div class="text-left">
              <div class="font-bold text-[#0F2044] text-base leading-none">AutoHaus Müller</div>
              <div class="text-[10px] text-[#6B7585] leading-none mt-0.5 uppercase tracking-wider">Bayreuth</div>
            </div>
          </button>

          <!-- Desktop-Links -->
          <div class="hidden md:flex items-center gap-8">
            <button
              v-for="[id, label] in NAV_LINKS"
              :key="id"
              @click="scrollTo(id)"
              class="text-[#0F2044]/80 hover:text-[#D41C1C] font-semibold text-sm transition-colors"
            >
              {{ label }}
            </button>
          </div>

          <!-- Telefon + Warenkorb -->
          <div class="hidden md:flex items-center gap-5">
            <a
              href="tel:+4989123456789"
              class="flex items-center gap-2 text-[#0F2044] font-semibold text-sm hover:text-[#D41C1C] transition-colors"
            >
              <Phone :size="14" />
              0921 123 456 789
            </a>
            <button
              @click="scrollTo('fahrzeuge')"
              class="relative w-9 h-9 flex items-center justify-center border border-[#0F2044]/20 rounded-full hover:bg-[#0F2044]/5 transition-colors"
              aria-label="Warenkorb"
            >
              <ShoppingCart :size="16" class="text-[#0F2044]" />
              <span
                v-if="cart.length > 0"
                class="absolute -top-1 -right-1 w-4 h-4 bg-[#D41C1C] text-white text-[9px] font-bold rounded-full flex items-center justify-center"
              >
                {{ cart.length }}
              </span>
            </button>
          </div>

          <!-- Mobile-Toggle -->
          <button
            class="md:hidden p-2 text-[#0F2044]"
            @click="mobileMenuOpen = !mobileMenuOpen"
            aria-label="Menü"
          >
            <X v-if="mobileMenuOpen" :size="22" />
            <Menu v-else :size="22" />
          </button>

        </div>
      </div>

      <!-- Mobile-Menü -->
      <div
        v-if="mobileMenuOpen"
        class="md:hidden bg-white border-t border-[#0F2044]/10 px-4 py-4 space-y-1"
      >
        <button
          v-for="[id, label] in NAV_LINKS"
          :key="id"
          @click="scrollTo(id)"
          class="block w-full text-left text-[#0F2044] font-semibold py-2.5 text-sm"
        >
          {{ label }}
        </button>
        <a
          href="tel:+4989123456789"
          class="flex items-center gap-2 text-[#0F2044] font-semibold py-2.5 text-sm"
        >
          <Phone :size="14" />
          0921 123 456 789
        </a>
      </div>
    </nav>

    <!-- ── Hero ───────────────────────────────────────────────── -->
    <section id="hero" class="relative min-h-[90vh] flex items-center overflow-hidden pt-16">
      <div class="absolute inset-0 bg-[#0F2044]">
        <img
          src="https://images.unsplash.com/photo-1692406069831-0bb7ea297645?w=1920&h=1080&fit=crop&auto=format"
          alt="AutoHaus Müller Showroom"
          class="w-full h-full object-cover opacity-20"
        />
        <div class="absolute inset-0 bg-gradient-to-r from-[#0F2044]/95 via-[#0F2044]/70 to-[#0F2044]/30" />
      </div>

      <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 w-full">
        <div class="max-w-2xl">
          <p class="text-[#D41C1C] font-bold text-xs uppercase tracking-[0.2em] mb-5">
            Ihr Autohaus in Bayreuth
          </p>
          <h1
            class="text-white font-bold leading-[1.1] mb-6"
            style="font-size: clamp(2.4rem, 6vw, 4rem)"
          >
            Ihr nächstes<br />
            <span class="text-white/85">Fahrzeug wartet.</span>
          </h1>
          <p class="text-white/65 text-lg leading-relaxed mb-10 max-w-lg">
            Über 80 geprüfte Gebrauchtwagen — transparent bepreist, professionell aufbereitet, sofort verfügbar.
          </p>

          <div class="flex flex-wrap gap-4">
            <button
              @click="scrollTo('fahrzeuge')"
              class="bg-[#D41C1C] hover:bg-[#BB1818] text-white font-bold px-8 py-4 rounded text-base transition-colors"
            >
              Fahrzeuge entdecken
            </button>
            <button
              @click="scrollTo('kontakt')"
              class="border border-white/35 hover:border-white/60 text-white font-semibold px-8 py-4 rounded text-base transition-colors"
            >
              Kontakt aufnehmen
            </button>
          </div>

          <!-- Stats -->
          <div class="mt-14 pt-10 border-t border-white/12 flex gap-10 flex-wrap">
            <div v-for="[val, label] in STATS" :key="label">
              <div class="text-white font-bold text-2xl">{{ val }}</div>
              <div class="text-white/45 text-xs mt-0.5 uppercase tracking-wider">{{ label }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Fahrzeuge ──────────────────────────────────────────── -->
    <section id="fahrzeuge" class="py-16 bg-background">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        <div class="mb-8">
          <h2 class="text-[#0F2044] text-3xl font-bold mb-1">Unsere Fahrzeuge</h2>
          <p class="text-[#6B7585] text-sm">
            {{ filteredFahrzeuge.length }} von {{ FAHRZEUGE.length }} Fahrzeugen angezeigt
          </p>
        </div>

        <!-- Filter-Bar -->
        <div class="bg-white border border-[#0F2044]/10 rounded-lg px-5 py-4 mb-8 shadow-sm">
          <div class="flex flex-wrap gap-x-6 gap-y-3 items-end">

            <!-- Marke -->
            <div class="flex flex-col gap-1.5 flex-1 min-w-[150px]">
              <label class="text-[10px] font-bold text-[#6B7585] uppercase tracking-widest">Marke</label>
              <div class="relative">
                <select
                  v-model="markeFilter"
                  class="w-full appearance-none bg-[#F0F0EC] border border-[#0F2044]/10 rounded px-3 py-2 text-sm text-[#0F2044] font-semibold pr-7 focus:outline-none focus:ring-2 focus:ring-[#0F2044]/20 cursor-pointer"
                >
                  <option v-for="m in MARKEN" :key="m" :value="m">{{ m }}</option>
                </select>
                <ChevronDown :size="13" class="absolute right-2.5 top-1/2 -translate-y-1/2 text-[#0F2044]/40 pointer-events-none" />
              </div>
            </div>

            <!-- Kraftstoff -->
            <div class="flex flex-col gap-1.5 flex-1 min-w-[150px]">
              <label class="text-[10px] font-bold text-[#6B7585] uppercase tracking-widest">Kraftstoff</label>
              <div class="relative">
                <select
                  v-model="kraftstoffFilter"
                  class="w-full appearance-none bg-[#F0F0EC] border border-[#0F2044]/10 rounded px-3 py-2 text-sm text-[#0F2044] font-semibold pr-7 focus:outline-none focus:ring-2 focus:ring-[#0F2044]/20 cursor-pointer"
                >
                  <option v-for="k in KRAFTSTOFFE" :key="k" :value="k">{{ k }}</option>
                </select>
                <ChevronDown :size="13" class="absolute right-2.5 top-1/2 -translate-y-1/2 text-[#0F2044]/40 pointer-events-none" />
              </div>
            </div>

            <!-- Max. Preis -->
            <div class="flex flex-col gap-1.5 flex-1 min-w-[150px]">
              <label class="text-[10px] font-bold text-[#6B7585] uppercase tracking-widest">Max. Preis</label>
              <div class="relative">
                <select
                  v-model.number="maxPreis"
                  class="w-full appearance-none bg-[#F0F0EC] border border-[#0F2044]/10 rounded px-3 py-2 text-sm text-[#0F2044] font-semibold pr-7 focus:outline-none focus:ring-2 focus:ring-[#0F2044]/20 cursor-pointer"
                >
                  <option v-for="p in MAX_PREISE" :key="p.value" :value="p.value">{{ p.label }}</option>
                </select>
                <ChevronDown :size="13" class="absolute right-2.5 top-1/2 -translate-y-1/2 text-[#0F2044]/40 pointer-events-none" />
              </div>
            </div>

            <button
              v-if="hasActiveFilters"
              @click="resetFilters"
              class="text-[#D41C1C] text-sm font-semibold hover:underline whitespace-nowrap self-end pb-2"
            >
              Zurücksetzen
            </button>

          </div>
        </div>

        <!-- Kein Ergebnis -->
        <div v-if="filteredFahrzeuge.length === 0" class="text-center py-24">
          <p class="text-[#0F2044] font-bold text-xl mb-2">Keine Fahrzeuge gefunden.</p>
          <p class="text-[#6B7585] text-sm">Bitte passen Sie Ihre Filtereinstellungen an.</p>
        </div>

        <!-- Fahrzeug-Grid -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <article
            v-for="fahrzeug in filteredFahrzeuge"
            :key="fahrzeug.id"
            class="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200 overflow-hidden border border-[#0F2044]/8 group flex flex-col"
          >
            <!-- Bild -->
            <div class="relative overflow-hidden bg-[#E4E4E0] aspect-[16/10] shrink-0">
              <img
                :src="fahrzeug.bild"
                :alt="`${fahrzeug.marke} ${fahrzeug.modell}`"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              />
              <div class="absolute top-3 left-3">
                <span class="bg-[#0F2044] text-white text-xs font-bold px-2.5 py-1 rounded">
                  {{ fahrzeug.marke }}
                </span>
              </div>
              <div v-if="cart.includes(fahrzeug.id)" class="absolute top-3 right-3">
                <span class="bg-[#D41C1C] text-white text-xs font-bold px-2.5 py-1 rounded flex items-center gap-1">
                  <Check :size="10" />
                  Vorgemerkt
                </span>
              </div>
            </div>

            <!-- Inhalt -->
            <div class="p-5 flex flex-col flex-1">
              <h3 class="text-[#0F2044] font-bold text-lg leading-tight mb-3">
                {{ fahrzeug.modell }}
              </h3>

              <!-- Kennzahlen -->
              <div class="flex items-center gap-4 text-xs text-[#6B7585] mb-4">
                <span class="flex items-center gap-1.5">
                  <Calendar :size="12" class="shrink-0" />
                  {{ fahrzeug.baujahr }}
                </span>
                <span class="w-px h-3 bg-[#0F2044]/12" />
                <span class="flex items-center gap-1.5">
                  <Gauge :size="12" class="shrink-0" />
                  {{ formatKm(fahrzeug.km) }}
                </span>
                <span class="w-px h-3 bg-[#0F2044]/12" />
                <span class="flex items-center gap-1.5">
                  <Fuel :size="12" class="shrink-0" />
                  {{ fahrzeug.kraftstoff }}
                </span>
              </div>

              <!-- Preis -->
              <div class="flex items-baseline gap-1.5 mb-5 mt-auto">
                <span class="text-[#0F2044] font-bold text-2xl">{{ formatPreis(fahrzeug.preis) }}</span>
                <span class="text-[#6B7585] text-sm">brutto</span>
              </div>

              <!-- Aktionen -->
              <div class="flex gap-2">
                <button class="flex-1 flex items-center justify-center gap-1.5 border border-[#0F2044] text-[#0F2044] hover:bg-[#0F2044] hover:text-white text-sm font-semibold py-2.5 rounded transition-colors">
                  <Info :size="14" />
                  Details
                </button>
                <button
                  @click="toggleCart(fahrzeug)"
                  :class="[
                    'flex-1 flex items-center justify-center gap-1.5 text-sm font-semibold py-2.5 rounded transition-colors',
                    cart.includes(fahrzeug.id)
                      ? 'bg-[#0F2044] text-white hover:bg-[#0F2044]/85'
                      : 'bg-[#D41C1C] hover:bg-[#BB1818] text-white',
                  ]"
                >
                  <Check v-if="cart.includes(fahrzeug.id)" :size="14" />
                  <ShoppingCart v-else :size="14" />
                  {{ cart.includes(fahrzeug.id) ? 'Im Warenkorb' : 'In den Warenkorb' }}
                </button>
              </div>
            </div>
          </article>
        </div>

      </div>
    </section>

    <!-- ── Über uns ───────────────────────────────────────────── -->
    <section id="ueber-uns" class="py-16 bg-[#0F2044]">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">

          <div>
            <p class="text-[#D41C1C] font-bold text-xs uppercase tracking-[0.2em] mb-4">Über uns</p>
            <h2 class="text-white font-bold text-4xl leading-tight mb-6">
              Seit 2009 Ihr<br />verlässlicher Partner.
            </h2>
            <p class="text-white/65 text-base leading-relaxed mb-8">
              AutoHaus Müller steht seit über 15 Jahren für Seriosität, Transparenz und erstklassigen Service im Fahrzeughandel. Ob gepflegter Jahreswagen oder Familienauto — wir begleiten Sie vom ersten Gespräch bis zur Übergabe.
            </p>
            <ul class="space-y-3.5">
              <li
                v-for="item in UEBER_UNS_PUNKTE"
                :key="item"
                class="flex items-center gap-3 text-white/75 text-sm"
              >
                <span class="w-5 h-5 border border-[#D41C1C]/50 bg-[#D41C1C]/15 rounded-full flex items-center justify-center shrink-0">
                  <Check :size="10" class="text-[#D41C1C]" />
                </span>
                {{ item }}
              </li>
            </ul>
          </div>

          <div class="relative rounded-lg overflow-hidden aspect-[4/3] bg-[#0A1836]">
            <img
              src="https://images.unsplash.com/photo-1574023240744-64c47c8c0676?w=900&h=675&fit=crop&auto=format"
              alt="AutoHaus Müller Außenansicht"
              class="w-full h-full object-cover opacity-60"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-[#0F2044]/60 to-transparent" />
          </div>

        </div>
      </div>
    </section>

    <!-- ── Kontakt ────────────────────────────────────────────── -->
    <section id="kontakt" class="py-16 bg-background">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        <div class="mb-10">
          <h2 class="text-[#0F2044] text-3xl font-bold mb-1">Kontakt & Anfahrt</h2>
          <p class="text-[#6B7585] text-sm">Wir freuen uns auf Ihren Besuch — persönlich oder telefonisch.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">

          <!-- Adresse -->
          <div class="bg-white rounded-lg p-6 shadow-sm border border-[#0F2044]/8">
            <div class="w-11 h-11 bg-[#0F2044] rounded flex items-center justify-center mb-5">
              <MapPin :size="18" class="text-white" />
            </div>
            <h3 class="text-[#0F2044] font-bold text-base mb-3">Adresse</h3>
            <p class="text-[#6B7585] text-sm leading-relaxed">
              Amselweg 18<br />
              95445 Bayreuth <br />
              Deutschland
            </p>
          </div>

          <!-- Telefon & E-Mail -->
          <div class="bg-white rounded-lg p-6 shadow-sm border border-[#0F2044]/8">
            <div class="w-11 h-11 bg-[#0F2044] rounded flex items-center justify-center mb-5">
              <Phone :size="18" class="text-white" />
            </div>
            <h3 class="text-[#0F2044] font-bold text-base mb-3">Telefon & E-Mail</h3>
            <p class="text-[#6B7585] text-sm leading-relaxed mb-5">
              <a href="tel:+4989123456789" class="hover:text-[#D41C1C] transition-colors block">
                0921 123 456 789
              </a>
              <a href="mailto:info@autohaus-mueller.de" class="hover:text-[#D41C1C] transition-colors block mt-1">
                info@autohaus-mueller.de
              </a>
            </p>
            <a
              href="tel:+4989123456789"
              class="inline-flex items-center gap-2 bg-[#D41C1C] hover:bg-[#BB1818] text-white text-sm font-bold px-5 py-2.5 rounded transition-colors"
            >
              <Phone :size="13" />
              Jetzt anrufen
            </a>
          </div>

          <!-- Öffnungszeiten -->
          <div class="bg-white rounded-lg p-6 shadow-sm border border-[#0F2044]/8">
            <div class="w-11 h-11 bg-[#0F2044] rounded flex items-center justify-center mb-5">
              <Clock :size="18" class="text-white" />
            </div>
            <h3 class="text-[#0F2044] font-bold text-base mb-3">Öffnungszeiten</h3>
            <table class="w-full text-sm">
              <tbody>
                <tr v-for="[day, time] in OEFFNUNGSZEITEN" :key="day">
                  <td class="font-semibold text-[#0F2044] pr-4 py-1">{{ day }}</td>
                  <td class="text-[#6B7585]">{{ time }}</td>
                </tr>
              </tbody>
            </table>
          </div>

        </div>
      </div>
    </section>

    <!-- ── Footer ─────────────────────────────────────────────── -->
    <footer class="bg-[#07152E] py-8">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col md:flex-row items-center justify-between gap-5">

          <div class="flex items-center gap-2.5">
            <div class="w-7 h-7 bg-white/10 rounded flex items-center justify-center shrink-0">
              <span class="text-white font-bold text-xs">AH</span>
            </div>
            <span class="text-white font-semibold text-sm">AutoHaus Müller GmbH</span>
          </div>

          <p class="text-white/35 text-xs order-last md:order-none">
            © 2026 AutoHaus Müller GmbH · Alle Rechte vorbehalten
          </p>

          <div class="flex items-center gap-6">
            <button
              v-for="link in ['Impressum', 'Datenschutz', 'AGB']"
              :key="link"
              class="text-white/45 hover:text-white/80 text-sm transition-colors"
            >
              {{ link }}
            </button>
          </div>

        </div>
      </div>
    </footer>

  </div>
</template>
