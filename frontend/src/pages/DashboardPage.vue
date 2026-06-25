<!--
  DashboardPage.vue – Geschütztes Benutzer-Dashboard
  ════════════════════════════════════════════════════
  Route: /dashboard (auth-guard: nur für eingeloggte Nutzer)

  Was ist diese Seite?
    Eine Seite, die nur nach erfolgreichem Login erreichbar ist.
    Der Router (router/index.ts) prüft den JWT-Token BEVOR
    diese Seite geladen wird. Kein Token → Weiterleitung zu /login.

  Daten aus der API:
    • GET /api/accounts/me/         → Benutzerinfo (Name, Rolle)
    • GET /api/vehicles/            → Alle Fahrzeuge (mit Preisverlauf)
    • Preisverlauf aus vehicle.price_history[]

  Besonderheiten dieser Seite:
    • Mehr Infos als auf der öffentlichen Startseite
    • Preisverlauf-Diagramm (SVG-basiert, ohne externe Bibliothek)
    • Favoriten (localStorage-basiert)
    • Fahrzeuge können gefiltert werden
    • Status-Badges (Verfügbar/Reserviert/Verkauft)
-->
<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  LogOut, User, Star, StarOff, Car, TrendingUp,
  Eye, Phone, Calendar, Gauge, Fuel, Settings2,
  ChevronDown, ChevronUp, Filter,
} from 'lucide-vue-next'
import NavBar    from '../components/NavBar.vue'
import AppFooter from '../components/AppFooter.vue'
import { useAuth }        from '../composables/useAuth'
import { useFahrzeuge }   from '../composables/useFahrzeuge'
import { formatKm, formatPreis, formatStatus, statusBadgeClass } from '../data/fahrzeuge'
import type { Fahrzeug } from '../data/fahrzeuge'

const router = useRouter()
const { user, logout }                = useAuth()
const { fahrzeuge, loading, laden }   = useFahrzeuge()

const scrolled = ref(false)
const onScroll = () => { scrolled.value = window.scrollY > 24 }
onMounted(()  => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))

// ── Favoriten (localStorage) ──────────────────────────────────────────
// Favoriten werden im Browser gespeichert – kein Backend nötig
const favoriteIds = ref<number[]>(
  JSON.parse(localStorage.getItem('dashboard_favorites') ?? '[]')
)

function toggleFavorite(id: number) {
  const idx = favoriteIds.value.indexOf(id)
  if (idx === -1) {
    favoriteIds.value.push(id)
  } else {
    favoriteIds.value.splice(idx, 1)
  }
  localStorage.setItem('dashboard_favorites', JSON.stringify(favoriteIds.value))
}

// ── Detailansicht (aufgeklappt) ───────────────────────────────────────
const expandedId = ref<number | null>(null)
function toggleExpand(id: number) {
  expandedId.value = expandedId.value === id ? null : id
}

// ── Preisverlauf-Diagramm (SVG) ───────────────────────────────────────
/**
 * Erstellt SVG-Pfad-Daten für einen Preisverlauf
 * @param punkte  Array von Preispunkten
 * @param w       Breite des SVG
 * @param h       Höhe des SVG
 */
function preisPfad(punkte: Fahrzeug['preisverlauf'], w = 300, h = 80): string {
  if (!punkte || punkte.length < 2) return ''
  const preise = punkte.map(p => p.preis)
  const min    = Math.min(...preise)
  const max    = Math.max(...preise)
  const range  = max - min || 1
  const step   = w / (punkte.length - 1)
  const points = punkte.map((p, i) => {
    const x = i * step
    const y = h - ((p.preis - min) / range) * (h - 10) - 5
    return `${x.toFixed(1)},${y.toFixed(1)}`
  })
  return `M${points.join(' L')}`
}

// ── Filter ────────────────────────────────────────────────────────────
const filterStatus = ref<'' | 'available' | 'reserved' | 'sold'>('')
const filterNurFavoriten = ref(false)
const suchtext = ref('')

