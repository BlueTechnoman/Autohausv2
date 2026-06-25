<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
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

  <main class="pt-16 min-h-screen bg-background">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">

      <!-- Breadcrumb -->
      <nav class="flex items-center gap-2 text-xs text-[#8e9aaa] mb-6">
        <button @click="router.push('/')" class="hover:text-[#e85c1a] transition-colors">Startseite</button>
        <span>/</span>
        <span class="text-[#1a2e5a] font-semibold">Impressum</span>
      </nav>

      <h1 class="text-[#1a2e5a] font-bold text-3xl mb-8">Impressum</h1>

      <div class="bg-white rounded-xl border border-[#1a2e5a]/8 p-8 shadow-sm space-y-8 text-sm text-[#4B5563] leading-relaxed">

        <!-- Anbieter -->
        <section>
          <h2 class="text-[#1a2e5a] font-bold text-lg mb-3">Angaben gemäß § 5 TMG</h2>
          <p>
            <strong class="text-[#1a2e5a]">AutoHaus Müller GmbH</strong><br />
            Amselstraße 1B<br />
            95444 Bayreuth<br />
            Deutschland
          </p>
        </section>

        <!-- Kontakt -->
        <section>
          <h2 class="text-[#1a2e5a] font-bold text-base mb-3">Kontakt</h2>
          <p>
            Telefon: <a href="tel:+499211234567" class="text-[#e85c1a] hover:underline">0921 123 456</a><br />
            Telefax: 0921 123 457<br />
            E-Mail: <a href="mailto:info@autohaus-mueller.de" class="text-[#e85c1a] hover:underline">info@autohaus-mueller.de</a>
          </p>
        </section>

        <!-- Registereintrag -->
        <section>
          <h2 class="text-[#1a2e5a] font-bold text-base mb-3">Registereintrag</h2>
          <p>
            Eingetragen im Handelsregister.<br />
            Registergericht: Amtsgericht Bayreuth<br />
            Registernummer: HRB 123456
          </p>
        </section>

        <!-- Umsatzsteuer -->
        <section>
          <h2 class="text-[#1a2e5a] font-bold text-base mb-3">Umsatzsteuer-ID</h2>
          <p>
            Umsatzsteuer-Identifikationsnummer gemäß § 27a Umsatzsteuergesetz:<br />
            DE 123456789
          </p>
        </section>

        <!-- Geschäftsführung -->
        <section>
          <h2 class="text-[#1a2e5a] font-bold text-base mb-3">Vertreten durch</h2>
          <p>Geschäftsführer: Thomas Müller</p>
        </section>

        <!-- Aufsichtsbehörde -->
        <section>
          <h2 class="text-[#1a2e5a] font-bold text-base mb-3">Zuständige Aufsichtsbehörde</h2>
          <p>
            Kraftfahrzeughändler sind gewerberechtlich der zuständigen Gemeinde unterstellt.<br />
            Kreisverwaltungsreferat Bayreuth<br />
            Markgrafenallee 38, 95448 Bayreuth
          </p>
        </section>

        <!-- Streitschlichtung -->
        <section>
          <h2 class="text-[#1a2e5a] font-bold text-base mb-3">Streitschlichtung</h2>
          <p>
            Die Europäische Kommission stellt eine Plattform zur Online-Streitbeilegung (OS) bereit:
            <a href="https://ec.europa.eu/consumers/odr/" target="_blank" rel="noopener noreferrer" class="text-[#e85c1a] hover:underline">
              https://ec.europa.eu/consumers/odr/
            </a>.<br /><br />
            Unsere E-Mail-Adresse finden Sie oben im Impressum.<br /><br />
            Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer
            Verbraucherschlichtungsstelle teilzunehmen.
          </p>
        </section>

        <!-- Haftung für Inhalte -->
        <section>
          <h2 class="text-[#1a2e5a] font-bold text-base mb-3">Haftung für Inhalte</h2>
          <p>
            Als Diensteanbieter sind wir gemäß § 7 Abs. 1 TMG für eigene Inhalte auf diesen Seiten nach den
            allgemeinen Gesetzen verantwortlich. Nach §§ 8 bis 10 TMG sind wir als Diensteanbieter jedoch nicht
            verpflichtet, übermittelte oder gespeicherte fremde Informationen zu überwachen oder nach Umständen
            zu forschen, die auf eine rechtswidrige Tätigkeit hinweisen.
          </p>
        </section>

        <!-- Haftung für Links -->
        <section>
          <h2 class="text-[#1a2e5a] font-bold text-base mb-3">Haftung für Links</h2>
          <p>
            Unser Angebot enthält Links zu externen Websites Dritter, auf deren Inhalte wir keinen Einfluss haben.
            Deshalb können wir für diese fremden Inhalte auch keine Gewähr übernehmen. Für die Inhalte der
            verlinkten Seiten ist stets der jeweilige Anbieter oder Betreiber der Seiten verantwortlich.
          </p>
        </section>

        <!-- Urheberrecht -->
        <section>
          <h2 class="text-[#1a2e5a] font-bold text-base mb-3">Urheberrecht</h2>
          <p>
            Die durch die Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten unterliegen dem deutschen
            Urheberrecht. Die Vervielfältigung, Bearbeitung, Verbreitung und jede Art der Verwertung außerhalb der
            Grenzen des Urheberrechtes bedürfen der schriftlichen Zustimmung des jeweiligen Autors bzw. Erstellers.
          </p>
        </section>

      </div>
    </div>
  </main>

  <AppFooter />
</template>
