<!--
  HeroSection.vue – Fullscreen-Einstiegsbereich der Startseite
  ═════════════════════════════════════════════════════════════
  Zeigt Headline, Subtext, CTA-Buttons und Kennzahlen
  vor einem Hintergrundbild mit Farbüberlagerung (Overlay).

  Transparenz-Fix:
    Zuvor: opacity-20 → Bild zu dunkel / kaum sichtbar
    Jetzt: opacity-40 → Bild deutlich sichtbarer, trotzdem lesbar
    Der Gradient (from-70%) sorgt dafür, dass Text links immer lesbar bleibt.

  Scroll-Verhalten:
    Buttons scrollen direkt zu #fahrzeuge bzw. #kontakt
    ohne Router-Emit – direktes DOM-API (scrollIntoView).
-->
<script setup lang="ts">
// Kein Emit mehr nötig – direktes Scrollen
function scrollTo(id: string) {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
}

const STATS: [string, string][] = [
  ['80+',   'Fahrzeuge im Bestand'],
  ['15 J.', 'Erfahrung'],
  ['4,9 ★', 'Kundenbewertung'],
]
</script>

<template>
  <section id="hero" class="relative min-h-[90vh] flex items-center overflow-hidden pt-16 w-full">

    <!-- Hintergrundbild mit Overlay -->
    <div class="absolute inset-0 bg-[#1a2e5a]">
      <img
        src="https://images.unsplash.com/photo-1692406069831-0bb7ea297645?w=1920&h=1080&fit=crop&auto=format"
        alt="AutoHaus Bayreuth Showroom"
        class="w-full h-full object-cover opacity-40"
      />
      <!--
        Gradient-Overlay:
        Links (from): sehr dicht → Text immer lesbar
        Rechts (to): transparent → Bild sichtbar
        via-70%: Gradient beginnt spät → mehr Bild sichtbar
      -->
      <div class="absolute inset-0 bg-gradient-to-r from-[#1a2e5a]/90 via-[#1a2e5a]/55 to-transparent" />
    </div>

    <!-- Seiteninhalt (über Overlay) -->
    <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 w-full">
      <div class="max-w-2xl">

        <!-- Eyebrow-Label -->
        <p class="text-[#e85c1a] font-bold text-xs uppercase tracking-[0.2em] mb-5">
          Ihr Autohaus in Bayreuth
        </p>

        <!-- Hauptüberschrift -->
        <h1
          class="text-white font-bold leading-[1.1] mb-6"
          style="font-size: clamp(2.4rem, 6vw, 4rem)"
        >
          Ihr nächstes<br />
          <span class="text-white/85">Fahrzeug wartet.</span>
        </h1>

        <!-- Untertext -->
        <p class="text-white/70 text-lg leading-relaxed mb-10 max-w-lg">
          Über 80 geprüfte Gebrauchtwagen - transparent bepreist,
          professionell aufbereitet, sofort verfügbar.
        </p>

        <!-- CTA-Buttons -->
        <div class="flex flex-wrap gap-4">
          <button
            @click="scrollTo('fahrzeuge')"
            class="bg-[#e85c1a] hover:bg-[#d44e12] text-white font-bold px-8 py-4 rounded text-base transition-colors"
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

        <!-- Statistiken -->
        <div class="mt-14 pt-10 border-t border-white/12 flex gap-10 flex-wrap">
          <div v-for="[val, label] in STATS" :key="label">
            <div class="text-white font-bold text-2xl">{{ val }}</div>
            <div class="text-white/45 text-xs mt-0.5 uppercase tracking-wider">{{ label }}</div>
          </div>
        </div>

      </div>
    </div>

  </section>
</template>
