/**
 * services/api.ts – Zentraler API-Client
 * ══════════════════════════════════════════
 *
 * Diese Datei ist die einzige Stelle im Frontend, die direkt
 * mit der Django REST API kommuniziert.
 *
 * Architektur (Datenfluss):
 *   Vue-Komponente
 *     → ruft Composable auf (z.B. useFahrzeuge)
 *       → Composable ruft apiFetch() auf
 *         → apiFetch() sendet HTTP-Request an /api/...
 *           → Django REST Framework verarbeitet
 *             → Antwort: JSON
 *           ← JSON zurück ins Frontend
 *         ← apiFetch() gibt getyptes Objekt zurück
 *       ← Composable speichert in reaktivem ref()
 *     ← Komponente rendert Daten reaktiv
 *
 * Sicherheit:
 *   • JWT-Token wird aus dem localStorage gelesen
 *     und automatisch als Authorization-Header mitgesendet
 *   • Kein Token → nur öffentliche Endpunkte erreichbar
 *
 * Konfiguration:
 *   VITE_API_BASE_URL aus .env – normalerweise http://localhost:8000
 *   Mit Vite-Proxy (vite.config.ts) kann man auch leer lassen.
 */

// API-Basisadresse aus Umgebungsvariable
// import.meta.env.* ist Vite-spezifisch (entspricht process.env.* in CRA)
const API_BASE = (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? ''

/**
 * Gibt die vollständige URL für ein Django-Media-Bild zurück.
 * Django speichert Bilder relativ: "vehicles/foto.jpg"
 * → wir brauchen: "http://localhost:8000/media/vehicles/foto.jpg"
 *
 * Mit Vite-Proxy (empfohlen): Einfach den Pfad direkt nutzen.
 */
export function getImageUrl(path: string): string {
  if (!path) return ''
  if (path.startsWith('http')) return path     // bereits absolute URL
  if (path.startsWith('/')) return `${API_BASE}${path}`  // z.B. /media/...
  return `${API_BASE}/media/${path}`           // relative Pfade
}

/**
 * apiFetch<T> – Universelle Fetch-Funktion
 * ──────────────────────────────────────────
 * Sendet HTTP-Request an die API und gibt getyptes T zurück.
 *
 * @param endpoint  - Pfad z.B. '/api/vehicles/' oder '/api/vehicles/1/'
 * @param options   - Optionale RequestInit-Parameter (method, body, etc.)
 * @returns         - Geparste JSON-Antwort als Typ T
 * @throws          - Error mit Fehlermeldung wenn HTTP != 2xx
 */
export async function apiFetch<T>(
  endpoint: string,
  options: RequestInit & { headers?: Record<string, string> } = {}
): Promise<T> {
  // Standard-Header: JSON-Kommunikation
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...options.headers,
  }

  // JWT-Token aus localStorage holen (gesetzt nach Login)
  const token = localStorage.getItem('auth_access')
  if (token) {
    // Bearer-Token nach RFC 6750
    headers['Authorization'] = `Bearer ${token}`
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  })

  // 204 No Content: kein Body → leeres Objekt zurück
  if (response.status === 204) return {} as T

  // Fehlerbehandlung: 4xx/5xx lösen Exception aus
  if (!response.ok) {
    let errorMessage = `HTTP ${response.status}: ${response.statusText}`
    try {
      const errorData = await response.json()
      // Django sendet Fehler meistens als { detail: "..." }
      errorMessage = errorData.detail ?? errorData.non_field_errors?.[0] ?? errorMessage
    } catch {
      // JSON-Parsing fehlgeschlagen → Standard-Fehlermeldung behalten
    }
    throw new Error(errorMessage)
  }

  return response.json() as Promise<T>
}

// ── Typen für API-Antworten ──────────────────────────────────────────

/** Bild-Objekt wie es die API zurückgibt */
export interface ApiVehicleImage {
  id:          number
  vehicle:     number
  image:       string       // relativer Pfad z.B. "vehicles/foto.jpg"
  image_url:   string | null // absolute URL (vom Serializer gebaut)
  uploaded_at: string
}

/** Preisverlauf-Eintrag aus der API */
export interface ApiPriceHistory {
  id:          number
  price:       string        // Dezimalzahl als String z.B. "32900.00"
  recorded_at: string        // ISO-Datum z.B. "2026-01-15"
  note:        string
}

/** Fahrzeug-Objekt wie es die API zurückgibt (rohe API-Felder) */
export interface ApiVehicle {
  id:           number
  brand:        string
  model:        string
  year:         number
  mileage:      number
  price:        string        // Dezimalzahl als String
  status:       'available' | 'reserved' | 'sold'
  kraftstoff:   string
  leistung:     number | null
  getriebe:     string
  farbe:        string
  ez:           string
  tueren:       number | null
  hu:           string
  beschreibung: string
  ausstattung:  string[]
  images:       ApiVehicleImage[]
  price_history:ApiPriceHistory[]
}

/** Benutzer-Objekt aus GET /api/accounts/me/ */
export interface ApiUser {
  id:       number
  username: string
  email:    string
  role:     'admin' | 'employee' | 'customer'
}

/** JWT-Token-Antwort aus POST /api/accounts/login/ */
export interface ApiTokenResponse {
  access:  string
  refresh: string
}
