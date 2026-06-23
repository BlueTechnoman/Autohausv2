<script setup lang="ts">
import { Check } from 'lucide-vue-next'

const PUNKTE = [
  'TÜV-geprüfte Fahrzeuge',
  'Finanzierungsberatung vor Ort',
  'Inzahlungnahme Ihres Altfahrzeugs',
  '12 Monate Gebrauchtwagengarantie',
]
</script>

<template>
  <section id="ueber-uns" class="py-16 bg-[#0F2044]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">

        <!-- Text-Spalte -->
        <div>
          <p class="text-[#D41C1C] font-bold text-xs uppercase tracking-[0.2em] mb-4">Über uns</p>
          <h2 class="text-white font-bold text-4xl leading-tight mb-6">
            Seit 2009 Ihr<br />verlässlicher Partner.
          </h2>
          <p class="text-white/65 text-base leading-relaxed mb-8">
            AutoHaus Müller steht seit über 15 Jahren für Seriosität, Transparenz und erstklassigen
            Service im Fahrzeughandel. Ob gepflegter Jahreswagen oder Familienauto — wir begleiten
            Sie vom ersten Gespräch bis zur Übergabe.
          </p>
          <ul class="space-y-3.5">
            <li
              v-for="punkt in PUNKTE"
              :key="punkt"
              class="flex items-center gap-3 text-white/75 text-sm"
            >
              <span class="w-5 h-5 border border-[#D41C1C]/50 bg-[#D41C1C]/15 rounded-full flex items-center justify-center shrink-0">
                <Check :size="10" class="text-[#D41C1C]" />
              </span>
              {{ punkt }}
            </li>
          </ul>
        </div>

        <!-- Bild-Spalte -->
        <div class="relative rounded-lg overflow-hidden aspect-[4/3] bg-[#0A1836]">
          <img
            src="https://images.unsplash.com/photo-1574023240744-64c47c8c0676?w=900&h=675&fit=crop&auto=format"
            alt="AutoHaus Müller Außenansicht"
            class="w-full h-full object-cover opacity-60"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-[#0F2044]/60 to-transparent" />
        </div>

      </div>
    </div>
  </section>
</template>
