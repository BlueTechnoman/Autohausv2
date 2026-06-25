<!--
  FilterBar.vue – Fahrzeug-Filterleiste
  ═══════════════════════════════════════
  Zeigt drei Dropdowns: Marke, Kraftstoff, Max. Preis.
  Ermöglicht clientseitiges Filtern der geladenen Fahrzeugliste.

  v-model (defineModel):
    Vue 3.4+: defineModel() erstellt automatisch eine bidirektionale
    Datenbindung mit dem Elternelement (FahrzeugeSection.vue).
    Das bedeutet: Wählt der Benutzer "BMW", ändert sich der State
    in FahrzeugeSection sofort → computed() filtert die Liste neu.

  Datenfluss:
    1. FahrzeugeSection hat: markeFilter = ref('Alle Marken')
    2. FilterBar bekommt: v-model:marke="markeFilter"
    3. User wählt "BMW" → defineModel('marke') ändert sich
    4. markeFilter in FahrzeugeSection = "BMW"
    5. computed() in FahrzeugeSection filtert neu → Grid aktualisiert

  Props:
    hasActiveFilters: boolean – zeigt "Zurücksetzen"-Button wenn true
  Emits:
    reset – teilt Elternelement mit: Filter zurücksetzen
-->
<script setup lang="ts">
import { ChevronDown } from 'lucide-vue-next'

// ── Statische Filter-Optionen ─────────────────────────────────────────
// Diese werden nicht aus der API geladen – sie definieren das UI-Verhalten.
// Neue Marken werden hier und im Backend-Filterfeld gepflegt.
const MARKEN = ['Alle Marken', 'Audi', 'BMW', 'Mercedes-Benz', 'Volkswagen']

const KRAFTSTOFFE = ['Alle', 'Benzin', 'Diesel', 'Elektro', 'Hybrid']

const MAX_PREISE: { label: string; value: number }[] = [
  { label: 'Alle Preise',  value: 100000 },
  { label: 'bis 25.000 €', value: 25000  },
  { label: 'bis 30.000 €', value: 30000  },
  { label: 'bis 40.000 €', value: 40000  },
  { label: 'bis 50.000 €', value: 50000  },
]

// ── defineModel: Bidirektionale v-model-Bindungen ─────────────────────
// Jedes Model ist mit einem v-model:* in FahrzeugeSection verknüpft.
const marke      = defineModel<string>('marke',      { required: true })
const kraftstoff = defineModel<string>('kraftstoff', { required: true })
const maxPreis   = defineModel<number>('maxPreis',   { required: true })

// ── Props & Emits ─────────────────────────────────────────────────────
defineProps<{ hasActiveFilters: boolean }>()
const emit = defineEmits<{ reset: [] }>()
</script>

<template>
  <!--
    Filterleiste-Container: weißer Hintergrund, leichter Rahmen.
    flex-wrap: auf Mobile untereinander, Desktop nebeneinander.
  -->
  <div class="bg-white border border-[#1a2e5a]/10 rounded-lg px-5 py-4 mb-8 shadow-sm">
    <div class="flex flex-wrap gap-x-6 gap-y-3 items-end">

      <!-- ── Marken-Dropdown ── -->
      <div class="flex flex-col gap-1.5 flex-1 min-w-[150px]">
        <label class="text-[10px] font-bold text-[#8e9aaa] uppercase tracking-widest">Marke</label>
        <div class="relative">
          <!--
            v-model="marke": Ändert den defineModel-Wert
            → propagiert sofort zurück zu FahrzeugeSection
          -->
          <select
            v-model="marke"
            class="w-full appearance-none bg-[#f8f9fa] border border-[#1a2e5a]/10 rounded
                   px-3 py-2 text-sm text-[#1a2e5a] font-semibold pr-7
                   focus:outline-none focus:ring-2 focus:ring-[#1a2e5a]/20 cursor-pointer"
          >
            <option v-for="m in MARKEN" :key="m" :value="m">{{ m }}</option>
          </select>
          <!-- Pfeil-Icon (pointer-events-none: nicht anklickbar) -->
          <ChevronDown :size="13" class="absolute right-2.5 top-1/2 -translate-y-1/2 text-[#1a2e5a]/40 pointer-events-none" />
        </div>
      </div>

      <!-- ── Kraftstoff-Dropdown ── -->
      <div class="flex flex-col gap-1.5 flex-1 min-w-[150px]">
        <label class="text-[10px] font-bold text-[#8e9aaa] uppercase tracking-widest">Kraftstoff</label>
        <div class="relative">
          <select
            v-model="kraftstoff"
            class="w-full appearance-none bg-[#f8f9fa] border border-[#1a2e5a]/10 rounded
                   px-3 py-2 text-sm text-[#1a2e5a] font-semibold pr-7
                   focus:outline-none focus:ring-2 focus:ring-[#1a2e5a]/20 cursor-pointer"
          >
            <option v-for="k in KRAFTSTOFFE" :key="k" :value="k">{{ k }}</option>
          </select>
          <ChevronDown :size="13" class="absolute right-2.5 top-1/2 -translate-y-1/2 text-[#1a2e5a]/40 pointer-events-none" />
        </div>
      </div>

      <!-- ── Max.-Preis-Dropdown ── -->
      <div class="flex flex-col gap-1.5 flex-1 min-w-[150px]">
        <label class="text-[10px] font-bold text-[#8e9aaa] uppercase tracking-widest">Max. Preis</label>
        <div class="relative">
          <!--
            .number: Wandelt String-Wert aus <select> in Zahl um
            → nötig weil HTML-Formulare immer Strings liefern
          -->
          <select
            v-model.number="maxPreis"
            class="w-full appearance-none bg-[#f8f9fa] border border-[#1a2e5a]/10 rounded
                   px-3 py-2 text-sm text-[#1a2e5a] font-semibold pr-7
                   focus:outline-none focus:ring-2 focus:ring-[#1a2e5a]/20 cursor-pointer"
          >
            <option v-for="p in MAX_PREISE" :key="p.value" :value="p.value">
              {{ p.label }}
            </option>
          </select>
          <ChevronDown :size="13" class="absolute right-2.5 top-1/2 -translate-y-1/2 text-[#1a2e5a]/40 pointer-events-none" />
        </div>
      </div>

      <!-- Zurücksetzen: nur sichtbar wenn mind. ein Filter aktiv -->
      <button
        v-if="hasActiveFilters"
        @click="emit('reset')"
        class="text-[#e85c1a] text-sm font-semibold hover:underline whitespace-nowrap self-end pb-2"
      >
        Zurücksetzen
      </button>

    </div>
  </div>
</template>
