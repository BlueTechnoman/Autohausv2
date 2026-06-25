<!--
  FahrzeugKarte.vue – Objektorientierte Fahrzeug-Kachel (Car Card)
  ════════════════════════════════════════════════════════════════
  Zeigt ein Fahrzeug als kompakte, klickbare Karte an.
  Wird in FahrzeugeSection.vue in einem Raster (Grid) verwendet.

  Architektur (Objektorientierung):
    Jede Karte ist eine "Instanz" dieser Komponente.
    Sie erhält ihr Fahrzeug-Objekt via Props (defineProps).
    Daten kommen immer von außen → "Dependency Injection".
    Die Karte KANN die Daten NICHT verändern (read-only durch v-bind).

  Schreibschutz (important!):
    Die Karte zeigt Daten nur an. Es gibt keine Edit-Felder,
    kein v-model, keine Formular-Inputs. Die Daten sind
    serverseitig geschützt (Django REST Framework Permissions).

  Props:
    fahrzeug: Fahrzeug  – Vollständiges Fahrzeug-Objekt aus der API

  Emits: keine (rein darstellend)

  Composables:
    useCart()         – Warenkorb hinzufügen/entfernen
    useNotification() – Toast-Nachricht nach Warenkorb-Aktion

  Router-Integration:
    RouterLink: Klick auf Bild oder Details-Button navigiert zur
    Detailseite /fahrzeug/{id} ohne Seitenreload (SPA-Navigation).
-->
<script setup lang="ts">
import { Check, ShoppingCart, Info, Calendar, Gauge, Fuel } from 'lucide-vue-next'
import { RouterLink } from 'vue-router'
import { useCart }        from '../composables/useCart'
import { useNotification }from '../composables/useNotification'
import type { Fahrzeug }  from '../data/fahrzeuge'
import { formatKm, formatPreis } from '../data/fahrzeuge'

// ── Props (read-only von außen) ───────────────────────────────────────
// defineProps: Vue-Mechanismus für Eltern → Kind Datenweitergabe
// Das Objekt kann NICHT verändert werden – nur lesen!
const props = defineProps<{ fahrzeug: Fahrzeug }>()

// ── Composables ───────────────────────────────────────────────────────
const { isInCart, toggle } = useCart()
const { show }             = useNotification()

/**
 * handleCart() – Fahrzeug zum Warenkorb hinzufügen / entfernen
 * toggle() gibt true zurück wenn hinzugefügt, false wenn entfernt.
 * show() zeigt 2,8 Sekunden lang eine Toast-Benachrichtigung.
 */
function handleCart() {
  const added = toggle(props.fahrzeug)
  show(
    added
      ? `${props.fahrzeug.marke} ${props.fahrzeug.modell} zum Warenkorb hinzugefügt`
      : `${props.fahrzeug.marke} ${props.fahrzeug.modell} entfernt`
  )
}
</script>

