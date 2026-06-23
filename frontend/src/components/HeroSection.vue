<script setup lang="ts">
// ── Emits ────────────────────────────────────────────────────────────
const emit = defineEmits<{
  scrollTo: [id: string]
}>()

const STATS: [string, string][] = [
  ['80+',   'Fahrzeuge im Bestand'],
  ['15 J.', 'Erfahrung'],
  ['4,9 ★', 'Kundenbewertung'],
]
</script>

<template>
  <section id="hero" class="relative min-h-[90vh] flex items-center overflow-hidden pt-16">

    <!-- Hintergrundbild -->
    <div class="absolute inset-0 bg-[#0F2044]">
      <img
        src="https://images.unsplash.com/photo-1692406069831-0bb7ea297645?w=1920&h=1080&fit=crop&auto=format"
        alt="AutoHaus Müller Showroom"
        class="w-full h-full object-cover opacity-20"
      />
      <div class="absolute inset-0 bg-gradient-to-r from-[#0F2044]/95 via-[#0F2044]/70 to-[#0F2044]/30" />
    </div>

    <!-- Inhalt -->
    <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 w-full">
      <div class="max-w-2xl">
        <p class="text-[#D41C1C] font-bold text-xs uppercase tracking-[0.2em] mb-5">
          Ihr Autohaus in München
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

        <!-- CTA-Buttons -->
        <div class="flex flex-wrap gap-4">
          <button
            @click="emit('scrollTo', 'fahrzeuge')"
            class="bg-[#D41C1C] hover:bg-[#BB1818] text-white font-bold px-8 py-4 rounded text-base transition-colors"
          >
            Fahrzeuge entdecken
          </button>
          <button
            @click="emit('scrollTo', 'kontakt')"
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
