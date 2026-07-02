/**
 * composables/useFahrzeuge.ts – Fahrzeugdaten aus der API
 * ═══════════════════════════════════════════════════════
 *
 * Lädt Fahrzeuge von GET /api/vehicles/ und mappt die API-Felder
 * (Englisch: brand, model, mileage) auf deutsche Vue-Felder
 * (marke, modell, km) aus der Fahrzeug-Interface.
 *
 * Warum ein eigenes Composable?
 *   Trennung von Verantwortlichkeiten:
 *   • Komponente  = Darstellung (Template, CSS)
 *   • Composable  = Datenlogik (API-Call, Mapping, Laden-State)
 *   → Komponente bleibt schlank und testbar
 *
 * Verwendung:
 *   const { fahrzeuge, loading, error, laden } = useFahrzeuge()
 *   await laden()  // lädt Fahrzeuge von API
 *
 * Fallback-Bild:
 *   Wenn ein Fahrzeug kein Bild hat, wird ein Unsplash-Placeholder gezeigt.
 */

import { ref } from 'vue'
import { apiFetch, getImageUrl, type ApiVehicle, type PaginatedResponse } from '../services/api'
import type { Fahrzeug } from '../data/fahrzeuge'

// Fallback-Bild wenn kein Foto hochgeladen
const PLACEHOLDER_IMAGE = 'https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=800&h=500&fit=crop&auto=format'

/**
 * mapApiToFahrzeug – Übersetzt API-Daten → Frontend-Typ
 *
 * Die Django-API spricht Englisch (brand, model, mileage, price als String).
 * Das Frontend arbeitet mit deutschen Bezeichnungen (marke, modell, km)
 * und erwartet Zahlen statt Strings.
 */
export function mapApiToFahrzeug(raw: ApiVehicle): Fahrzeug {
  // Bilder: image_url bevorzugen, sonst getImageUrl() für relative Pfade
  const bilder = raw.images
    .map(img => img.image_url ?? getImageUrl(img.image))
    .filter(Boolean) as string[]

  return {
    id:          raw.id,
    marke:       raw.brand,
    modell:      raw.model,
    baujahr:     raw.year,
    km:          raw.mileage,
    // price kommt als String "32900.00" → parseFloat → Zahl 32900
    preis:       parseFloat(raw.price),
    status:      raw.status,
    bild:        bilder[0] ?? PLACEHOLDER_IMAGE,
    bilder:      bilder.length > 0 ? bilder : [PLACEHOLDER_IMAGE],
    kraftstoff:  raw.kraftstoff ?? '',
    leistung:    raw.leistung   ?? 0,
    getriebe:    raw.getriebe   ?? '',
    farbe:       raw.farbe      ?? '',
    ez:          raw.ez         ?? '',
    tueren:      raw.tueren     ?? 4,
    hu:          raw.hu         ?? '',
    beschreibung:raw.beschreibung ?? '',
    ausstattung: raw.ausstattung  ?? [],
    preisverlauf: raw.price_history.map(p => ({
      preis:  parseFloat(p.price),
      datum:  p.recorded_at,
      notiz:  p.note,
    })),
  }
}

