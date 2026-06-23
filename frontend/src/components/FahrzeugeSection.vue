<script setup lang="ts">
import { ref, computed } from 'vue'
import FahrzeugKarte from './FahrzeugKarte.vue'
import FilterBar     from './FilterBar.vue'

// ── Fahrzeug-Typ ──────────────────────────────────────────────────────
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

// ── Fahrzeugdaten ─────────────────────────────────────────────────────
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

// ── Props & Emits ─────────────────────────────────────────────────────
const props = defineProps<{ cart: number[] }>()
const emit  = defineEmits<{ toggleCart: [fahrzeug: Fahrzeug] }>()

// ── Filter-State ──────────────────────────────────────────────────────
const markeFilter      = ref('Alle Marken')
const kraftstoffFilter = ref('Alle')
const maxPreis         = ref(100000)

// ── Computed ──────────────────────────────────────────────────────────
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

function resetFilters() {
  markeFilter.value      = 'Alle Marken'
  kraftstoffFilter.value = 'Alle'
  maxPreis.value         = 100000
}
</script>

<template>
  <section id="fahrzeuge" class="py-16 bg-background">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

      <div class="mb-8">
        <h2 class="text-[#0F2044] text-3xl font-bold mb-1">Unsere Fahrzeuge</h2>
        <p class="text-[#6B7585] text-sm">
          {{ filteredFahrzeuge.length }} von {{ FAHRZEUGE.length }} Fahrzeugen angezeigt
        </p>
      </div>

      <FilterBar
        v-model:marke="markeFilter"
        v-model:kraftstoff="kraftstoffFilter"
        v-model:maxPreis="maxPreis"
        :hasActiveFilters="hasActiveFilters"
        @reset="resetFilters"
      />

      <div v-if="filteredFahrzeuge.length === 0" class="text-center py-24">
        <p class="text-[#0F2044] font-bold text-xl mb-2">Keine Fahrzeuge gefunden.</p>
        <p class="text-[#6B7585] text-sm">Bitte passen Sie Ihre Filtereinstellungen an.</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <FahrzeugKarte
          v-for="fahrzeug in filteredFahrzeuge"
          :key="fahrzeug.id"
          :fahrzeug="fahrzeug"
          :inCart="cart.includes(fahrzeug.id)"
          @toggleCart="emit('toggleCart', $event)"
        />
      </div>

    </div>
  </section>
</template>
