<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Home, ArrowLeft, Car } from 'lucide-vue-next'
import NavBar    from '../components/NavBar.vue'
import AppFooter from '../components/AppFooter.vue'

const router   = useRouter()
const scrolled = ref(false)
const onScroll = () => { scrolled.value = window.scrollY > 24 }
onMounted(()  => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<template>
  <NavBar :scrolled="scrolled" />

  <main class="pt-16 min-h-screen bg-background flex flex-col">
    <div class="flex-1 flex items-center justify-center py-20 px-4">
      <div class="text-center max-w-md">

        <!-- 404 Zahl -->
        <div class="text-[#1a2e5a]/8 font-bold select-none mb-4" style="font-size: clamp(8rem, 20vw, 12rem); line-height: 1;">
          404
        </div>

        <div class="w-16 h-16 bg-[#e85c1a]/10 rounded-full flex items-center justify-center mx-auto mb-6 -mt-4">
          <Car :size="28" class="text-[#e85c1a]" />
        </div>

        <h1 class="text-[#1a2e5a] font-bold text-2xl mb-3">Seite nicht gefunden</h1>
        <p class="text-[#8e9aaa] text-base mb-8">
          Die gesuchte Seite existiert leider nicht oder wurde verschoben.
          Vielleicht haben Sie sich vertippt?
        </p>

        <div class="flex flex-col sm:flex-row gap-3 justify-center">
          <button
            @click="router.back()"
            class="flex items-center justify-center gap-2 border border-[#1a2e5a]/20 text-[#1a2e5a]
                   hover:bg-[#1a2e5a]/5 font-semibold px-6 py-3 rounded-lg text-sm transition-colors"
          >
            <ArrowLeft :size="15" />
            Zurück
          </button>
          <button
            @click="router.push('/')"
            class="flex items-center justify-center gap-2 bg-[#e85c1a] hover:bg-[#d44e12]
                   text-white font-bold px-6 py-3 rounded-lg text-sm transition-colors"
          >
            <Home :size="15" />
            Zur Startseite
          </button>
        </div>

      </div>
    </div>
  </main>

  <AppFooter />
</template>
