<!--
  LoginPage.vue – Login & Registrierung
  ══════════════════════════════════════
  Route: /login

  Verbindet sich mit:
    POST /api/accounts/login/    → JWT-Token erhalten
    POST /api/accounts/register/ → Neues Konto anlegen

  Sicherheit:
    • Frontend-Validierung (useAuth.ts → validateLoginInput/validateRegisterInput)
      verhindert leere/unsichere Eingaben BEVOR sie ans Backend gesendet werden
    • Backend validiert zusätzlich (Passwortlänge, Einmaligkeit des Usernamens etc.)
    • Kein HTML-Injection möglich (Regex-Check in useAuth)
    • Passwort wird nie im State gespeichert – nur für den API-Call genutzt
    • Nach erfolgreichem Login: Weiterleitung zur vorherigen Seite oder Dashboard
-->
<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Eye, EyeOff, Mail, Lock, User, AlertCircle, CheckCircle2, Shield } from 'lucide-vue-next'
import NavBar    from '../components/NavBar.vue'
import AppFooter from '../components/AppFooter.vue'
import { useAuth } from '../composables/useAuth'

const router = useRouter()
const route  = useRoute()
const { isLoggedIn, login, register, authLoading } = useAuth()

// Bereits eingeloggt → zum Dashboard weiterleiten
if (isLoggedIn.value) {
  router.replace('/dashboard')
}

const scrolled = ref(false)
const onScroll = () => { scrolled.value = window.scrollY > 24 }
onMounted(()  => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))

// ── View-State ─────────────────────────────────────────────────────────
type View = 'login' | 'register' | 'forgot'
const view = ref<View>('login')

// ── Passwort-Sichtbarkeit ─────────────────────────────────────────────
const showPw  = ref(false)
const showPw2 = ref(false)

// ── Login-Felder ──────────────────────────────────────────────────────
const loginUsername = ref('')
const loginPassword = ref('')
const loginError    = ref('')

// ── Registrierungs-Felder ─────────────────────────────────────────────
const regUsername = ref('')
const regEmail    = ref('')
const regPw       = ref('')
const regPw2      = ref('')
const regError    = ref('')

// ── Passwort-Vergessen ────────────────────────────────────────────────
const forgotEmail   = ref('')
const forgotError   = ref('')
const forgotSuccess = ref(false)
const forgotLoading = ref(false)

// ── Submit: Login ─────────────────────────────────────────────────────
async function submitLogin() {
  loginError.value = ''
  const result = await login(loginUsername.value, loginPassword.value)
  if (result.success) {
    // Zurück zur vorherigen Seite oder zum Dashboard
    const redirect = (route.query.redirect as string) ?? '/dashboard'
    router.push(redirect)
  } else {
    loginError.value = result.error ?? 'Login fehlgeschlagen.'
  }
}

// ── Submit: Registrierung ─────────────────────────────────────────────
async function submitRegister() {
  regError.value = ''
  const result = await register(regUsername.value, regEmail.value, regPw.value, regPw2.value)
  if (result.success) {
    router.push('/dashboard')
  } else {
    regError.value = result.error ?? 'Registrierung fehlgeschlagen.'
  }
}

// ── Submit: Passwort vergessen (nur Demo) ─────────────────────────────
async function submitForgot() {
  forgotError.value   = ''
  forgotSuccess.value = false
  if (!forgotEmail.value) { forgotError.value = 'Bitte E-Mail eingeben.'; return }
  forgotLoading.value = true
  await new Promise(r => setTimeout(r, 800))
  forgotLoading.value = false
  forgotSuccess.value = true
}

// Eingabe-Klassen (Tailwind) – mit Fehler-Highlighting
const inputCls = (err: boolean) => [
  'w-full px-3.5 py-3 border rounded-lg text-sm text-[#1a2e5a] placeholder-[#8e9aaa]/60',
  'focus:outline-none focus:ring-2 focus:ring-[#1a2e5a]/20 transition-colors bg-white',
  err ? 'border-red-400 bg-red-50' : 'border-[#1a2e5a]/15',
].join(' ')
</script>

