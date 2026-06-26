<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { Cookie, Settings, X, Shield, BarChart2, Megaphone } from 'lucide-vue-next'
import { useCookieConsent } from '../composables/useCookieConsent'

const { showBanner, accept, reject, saveCustom } = useCookieConsent()

const showSettings   = ref(false)
const localAnalytics = ref(false)
const localMarketing = ref(false)

function openSettings() {
  showSettings.value = true
}

function saveSelection() {
  saveCustom(localAnalytics.value, localMarketing.value)
  showSettings.value = false
}
</script>

<template>
  <!-- Backdrop wenn Einstellungen offen -->
  <Transition name="fade">
    <div
      v-if="showBanner && showSettings"
      class="fixed inset-0 bg-black/50 z-[90]"
      @click="showSettings = false"
    />
  </Transition>

  <!-- Einstellungs-Modal -->
  <Transition name="slide-up">
    <div
      v-if="showBanner && showSettings"
      class="fixed inset-x-4 bottom-4 md:inset-x-auto md:left-1/2 md:-translate-x-1/2 md:w-full md:max-w-xl
             bg-white rounded-xl shadow-2xl z-[91] overflow-hidden"
    >
      <!-- Header -->
      <div class="bg-[#1a2e5a] px-6 py-4 flex items-center justify-between">
        <div class="flex items-center gap-2.5">
          <Settings :size="18" class="text-white/80" />
          <h3 class="text-white font-bold text-base">Cookie-Einstellungen</h3>
        </div>
        <button @click="showSettings = false" class="text-white/60 hover:text-white transition-colors">
          <X :size="18" />
        </button>
      </div>

      <!-- Body -->
      <div class="px-6 py-5 space-y-4">

        <!-- Notwendige Cookies (immer aktiv) -->
        <div class="flex items-start justify-between gap-4 p-4 bg-[#f8f9fa] rounded-lg">
          <div class="flex gap-3">
            <Shield :size="18" class="text-[#1a2e5a] shrink-0 mt-0.5" />
            <div>
              <div class="font-bold text-[#1a2e5a] text-sm">Notwendige Cookies</div>
              <div class="text-[#8e9aaa] text-xs mt-1 leading-relaxed">
                Erforderlich für Grundfunktionen der Website (Session, Cookie-Einstellungen). Können nicht deaktiviert werden.
              </div>
            </div>
          </div>
          <span class="text-xs font-bold text-[#1a2e5a]/40 whitespace-nowrap mt-0.5">Immer aktiv</span>
        </div>

        <!-- Analyse-Cookies -->
        <div class="flex items-start justify-between gap-4 p-4 border border-[#1a2e5a]/10 rounded-lg">
          <div class="flex gap-3">
            <BarChart2 :size="18" class="text-[#1a2e5a] shrink-0 mt-0.5" />
            <div>
              <div class="font-bold text-[#1a2e5a] text-sm">Analyse-Cookies</div>
              <div class="text-[#8e9aaa] text-xs mt-1 leading-relaxed">
                Helfen uns, die Nutzung der Website zu verstehen und das Angebot zu verbessern (z.B. Google Analytics).
              </div>
            </div>
          </div>
          <!-- Toggle -->
          <button
            @click="localAnalytics = !localAnalytics"
            :class="[
              'relative w-11 h-6 rounded-full transition-colors shrink-0 mt-0.5',
              localAnalytics ? 'bg-[#e85c1a]' : 'bg-[#1a2e5a]/20',
            ]"
            :aria-checked="localAnalytics"
            role="switch"
          >
            <span
              :class="[
                'absolute top-0.5 w-5 h-5 bg-white rounded-full shadow transition-all duration-200',
                localAnalytics ? 'left-[22px]' : 'left-[2px]',
              ]"
            />
          </button>
        </div>

        <!-- Marketing-Cookies -->
        <div class="flex items-start justify-between gap-4 p-4 border border-[#1a2e5a]/10 rounded-lg">
          <div class="flex gap-3">
            <Megaphone :size="18" class="text-[#1a2e5a] shrink-0 mt-0.5" />
            <div>
              <div class="font-bold text-[#1a2e5a] text-sm">Marketing-Cookies</div>
              <div class="text-[#8e9aaa] text-xs mt-1 leading-relaxed">
                Werden verwendet, um Ihnen relevante Werbeanzeigen anzuzeigen und die Effektivität von Kampagnen zu messen.
              </div>
            </div>
          </div>
          <!-- Toggle -->
          <button
            @click="localMarketing = !localMarketing"
            :class="[
              'relative w-11 h-6 rounded-full transition-colors shrink-0 mt-0.5',
              localMarketing ? 'bg-[#e85c1a]' : 'bg-[#1a2e5a]/20',
            ]"
            :aria-checked="localMarketing"
            role="switch"
          >
            <span
              :class="[
                'absolute top-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform',
                localMarketing ? 'translate-x-5' : 'translate-x-0.5',
              ]"
            />
          </button>
        </div>

      </div>

      <!-- Footer Buttons -->
      <div class="px-6 pb-5 flex flex-col sm:flex-row gap-3">
        <button
          @click="saveSelection"
          class="flex-1 bg-[#1a2e5a] hover:bg-[#1a2e5a]/85 text-white font-bold text-sm py-3 rounded transition-colors"
        >
          Auswahl speichern
        </button>
        <button
          @click="accept"
          class="flex-1 bg-[#e85c1a] hover:bg-[#d44e12] text-white font-bold text-sm py-3 rounded transition-colors"
        >
          Alle akzeptieren
        </button>
      </div>
    </div>
  </Transition>

  <!-- ── Haupt-Banner (unten) ── -->
  <Transition name="slide-up">
    <div
      v-if="showBanner && !showSettings"
      class="fixed bottom-0 inset-x-0 z-[90] bg-white border-t border-[#1a2e5a]/12 shadow-2xl"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex flex-col md:flex-row md:items-center gap-4">

          <!-- Icon + Text -->
          <div class="flex gap-3 flex-1 min-w-0">
            <div class="w-9 h-9 bg-[#1a2e5a] rounded flex items-center justify-center shrink-0 mt-0.5">
              <Cookie :size="16" class="text-white" />
            </div>
            <div>
              <p class="text-[#1a2e5a] font-bold text-sm">Diese Website verwendet Cookies</p>
              <p class="text-[#8e9aaa] text-xs mt-0.5 leading-relaxed">
                Wir nutzen Cookies, um Ihnen die bestmögliche Nutzererfahrung zu bieten und unsere Website
                kontinuierlich zu verbessern. Mehr dazu in unserer
                <RouterLink to="/datenschutz" class="underline hover:text-[#e85c1a] transition-colors">
                  Datenschutzerklärung
                </RouterLink>.
              </p>
            </div>
          </div>

          <!-- Buttons -->
          <div class="flex flex-wrap gap-2 shrink-0">
            <button
              @click="reject"
              class="text-sm font-semibold text-[#8e9aaa] hover:text-[#1a2e5a] px-4 py-2.5 rounded border border-[#1a2e5a]/15 hover:border-[#1a2e5a]/30 transition-colors"
            >
              Ablehnen
            </button>
            <button
              @click="openSettings"
              class="text-sm font-semibold text-[#1a2e5a] px-4 py-2.5 rounded border border-[#1a2e5a]/30 hover:bg-[#1a2e5a]/5 transition-colors flex items-center gap-1.5"
            >
              <Settings :size="13" />
              Einstellungen
            </button>
            <button
              @click="accept"
              class="text-sm font-bold bg-[#e85c1a] hover:bg-[#d44e12] text-white px-5 py-2.5 rounded transition-colors"
            >
              Alle akzeptieren
            </button>
          </div>

        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.slide-up-enter-active, .slide-up-leave-active { transition: transform 0.3s ease, opacity 0.3s ease; }
.slide-up-enter-from, .slide-up-leave-to { transform: translateY(20px); opacity: 0; }
</style>