export function useFahrzeuge() {
  /** Geladene Fahrzeuge (reaktiv – Vue re-rendert wenn sich dies ändert) */
  const fahrzeuge   = ref<Fahrzeug[]>([])
  const loading     = ref(false)
  const loadingMore = ref(false)
  const error       = ref<string | null>(null)

  /** Gesamtzahl der Fahrzeuge auf dem Server (über alle Seiten hinweg) */
  const gesamtAnzahl = ref(0)
  /** Gibt es noch weitere Seiten zum Nachladen? */
  const hasMore = ref(false)

  // Aktuelle Seite + zuletzt genutzte Filter, damit "Mehr laden" dieselben
  // Filterparameter mit der naechsten Seite weiterverwendet.
  let currentPage = 1
  let currentParams: Record<string, string | number> = {}

  function buildEndpoint(params: Record<string, string | number>, page: number): string {
    // Query-String aufbauen: { brand: 'BMW', year: 2021 } → ?brand=BMW&year=2021
    const query = new URLSearchParams()
    Object.entries(params).forEach(([key, val]) => {
      if (val !== '' && val !== undefined) query.append(key, String(val))
    })
    if (page > 1) query.append('page', String(page))

    return `/api/vehicles/${query.toString() ? '?' + query.toString() : ''}`
  }

  /**
   * laden() – Lädt die erste Seite der Fahrzeuge von der API
   * Optional können API-Filterparameter übergeben werden:
   *   laden({ brand: 'BMW', status: 'available' })
   */
  async function laden(params: Record<string, string | number> = {}): Promise<void> {
    loading.value = true
    error.value   = null
    currentPage   = 1
    currentParams = params

    try {
      // Die Liste ist paginiert (Backend-Update): die API liefert
      // { count, next, previous, results: [...] } statt einer nackten
      // Liste. Die eigentlichen Fahrzeuge stecken in "results".
      const raw = await apiFetch<PaginatedResponse<ApiVehicle>>(buildEndpoint(params, 1))

      // API-Daten → Vue-Frontend-Format mappen
      fahrzeuge.value  = raw.results.map(mapApiToFahrzeug)
      gesamtAnzahl.value = raw.count
      hasMore.value      = raw.next !== null

    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Fehler beim Laden der Fahrzeuge.'
      console.error('[useFahrzeuge] Ladefehler:', err)
    } finally {
      loading.value = false
    }
  }

  /**
   * mehrLaden() – Lädt die nächste Seite nach und hängt sie an die
   * bereits geladenen Fahrzeuge an ("Mehr laden"-Button).
   * Nutzt dieselben Filterparameter wie der letzte laden()-Aufruf.
   */
  async function mehrLaden(): Promise<void> {
    if (!hasMore.value || loadingMore.value) return

    loadingMore.value = true
    error.value = null

    try {
      const nextPage = currentPage + 1
      const raw = await apiFetch<PaginatedResponse<ApiVehicle>>(buildEndpoint(currentParams, nextPage))

      fahrzeuge.value = [...fahrzeuge.value, ...raw.results.map(mapApiToFahrzeug)]
      gesamtAnzahl.value = raw.count
      hasMore.value      = raw.next !== null
      currentPage        = nextPage

    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Fehler beim Nachladen der Fahrzeuge.'
      console.error('[useFahrzeuge] Nachladefehler:', err)
    } finally {
      loadingMore.value = false
    }
  }

  /**
   * ladenAlle() – Lädt WIRKLICH alle Fahrzeuge, seitenweise im Hintergrund
   * nachgeladen bis keine weitere Seite mehr da ist.
   *
   * Für Ansichten wie das Dashboard gedacht, die (anders als die öffentliche
   * Startseite mit "Mehr laden"-Button) die komplette Liste zum Filtern
   * brauchen, z.B. weil Statistik-Kacheln (gesamt/verfügbar/reserviert)
   * auf der vollständigen Liste basieren.
   */
  async function ladenAlle(params: Record<string, string | number> = {}): Promise<void> {
    await laden(params)
    while (hasMore.value) {
      await mehrLaden()
    }
  }

  /**
   * ladenEinzel() – Lädt ein einzelnes Fahrzeug per ID
   * GET /api/vehicles/{id}/
   */
  async function ladenEinzel(id: number): Promise<Fahrzeug | null> {
    try {
      const raw = await apiFetch<ApiVehicle>(`/api/vehicles/${id}/`)
      return mapApiToFahrzeug(raw)
    } catch (err: unknown) {
      console.error('[useFahrzeuge] Einzelladefehler:', err)
      return null
    }
  }

  return {
    fahrzeuge,
    loading,
    loadingMore,
    error,
    gesamtAnzahl,
    hasMore,
    laden,
    ladenAlle,
    mehrLaden,
    ladenEinzel,
  }
}