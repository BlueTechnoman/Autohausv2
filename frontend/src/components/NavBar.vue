<script setup lang="ts">
import { ref } from 'vue'
import { Phone, ShoppingCart, Menu, X } from 'lucide-vue-next'

// ── Props ────────────────────────────────────────────────────────────
const props = defineProps<{
  scrolled: boolean
  cartCount: number
}>()

// ── Emits ────────────────────────────────────────────────────────────
const emit = defineEmits<{
  scrollTo: [id: string]
}>()

// ── Lokaler State ────────────────────────────────────────────────────
const mobileMenuOpen = ref(false)

const NAV_LINKS: [string, string][] = [
  ['fahrzeuge', 'Fahrzeuge'],
  ['ueber-uns', 'Über uns'],
  ['kontakt', 'Kontakt'],
]

function handleNav(id: string) {
  emit('scrollTo', id)
  mobileMenuOpen.value = false
}
</script>

<template>
  <nav
    :class="[
      'fixed top-0 inset-x-0 z-40 transition-all duration-200',
      scrolled ? 'bg-white shadow-md' : 'bg-white border-b border-[#0F2044]/8',
    ]"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">

        <!-- Logo -->
        <button @click="handleNav('hero')" class="flex items-center gap-2.5">
          <div class="w-8 h-8 bg-[#0F2044] rounded flex items-center justify-center shrink-0">
            <span class="text-white font-bold text-xs tracking-tight">AH</span>
          </div>
          <div class="text-left">
            <div class="font-bold text-[#0F2044] text-base leading-none">AutoHaus Müller</div>
            <div class="text-[10px] text-[#6B7585] leading-none mt-0.5 uppercase tracking-wider">München</div>
          </div>
        </button>

        <!-- Desktop-Links -->
        <div class="hidden md:flex items-center gap-8">
          <button
            v-for="[id, label] in NAV_LINKS"
            :key="id"
            @click="handleNav(id)"
            class="text-[#0F2044]/80 hover:text-[#D41C1C] font-semibold text-sm transition-colors"
          >
            {{ label }}
          </button>
        </div>

        <!-- Telefon + Warenkorb -->
        <div class="hidden md:flex items-center gap-5">
          <a
            href="tel:+4989123456789"
            class="flex items-center gap-2 text-[#0F2044] font-semibold text-sm hover:text-[#D41C1C] transition-colors"
          >
            <Phone :size="14" />
            089 123 456 789
          </a>
          <button
            @click="handleNav('fahrzeuge')"
            class="relative w-9 h-9 flex items-center justify-center border border-[#0F2044]/20 rounded-full hover:bg-[#0F2044]/5 transition-colors"
            aria-label="Warenkorb"
          >
            <ShoppingCart :size="16" class="text-[#0F2044]" />
            <span
              v-if="cartCount > 0"
              class="absolute -top-1 -right-1 w-4 h-4 bg-[#D41C1C] text-white text-[9px] font-bold rounded-full flex items-center justify-center"
            >
              {{ cartCount }}
            </span>
          </button>
        </div>

        <!-- Mobile-Toggle -->
        <button
          class="md:hidden p-2 text-[#0F2044]"
          @click="mobileMenuOpen = !mobileMenuOpen"
          aria-label="Menü"
        >
          <X v-if="mobileMenuOpen" :size="22" />
          <Menu v-else :size="22" />
        </button>

      </div>
    </div>

    <!-- Mobile-Menü -->
    <div
      v-if="mobileMenuOpen"
      class="md:hidden bg-white border-t border-[#0F2044]/10 px-4 py-4 space-y-1"
    >
      <button
        v-for="[id, label] in NAV_LINKS"
        :key="id"
        @click="handleNav(id)"
        class="block w-full text-left text-[#0F2044] font-semibold py-2.5 text-sm"
      >
        {{ label }}
      </button>
      <a
        href="tel:+4989123456789"
        class="flex items-center gap-2 text-[#0F2044] font-semibold py-2.5 text-sm"
      >
        <Phone :size="14" />
        089 123 456 789
      </a>
    </div>
  </nav>
</template>
