<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import NavBar           from '../components/NavBar.vue'
import HeroSection      from '../components/HeroSection.vue'
import FahrzeugeSection from '../components/FahrzeugeSection.vue'
import UeberUnsSection  from '../components/UeberUnsSection.vue'
import KontaktSection   from '../components/KontaktSection.vue'
import AppFooter        from '../components/AppFooter.vue'

const scrolled = ref(false)
const onScroll = () => { scrolled.value = window.scrollY > 24 }
onMounted(()  => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<template>
  <NavBar :scrolled="scrolled" />
  <HeroSection />
  <FahrzeugeSection />
  <UeberUnsSection />
  <KontaktSection />
  <AppFooter />
</template>
