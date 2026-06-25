<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useNotification } from './composables/useNotification'
import CookieBanner from './components/CookieBanner.vue'

const { text, visible } = useNotification()
</script>

<template>
  <div class="min-h-screen bg-background">

    <!-- Globale Toast-Notification -->
    <div
      :class="[
        'fixed top-20 right-4 z-[100] transition-all duration-300',
        visible
          ? 'opacity-100 translate-y-0'
          : 'opacity-0 -translate-y-2 pointer-events-none',
      ]"
    >
      <div class="bg-[#1a2e5a] text-white text-sm font-medium px-4 py-3 rounded shadow-xl flex items-center gap-2.5">
        <span class="text-[#e85c1a]">✓</span>
        {{ text }}
      </div>
    </div>

    <RouterView />

    <CookieBanner />

  </div>
</template>
