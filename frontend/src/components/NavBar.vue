<!--
  NavBar.vue – Globale Navigationsleiste
  ════════════════════════════════════════
  Erscheint auf jeder Seite (eingebunden in jede Page-Komponente).

  Besonderheiten:
    • Scrolled-Effekt: Hintergrund wird bei scroll > 24px sichtbarer
    • Reaktiv auf Login-Status: Dashboard-Link nur für eingeloggte User
    • Router-Integration: Klicks navigieren via vue-router (kein Reload)
    • Hash-Navigation: "Fahrzeuge" scrollt auf #fahrzeuge egal wo man ist
    • Warenkorb-Badge: Zeigt Anzahl vorgemerkter Fahrzeuge

  Props:
    scrolled: boolean – ob Seite gescrollt ist (kommt von der Page-Komponente)
-->
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Phone, ShoppingCart, Menu, X, User, LayoutDashboard } from 'lucide-vue-next'
import { useCart } from '../composables/useCart'
import { useAuth } from '../composables/useAuth'

defineProps<{ scrolled: boolean }>()

const router = useRouter()
const route  = useRoute()
const { cartCount }  = useCart()
const { isLoggedIn, user } = useAuth()

const mobileMenuOpen = ref(false)

// ── Navigation-Handler ────────────────────────────────────────────────

function goHome() {
  router.push('/')
  mobileMenuOpen.value = false
}

async function handleNav(target: string) {
  mobileMenuOpen.value = false
  if (target === 'ueber-uns-page') { router.push('/ueber-uns'); return }
  if (target === 'dashboard')      { router.push('/dashboard'); return }

  // Scroll-Ziele: wenn schon auf '/', direkt scrollen; sonst erst navigieren
  if (route.path === '/') {
    document.getElementById(target)?.scrollIntoView({ behavior: 'smooth' })
  } else {
    await router.push({ path: '/', hash: `#${target}` })
  }
}

function goCart()  { router.push('/warenkorb'); mobileMenuOpen.value = false }
function goLogin() { router.push('/login');     mobileMenuOpen.value = false }
</script>

