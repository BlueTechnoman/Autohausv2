// ── useCookieConsent.ts ── Cookie-Consent-State (localStorage)
import { ref, computed } from 'vue'

const STORAGE_KEY = 'autohaus-cookie-consent'

type ConsentState = 'pending' | 'accepted' | 'rejected' | 'custom'

interface ConsentData {
  state: ConsentState
  analytics: boolean
  marketing: boolean
}

function loadFromStorage(): ConsentData | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return null
    return JSON.parse(raw) as ConsentData
  } catch {
    return null
  }
}

function saveToStorage(data: ConsentData) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
  } catch {
    // silently fail if localStorage is not available
  }
}

// Modul-Level-State
const stored = loadFromStorage()
const consentState  = ref<ConsentState>(stored?.state ?? 'pending')
const analytics     = ref<boolean>(stored?.analytics ?? false)
const marketing     = ref<boolean>(stored?.marketing ?? false)

export function useCookieConsent() {
  const showBanner = computed(() => consentState.value === 'pending')

  function accept() {
    consentState.value = 'accepted'
    analytics.value    = true
    marketing.value    = true
    saveToStorage({ state: 'accepted', analytics: true, marketing: true })
  }

  function reject() {
    consentState.value = 'rejected'
    analytics.value    = false
    marketing.value    = false
    saveToStorage({ state: 'rejected', analytics: false, marketing: false })
  }

  function saveCustom(a: boolean, m: boolean) {
    consentState.value = 'custom'
    analytics.value    = a
    marketing.value    = m
    saveToStorage({ state: 'custom', analytics: a, marketing: m })
  }

  return {
    showBanner,
    consentState,
    analytics,
    marketing,
    accept,
    reject,
    saveCustom,
  }
}
