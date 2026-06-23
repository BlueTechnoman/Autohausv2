<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

// ── Komponenten ───────────────────────────────────────────────────────
import NavBar           from './components/NavBar.vue'
import HeroSection      from './components/HeroSection.vue'
import FahrzeugeSection from './components/FahrzeugeSection.vue'
import UeberUnsSection  from './components/UeberUnsSection.vue'
import KontaktSection   from './components/KontaktSection.vue'
import AppFooter        from './components/AppFooter.vue'

// ── Fahrzeug-Typ (wird nur für toggleCart hier gebraucht) ─────────────
interface Fahrzeug {
  id: number
  marke: string
  modell: string
}

// ── Globaler State ────────────────────────────────────────────────────
const scrolled     = ref(false)
const cart         = ref<number[]>([])
const notification = ref({ text: '', visible: false })

// ── Scroll-Listener ───────────────────────────────────────────────────
const onScroll = () => { scrolled.value = window.scrollY > 24 }
onMounted(()  => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))

// ── Toast-Notification ────────────────────────────────────────────────
let notifTimeout: ReturnType<typeof setTimeout> | null = null

function showNotification(text: string) {
  if (notifTimeout) clearTimeout(notifTimeout)
  notification.value = { text, visible: true }
  notifTimeout = setTimeout(() => {
    notification.value = { ...notification.value, visible: false }
  }, 2800)
}

// ── Warenkorb ─────────────────────────────────────────────────────────
function toggleCart(fahrzeug: Fahrzeug) {
  const inCart = cart.value.includes(fahrzeug.id)
  showNotification(
    inCart
      ? `${fahrzeug.marke} ${fahrzeug.modell} entfernt`
      : `${fahrzeug.marke} ${fahrzeug.modell} zum Warenkorb hinzugefügt`
  )
  cart.value = inCart
    ? cart.value.filter((id) => id !== fahrzeug.id)
    : [...cart.value, fahrzeug.id]
}

// ── Scroll-Navigation ─────────────────────────────────────────────────
function scrollTo(id: string) {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
}
</script>

<template>
  <div class="min-h-screen bg-background">

    <!-- Toast-Notification -->
    <div
      :class="[
        'fixed top-20 right-4 z-50 transition-all duration-300',
        notification.visible
          ? 'opacity-100 translate-y-0'
          : 'opacity-0 -translate-y-2 pointer-events-none',
      ]"
    >
      <div class="bg-[#0F2044] text-white text-sm font-medium px-4 py-3 rounded shadow-xl flex items-center gap-2.5">
        ✓ {{ notification.text }}
      </div>
    </div>

    <NavBar
      :scrolled="scrolled"
      :cartCount="cart.length"
      @scrollTo="scrollTo"
    />

    <HeroSection @scrollTo="scrollTo" />

    <FahrzeugeSection
      :cart="cart"
      @toggleCart="toggleCart"
    />

    <UeberUnsSection />
    <KontaktSection />
    <AppFooter />

  </div>
</template>
