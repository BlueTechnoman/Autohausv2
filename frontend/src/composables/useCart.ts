// ── useCart.ts ── Singleton-Composable für globalen Warenkorb-State
import { ref, computed } from 'vue'
import type { Fahrzeug } from '../data/fahrzeuge'
import { formatPreis } from '../data/fahrzeuge'

// Modul-Level-Refs = einmalige Instanz, geteilt über alle Komponenten
const cartFahrzeuge = ref<Fahrzeug[]>([])

export function useCart() {
  // ── Computed ──────────────────────────────────────────────────────
  const cartCount = computed(() => cartFahrzeuge.value.length)

  const cartTotal = computed(() =>
    cartFahrzeuge.value.reduce((sum, f) => sum + f.preis, 0)
  )

  const cartTotalFormatted = computed(() => formatPreis(cartTotal.value))

  // ── Helpers ───────────────────────────────────────────────────────
  function isInCart(id: number): boolean {
    return cartFahrzeuge.value.some((f) => f.id === id)
  }

  // ── Aktionen ──────────────────────────────────────────────────────
  /** Gibt true zurück wenn hinzugefügt, false wenn entfernt */
  function toggle(fahrzeug: Fahrzeug): boolean {
    if (isInCart(fahrzeug.id)) {
      cartFahrzeuge.value = cartFahrzeuge.value.filter((f) => f.id !== fahrzeug.id)
      return false
    } else {
      cartFahrzeuge.value = [...cartFahrzeuge.value, fahrzeug]
      return true
    }
  }

  function remove(id: number) {
    cartFahrzeuge.value = cartFahrzeuge.value.filter((f) => f.id !== id)
  }

  function clear() {
    cartFahrzeuge.value = []
  }

  return {
    cartItems: cartFahrzeuge,
    cartCount,
    cartTotal,
    cartTotalFormatted,
    isInCart,
    toggle,
    remove,
    clear,
  }
}
