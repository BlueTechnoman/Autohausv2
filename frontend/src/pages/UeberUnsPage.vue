<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  Award, Shield, Heart, Wrench, Check, ArrowRight,
  Users, Car, Star, Clock,
} from 'lucide-vue-next'
import NavBar    from '../components/NavBar.vue'
import AppFooter from '../components/AppFooter.vue'

const router   = useRouter()
const scrolled = ref(false)
const onScroll = () => { scrolled.value = window.scrollY > 24 }
onMounted(()  => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))

// ── Kennzahlen ────────────────────────────────────────────────────────
const KENNZAHLEN = [
  { icon: Car,   wert: '80+',    label: 'Fahrzeuge im Bestand' },
  { icon: Users, wert: '2.400+', label: 'Zufriedene Kunden' },
  { icon: Star,  wert: '4,9 / 5',label: 'Kundenbewertung' },
  { icon: Clock, wert: '15 J.',  label: 'Erfahrung im Handel' },
]

// ── Timeline ──────────────────────────────────────────────────────────
const TIMELINE = [
  {
    jahr: '2009',
    titel: 'Gründung des Autohauses',
    text: 'Thomas Müller gründet AutoHaus Müller GmbH in Bayreuth mit einem Startbestand von 12 Fahrzeugen und 3 Mitarbeitern.',
  },
  {
    jahr: '2012',
    titel: 'Erweiterung des Standorts',
    text: 'Umzug in größere Räumlichkeiten an der Amselstraße 1B. Bestand wächst auf über 30 Fahrzeuge. Eröffnung der eigenen Werkstatt.',
  },
  {
    jahr: '2015',
    titel: 'Zertifizierung & Auszeichnungen',
    text: 'Auszeichnung als "Bester Gebrauchtwagenhändler Nordbayern" durch den ADAC. TÜV-Partnerbetrieb-Zertifizierung.',
  },
  {
    jahr: '2018',
    titel: 'Digitalisierung',
    text: 'Launch des Online-Fahrzeugkatalogs und Einführung digitaler Fahrzeugunterlagen. Über 500 Fahrzeuge vermittelt.',
  },
  {
    jahr: '2022',
    titel: 'Expansion Elektromobilität',
    text: 'Integration von Elektro- und Hybridfahrzeugen ins Sortiment. Installation von 4 Ladestationen auf dem Gelände.',
  },
  {
    jahr: '2026',
    titel: 'Heute',
    text: 'Über 2.400 verkaufte Fahrzeuge, 15 Mitarbeiter und ein Bestand von 80+ Fahrzeugen. Weiterhin familiengeführt.',
  },
]

// ── Werte ─────────────────────────────────────────────────────────────
const WERTE = [
  {
    icon: Shield,
    titel: 'Vertrauen & Transparenz',
    text: 'Jedes Fahrzeug wird vollständig dokumentiert - mit lückenlosem Servicehistorie, HU-Bericht und ehrlicher Zustandsbeschreibung. Keine versteckten Kosten.',
  },
  {
    icon: Award,
    titel: 'Qualitätsanspruch',
    text: 'Nur TÜV-geprüfte Fahrzeuge mit professioneller Aufbereitung. Unsere hauseigene Werkstatt stellt sicher, dass jedes Auto in einwandfreiem Zustand übergeben wird.',
  },
  {
    icon: Heart,
    titel: 'Kundenorientierung',
    text: 'Persönliche Beratung ohne Verkaufsdruck. Wir nehmen uns Zeit für Ihre Fragen und begleiten Sie von der Besichtigung bis zur Zulassung.',
  },
  {
    icon: Wrench,
    titel: 'Kompetenz & Service',
    text: '15 Jahre Erfahrung im Fahrzeughandel. Unser Team aus erfahrenen Automobilfachleuten steht Ihnen auch nach dem Kauf für Wartung und Reparaturen zur Seite.',
  },
]

// ── Team ──────────────────────────────────────────────────────────────
const TEAM = [
  { name: 'Thomas Müller',   rolle: 'Geschäftsführer',          initialen: 'TM' },
  { name: 'Sandra Berger',   rolle: 'Verkaufsleitung',          initialen: 'SB' },
  { name: 'Klaus Fischer',   rolle: 'Fahrzeugaufbereitung',     initialen: 'KF' },
  { name: 'Petra Holm',      rolle: 'Kundenberatung',           initialen: 'PH' },
  { name: 'Michael Roth',    rolle: 'Werkstattleiter',          initialen: 'MR' },
  { name: 'Anna Steinbach',  rolle: 'Finanzierungsberatung',    initialen: 'AS' },
]

