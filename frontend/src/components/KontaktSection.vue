<script setup lang="ts">
import { Phone, MapPin, Clock, Mail, ExternalLink } from 'lucide-vue-next'

const OEFFNUNGSZEITEN: [string, string][] = [
  ['Mo – Fr',  '09:00 – 18:30'],
  ['Samstag',  '10:00 – 16:00'],
  ['Sonntag',  'Geschlossen'],
]

// Vorgefertigte E-Mail: öffnet E-Mail-Programm mit vorausgefülltem Betreff + Text
const MAIL_HREF = `mailto:info@autohaus-mueller.de?subject=${encodeURIComponent('Anfrage – AutoHaus Müller Bayreuth')}&body=${encodeURIComponent('Guten Tag,\n\nich interessiere mich für ein Fahrzeug aus Ihrem Bestand.\n\nMit freundlichen Grüßen\n')}`

// Google Maps Link zur Adresse
const MAPS_HREF = 'https://www.google.com/maps/search/?api=1&query=Amselstra%C3%9Fe+1B+95444+Bayreuth'
</script>

<template>
  <section id="kontakt" class="py-16 bg-background">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

      <div class="mb-10">
        <h2 class="text-[#1a2e5a] text-3xl font-bold mb-1">Kontakt & Anfahrt</h2>
        <p class="text-[#8e9aaa] text-sm">Wir freuen uns auf Ihren Besuch - persönlich oder telefonisch.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">

        <!-- Adresse + Google Maps -->
        <div class="bg-white rounded-lg p-6 shadow-sm border border-[#1a2e5a]/8">
          <div class="w-11 h-11 bg-[#1a2e5a] rounded flex items-center justify-center mb-5">
            <MapPin :size="18" class="text-white" />
          </div>
          <h3 class="text-[#1a2e5a] font-bold text-base mb-3">Adresse</h3>
          <p class="text-[#8e9aaa] text-sm leading-relaxed mb-4">
            Amselstraße 1B<br />
            95444 Bayreuth<br />
            Deutschland
          </p>
          <!-- Google Maps Link -->
          <a
            :href="MAPS_HREF"
            target="_blank"
            rel="noopener noreferrer"
            class="inline-flex items-center gap-2 text-[#e85c1a] hover:underline text-sm font-semibold"
          >
            <ExternalLink :size="13" />
            In Google Maps öffnen
          </a>
        </div>

        <!-- Telefon & E-Mail -->
        <div class="bg-white rounded-lg p-6 shadow-sm border border-[#1a2e5a]/8">
          <div class="w-11 h-11 bg-[#1a2e5a] rounded flex items-center justify-center mb-5">
            <Phone :size="18" class="text-white" />
          </div>
          <h3 class="text-[#1a2e5a] font-bold text-base mb-3">Telefon & E-Mail</h3>
          <div class="space-y-2 mb-5">
            <a href="tel:+499211234567" class="flex items-center gap-2 text-[#8e9aaa] hover:text-[#e85c1a] transition-colors text-sm">
              <Phone :size="13" class="shrink-0" /> 0921 123 456
            </a>
            <!-- E-Mail öffnet Mailprogramm mit vorgefülltem Betreff -->
            <a :href="MAIL_HREF" class="flex items-center gap-2 text-[#8e9aaa] hover:text-[#e85c1a] transition-colors text-sm">
              <Mail :size="13" class="shrink-0" /> info@autohaus-mueller.de
            </a>
          </div>
          <div class="flex flex-col gap-2">
            <a
              href="tel:+499211234567"
              class="inline-flex items-center justify-center gap-2 bg-[#e85c1a] hover:bg-[#d44e12] text-white text-sm font-bold px-5 py-2.5 rounded transition-colors"
            >
              <Phone :size="13" /> Jetzt anrufen
            </a>
            <a
              :href="MAIL_HREF"
              class="inline-flex items-center justify-center gap-2 border border-[#1a2e5a]/20 text-[#1a2e5a] hover:bg-[#1a2e5a]/5 text-sm font-semibold px-5 py-2.5 rounded transition-colors"
            >
              <Mail :size="13" /> E-Mail schreiben
            </a>
          </div>
        </div>

        <!-- Öffnungszeiten -->
        <div class="bg-white rounded-lg p-6 shadow-sm border border-[#1a2e5a]/8">
          <div class="w-11 h-11 bg-[#1a2e5a] rounded flex items-center justify-center mb-5">
            <Clock :size="18" class="text-white" />
          </div>
          <h3 class="text-[#1a2e5a] font-bold text-base mb-3">Öffnungszeiten</h3>
          <table class="w-full text-sm">
            <tbody>
              <tr v-for="[day, time] in OEFFNUNGSZEITEN" :key="day">
                <td class="font-semibold text-[#1a2e5a] pr-4 py-1">{{ day }}</td>
                <td class="text-[#8e9aaa]">{{ time }}</td>
              </tr>
            </tbody>
          </table>
        </div>

      </div>
    </div>
  </section>
</template>