<template>
  <nav
    :class="[
      'fixed top-0 inset-x-0 z-40 transition-all duration-200',
      scrolled ? 'bg-white shadow-md' : 'bg-white border-b border-[#1a2e5a]/8',
    ]"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">

        <!-- Logo -->
        <button @click="goHome" class="flex items-center gap-2.5">
          <div class="w-8 h-8 bg-[#1a2e5a] rounded flex items-center justify-center shrink-0">
            <span class="text-white font-bold text-xs tracking-tight">AH</span>
          </div>
          <div class="text-left">
            <div class="font-bold text-[#1a2e5a] text-base leading-none">AutoHaus Müller</div>
            <div class="text-[10px] text-[#8e9aaa] leading-none mt-0.5 uppercase tracking-wider">Bayreuth</div>
          </div>
        </button>

        <!-- Desktop-Links -->
        <div class="hidden md:flex items-center gap-8">
          <button @click="handleNav('fahrzeuge')"
            class="text-[#1a2e5a]/80 hover:text-[#e85c1a] font-semibold text-sm transition-colors">
            Fahrzeuge
          </button>
          <button @click="handleNav('ueber-uns-page')"
            :class="['font-semibold text-sm transition-colors',
              $route.path === '/ueber-uns' ? 'text-[#e85c1a]' : 'text-[#1a2e5a]/80 hover:text-[#e85c1a]']">
            Über uns
          </button>
          <button @click="handleNav('kontakt')"
            class="text-[#1a2e5a]/80 hover:text-[#e85c1a] font-semibold text-sm transition-colors">
            Kontakt
          </button>
          <!-- Dashboard-Link: nur für eingeloggte Nutzer -->
          <button v-if="isLoggedIn" @click="handleNav('dashboard')"
            :class="['font-semibold text-sm transition-colors flex items-center gap-1.5',
              $route.path === '/dashboard' ? 'text-[#e85c1a]' : 'text-[#1a2e5a]/80 hover:text-[#e85c1a]']">
            <LayoutDashboard :size="14" /> Mein Bereich
          </button>
        </div>

        <!-- Telefon + Aktions-Icons -->
        <div class="hidden md:flex items-center gap-4">
          <a href="tel:+499211234567"
            class="flex items-center gap-2 text-[#1a2e5a] font-semibold text-sm hover:text-[#e85c1a] transition-colors">
            <Phone :size="14" /> 0921 123 456
          </a>

          <!-- Login-Icon (zeigt Benutzername wenn eingeloggt) -->
          <button @click="goLogin"
            :class="['flex items-center gap-1.5 w-auto px-3 h-9 border rounded-full transition-colors text-xs font-semibold',
              $route.path === '/login' ? 'border-[#e85c1a] bg-[#e85c1a]/8 text-[#e85c1a]'
                : isLoggedIn ? 'border-green-300 bg-green-50 text-green-700'
                : 'border-[#1a2e5a]/20 hover:bg-[#1a2e5a]/5 text-[#1a2e5a]']"
            aria-label="Anmelden"
          >
            <User :size="14" />
            <span v-if="isLoggedIn">{{ user?.username }}</span>
            <span v-else>Login</span>
          </button>

          <!-- Warenkorb-Icon mit Badge -->
          <button @click="goCart"
            :class="['relative w-9 h-9 flex items-center justify-center border rounded-full transition-colors',
              $route.path === '/warenkorb' ? 'border-[#e85c1a] bg-[#e85c1a]/8' : 'border-[#1a2e5a]/20 hover:bg-[#1a2e5a]/5']"
            aria-label="Warenkorb">
            <ShoppingCart :size="16" class="text-[#1a2e5a]" />
            <span v-if="cartCount > 0"
              class="absolute -top-1 -right-1 w-4 h-4 bg-[#e85c1a] text-white text-[9px] font-bold rounded-full flex items-center justify-center">
              {{ cartCount }}
            </span>
          </button>
        </div>

        <!-- Mobile: Cart + Hamburger -->
        <div class="md:hidden flex items-center gap-2">
          <button @click="goCart" class="relative w-9 h-9 flex items-center justify-center border border-[#1a2e5a]/20 rounded-full">
            <ShoppingCart :size="16" class="text-[#1a2e5a]" />
            <span v-if="cartCount > 0"
              class="absolute -top-1 -right-1 w-4 h-4 bg-[#e85c1a] text-white text-[9px] font-bold rounded-full flex items-center justify-center">
              {{ cartCount }}
            </span>
          </button>
          <button class="p-2 text-[#1a2e5a]" @click="mobileMenuOpen = !mobileMenuOpen">
            <X v-if="mobileMenuOpen" :size="22" /><Menu v-else :size="22" />
          </button>
        </div>

      </div>
    </div>

    <!-- Mobile-Menü -->
    <div v-if="mobileMenuOpen" class="md:hidden bg-white border-t border-[#1a2e5a]/10 px-4 py-4 space-y-1">
      <button @click="handleNav('fahrzeuge')" class="block w-full text-left text-[#1a2e5a] font-semibold py-2.5 text-sm">Fahrzeuge</button>
      <button @click="handleNav('ueber-uns-page')" class="block w-full text-left text-[#1a2e5a] font-semibold py-2.5 text-sm">Über uns</button>
      <button @click="handleNav('kontakt')" class="block w-full text-left text-[#1a2e5a] font-semibold py-2.5 text-sm">Kontakt</button>
      <button v-if="isLoggedIn" @click="handleNav('dashboard')" class="block w-full text-left text-[#e85c1a] font-semibold py-2.5 text-sm flex items-center gap-2">
        <LayoutDashboard :size="14" /> Mein Bereich
      </button>
      <button @click="goLogin" class="block w-full text-left text-[#1a2e5a] font-semibold py-2.5 text-sm">
        {{ isLoggedIn ? user?.username + ' (angemeldet)' : 'Anmelden / Registrieren' }}
      </button>
      <a href="tel:+499211234567" class="flex items-center gap-2 text-[#1a2e5a] font-semibold py-2.5 text-sm">
        <Phone :size="14" /> 0921 123 456
      </a>
    </div>
  </nav>
</template>
