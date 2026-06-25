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
        <span class="text-[#1a2e5a] font-semibold">Datenschutzerklärung</span>
      </nav>

      <h1 class="text-[#1a2e5a] font-bold text-3xl mb-2">Datenschutzerklärung</h1>
      <p class="text-[#8e9aaa] text-sm mb-8">Stand: {{ new Date().toLocaleDateString('de-DE', { month: 'long', year: 'numeric' }) }}</p>

      <div class="bg-white rounded-xl border border-[#1a2e5a]/8 p-8 shadow-sm space-y-8 text-sm text-[#4B5563] leading-relaxed">

        <section>
          <h2 class="text-[#1a2e5a] font-bold text-lg mb-3">1. Datenschutz auf einen Blick</h2>
          <h3 class="text-[#1a2e5a] font-semibold mb-2">Allgemeine Hinweise</h3>
          <p>
            Die folgenden Hinweise geben einen einfachen Überblick darüber, was mit Ihren personenbezogenen Daten
            passiert, wenn Sie diese Website besuchen. Personenbezogene Daten sind alle Daten, mit denen Sie
            persönlich identifiziert werden können.
          </p>
        </section>

        <section>
          <h2 class="text-[#1a2e5a] font-bold text-lg mb-3">2. Verantwortliche Stelle</h2>
          <p>
            Verantwortlich für die Datenverarbeitung auf dieser Website ist:<br /><br />
            <strong class="text-[#1a2e5a]">AutoHaus Müller GmbH</strong><br />
            Amselstraße 1B, 95444 Bayreuth<br />
            Telefon: 0921 123 456<br />
            E-Mail: <a href="mailto:datenschutz@autohaus-mueller.de" class="text-[#e85c1a] hover:underline">datenschutz@autohaus-mueller.de</a>
          </p>
        </section>

        <section>
          <h2 class="text-[#1a2e5a] font-bold text-lg mb-3">3. Datenerfassung auf dieser Website</h2>
          <h3 class="text-[#1a2e5a] font-semibold mb-2">Cookies</h3>
          <p class="mb-4">
            Unsere Website verwendet Cookies. Das sind kleine Textdateien, die Ihr Webbrowser auf Ihrem Endgerät speichert.
            Cookies helfen uns dabei, unser Angebot nutzerfreundlicher, effektiver und sicherer zu machen.
          </p>
          <p class="mb-4">
            Einige Cookies sind "notwendig", weil ohne sie die Webseite nicht richtig funktionieren würde.
            Andere Cookies dienen dazu, das Nutzerverhalten auszuwerten oder Werbung zu personalisieren.
          </p>
          <p>
            Sie können in unserem Cookie-Banner wählen, welche Cookies Sie zulassen möchten.
            Notwendige Cookies können nicht deaktiviert werden.
          </p>
        </section>

        <section>
          <h2 class="text-[#1a2e5a] font-bold text-lg mb-3">4. Kontaktformular & Anfragen</h2>
          <p>
            Wenn Sie uns per Kontaktformular oder E-Mail Anfragen zukommen lassen, werden Ihre Angaben inklusive
            der von Ihnen angegebenen Kontaktdaten zwecks Bearbeitung der Anfrage und für den Fall von
            Anschlussfragen bei uns gespeichert. Diese Daten geben wir nicht ohne Ihre Einwilligung weiter.
          </p>
          <p class="mt-3">
            Rechtsgrundlage: Art. 6 Abs. 1 lit. b DSGVO (Vertragserfüllung) und Art. 6 Abs. 1 lit. f DSGVO
            (berechtigtes Interesse an der Bearbeitung von Anfragen).
          </p>
        </section>

        <section>
          <h2 class="text-[#1a2e5a] font-bold text-lg mb-3">5. Ihre Rechte</h2>
          <p class="mb-3">Sie haben jederzeit das Recht:</p>
          <ul class="space-y-2 list-disc pl-5">
            <li>Auskunft über Ihre bei uns gespeicherten Daten (Art. 15 DSGVO)</li>
            <li>Berichtigung unrichtiger Daten (Art. 16 DSGVO)</li>
            <li>Löschung Ihrer Daten, sofern keine gesetzliche Aufbewahrungspflicht besteht (Art. 17 DSGVO)</li>
            <li>Einschränkung der Verarbeitung (Art. 18 DSGVO)</li>
            <li>Datenübertragbarkeit (Art. 20 DSGVO)</li>
            <li>Widerspruch gegen die Verarbeitung (Art. 21 DSGVO)</li>
          </ul>
          <p class="mt-4">
            Zur Ausübung dieser Rechte wenden Sie sich bitte an:
            <a href="mailto:datenschutz@autohaus-mueller.de" class="text-[#e85c1a] hover:underline">
              datenschutz@autohaus-mueller.de
            </a>
          </p>
        </section>

        <section>
          <h2 class="text-[#1a2e5a] font-bold text-lg mb-3">6. Beschwerderecht</h2>
          <p>
            Sie haben das Recht, sich bei einer Datenschutz-Aufsichtsbehörde zu beschweren. Die für Bayern
            zuständige Aufsichtsbehörde ist:<br /><br />
            <strong class="text-[#1a2e5a]">Bayerisches Landesamt für Datenschutzaufsicht (BayLDA)</strong><br />
            Promenade 18, 91522 Ansbach<br />
            <a href="https://www.lda.bayern.de" target="_blank" rel="noopener noreferrer" class="text-[#e85c1a] hover:underline">
              www.lda.bayern.de
            </a>
          </p>
        </section>

        <section>
          <h2 class="text-[#1a2e5a] font-bold text-lg mb-3">7. Datensicherheit</h2>
          <p>
            Wir verwenden innerhalb des Website-Besuchs das verbreitete SSL/TLS-Verfahren (Secure Socket Layer)
            in Verbindung mit der jeweils höchsten Verschlüsselungsstufe, die von Ihrem Browser unterstützt wird.
            In der Regel handelt es sich dabei um eine 256 Bit Verschlüsselung.
          </p>
        </section>

      </div>
    </div>
  </main>

  <AppFooter />
</template>
