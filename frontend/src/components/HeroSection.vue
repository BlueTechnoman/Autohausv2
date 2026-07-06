<!--
  HeroSection.vue – Fullscreen-Einstiegsbereich der Startseite
  ═════════════════════════════════════════════════════════════
  Zeigt Headline, Subtext, CTA-Buttons und Kennzahlen
  vor einem Hintergrundbild mit Farbüberlagerung (Overlay).

  Mobile-Optimierungen:
    • Buttons auf Mobile volle Breite (w-full sm:w-auto) → sieht sauberer aus
    • py-24 → pt-8 pb-14 auf Mobile → weniger Leerraum, mehr Inhalt sichtbar
    • Statistiken: engerer Abstand auf Mobile (gap-6 sm:gap-10)
    • Gradient auf Mobile stärker (mehr Text-Lesbarkeit auf schmalem Viewport)

  Transparenz:
    opacity-40 → Bild deutlich sichtbar, trotzdem lesbar
-->
<script setup lang="ts">
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
        class="w-full h-full object-cover opacity-60"
      />
      <!--
        Gradient-Overlay:
        Mobile:  stärkeres Overlay (from-[#1a2e5a]/95) weil Viewport schmal
                 und Text über fast die gesamte Breite geht
        Desktop: from-[#1a2e5a]/90 via-55% to-transparent → Bild rechts sichtbar
      -->
      <div class="absolute inset-0 bg-[#1a2e5a]/55 sm:bg-[#1a2e5a]/55" />
    </div>

    <!-- Seiteninhalt (über Overlay) -->
    <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-14 sm:py-24 w-full">
      <div class="max-w-2xl">

        <!-- Eyebrow-Label -->
        <p class="text-[#e85c1a] font-bold text-xs uppercase tracking-[0.2em] mb-4 sm:mb-5">
          Ihr Autohaus in Bayreuth
        </p>

        <!-- Hauptüberschrift -->
        <h1
          class="text-white font-bold leading-[1.1] mb-5 sm:mb-6"
          style="font-size: clamp(2rem, 6vw, 4rem)"
        >
          Ihr nächstes<br />
          <span class="text-white/85">Fahrzeug wartet.</span>
        </h1>

        <!-- Untertext -->
        <p class="text-white/70 text-base sm:text-lg leading-relaxed mb-8 sm:mb-10 max-w-lg">
          Über 80 geprüfte Gebrauchtwagen — transparent bepreist,
          professionell aufbereitet, sofort verfügbar.
        </p>

        <!-- CTA-Buttons: auf Mobile volle Breite, auf Desktop normal -->
        <div class="flex flex-col sm:flex-row flex-wrap gap-3 sm:gap-4">
          <button
            @click="scrollTo('fahrzeuge')"
            class="w-full sm:w-auto bg-[#e85c1a] hover:bg-[#d44e12] text-white font-bold px-8 py-4 rounded text-base transition-colors"
          >
            Fahrzeuge entdecken
          </button>
          <button
            @click="scrollTo('kontakt')"
            class="w-full sm:w-auto border border-white/35 hover:border-white/60 text-white font-semibold px-8 py-4 rounded text-base transition-colors"
          >
            Kontakt aufnehmen
          </button>
        </div>

        <!-- Statistiken -->
        <div class="mt-10 sm:mt-14 pt-8 sm:pt-10 border-t border-white/12 flex gap-6 sm:gap-10 flex-wrap">
          <div v-for="[val, label] in STATS" :key="label">
            <div class="text-white font-bold text-xl sm:text-2xl">{{ val }}</div>
            <div class="text-white/45 text-xs mt-0.5 uppercase tracking-wider">{{ label }}</div>
          </div>
        </div>

      </div>
    </div>

  </section>
</template>
