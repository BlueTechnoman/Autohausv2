<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Phone, ShoppingCart, Menu, X, User, LayoutDashboard, Calendar, MessageSquare, Plus } from 'lucide-vue-next'
import { useCart } from '../composables/useCart'
import { useAuth } from '../composables/useAuth'

defineProps<{ scrolled: boolean }>()

const router = useRouter()
const route  = useRoute()
const { cartCount }             = useCart()
const { isLoggedIn, user }      = useAuth()

// Rollen-Checks
const isAdmin    = () => user.value?.role === 'admin'
const isEmployee = () => user.value?.role === 'employee' || user.value?.role === 'admin'

const mobileMenuOpen = ref(false)

function goHome() { router.push('/'); mobileMenuOpen.value = false }

async function handleNav(target: string) {
  mobileMenuOpen.value = false
  if (target.startsWith('/')) { router.push(target); return }
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
  <nav :class="['fixed top-0 inset-x-0 z-40 transition-all duration-200', scrolled ? 'bg-white shadow-md' : 'bg-white border-b border-[#1a2e5a]/8']">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">

        <!-- Logo -->
        <button @click="goHome" class="flex items-center gap-2.5">
          <div class="w-8 h-8 bg-[#1a2e5a] rounded flex items-center justify-center shrink-0">
            <span class="text-white font-bold text-xs">AH</span>
          </div>
          <div class="text-left">
            <div class="font-bold text-[#1a2e5a] text-base leading-none">AutoHaus Müller</div>
            <div class="text-[10px] text-[#8e9aaa] leading-none mt-0.5 uppercase tracking-wider">Bayreuth</div>
          </div>
        </button>

        <!-- Desktop Links -->
        <div class="hidden md:flex items-center gap-6">
          <button @click="handleNav('fahrzeuge')"    class="text-[#1a2e5a]/80 hover:text-[#e85c1a] font-semibold text-sm transition-colors">Fahrzeuge</button>
          <button @click="handleNav('/ueber-uns')"   class="text-[#1a2e5a]/80 hover:text-[#e85c1a] font-semibold text-sm transition-colors">Über uns</button>
          <button @click="handleNav('kontakt')"      class="text-[#1a2e5a]/80 hover:text-[#e85c1a] font-semibold text-sm transition-colors">Kontakt</button>
          <!-- Eingeloggt: Dashboard + Termine -->
          <template v-if="isLoggedIn">
            <button @click="handleNav('/dashboard')"  class="font-semibold text-sm transition-colors flex items-center gap-1.5" :class="$route.path === '/dashboard' ? 'text-[#e85c1a]' : 'text-[#1a2e5a]/80 hover:text-[#e85c1a]'">
              <LayoutDashboard :size="14" /> Mein Bereich
            </button>
            <button @click="handleNav('/termine')"  class="font-semibold text-sm transition-colors flex items-center gap-1.5" :class="$route.path === '/termine' ? 'text-[#e85c1a]' : 'text-[#1a2e5a]/80 hover:text-[#e85c1a]'">
              <Calendar :size="14" /> Termine
            </button>
          </template>
          <!-- Admin/Employee: Anfragen + Fahrzeug anlegen -->
          <template v-if="isEmployee()">
            <button @click="handleNav('/anfragen')" class="font-semibold text-sm transition-colors flex items-center gap-1.5" :class="$route.path === '/anfragen' ? 'text-[#e85c1a]' : 'text-[#1a2e5a]/80 hover:text-[#e85c1a]'">
              <MessageSquare :size="14" /> Anfragen
            </button>
            <button @click="handleNav('/fahrzeug-anlegen')" class="font-semibold text-sm transition-colors flex items-center gap-1.5" :class="$route.path === '/fahrzeug-anlegen' ? 'text-[#e85c1a]' : 'text-[#1a2e5a]/80 hover:text-[#e85c1a]'">
              <Plus :size="14" /> Anlegen
            </button>
          </template>
        </div>

        <!-- Rechts: Telefon + Login + Cart -->
        <div class="hidden md:flex items-center gap-4">
          <a href="tel:+499211234567" class="flex items-center gap-2 text-[#1a2e5a] font-semibold text-sm hover:text-[#e85c1a] transition-colors">
            <Phone :size="14" /> 0921 123 456
          </a>
          <button @click="goLogin"
            :class="['flex items-center gap-1.5 px-3 h-9 border rounded-full transition-colors text-xs font-semibold',
              isLoggedIn ? 'border-green-300 bg-green-50 text-green-700' : 'border-[#1a2e5a]/20 hover:bg-[#1a2e5a]/5 text-[#1a2e5a]']">
            <User :size="14" />
            <span v-if="isLoggedIn">{{ user?.username }}</span>
            <span v-else>Login</span>
          </button>
          <button @click="goCart"
            class="relative w-9 h-9 flex items-center justify-center border border-[#1a2e5a]/20 hover:bg-[#1a2e5a]/5 rounded-full transition-colors">
            <ShoppingCart :size="16" class="text-[#1a2e5a]" />
            <span v-if="cartCount > 0"
              class="absolute -top-1 -right-1 w-4 h-4 bg-[#e85c1a] text-white text-[9px] font-bold rounded-full flex items-center justify-center">
              {{ cartCount }}
            </span>
          </button>
        </div>

        <!-- Mobile -->
        <div class="md:hidden flex items-center gap-2">
          <button @click="goCart" class="relative w-9 h-9 flex items-center justify-center border border-[#1a2e5a]/20 rounded-full">
            <ShoppingCart :size="16" class="text-[#1a2e5a]" />
            <span v-if="cartCount > 0" class="absolute -top-1 -right-1 w-4 h-4 bg-[#e85c1a] text-white text-[9px] font-bold rounded-full flex items-center justify-center">{{ cartCount }}</span>
          </button>
          <button class="p-2 text-[#1a2e5a]" @click="mobileMenuOpen = !mobileMenuOpen">
            <X v-if="mobileMenuOpen" :size="22" /><Menu v-else :size="22" />
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Menü -->
    <div v-if="mobileMenuOpen" class="md:hidden bg-white border-t border-[#1a2e5a]/10 px-4 py-4 space-y-1">
      <button @click="handleNav('fahrzeuge')"   class="block w-full text-left text-[#1a2e5a] font-semibold py-2.5 text-sm">Fahrzeuge</button>
      <button @click="handleNav('/ueber-uns')"  class="block w-full text-left text-[#1a2e5a] font-semibold py-2.5 text-sm">Über uns</button>
      <button @click="handleNav('kontakt')"     class="block w-full text-left text-[#1a2e5a] font-semibold py-2.5 text-sm">Kontakt</button>
      <template v-if="isLoggedIn">
        <button @click="handleNav('/dashboard')" class="block w-full text-left text-[#e85c1a] font-semibold py-2.5 text-sm flex items-center gap-2"><LayoutDashboard :size="14" /> Mein Bereich</button>
        <button @click="handleNav('/termine')"   class="block w-full text-left text-[#1a2e5a] font-semibold py-2.5 text-sm flex items-center gap-2"><Calendar :size="14" /> Termine</button>
      </template>
      <template v-if="isEmployee()">
        <button @click="handleNav('/anfragen')"          class="block w-full text-left text-[#1a2e5a] font-semibold py-2.5 text-sm flex items-center gap-2"><MessageSquare :size="14" /> Anfragen</button>
        <button @click="handleNav('/fahrzeug-anlegen')"  class="block w-full text-left text-[#1a2e5a] font-semibold py-2.5 text-sm flex items-center gap-2"><Plus :size="14" /> Fahrzeug anlegen</button>
      </template>
      <button @click="goLogin" class="block w-full text-left text-[#1a2e5a] font-semibold py-2.5 text-sm">
        {{ isLoggedIn ? user?.username + ' (angemeldet)' : 'Anmelden / Registrieren' }}
      </button>
      <a href="tel:+499211234567" class="flex items-center gap-2 text-[#1a2e5a] font-semibold py-2.5 text-sm"><Phone :size="14" /> 0921 123 456</a>
    </div>
  </nav>
</template>
