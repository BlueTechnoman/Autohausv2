<script setup lang="ts">
import { RouterLink } from 'vue-router'
const year = new Date().getFullYear()
</script>

<template>
  <footer class="bg-[#2d3748] py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col md:flex-row items-center justify-between gap-5">

        <div class="flex items-center gap-2.5">
          <div class="w-7 h-7 bg-white/10 rounded flex items-center justify-center shrink-0">
            <span class="text-white font-bold text-xs">AH</span>
          </div>
          <span class="text-white font-semibold text-sm">AutoHaus Müller GmbH</span>
        </div>

        <p class="text-white/35 text-xs order-last md:order-none">
          © {{ year }} AutoHaus Müller GmbH · Alle Rechte vorbehalten
        </p>

        <div class="flex items-center gap-6">
          <RouterLink to="/impressum"  class="text-white/45 hover:text-white/80 text-sm transition-colors">Impressum</RouterLink>
          <RouterLink to="/datenschutz" class="text-white/45 hover:text-white/80 text-sm transition-colors">Datenschutz</RouterLink>
          <!-- AGB: RouterLink zur echten AGB-Seite -->
          <RouterLink to="/agb" class="text-white/45 hover:text-white/80 text-sm transition-colors">AGB</RouterLink>
        </div>

      </div>
    </div>
  </footer>
</template>
