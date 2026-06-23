<script setup lang="ts">
import { ChevronDown } from 'lucide-vue-next'

// ── Filter-Optionen ───────────────────────────────────────────────────
const MARKEN = ['Alle Marken', 'Audi', 'BMW', 'Mercedes-Benz', 'Volkswagen']

const KRAFTSTOFFE = ['Alle', 'Benzin', 'Diesel', 'Elektro', 'Hybrid']

const MAX_PREISE: { label: string; value: number }[] = [
  { label: 'Alle Preise',  value: 100000 },
  { label: 'bis 25.000 €', value: 25000  },
  { label: 'bis 30.000 €', value: 30000  },
  { label: 'bis 40.000 €', value: 40000  },
  { label: 'bis 50.000 €', value: 50000  },
]

// ── v-model-Bindungen ────────────────────────────────────────────────
const marke      = defineModel<string>('marke',      { required: true })
const kraftstoff = defineModel<string>('kraftstoff', { required: true })
const maxPreis   = defineModel<number>('maxPreis',   { required: true })

// ── Props & Emits ─────────────────────────────────────────────────────
const props = defineProps<{ hasActiveFilters: boolean }>()
const emit  = defineEmits<{ reset: [] }>()
</script>

<template>
  <div class="bg-white border border-[#0F2044]/10 rounded-lg px-5 py-4 mb-8 shadow-sm">
    <div class="flex flex-wrap gap-x-6 gap-y-3 items-end">

      <!-- Marke -->
      <div class="flex flex-col gap-1.5 flex-1 min-w-[150px]">
        <label class="text-[10px] font-bold text-[#6B7585] uppercase tracking-widest">Marke</label>
        <div class="relative">
          <select
            v-model="marke"
            class="w-full appearance-none bg-[#F0F0EC] border border-[#0F2044]/10 rounded
                   px-3 py-2 text-sm text-[#0F2044] font-semibold pr-7
                   focus:outline-none focus:ring-2 focus:ring-[#0F2044]/20 cursor-pointer"
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
            v-model="kraftstoff"
            class="w-full appearance-none bg-[#F0F0EC] border border-[#0F2044]/10 rounded
                   px-3 py-2 text-sm text-[#0F2044] font-semibold pr-7
                   focus:outline-none focus:ring-2 focus:ring-[#0F2044]/20 cursor-pointer"
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
            class="w-full appearance-none bg-[#F0F0EC] border border-[#0F2044]/10 rounded
                   px-3 py-2 text-sm text-[#0F2044] font-semibold pr-7
                   focus:outline-none focus:ring-2 focus:ring-[#0F2044]/20 cursor-pointer"
          >
            <option v-for="p in MAX_PREISE" :key="p.value" :value="p.value">
              {{ p.label }}
            </option>
          </select>
          <ChevronDown :size="13" class="absolute right-2.5 top-1/2 -translate-y-1/2 text-[#0F2044]/40 pointer-events-none" />
        </div>
      </div>

      <!-- Reset -->
      <button
        v-if="hasActiveFilters"
        @click="emit('reset')"
        class="text-[#D41C1C] text-sm font-semibold hover:underline whitespace-nowrap self-end pb-2"
      >
        Zurücksetzen
      </button>

    </div>
  </div>
</template>
