<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import NavBar    from '../components/NavBar.vue'
import AppFooter from '../components/AppFooter.vue'

const scrolled = ref(false)
const onScroll = () => { scrolled.value = window.scrollY > 24 }
onMounted(()  => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<template>
  <NavBar :scrolled="scrolled" />
  <main class="pt-16 min-h-screen bg-background">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">

      <nav class="flex items-center gap-2 text-xs text-[#8e9aaa] font-medium mb-8 tracking-wide">
        <a href="/" class="hover:text-[#e85c1a] transition-colors">Startseite</a>
        <span class="text-[#8e9aaa]/50">/</span>
        <span class="text-[#1a2e5a] font-semibold">AGB</span>
      </nav>

      <h1 class="text-[#1a2e5a] font-bold text-3xl mb-2">Allgemeine Geschäftsbedingungen</h1>
      <p class="text-[#8e9aaa] text-sm mb-10">AutoHaus Müller GmbH · Stand: Januar 2025</p>

      <div class="prose prose-sm max-w-none space-y-8 text-[#8e9aaa] leading-relaxed">

        <section>
          <h2 class="text-[#1a2e5a] font-bold text-lg mb-3">§ 1 Geltungsbereich</h2>
          <p>Diese Allgemeinen Geschäftsbedingungen gelten für alle Verträge zwischen der AutoHaus Müller GmbH, Amselstraße 1B, 95444 Bayreuth (nachfolgend „Verkäufer") und dem Kunden (nachfolgend „Käufer") über den Kauf von Kraftfahrzeugen und Zubehör.</p>
        </section>

        <section>
          <h2 class="text-[#1a2e5a] font-bold text-lg mb-3">§ 2 Vertragsabschluss</h2>
          <p>Die Darstellung der Fahrzeuge auf dieser Website stellt kein rechtlich bindendes Angebot dar, sondern eine Aufforderung zur Abgabe eines Angebots. Ein Kaufvertrag kommt erst durch schriftliche Bestätigung des Verkäufers zustande.</p>
        </section>

        <section>
          <h2 class="text-[#1a2e5a] font-bold text-lg mb-3">§ 3 Preise und Zahlung</h2>
          <p>Alle Preise sind Brutto-Verkaufspreise inklusive der gesetzlichen Mehrwertsteuer. Die Zahlung erfolgt bei Fahrzeugübergabe in bar, per EC-Karte oder durch vorherige Banküberweisung.</p>
        </section>

        <section>
          <h2 class="text-[#1a2e5a] font-bold text-lg mb-3">§ 4 Lieferung und Übergabe</h2>
          <p>Die Übergabe des Fahrzeugs erfolgt nach Eingang der vollständigen Zahlung in unseren Geschäftsräumen in Bayreuth. Liefertermine werden individuell vereinbart.</p>
        </section>

        <section>
          <h2 class="text-[#1a2e5a] font-bold text-lg mb-3">§ 5 Gewährleistung</h2>
          <p>Für Gebrauchtfahrzeuge gilt eine Gewährleistungsfrist von 12 Monaten ab Übergabe gemäß § 476 BGB. Davon ausgenommen sind Verschleißteile sowie Mängel, die bei der Übergabe bekannt waren.</p>
        </section>

        <section>
          <h2 class="text-[#1a2e5a] font-bold text-lg mb-3">§ 6 Widerrufsrecht</h2>
          <p>Bei Verträgen, die außerhalb von Geschäftsräumen oder im Fernabsatz geschlossen werden, steht Verbrauchern ein Widerrufsrecht von 14 Tagen zu. Bei Fahrzeugen, die vor Ort besichtigt und erworben werden, besteht kein gesetzliches Widerrufsrecht.</p>
        </section>

        <section>
          <h2 class="text-[#1a2e5a] font-bold text-lg mb-3">§ 7 Haftungsbeschränkung</h2>
          <p>Der Verkäufer haftet unbeschränkt für Vorsatz und grobe Fahrlässigkeit. Für leichte Fahrlässigkeit haftet der Verkäufer nur bei Verletzung wesentlicher Vertragspflichten.</p>
        </section>

        <section>
          <h2 class="text-[#1a2e5a] font-bold text-lg mb-3">§ 8 Anwendbares Recht</h2>
          <p>Es gilt das Recht der Bundesrepublik Deutschland. Gerichtsstand ist Bayreuth, sofern der Käufer Kaufmann ist.</p>
        </section>

        <div class="border-t border-[#1a2e5a]/10 pt-6 text-xs text-[#8e9aaa]/70">
          AutoHaus Müller GmbH · Amselstraße 1B · 95444 Bayreuth · Tel: 0921 123 456 · info@autohaus-mueller.de
        </div>

      </div>
    </div>
  </main>
  <AppFooter />
</template>
