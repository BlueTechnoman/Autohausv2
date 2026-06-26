<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterView } from 'vue-router'
import { useNotification } from './composables/useNotification'
import CookieBanner from './components/CookieBanner.vue'

const { text, visible } = useNotification()

// Konami Code Sonic Easter Egg 
const KONAMI = ['ArrowUp','ArrowUp','ArrowDown','ArrowDown',
                'ArrowLeft','ArrowRight','ArrowLeft','ArrowRight','b','a']
const progress    = ref(0)
const sonicActive = ref(false)
const sonicPhase  = ref<'start'|'slow'|'fast'>('start')
const sonicRight  = ref(-80)

let animFrame: number
let startTime: number

// Geschwindigkeit pro Phase in px/sekunde
const SPEED = { start: 60, slow: 120, fast: 600 }

function animate(ts: number) {
  if (!startTime) startTime = ts
  const elapsed = (ts - startTime) / 1000

  // start: 0 – 2500ms | slow: 2500 – 7000ms | fast: 7000ms+
  if (elapsed < 2.5)      sonicPhase.value = 'start'
  else if (elapsed < 5.0) sonicPhase.value = 'slow'
  else                    sonicPhase.value = 'fast'

  const speed = SPEED[sonicPhase.value]
  sonicRight.value += speed * (1 / 60)

  if (sonicRight.value > window.innerWidth + 80) {
    sonicActive.value = false
    sonicRight.value  = -80
    return
  }
  animFrame = requestAnimationFrame(animate)
}

function triggerSonic() {
  if (sonicActive.value) return
  sonicActive.value = true
  sonicPhase.value  = 'start'
  sonicRight.value  = -80
  startTime         = 0
  animFrame         = requestAnimationFrame(animate)
}

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

onMounted(()  => window.addEventListener('keydown', onKeyDown))
onUnmounted(() => {
  window.removeEventListener('keydown', onKeyDown)
  cancelAnimationFrame(animFrame)
})
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

    <!-- Sonic Easter Egg: kommt von rechts, läuft nach links -->
    <div
      v-if="sonicActive"
      class="fixed bottom-6 z-[9999] pointer-events-none"
      :style="{ right: sonicRight + 'px' }"
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
/* Position wird per JavaScript gesteuert – kein CSS-Animation */
</style>