// ── Leistungen ────────────────────────────────────────────────────────
const LEISTUNGEN = [
  'TÜV-Generalinspektionen & HU-Abnahme',
  'Professionelle Fahrzeugaufbereitung',
  'Finanzierungsberatung & Kreditvermittlung',
  'Inzahlungnahme Ihres Altfahrzeugs',
  '12 Monate Gebrauchtwagengarantie',
  'Überführungsservice deutschlandweit',
  'Zulassungsservice & Kennzeichenbeschaffung',
  'Hol- & Bringservice bei Werkstattaufenthalten',
]
</script>

<template>
  <NavBar :scrolled="scrolled" />

  <main class="pt-16">

    <!-- ── Hero-Banner ─────────────────────────────────────────────── -->
    <section class="relative bg-[#1a2e5a] py-24 overflow-hidden">
      <div class="absolute inset-0">
        <img
          src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1920&h=600&fit=crop&auto=format"
          alt=""
          class="w-full h-full object-cover opacity-10"
        />
        <div class="absolute inset-0 bg-gradient-to-r from-[#1a2e5a] to-[#1a2e5a]/70" />
      </div>
      <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Breadcrumb -->
        <nav class="flex items-center gap-2 text-white/50 text-xs font-medium mb-8 tracking-wide">
          <button @click="router.push('/')" class="hover:text-white/80 transition-colors font-medium">Startseite</button>
           <span class="text-white/30">/</span>
           <span class="text-white/80 font-semibold">Über uns</span>
        </nav>
        <p class="text-[#e85c1a] font-bold text-xs uppercase tracking-[0.2em] mb-4">Wer wir sind</p>
        <h1 class="text-white font-bold text-4xl md:text-5xl leading-tight mb-6">
          Ihr verlässlicher<br />Fahrzeugpartner seit 2009.
        </h1>
        <p class="text-white/60 text-lg leading-relaxed max-w-2xl">
          AutoHaus Müller ist ein familiengeführtes Autohaus in Bayreuth mit über 15 Jahren Erfahrung im
          Gebrauchtwagenhandel. Wir verbinden persönlichen Service mit hohen Qualitätsstandards.
        </p>
      </div>
    </section>

    <!-- ── Kennzahlen ──────────────────────────────────────────────── -->
    <section class="bg-[#e85c1a] py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div
            v-for="k in KENNZAHLEN"
            :key="k.label"
            class="text-center"
          >
            <component :is="k.icon" :size="22" class="text-white/70 mx-auto mb-3" />
            <div class="text-white font-bold text-3xl mb-1">{{ k.wert }}</div>
            <div class="text-white/65 text-xs uppercase tracking-wider">{{ k.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Geschichte / Timeline ───────────────────────────────────── -->
    <section class="py-20 bg-background">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="max-w-2xl mb-12">
          <p class="text-[#e85c1a] font-bold text-xs uppercase tracking-[0.2em] mb-3">Unsere Geschichte</p>
          <h2 class="text-[#1a2e5a] font-bold text-3xl mb-4">15 Jahre AutoHaus Müller</h2>
          <p class="text-[#8e9aaa] text-base leading-relaxed">
            Von einem kleinen Gebrauchtwagenhändler zu einem der bekanntesten Autohäuser Bayreuths -
            unsere Geschichte ist geprägt von Leidenschaft, Vertrauen und kontinuierlichem Wachstum.
          </p>
        </div>

        <!-- Timeline -->
        <div class="relative">
          <!-- Vertikale Linie -->
          <div class="absolute left-6 md:left-1/2 top-0 bottom-0 w-px bg-[#1a2e5a]/12 -translate-x-px hidden sm:block" />

          <div class="space-y-8">
            <div
              v-for="(item, i) in TIMELINE"
              :key="item.jahr"
              :class="[
                'relative flex gap-6 sm:gap-0',
                i % 2 === 0 ? 'sm:flex-row' : 'sm:flex-row-reverse',
              ]"
            >
              <!-- Inhalt -->
              <div :class="['sm:w-1/2', i % 2 === 0 ? 'sm:pr-12 sm:text-right' : 'sm:pl-12']">
                <div class="bg-white border border-[#1a2e5a]/8 rounded-lg p-6 shadow-sm">
                  <div class="text-[#e85c1a] font-bold text-xs uppercase tracking-widest mb-2">{{ item.jahr }}</div>
                  <h3 class="text-[#1a2e5a] font-bold text-base mb-2">{{ item.titel }}</h3>
                  <p class="text-[#8e9aaa] text-sm leading-relaxed">{{ item.text }}</p>
                </div>
              </div>

              <!-- Punkt auf der Linie -->
              <div class="hidden sm:flex absolute left-1/2 top-6 -translate-x-1/2 w-4 h-4 bg-[#e85c1a] rounded-full border-4 border-white shadow-sm" />

              <!-- Mobile Spacer -->
              <div class="sm:w-1/2" />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Werte ───────────────────────────────────────────────────── -->
    <section class="py-20 bg-[#1a2e5a]">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-2xl mx-auto mb-12">
          <p class="text-[#e85c1a] font-bold text-xs uppercase tracking-[0.2em] mb-3">Was uns antreibt</p>
          <h2 class="text-white font-bold text-3xl">Unsere Werte</h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div
            v-for="wert in WERTE"
            :key="wert.titel"
            class="bg-white/6 border border-white/10 rounded-lg p-7"
          >
            <div class="w-11 h-11 bg-[#e85c1a]/20 rounded flex items-center justify-center mb-5">
              <component :is="wert.icon" :size="20" class="text-[#e85c1a]" />
            </div>
            <h3 class="text-white font-bold text-base mb-3">{{ wert.titel }}</h3>
            <p class="text-white/55 text-sm leading-relaxed">{{ wert.text }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Team ───────────────────────────────────────────────────── -->
    <section class="py-20 bg-background">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="max-w-2xl mb-12">
          <p class="text-[#e85c1a] font-bold text-xs uppercase tracking-[0.2em] mb-3">Wer wir sind</p>
          <h2 class="text-[#1a2e5a] font-bold text-3xl mb-4">Unser Team</h2>
          <p class="text-[#8e9aaa] text-base leading-relaxed">
            Hinter AutoHaus Müller stehen Menschen mit echter Leidenschaft für Automobile
            und einem hohen Anspruch an persönlichen Service.
          </p>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-5">
          <div
            v-for="member in TEAM"
            :key="member.name"
            class="text-center"
          >
            <div class="w-20 h-20 bg-[#1a2e5a] rounded-full flex items-center justify-center mx-auto mb-4">
              <span class="text-white font-bold text-lg">{{ member.initialen }}</span>
            </div>
            <div class="text-[#1a2e5a] font-bold text-sm">{{ member.name }}</div>
            <div class="text-[#8e9aaa] text-xs mt-1">{{ member.rolle }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Leistungen ──────────────────────────────────────────────── -->
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <p class="text-[#e85c1a] font-bold text-xs uppercase tracking-[0.2em] mb-3">Was wir bieten</p>
            <h2 class="text-[#1a2e5a] font-bold text-3xl mb-6">Unsere Leistungen</h2>
            <p class="text-[#8e9aaa] text-base leading-relaxed mb-8">
              Von der ersten Beratung über den Kauf bis hin zur laufenden Betreuung -
              wir sind Ihr Ansprechpartner für alles rund ums Fahrzeug.
            </p>
            <ul class="grid grid-cols-1 gap-3">
              <li
                v-for="leistung in LEISTUNGEN"
                :key="leistung"
                class="flex items-start gap-3 text-[#1a2e5a] text-sm"
              >
                <span class="w-5 h-5 bg-[#e85c1a]/12 border border-[#e85c1a]/30 rounded-full flex items-center justify-center shrink-0 mt-0.5">
                  <Check :size="10" class="text-[#e85c1a]" />
                </span>
                {{ leistung }}
              </li>
            </ul>
          </div>
          <div class="relative rounded-lg overflow-hidden aspect-[4/3]">
            <img
              src="https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=800&h=600&fit=crop&auto=format"
              alt="AutoHaus Müller Werkstatt"
              class="w-full h-full object-cover"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-[#1a2e5a]/40 to-transparent" />
          </div>
        </div>
      </div>
    </section>

    <!-- ── CTA-Banner ─────────────────────────────────────────────── -->
    <section class="bg-[#e85c1a] py-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-white font-bold text-3xl mb-4">Bereit, Ihr nächstes Fahrzeug zu finden?</h2>
        <p class="text-white/75 text-base mb-8 max-w-lg mx-auto">
          Besuchen Sie uns persönlich oder stöbern Sie jetzt in unserem aktuellen Fahrzeugbestand.
        </p>
        <div class="flex flex-wrap gap-4 justify-center">
          <button
            @click="router.push('/#fahrzeuge')"
            class="bg-white text-[#e85c1a] hover:bg-white/90 font-bold px-8 py-4 rounded text-base transition-colors flex items-center gap-2"
          >
            Fahrzeuge ansehen
            <ArrowRight :size="16" />
          </button>
          <a
            href="tel:+499211234567"
            class="border-2 border-white text-white hover:bg-white/10 font-bold px-8 py-4 rounded text-base transition-colors"
          >
            0921 123 456
          </a>
        </div>
      </div>
    </section>

  </main>

  <AppFooter />
</template>
