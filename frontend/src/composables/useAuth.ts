/**
 * composables/useAuth.ts – Authentifizierungs-State (Singleton)
 * ══════════════════════════════════════════════════════════════
 *
 * Verwaltet den Login-Status des Benutzers mit JWT (JSON Web Tokens).
 *
 * Was ist JWT?
 *   JWT = JSON Web Token. Nach dem Login gibt der Server zwei Tokens:
 *   • access  (gültig 8 Stunden) – für API-Anfragen im Authorization-Header
 *   • refresh (gültig 7 Tage)    – um neuen Access-Token zu holen ohne erneuten Login
 *   Beide werden im localStorage des Browsers gespeichert.
 *
 * Singleton-Pattern:
 *   Die refs (accessToken, user, etc.) liegen auf Modul-Ebene,
 *   nicht innerhalb der Funktion. Dadurch teilen alle Komponenten
 *   denselben State – kein Vuex/Pinia nötig.
 *
 * Validierung beim Login:
 *   Frontend-Validierung verhindert, dass leere/unsichere Eingaben
 *   überhaupt an den Server geschickt werden.
 *   Serverseitig validiert Django zusätzlich (Passwortlänge, etc.).
 *
 * Verwendung:
 *   const { isLoggedIn, user, login, logout } = useAuth()
 */

import { ref, computed } from 'vue'
import { apiFetch, type ApiUser, type ApiTokenResponse } from '../services/api'

// ── Modul-Level Singleton-State ──────────────────────────────────────
// Diese refs existieren einmal für die gesamte App
const accessToken  = ref<string | null>(localStorage.getItem('auth_access'))
const refreshToken = ref<string | null>(localStorage.getItem('auth_refresh'))
const user         = ref<ApiUser | null>(null)
const authLoading  = ref(false)
const authError    = ref<string | null>(null)

// Beim ersten Import: User-Daten laden falls Token vorhanden
if (accessToken.value) {
  // Async in Modul-Top-Level nicht möglich → fire-and-forget
  fetchCurrentUser()
}

/** Lädt den eingeloggten User von der API */
async function fetchCurrentUser(): Promise<void> {
  if (!accessToken.value) return
  try {
    user.value = await apiFetch<ApiUser>('/api/accounts/me/')
  } catch {
    // Token ungültig → ausloggen
    performLogout()
  }
}

/** Räumt Token und User-State auf */
function performLogout(): void {
  accessToken.value  = null
  refreshToken.value = null
  user.value         = null
  localStorage.removeItem('auth_access')
  localStorage.removeItem('auth_refresh')
}

// ── Frontend-Validierung ──────────────────────────────────────────────

/**
 * Validiert Login-Eingaben VOR dem API-Call.
 * Verhindert XSS-Versuche und leere Felder.
 * Gibt null zurück wenn OK, sonst Fehlermeldung.
 */
function validateLoginInput(username: string, password: string): string | null {
  if (!username.trim()) return 'Benutzername darf nicht leer sein.'
  if (username.length > 150) return 'Benutzername zu lang.'
  if (!password) return 'Passwort darf nicht leer sein.'
  // Einfacher XSS-Check: HTML-Tags verboten
  if (/<[^>]+>/.test(username) || /<[^>]+>/.test(password)) {
    return 'Ungültige Zeichen in der Eingabe.'
  }
  return null
}

/**
 * Validiert Registrierungseingaben.
 * Überprüft: Länge, Format, Passwort-Stärke, E-Mail-Format.
 */
function validateRegisterInput(
  username: string, email: string, password: string, password2: string
): string | null {
  // Benutzername
  if (!username.trim()) return 'Benutzername ist erforderlich.'
  if (username.length < 3) return 'Benutzername muss mindestens 3 Zeichen haben.'
  if (username.length > 150) return 'Benutzername zu lang (max. 150 Zeichen).'
  if (!/^[a-zA-Z0-9@.+\-_]+$/.test(username)) {
    return 'Benutzername darf nur Buchstaben, Zahlen und @.+-_ enthalten.'
  }

  // E-Mail
  if (!email.trim()) return 'E-Mail ist erforderlich.'
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return 'Ungültige E-Mail-Adresse.'

  // Passwort-Stärke
  if (password.length < 8) return 'Passwort muss mindestens 8 Zeichen lang sein.'
  if (/^\d+$/.test(password)) return 'Passwort darf nicht nur aus Zahlen bestehen.'
  if (/^(.)\1+$/.test(password)) return 'Passwort ist zu einfach.'

  // Passwörter übereinstimmen
  if (password !== password2) return 'Die Passwörter stimmen nicht überein.'

  // Injection-Check
  if (/<[^>]+>/.test(username) || /<[^>]+>/.test(email)) {
    return 'Ungültige Zeichen in der Eingabe.'
  }

  return null  // alles OK
}

// ── Exportiertes Composable ───────────────────────────────────────────
export function useAuth() {
  /** true wenn gültiger Access-Token vorhanden */
  const isLoggedIn = computed(() => !!accessToken.value)

  /**
   * login() – Sendet Zugangsdaten an /api/accounts/login/
   * Empfängt JWT-Tokens und speichert sie im localStorage.
   * Lädt danach den User-Datensatz (/api/accounts/me/).
   */
  async function login(username: string, password: string): Promise<{ success: boolean; error?: string }> {
    // Frontend-Validierung
    const validationError = validateLoginInput(username, password)
    if (validationError) return { success: false, error: validationError }

    authLoading.value = true
    authError.value   = null

    try {
      const data = await apiFetch<ApiTokenResponse>('/api/accounts/login/', {
        method: 'POST',
        body:   JSON.stringify({ username: username.trim(), password }),
      })

      // Tokens im State & localStorage speichern
      accessToken.value  = data.access
      refreshToken.value = data.refresh
      localStorage.setItem('auth_access',  data.access)
      localStorage.setItem('auth_refresh', data.refresh)

      // User-Daten laden
      await fetchCurrentUser()
      return { success: true }

    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Login fehlgeschlagen.'
      authError.value = msg
      return { success: false, error: msg }
    } finally {
      authLoading.value = false
    }
  }

  /**
   * register() – Registriert neuen Benutzer über /api/accounts/register/
   * Sendet: username, email, password, role="customer"
   */
  async function register(
    username: string, email: string, password: string, password2: string
  ): Promise<{ success: boolean; error?: string }> {
    const validationError = validateRegisterInput(username, email, password, password2)
    if (validationError) return { success: false, error: validationError }

    authLoading.value = true
    authError.value   = null

    try {
      await apiFetch('/api/accounts/register/', {
        method: 'POST',
        body:   JSON.stringify({
          username: username.trim(),
          email:    email.trim(),
          password,
          role:     'customer',  // Standard-Rolle für neue Nutzer
        }),
      })
      // Nach Registrierung direkt einloggen
      return await login(username, password)

    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Registrierung fehlgeschlagen.'
      authError.value = msg
      return { success: false, error: msg }
    } finally {
      authLoading.value = false
    }
  }

  /** logout() – Löscht alle Token und User-Daten */
  function logout(): void {
    performLogout()
  }

  return {
    // State (read-only von außen)
    isLoggedIn,
    user,
    accessToken: computed(() => accessToken.value),
    authLoading,
    authError,
    // Aktionen
    login,
    register,
    logout,
    fetchCurrentUser,
  }
}