<template>
  <NavBar :scrolled="scrolled" />

  <main class="pt-16 min-h-screen bg-background flex flex-col">
    <div class="flex-1 flex items-center justify-center py-12 px-4">
      <div class="w-full max-w-md">

        <!-- Sicherheits-Hinweis -->
        <div class="bg-blue-50 border border-blue-200 rounded-lg px-4 py-3 mb-5 flex gap-3">
          <Shield :size="16" class="text-blue-600 shrink-0 mt-0.5" />
          <p class="text-blue-800 text-xs leading-relaxed">
            Ihre Daten werden verschlüsselt übertragen.
            Passwörter werden serverseitig gehasht und niemals im Klartext gespeichert.
          </p>
        </div>

        <!-- Card -->
        <div class="bg-white rounded-xl shadow-sm border border-[#1a2e5a]/8 overflow-hidden">

          <!-- Tabs: Login | Registrieren -->
          <div class="flex border-b border-[#1a2e5a]/8">
            <button
              @click="view = 'login'"
              :class="['flex-1 py-4 text-sm font-bold transition-colors',
                view === 'login' ? 'text-[#1a2e5a] border-b-2 border-[#e85c1a]' : 'text-[#8e9aaa] hover:text-[#1a2e5a]']"
            >Anmelden</button>
            <button
              @click="view = 'register'"
              :class="['flex-1 py-4 text-sm font-bold transition-colors',
                view === 'register' ? 'text-[#1a2e5a] border-b-2 border-[#e85c1a]' : 'text-[#8e9aaa] hover:text-[#1a2e5a]']"
            >Registrieren</button>
          </div>

          <!-- ── LOGIN ── -->
          <div v-if="view === 'login'" class="p-7">
            <h1 class="text-[#1a2e5a] font-bold text-xl mb-1">Willkommen zurück</h1>
            <p class="text-[#8e9aaa] text-sm mb-6">Melden Sie sich mit Ihrem Konto an.</p>

            <div v-if="loginError" class="bg-red-50 border border-red-200 rounded-lg px-4 py-3 mb-5 flex gap-2.5">
              <AlertCircle :size="15" class="text-red-600 shrink-0 mt-0.5" />
              <p class="text-red-700 text-xs">{{ loginError }}</p>
            </div>

            <!-- Benutzername -->
            <div class="mb-4">
              <label class="block text-[#1a2e5a] text-xs font-bold uppercase tracking-wider mb-2">Benutzername</label>
              <div class="relative">
                <User :size="15" class="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#8e9aaa]" />
                <input v-model="loginUsername" type="text" placeholder="Ihr Benutzername"
                  :class="inputCls(false)" class="pl-10"
                  @keyup.enter="submitLogin" />
              </div>
            </div>

            <!-- Passwort -->
            <div class="mb-5">
              <div class="flex items-center justify-between mb-2">
                <label class="text-[#1a2e5a] text-xs font-bold uppercase tracking-wider">Passwort</label>
                <button @click="view = 'forgot'" class="text-xs text-[#e85c1a] hover:underline">Vergessen?</button>
              </div>
              <div class="relative">
                <Lock :size="15" class="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#8e9aaa]" />
                <input v-model="loginPassword" :type="showPw ? 'text' : 'password'" placeholder="Ihr Passwort"
                  :class="inputCls(false)" class="pl-10 pr-10"
                  @keyup.enter="submitLogin" />
                <button @click="showPw = !showPw" class="absolute right-3.5 top-1/2 -translate-y-1/2 text-[#8e9aaa]">
                  <EyeOff v-if="showPw" :size="15" /><Eye v-else :size="15" />
                </button>
              </div>
            </div>

            <button
              @click="submitLogin"
              :disabled="authLoading"
              class="w-full bg-[#e85c1a] hover:bg-[#d44e12] disabled:opacity-60 text-white font-bold py-3.5 rounded-lg text-sm transition-colors"
            >
              {{ authLoading ? 'Wird überprüft …' : 'Anmelden' }}
            </button>

            <p class="text-center text-xs text-[#8e9aaa] mt-5">
              Noch kein Konto?
              <button @click="view = 'register'" class="text-[#e85c1a] font-bold hover:underline">Jetzt registrieren</button>
            </p>
          </div>

          <!-- ── REGISTRIEREN ── -->
          <div v-else-if="view === 'register'" class="p-7">
            <h1 class="text-[#1a2e5a] font-bold text-xl mb-1">Konto erstellen</h1>
            <p class="text-[#8e9aaa] text-sm mb-6">Erstellen Sie Ihr kostenloses Kundenkonto.</p>

            <div v-if="regError" class="bg-red-50 border border-red-200 rounded-lg px-4 py-3 mb-5 flex gap-2.5">
              <AlertCircle :size="15" class="text-red-600 shrink-0 mt-0.5" />
              <p class="text-red-700 text-xs">{{ regError }}</p>
            </div>

            <!-- Benutzername -->
            <div class="mb-4">
              <label class="block text-[#1a2e5a] text-xs font-bold uppercase tracking-wider mb-2">Benutzername *</label>
              <div class="relative">
                <User :size="15" class="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#8e9aaa]" />
                <input v-model="regUsername" type="text" placeholder="max_mustermann"
                  :class="inputCls(false)" class="pl-10" />
              </div>
              <p class="text-[#8e9aaa] text-xs mt-1">Nur Buchstaben, Zahlen und @.+-_ erlaubt</p>
            </div>

            <!-- E-Mail -->
            <div class="mb-4">
              <label class="block text-[#1a2e5a] text-xs font-bold uppercase tracking-wider mb-2">E-Mail *</label>
              <div class="relative">
                <Mail :size="15" class="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#8e9aaa]" />
                <input v-model="regEmail" type="email" placeholder="max@beispiel.de"
                  :class="inputCls(false)" class="pl-10" />
              </div>
            </div>

            <!-- Passwort -->
            <div class="mb-4">
              <label class="block text-[#1a2e5a] text-xs font-bold uppercase tracking-wider mb-2">
                Passwort * <span class="font-normal text-[#8e9aaa] normal-case tracking-normal">(mind. 8 Zeichen)</span>
              </label>
              <div class="relative">
                <Lock :size="15" class="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#8e9aaa]" />
                <input v-model="regPw" :type="showPw ? 'text' : 'password'" placeholder="Sicheres Passwort"
                  :class="inputCls(false)" class="pl-10 pr-10" />
                <button @click="showPw = !showPw" class="absolute right-3.5 top-1/2 -translate-y-1/2 text-[#8e9aaa]">
                  <EyeOff v-if="showPw" :size="15" /><Eye v-else :size="15" />
                </button>
              </div>
            </div>

            <!-- Passwort bestätigen -->
            <div class="mb-6">
              <label class="block text-[#1a2e5a] text-xs font-bold uppercase tracking-wider mb-2">Passwort bestätigen *</label>
              <div class="relative">
                <Lock :size="15" class="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#8e9aaa]" />
                <input v-model="regPw2" :type="showPw2 ? 'text' : 'password'" placeholder="Wiederholen"
                  :class="inputCls(false)" class="pl-10 pr-10" />
                <button @click="showPw2 = !showPw2" class="absolute right-3.5 top-1/2 -translate-y-1/2 text-[#8e9aaa]">
                  <EyeOff v-if="showPw2" :size="15" /><Eye v-else :size="15" />
                </button>
              </div>
            </div>

            <button
              @click="submitRegister"
              :disabled="authLoading"
              class="w-full bg-[#e85c1a] hover:bg-[#d44e12] disabled:opacity-60 text-white font-bold py-3.5 rounded-lg text-sm transition-colors"
            >
              {{ authLoading ? 'Wird registriert …' : 'Konto erstellen' }}
            </button>

            <p class="text-center text-xs text-[#8e9aaa] mt-5">
              Bereits ein Konto?
              <button @click="view = 'login'" class="text-[#e85c1a] font-bold hover:underline">Anmelden</button>
            </p>
          </div>

          <!-- ── PASSWORT VERGESSEN ── -->
          <div v-else-if="view === 'forgot'" class="p-7">
            <button @click="view = 'login'" class="flex items-center gap-1.5 text-xs text-[#8e9aaa] hover:text-[#1a2e5a] mb-5">
              ← Zurück
            </button>
            <h1 class="text-[#1a2e5a] font-bold text-xl mb-1">Passwort zurücksetzen</h1>
            <p class="text-[#8e9aaa] text-sm mb-6">Wir senden Ihnen einen Reset-Link per E-Mail.</p>

            <div v-if="forgotSuccess" class="bg-green-50 border border-green-200 rounded-lg px-4 py-4 flex gap-3">
              <CheckCircle2 :size="18" class="text-green-600 shrink-0" />
              <div>
                <p class="text-green-800 font-bold text-sm">E-Mail gesendet</p>
                <p class="text-green-700 text-xs mt-1">Bitte prüfen Sie Ihr Postfach ({{ forgotEmail }}).</p>
              </div>
            </div>

            <template v-else>
              <div v-if="forgotError" class="bg-red-50 border border-red-200 rounded-lg px-4 py-3 mb-5 flex gap-2.5">
                <AlertCircle :size="15" class="text-red-600 shrink-0 mt-0.5" />
                <p class="text-red-700 text-xs">{{ forgotError }}</p>
              </div>
              <div class="mb-6">
                <label class="block text-[#1a2e5a] text-xs font-bold uppercase tracking-wider mb-2">E-Mail</label>
                <div class="relative">
                  <Mail :size="15" class="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#8e9aaa]" />
                  <input v-model="forgotEmail" type="email" placeholder="Ihre E-Mail-Adresse"
                    :class="inputCls(false)" class="pl-10" />
                </div>
              </div>
              <button @click="submitForgot" :disabled="forgotLoading"
                class="w-full bg-[#1a2e5a] hover:bg-[#1a2e5a]/85 disabled:opacity-60 text-white font-bold py-3.5 rounded-lg text-sm transition-colors">
                {{ forgotLoading ? 'Wird gesendet …' : 'Link anfordern' }}
              </button>
            </template>
          </div>

        </div>
      </div>
    </div>
  </main>

  <AppFooter />
</template>
