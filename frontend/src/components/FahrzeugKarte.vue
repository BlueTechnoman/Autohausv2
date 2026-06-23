<script setup lang="ts">
import { Check, ShoppingCart, Info, Calendar, Gauge, Fuel } from 'lucide-vue-next'

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

// ── Hilfsfunktionen ───────────────────────────────────────────────────
function formatKm(km: number): string {
  return km.toLocaleString('de-DE') + ' km'
}

function formatPreis(preis: number): string {
  return preis.toLocaleString('de-DE') + ' €'
}

// ── Props & Emits ─────────────────────────────────────────────────────
const props = defineProps<{
  fahrzeug: Fahrzeug
  inCart: boolean
}>()

const emit = defineEmits<{
  toggleCart: [fahrzeug: Fahrzeug]
}>()
</script>

<template>
  <article
    class="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200
           overflow-hidden border border-[#0F2044]/8 group flex flex-col"
  >
    <!-- ── Fahrzeugbild ────────────────────────────────────────────── -->
    <div class="relative overflow-hidden bg-[#E4E4E0] aspect-[16/10] shrink-0">
      <img
        :src="fahrzeug.bild"
        :alt="`${fahrzeug.marke} ${fahrzeug.modell}`"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
      />

      <!-- Marken-Badge (oben links) -->
      <div class="absolute top-3 left-3">
        <span class="bg-[#0F2044] text-white text-xs font-bold px-2.5 py-1 rounded">
          {{ fahrzeug.marke }}
        </span>
      </div>

      <!-- Vorgemerkt-Badge (nur wenn im Warenkorb) -->
      <div v-if="inCart" class="absolute top-3 right-3">
        <span class="bg-[#D41C1C] text-white text-xs font-bold px-2.5 py-1 rounded flex items-center gap-1">
          <Check :size="10" />
          Vorgemerkt
        </span>
      </div>
    </div>

    <!-- ── Karteninhalt ────────────────────────────────────────────── -->
    <div class="p-5 flex flex-col flex-1">

      <h3 class="text-[#0F2044] font-bold text-lg leading-tight mb-3">
        {{ fahrzeug.modell }}
      </h3>

      <!-- Baujahr · km · Kraftstoff -->
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
        <span class="text-[#0F2044] font-bold text-2xl">
          {{ formatPreis(fahrzeug.preis) }}
        </span>
        <span class="text-[#6B7585] text-sm">brutto</span>
      </div>

      <!-- Aktions-Buttons -->
      <div class="flex gap-2">
        <button
          class="flex-1 flex items-center justify-center gap-1.5
                 border border-[#0F2044] text-[#0F2044]
                 hover:bg-[#0F2044] hover:text-white
                 text-sm font-semibold py-2.5 rounded transition-colors"
        >
          <Info :size="14" />
          Details
        </button>

        <button
          @click="emit('toggleCart', fahrzeug)"
          :class="[
            'flex-1 flex items-center justify-center gap-1.5',
            'text-sm font-semibold py-2.5 rounded transition-colors',
            inCart
              ? 'bg-[#0F2044] text-white hover:bg-[#0F2044]/85'
              : 'bg-[#D41C1C] hover:bg-[#BB1818] text-white',
          ]"
        >
          <Check v-if="inCart" :size="14" />
          <ShoppingCart v-else :size="14" />
          {{ inCart ? 'Im Warenkorb' : 'In den Warenkorb' }}
        </button>
      </div>

    </div>
  </article>
</template>
