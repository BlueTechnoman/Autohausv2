<script setup lang="ts">
const FOOTER_LINKS = ['Impressum', 'Datenschutz', 'AGB']
</script>

<template>
  <footer class="bg-[#07152E] py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col md:flex-row items-center justify-between gap-5">

        <!-- Logo -->
        <div class="flex items-center gap-2.5">
          <div class="w-7 h-7 bg-white/10 rounded flex items-center justify-center shrink-0">
            <span class="text-white font-bold text-xs">AH</span>
          </div>
          <span class="text-white font-semibold text-sm">AutoHaus Müller GmbH</span>
        </div>

        <!-- Copyright -->
        <p class="text-white/35 text-xs order-last md:order-none">
          © 2024 AutoHaus Müller GmbH · Alle Rechte vorbehalten
        </p>

        <!-- Links -->
        <div class="flex items-center gap-6">
          <button
            v-for="link in FOOTER_LINKS"
            :key="link"
            class="text-white/45 hover:text-white/80 text-sm transition-colors"
          >
            {{ link }}
          </button>
        </div>

      </div>
    </div>
  </footer>
</template>