const gefilterteFahrzeuge = computed(() => {
  return fahrzeuge.value.filter(f => {
    if (filterStatus.value && f.status !== filterStatus.value) return false
    if (filterNurFavoriten.value && !favoriteIds.value.includes(f.id)) return false
    if (suchtext.value) {
      const q = suchtext.value.toLowerCase()
      if (!f.marke.toLowerCase().includes(q) && !f.modell.toLowerCase().includes(q)) return false
    }
    return true
  })
})

// ── Statistiken ───────────────────────────────────────────────────────
const stats = computed(() => ({
  gesamt:     fahrzeuge.value.length,
  verfuegbar: fahrzeuge.value.filter(f => f.status === 'available').length,
  reserviert: fahrzeuge.value.filter(f => f.status === 'reserved').length,
  favoriten:  favoriteIds.value.length,
}))

// ── Logout ────────────────────────────────────────────────────────────
function handleLogout() {
  logout()
  router.push('/')
}

// ── Datenladen ────────────────────────────────────────────────────────
onMounted(() => {
  laden()  // Alle Fahrzeuge mit Preisverlauf laden
})
</script>

<template>
  <NavBar :scrolled="scrolled" />

  <main class="pt-16 min-h-screen bg-background">

    <!-- ── Dashboard-Header ──────────────────────────────────────── -->
    <div class="bg-[#1a2e5a] py-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between flex-wrap gap-4">
          <div>
            <p class="text-white/50 text-xs uppercase tracking-widest mb-1">Benutzer-Dashboard</p>
            <h1 class="text-white font-bold text-2xl">
              Willkommen, {{ user?.username ?? 'Gast' }}
            </h1>
            <p class="text-white/60 text-sm mt-1">
              <span class="capitalize">{{ user?.role ?? '' }}</span>
              · {{ user?.email }}
            </p>
          </div>
          <button
            @click="handleLogout"
            class="flex items-center gap-2 border border-white/25 hover:bg-white/10 text-white/80 hover:text-white text-sm font-semibold px-4 py-2.5 rounded-lg transition-colors"
          >
            <LogOut :size="15" /> Abmelden
          </button>
        </div>

        <!-- Statistik-Kacheln -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8">
          <div class="bg-white/8 border border-white/15 rounded-lg p-4 text-center">
            <div class="text-white font-bold text-2xl">{{ stats.gesamt }}</div>
            <div class="text-white/55 text-xs mt-1">Fahrzeuge gesamt</div>
          </div>
          <div class="bg-white/8 border border-white/15 rounded-lg p-4 text-center">
            <div class="text-[#e85c1a] font-bold text-2xl">{{ stats.verfuegbar }}</div>
            <div class="text-white/55 text-xs mt-1">Verfügbar</div>
          </div>
          <div class="bg-white/8 border border-white/15 rounded-lg p-4 text-center">
            <div class="text-yellow-400 font-bold text-2xl">{{ stats.reserviert }}</div>
            <div class="text-white/55 text-xs mt-1">Reserviert</div>
          </div>
          <div class="bg-white/8 border border-white/15 rounded-lg p-4 text-center">
            <div class="text-white font-bold text-2xl">{{ stats.favoriten }}</div>
            <div class="text-white/55 text-xs mt-1">Favoriten</div>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Hauptbereich ───────────────────────────────────────────── -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

      <!-- Filter-Leiste -->
      <div class="bg-white rounded-xl border border-[#1a2e5a]/8 p-4 shadow-sm mb-6 flex flex-wrap gap-3 items-center">
        <Filter :size="15" class="text-[#8e9aaa]" />

        <!-- Suche -->
        <input
          v-model="suchtext"
          type="text"
          placeholder="Marke oder Modell …"
          class="flex-1 min-w-40 px-3 py-2 border border-[#1a2e5a]/15 rounded-lg text-sm text-[#1a2e5a] placeholder-[#8e9aaa]/60 focus:outline-none focus:ring-2 focus:ring-[#1a2e5a]/20"
        />

        <!-- Status-Filter -->
        <select
          v-model="filterStatus"
          class="px-3 py-2 border border-[#1a2e5a]/15 rounded-lg text-sm text-[#1a2e5a] focus:outline-none bg-white"
        >
          <option value="">Alle Status</option>
          <option value="available">Verfügbar</option>
          <option value="reserved">Reserviert</option>
          <option value="sold">Verkauft</option>
        </select>

        <!-- Nur Favoriten -->
        <button
          @click="filterNurFavoriten = !filterNurFavoriten"
          :class="[
            'flex items-center gap-1.5 text-sm font-semibold px-3 py-2 rounded-lg border transition-colors',
            filterNurFavoriten
              ? 'bg-[#e85c1a] border-[#e85c1a] text-white'
              : 'border-[#1a2e5a]/15 text-[#8e9aaa] hover:text-[#1a2e5a]',
          ]"
        >
          <Star :size="14" /> Nur Favoriten
        </button>

        <span class="text-[#8e9aaa] text-xs ml-auto">
          {{ gefilterteFahrzeuge.length }} Fahrzeuge
        </span>
      </div>

      <!-- ── Lade-Zustand ── -->
      <div v-if="loading" class="space-y-3">
        <div v-for="n in 4" :key="n" class="bg-white rounded-xl h-24 animate-pulse border border-[#1a2e5a]/8" />
      </div>

      <!-- ── Fahrzeug-Liste ── -->
      <div v-else class="space-y-4">
        <div
          v-for="f in gefilterteFahrzeuge"
          :key="f.id"
          class="bg-white rounded-xl border border-[#1a2e5a]/8 shadow-sm overflow-hidden"
        >
          <!-- Zeilen-Header (immer sichtbar) -->
          <div class="p-4 flex items-center gap-4">

            <!-- Fahrzeugbild (klein) -->
            <div class="w-20 h-14 shrink-0 rounded-lg overflow-hidden bg-[#e2e8f0]">
              <img :src="f.bild" :alt="f.modell" class="w-full h-full object-cover" />
            </div>

            <!-- Basis-Info -->
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 flex-wrap">
                <span class="text-[#1a2e5a] font-bold text-sm">{{ f.marke }} {{ f.modell }}</span>
                <!-- Status-Badge -->
                <span :class="['text-xs font-bold px-2 py-0.5 rounded-full', statusBadgeClass(f.status)]">
                  {{ formatStatus(f.status) }}
                </span>
              </div>
              <p class="text-[#8e9aaa] text-xs mt-0.5">
                {{ f.baujahr }} · {{ formatKm(f.km) }} · {{ f.kraftstoff || '–' }}
              </p>
            </div>

            <!-- Preis -->
            <div class="text-right shrink-0">
              <div class="text-[#1a2e5a] font-bold text-base">{{ formatPreis(f.preis) }}</div>
              <div class="text-[#8e9aaa] text-xs">{{ f.leistung ? f.leistung + ' PS' : '' }}</div>
            </div>

            <!-- Aktions-Buttons -->
            <div class="flex items-center gap-2 shrink-0">
              <!-- Favorit -->
              <button
                @click="toggleFavorite(f.id)"
                :class="['w-9 h-9 rounded-full border flex items-center justify-center transition-colors',
                  favoriteIds.includes(f.id) ? 'bg-[#e85c1a]/10 border-[#e85c1a]/30' : 'border-[#1a2e5a]/15 hover:bg-[#1a2e5a]/5']"
                :title="favoriteIds.includes(f.id) ? 'Aus Favoriten entfernen' : 'Zu Favoriten hinzufügen'"
              >
                <Star v-if="favoriteIds.includes(f.id)" :size="14" class="text-[#e85c1a] fill-[#e85c1a]" />
                <Star v-else :size="14" class="text-[#8e9aaa]" />
              </button>

              <!-- Details aufklappen -->
              <button
                @click="toggleExpand(f.id)"
                class="w-9 h-9 rounded-full border border-[#1a2e5a]/15 hover:bg-[#1a2e5a]/5 flex items-center justify-center transition-colors"
                :title="expandedId === f.id ? 'Einklappen' : 'Details anzeigen'"
              >
                <ChevronUp v-if="expandedId === f.id" :size="16" class="text-[#1a2e5a]" />
                <ChevronDown v-else :size="16" class="text-[#1a2e5a]" />
              </button>

              <!-- Zur Detailseite -->
              <button
                @click="$router.push(`/fahrzeug/${f.id}`)"
                class="w-9 h-9 rounded-full bg-[#1a2e5a] hover:bg-[#1a2e5a]/85 flex items-center justify-center transition-colors"
                title="Öffentliche Detailseite"
              >
                <Eye :size="14" class="text-white" />
              </button>
            </div>
          </div>

          <!-- ── Ausgeklappter Detailbereich ── -->
          <div v-if="expandedId === f.id" class="border-t border-[#1a2e5a]/8 bg-[#f8f9fa]">
            <div class="p-5 grid grid-cols-1 md:grid-cols-3 gap-6">

              <!-- Technische Daten -->
              <div class="md:col-span-1">
                <h3 class="text-[#1a2e5a] font-bold text-sm mb-3 flex items-center gap-2">
                  <Settings2 :size="14" class="text-[#e85c1a]" /> Technische Daten
                </h3>
                <dl class="space-y-2 text-sm">
                  <div class="flex justify-between">
                    <dt class="text-[#8e9aaa]">Erstzulassung</dt>
                    <dd class="text-[#1a2e5a] font-semibold">{{ f.ez || '–' }}</dd>
                  </div>
                  <div class="flex justify-between">
                    <dt class="text-[#8e9aaa]">Getriebe</dt>
                    <dd class="text-[#1a2e5a] font-semibold">{{ f.getriebe || '–' }}</dd>
                  </div>
                  <div class="flex justify-between">
                    <dt class="text-[#8e9aaa]">Farbe</dt>
                    <dd class="text-[#1a2e5a] font-semibold">{{ f.farbe || '–' }}</dd>
                  </div>
                  <div class="flex justify-between">
                    <dt class="text-[#8e9aaa]">Türen</dt>
                    <dd class="text-[#1a2e5a] font-semibold">{{ f.tueren ? f.tueren + '-türig' : '–' }}</dd>
                  </div>
                  <div class="flex justify-between">
                    <dt class="text-[#8e9aaa]">HU bis</dt>
                    <dd class="text-[#1a2e5a] font-semibold">{{ f.hu || '–' }}</dd>
                  </div>
                </dl>
              </div>

              <!-- Ausstattung -->
              <div>
                <h3 class="text-[#1a2e5a] font-bold text-sm mb-3 flex items-center gap-2">
                  <Car :size="14" class="text-[#e85c1a]" /> Ausstattung
                </h3>
                <div v-if="f.ausstattung.length > 0" class="flex flex-wrap gap-1.5">
                  <span
                    v-for="item in f.ausstattung"
                    :key="item"
                    class="bg-[#1a2e5a]/8 text-[#1a2e5a] text-xs px-2 py-0.5 rounded-full"
                  >
                    {{ item }}
                  </span>
                </div>
                <p v-else class="text-[#8e9aaa] text-xs">Keine Angaben</p>

                <!-- Beschreibung -->
                <h3 class="text-[#1a2e5a] font-bold text-sm mt-4 mb-2">Beschreibung</h3>
                <p class="text-[#8e9aaa] text-xs leading-relaxed">
                  {{ f.beschreibung || 'Keine Beschreibung vorhanden.' }}
                </p>
              </div>

              <!-- Preisverlauf-Diagramm -->
              <div>
                <h3 class="text-[#1a2e5a] font-bold text-sm mb-3 flex items-center gap-2">
                  <TrendingUp :size="14" class="text-[#e85c1a]" /> Preisverlauf
                </h3>

                <div v-if="f.preisverlauf && f.preisverlauf.length >= 2">
                  <!--
                    SVG-Liniendiagramm (kein Chart.js nötig)
                    preisPfad() berechnet den SVG-Pfad aus den Preispunkten
                  -->
                  <div class="bg-white border border-[#1a2e5a]/8 rounded-lg p-3">
                    <svg viewBox="0 0 300 80" class="w-full" preserveAspectRatio="none">
                      <!-- Hintergrundgitter -->
                      <line x1="0" y1="40" x2="300" y2="40" stroke="#e2e8f0" stroke-width="1" />
                      <line x1="0" y1="20" x2="300" y2="20" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="4" />
                      <line x1="0" y1="60" x2="300" y2="60" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="4" />
                      <!-- Linie des Preisverlaufs -->
                      <path
                        :d="preisPfad(f.preisverlauf)"
                        fill="none"
                        stroke="#e85c1a"
                        stroke-width="2.5"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      />
                      <!-- Datenpunkte -->
                      <circle
                        v-for="(p, i) in f.preisverlauf"
                        :key="i"
                        :cx="(i * 300 / (f.preisverlauf.length - 1)).toFixed(1)"
                        :cy="(80 - ((p.preis - Math.min(...f.preisverlauf.map(x => x.preis))) / (Math.max(...f.preisverlauf.map(x => x.preis)) - Math.min(...f.preisverlauf.map(x => x.preis)) || 1)) * 70 - 5).toFixed(1)"
                        r="3"
                        fill="#e85c1a"
                      />
                    </svg>
                    <!-- Achsenbeschriftung -->
                    <div class="flex justify-between mt-1">
                      <span class="text-[#8e9aaa] text-xs">{{ formatPreis(Math.min(...f.preisverlauf.map(p => p.preis))) }}</span>
                      <span class="text-[#8e9aaa] text-xs">{{ formatPreis(Math.max(...f.preisverlauf.map(p => p.preis))) }}</span>
                    </div>
                    <div class="text-center text-[#8e9aaa] text-xs mt-1">
                      {{ f.preisverlauf.length }} Datenpunkte ·
                      {{ f.preisverlauf[0]?.datum }} – {{ f.preisverlauf[f.preisverlauf.length - 1]?.datum }}
                    </div>
                  </div>
                </div>

                <div v-else-if="f.preisverlauf && f.preisverlauf.length === 1" class="bg-white border border-[#1a2e5a]/8 rounded-lg p-3 text-center">
                  <div class="text-[#1a2e5a] font-bold text-lg">{{ formatPreis(f.preisverlauf[0].preis) }}</div>
                  <div class="text-[#8e9aaa] text-xs mt-1">Letzter Preis: {{ f.preisverlauf[0].datum }}</div>
                </div>

                <div v-else class="bg-white border border-[#1a2e5a]/8 rounded-lg p-4 text-center text-[#8e9aaa] text-xs">
                  Noch keine Preishistorie für dieses Fahrzeug vorhanden.<br />
                  <span class="text-[#1a2e5a]/50">Wird vom Admin im Backend gepflegt.</span>
                </div>
              </div>

            </div>

            <!-- Footer des Detail-Bereichs -->
            <div class="px-5 pb-4 border-t border-[#1a2e5a]/8 mt-2 pt-4 flex gap-3">
              <button @click="$router.push(`/fahrzeug/${f.id}`)"
                class="flex items-center gap-2 text-sm font-semibold border border-[#1a2e5a]/20 text-[#1a2e5a] hover:bg-[#1a2e5a]/5 px-4 py-2 rounded-lg transition-colors">
                <Eye :size="14" /> Öffentliche Seite
              </button>
              <a :href="`tel:+499211234567`"
                class="flex items-center gap-2 text-sm font-semibold bg-[#e85c1a]/10 hover:bg-[#e85c1a]/20 text-[#e85c1a] px-4 py-2 rounded-lg transition-colors">
                <Phone :size="14" /> Anfragen
              </a>
            </div>
          </div>

        </div>

        <!-- Leer-State -->
        <div v-if="gefilterteFahrzeuge.length === 0 && !loading" class="text-center py-16 bg-white rounded-xl border border-[#1a2e5a]/8">
          <p class="text-[#1a2e5a] font-bold text-lg mb-2">Keine Fahrzeuge gefunden</p>
          <p class="text-[#8e9aaa] text-sm">Passen Sie die Filtereinstellungen an.</p>
        </div>
      </div>

    </div>
  </main>

  <AppFooter />
</template>
