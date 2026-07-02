<!--
  FahrzeugeSection.vue – Fahrzeugkatalog auf der Startseite
  ═══════════════════════════════════════════════════════════
  Zeigt alle verfügbaren Fahrzeuge als Kacheln (Cards).

  Datenladen:
    • onMounted(): Ruft useFahrzeuge().laden() auf
    • Daten kommen von GET /api/vehicles/?status=available
    • loading-State zeigt Skeleton-Cards während Laden

  Client-seitiges Filtern:
    • Marke, Kraftstoff, Maxpreis werden auf den geladenen Daten
      mit computed() gefiltert – kein erneuter API-Call nötig
    • Bei Bedarf könnten Filter auch als API-Parameter übergeben werden

  Schreibschutz:
    • Kacheln sind read-only: kein Edit-Button, keine Formular-Felder
    • Nur "Details" (→ Detailseite) und "Vormerken" (Warenkorb)
-->
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import FahrzeugKarte from './FahrzeugKarte.vue'
import FilterBar     from './FilterBar.vue'
import { useFahrzeuge } from '../composables/useFahrzeuge'

// ── Composable – Fahrzeuge aus API laden ──────────────────────────────
const { fahrzeuge, loading, loadingMore, error, gesamtAnzahl, hasMore, laden, mehrLaden } = useFahrzeuge()

// ── Filter-State ──────────────────────────────────────────────────────
const markeFilter      = ref('Alle Marken')
const kraftstoffFilter = ref('')
const maxPreis         = ref(100000)

// ── Computed: gefilterte Fahrzeuge ────────────────────────────────────
// Vue re-berechnet dies automatisch wenn fahrzeuge, markeFilter etc. sich ändern
const filteredFahrzeuge = computed(() =>
  fahrzeuge.value.filter((f) => {
    if (markeFilter.value !== 'Alle Marken' && f.marke !== markeFilter.value) return false
    if (kraftstoffFilter.value !== '' && f.kraftstoff !== kraftstoffFilter.value) return false
    if (f.preis > maxPreis.value) return false
    return true
  })
)

const hasActiveFilters = computed(() =>
  markeFilter.value !== 'Alle Marken' ||
  kraftstoffFilter.value !== ''       ||
  maxPreis.value !== 100000
)

function resetFilters() {
  markeFilter.value      = 'Alle Marken'
  kraftstoffFilter.value = ''
  maxPreis.value         = 100000
}

// ── Lifecycle: API-Aufruf beim Mounten der Komponente ─────────────────
// onMounted() = wird ausgeführt wenn die Komponente in den DOM eingehängt wurde
onMounted(() => {
  laden()  // Lädt Fahrzeuge von GET /api/vehicles/
})
</script>

<template>
  <!--
    id="fahrzeuge": Ankerpunkt für Scroll-Navigation aus dem Hero-Button
    und dem NavBar-Link "Fahrzeuge" (router.push({ path: '/', hash: '#fahrzeuge' }))
  -->
  <section id="fahrzeuge" class="py-16 bg-background">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

      <!-- Header -->
      <div class="mb-8">
        <h2 class="text-[#1a2e5a] text-3xl font-bold mb-1">Unsere Fahrzeuge</h2>
        <p v-if="!loading && !error" class="text-[#8e9aaa] text-sm">
          {{ filteredFahrzeuge.length }} von {{ gesamtAnzahl }} Fahrzeugen geladen
        </p>
      </div>

      <!-- Filterleiste -->
      <FilterBar
        v-model:marke="markeFilter"
        v-model:kraftstoff="kraftstoffFilter"
        v-model:maxPreis="maxPreis"
        :hasActiveFilters="hasActiveFilters"
        @reset="resetFilters"
      />

      <!-- ── Lade-Zustand: Skeleton-Cards ── -->
      <!-- Werden angezeigt während die API-Anfrage läuft -->
      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="n in 6"
          :key="n"
          class="bg-white rounded-lg shadow-sm border border-[#1a2e5a]/8 overflow-hidden animate-pulse"
        >
          <!-- Skeleton-Bild -->
          <div class="aspect-[16/10] bg-[#e2e8f0]" />
          <div class="p-5 space-y-3">
            <div class="h-4 bg-[#e2e8f0] rounded w-3/4" />
            <div class="h-3 bg-[#e2e8f0] rounded w-1/2" />
            <div class="h-6 bg-[#e2e8f0] rounded w-1/3" />
            <div class="flex gap-2">
              <div class="h-9 bg-[#e2e8f0] rounded flex-1" />
              <div class="h-9 bg-[#e2e8f0] rounded flex-1" />
            </div>
          </div>
        </div>
      </div>

      <!-- ── Fehler-Zustand ── -->
      <div v-else-if="error" class="text-center py-20">
        <div class="text-4xl mb-4">⚠️</div>
        <p class="text-[#1a2e5a] font-bold text-xl mb-2">Verbindungsfehler</p>
        <p class="text-[#8e9aaa] text-sm mb-6">
          Die Fahrzeuge konnten nicht geladen werden. Bitte stellen Sie sicher,
          dass der Backend-Server läuft.
        </p>
        <p class="text-xs text-red-500 mb-6 font-mono">{{ error }}</p>
        <button
          @click="laden()"
          class="bg-[#e85c1a] hover:bg-[#d44e12] text-white font-bold px-6 py-3 rounded transition-colors"
        >
          Erneut versuchen
        </button>
      </div>

      <!-- ── Leer-Zustand (Filter keine Treffer) ── -->
      <div v-else-if="filteredFahrzeuge.length === 0" class="text-center py-24">
        <p class="text-[#1a2e5a] font-bold text-xl mb-2">Keine Fahrzeuge gefunden.</p>
        <p class="text-[#8e9aaa] text-sm">Bitte passen Sie Ihre Filtereinstellungen an.</p>
      </div>

      <!-- ── Fahrzeug-Kacheln (Karten-Raster) ── -->
      <!-- Read-only: Kacheln können nicht bearbeitet werden -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <FahrzeugKarte
          v-for="fahrzeug in filteredFahrzeuge"
          :key="fahrzeug.id"
          :fahrzeug="fahrzeug"
        />
      </div>

      <!-- ── "Mehr laden"-Button (Pagination) ── -->
      <!-- Nur sichtbar solange die API weitere Seiten hat -->
      <div v-if="!loading && !error && hasMore" class="flex justify-center mt-10">
        <button
          @click="mehrLaden()"
          :disabled="loadingMore"
          class="bg-white border-2 border-[#1a2e5a] text-[#1a2e5a] font-bold px-8 py-3 rounded hover:bg-[#1a2e5a] hover:text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ loadingMore ? 'Lädt…' : 'Weitere Fahrzeuge laden' }}
        </button>
      </div>

    </div>
  </section>
</template>