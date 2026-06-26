<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterView } from 'vue-router'
import { useNotification } from './composables/useNotification'
import CookieBanner from './components/CookieBanner.vue'

const { text, visible } = useNotification()

// ── Konami Code Easter Egg ────────────────────────────────────────────
// Eingabe: ↑ ↑ ↓ ↓ ← → ← → B A → Sonic rennt über den Bildschirm
const KONAMI = ['ArrowUp','ArrowUp','ArrowDown','ArrowDown',
                'ArrowLeft','ArrowRight','ArrowLeft','ArrowRight','b','a']
const progress    = ref(0)
const sonicActive = ref(false)
const sonicPhase  = ref<'start'|'slow'|'fast'>('start')

function onKeyDown(e: KeyboardEvent) {
  if (e.key === KONAMI[progress.value]) {
    progress.value++
    if (progress.value === KONAMI.length) {
      progress.value = 0
      triggerSonic()
    }
  } else {
    progress.value = 0
  }
}

function triggerSonic() {
  if (sonicActive.value) return
  sonicActive.value = true
  sonicPhase.value  = 'start'
  // Nach 1.5s: läuft
  setTimeout(() => { sonicPhase.value = 'slow' }, 1500)
  // Nach 3s: rennt schnell
  setTimeout(() => { sonicPhase.value = 'fast' }, 3000)
  // Nach 6s: verschwindet
  setTimeout(() => { sonicActive.value = false  }, 6000)
}

onMounted(()  => window.addEventListener('keydown', onKeyDown))
onUnmounted(() => window.removeEventListener('keydown', onKeyDown))
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

    <!-- Sonic Easter Egg: erscheint nach Konami-Code ↑↑↓↓←→←→BA -->
    <div
      v-if="sonicActive"
      class="fixed bottom-6 z-[9999] pointer-events-none sonic-run"
    >
      <img
        :src="sonicPhase === 'start'
          ? '/sonic/sonic_running_start.gif'
          : sonicPhase === 'slow'
          ? '/sonic/sonic_running_slow.gif'
          : '/sonic/sonic_running_fast.gif'"
        alt=""
        style="image-rendering: pixelated; width: 64px; height: 64px;"
      />
    </div>

  </div>
</template>

<style scoped>
/* Sonic rennt von rechts nach links in 6 Sekunden, gespiegelt */
.sonic-run {
  animation: sonic-across 6s linear forwards;
  transform: scaleX(-1);
}
@keyframes sonic-across {
  from { right: -80px; }
  to   { right: 110vw; }
}
</style>