<template>
  <!--
    <article>: Semantisches HTML – eine Kachel ist ein eigenständiger Inhalt.
    group: Tailwind-Klasse → ermöglicht group-hover: auf Kindelementen.
    flex flex-col: Vertikale Anordnung damit der Preis-Button immer unten ist.
  -->
  <article
    class="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200
           overflow-hidden border border-[#1a2e5a]/8 group flex flex-col"
  >

    <!-- ── Fahrzeugbild ─────────────────────────────────────────────────
         RouterLink navigiert zur Detailseite ohne Browser-Reload.
         aspect-[16/10]: Seitenverhältnis fixiert → einheitliche Bildgröße.
         group-hover:scale-105: Zoom-Effekt wenn Maus über Karte ist.
    ──────────────────────────────────────────────────────────────────── -->
    <RouterLink :to="`/fahrzeug/${fahrzeug.id}`" class="block">
      <div class="relative overflow-hidden bg-[#e2e8f0] aspect-[16/10] shrink-0">
        <img
          :src="fahrzeug.bild"
          :alt="`${fahrzeug.marke} ${fahrzeug.modell}`"
          class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
        />

        <!-- Marken-Badge oben links: aus API-Daten (fahrzeug.marke) -->
        <div class="absolute top-3 left-3">
          <span class="bg-[#1a2e5a] text-white text-xs font-bold px-2.5 py-1 rounded">
            {{ fahrzeug.marke }}
          </span>
        </div>

        <!-- Warenkorb-Badge: erscheint wenn Fahrzeug bereits vorgemerkt -->
        <div v-if="isInCart(fahrzeug.id)" class="absolute top-3 right-3">
          <span class="bg-[#e85c1a] text-white text-xs font-bold px-2.5 py-1 rounded flex items-center gap-1">
            <Check :size="10" />
            Vorgemerkt
          </span>
        </div>
      </div>
    </RouterLink>

    <!-- ── Karteninhalt ─────────────────────────────────────────────────
         p-5: Innenabstand, flex flex-col flex-1: nimmt restliche Höhe ein.
         mt-auto beim Preis: Preis immer am unteren Ende der Karte.
    ──────────────────────────────────────────────────────────────────── -->
    <div class="p-5 flex flex-col flex-1">

      <!-- Fahrzeugname: Modell groß, Marke via Badge (oben) -->
      <h3 class="text-[#1a2e5a] font-bold text-lg leading-tight mb-3">
        {{ fahrzeug.modell }}
      </h3>

      <!-- Kurzinfo-Leiste: Baujahr · km · Kraftstoff (aus API) -->
      <div class="flex items-center gap-4 text-xs text-[#8e9aaa] mb-4">
        <span class="flex items-center gap-1.5">
          <Calendar :size="12" class="shrink-0" />
          {{ fahrzeug.baujahr }}
        </span>
        <span class="w-px h-3 bg-[#1a2e5a]/12" />
        <span class="flex items-center gap-1.5">
          <Gauge :size="12" class="shrink-0" />
          {{ formatKm(fahrzeug.km) }}        <!-- z.B. "48.200 km" -->
        </span>
        <span class="w-px h-3 bg-[#1a2e5a]/12" />
        <span class="flex items-center gap-1.5">
          <Fuel :size="12" class="shrink-0" />
          {{ fahrzeug.kraftstoff || '–' }}
        </span>
      </div>

      <!-- Preis (mt-auto: drückt alles nach unten) -->
      <div class="flex items-baseline gap-1.5 mb-5 mt-auto">
        <span class="text-[#1a2e5a] font-bold text-2xl">
          {{ formatPreis(fahrzeug.preis) }}   <!-- z.B. "32.900 €" -->
        </span>
        <span class="text-[#8e9aaa] text-sm">brutto</span>
      </div>

      <!-- Aktions-Buttons: Details (Router) + Vormerken (Warenkorb) -->
      <div class="flex gap-2">

        <!-- Details-Button → navigiert zu /fahrzeug/{id} -->
        <RouterLink
          :to="`/fahrzeug/${fahrzeug.id}`"
          class="flex-1 flex items-center justify-center gap-1.5
                 border border-[#1a2e5a] text-[#1a2e5a]
                 hover:bg-[#1a2e5a] hover:text-white
                 text-sm font-semibold py-2.5 rounded transition-colors"
        >
          <Info :size="14" />
          Details
        </RouterLink>

        <!-- Warenkorb-Button: Farbe wechselt je nach Status -->
        <button
          @click="handleCart"
          :class="[
            'flex-1 flex items-center justify-center gap-1.5',
            'text-sm font-semibold py-2.5 rounded transition-colors',
            isInCart(fahrzeug.id)
              ? 'bg-[#1a2e5a] text-white hover:bg-[#1a2e5a]/85'  // Im Warenkorb: Dunkelblau
              : 'bg-[#e85c1a] hover:bg-[#d44e12] text-white',     // Nicht im Warenkorb: Orange
          ]"
        >
          <Check v-if="isInCart(fahrzeug.id)" :size="14" />
          <ShoppingCart v-else :size="14" />
          {{ isInCart(fahrzeug.id) ? 'Im Warenkorb' : 'Vormerken' }}
        </button>
      </div>

    </div>
  </article>
</template>
