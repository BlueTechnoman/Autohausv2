/**
 * data/fahrzeuge.ts – Typ-Definitionen & Hilfsfunktionen
 * ════════════════════════════════════════════════════════
 *
 * Diese Datei enthält NUR Typen und Hilfsfunktionen.
 * Keine statischen Daten mehr – alle Fahrzeuge kommen aus der API
 * (GET /api/vehicles/).
 *
 * Warum ist das so?
 *   Single Source of Truth: Die Datenbank (Django/SQLite) ist die
 *   einzige Quelle für Fahrzeugdaten. Das Frontend darf keine
 *   eigenen Daten erfinden oder hardcoden.
 *
 * Schnittstelle Backend ↔ Frontend:
 *   API liefert:  brand (str), model (str), mileage (int), price (str)
 *   Frontend hat: marke (str), modell (str), km (int), preis (number)
 *   Das Mapping übernimmt useFahrzeuge.ts (mapApiToFahrzeug).
 *
 * Filter-Optionen (statisch, da diese vom Frontend bestimmt werden):
 *   MARKEN, KRAFTSTOFFE, MAX_PREISE – keine DB-Abfrage nötig
 */

/** Ein Preisverlauf-Datenpunkt für das Dashboard-Diagramm */
export interface PreisPunkt {
  preis: number    // Preis in Euro
  datum: string    // ISO-Datum z.B. "2026-01-15"
  notiz: string    // optionaler Kommentar
}

/**
 * Fahrzeug – Haupt-Datentyp des Frontends.
 * Alle Felder entsprechen einem Vehicle-Datensatz aus der Django-API,
 * aber mit deutschen Bezeichnungen und aufbereiteten Typen.
 */
export interface Fahrzeug {
  id:           number
  marke:        string
  modell:       string
  baujahr:      number
  km:           number
  preis:        number          // Float, keine Dezimalstring
  status:       'available' | 'reserved' | 'sold'
  bild:         string          // URL des ersten Bildes (Fallback: Placeholder)
  // Detailseite & Dashboard
  leistung:     number          // PS
  getriebe:     string
  kraftstoff:   string
  farbe:        string
  ez:           string          // Erstzulassung z.B. "03/2021"
  tueren:       number
  hu:           string          // HU-Datum z.B. "03/2026"
  beschreibung: string
  ausstattung:  string[]        // Liste wie ["Navi", "Ledersitze"]
  bilder:       string[]        // Alle Bild-URLs für die Galerie
  preisverlauf: PreisPunkt[]    // Für Dashboard-Diagramm
}

// ── Filter-Optionen ──────────────────────────────────────────────────
// Diese werden im FilterBar-Dropdown angezeigt.
// Statisch, weil sie das Frontend-Filterverhalten definieren.

export const MARKEN = ['Alle Marken', 'Audi', 'BMW', 'Mercedes-Benz', 'Volkswagen']

/**
 * Kraftstoff-Filteroptionen.
 *
 * WICHTIG: "value" muss exakt den Backend-Choices aus vehicles/models.py
 * (KRAFTSTOFF_CHOICES) entsprechen, da f.kraftstoff genau diese rohen
 * Werte enthält (z.B. "benzin", nicht "Benzin"). Nur "label" ist die
 * deutsche Anzeige im Dropdown.
 */
export const KRAFTSTOFF_OPTIONS: { value: string; label: string }[] = [
  { value: '',            label: 'Alle Kraftstoffe' },
  { value: 'benzin',      label: 'Benzin' },
  { value: 'diesel',      label: 'Diesel' },
  { value: 'elektro',     label: 'Elektro' },
  { value: 'hybrid',      label: 'Hybrid' },
  { value: 'plug_in',     label: 'Plug-in-Hybrid' },
  { value: 'lpg',         label: 'Autogas (LPG)' },
  { value: 'erdgas',      label: 'Erdgas (CNG)' },
  { value: 'wasserstoff', label: 'Wasserstoff' },
  { value: 'sonstige',    label: 'Sonstige' },
]

/** Gibt das deutsche Label für einen rohen Kraftstoff-Wert zurück */
export function formatKraftstoff(value: string): string {
  return KRAFTSTOFF_OPTIONS.find(o => o.value === value)?.label ?? value
}

/** Getriebe-Optionen – Werte entsprechen exakt den Backend-GETRIEBE_CHOICES */
export const GETRIEBE_OPTIONS: { value: string; label: string }[] = [
  { value: '',              label: 'Alle Getriebe' },
  { value: 'manuell',       label: 'Schaltgetriebe' },
  { value: 'automatik',     label: 'Automatik' },
  { value: 'halbautomatik', label: 'Halbautomatik' },
]

/** Gibt das deutsche Label für einen rohen Getriebe-Wert zurück */
export function formatGetriebe(value: string): string {
  return GETRIEBE_OPTIONS.find(o => o.value === value)?.label ?? value
}



export const MAX_PREISE: { label: string; value: number }[] = [
  { label: 'Alle Preise',   value: 100000 },
  { label: 'bis 25.000 €',  value: 25000  },
  { label: 'bis 30.000 €',  value: 30000  },
  { label: 'bis 40.000 €',  value: 40000  },
  { label: 'bis 50.000 €',  value: 50000  },
]

// ── Hilfsfunktionen ──────────────────────────────────────────────────

/** Formatiert Kilometerstand: 48200 → "48.200 km" */
export function formatKm(km: number): string {
  return km.toLocaleString('de-DE') + ' km'
}

/** Formatiert Preis: 32900 → "32.900,00 €" (immer 2 Dezimalstellen) */
export function formatPreis(preis: number): string {
  return preis.toLocaleString('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' €'
}

/** Gibt ein lesbares Status-Label zurück */
export function formatStatus(status: Fahrzeug['status']): string {
  const map = { available: 'Verfügbar', reserved: 'Reserviert', sold: 'Verkauft' }
  return map[status] ?? status
}

/** Gibt die CSS-Klassen für das Status-Badge zurück */
export function statusBadgeClass(status: Fahrzeug['status']): string {
  switch (status) {
    case 'available': return 'bg-green-100 text-green-800'
    case 'reserved':  return 'bg-yellow-100 text-yellow-800'
    case 'sold':      return 'bg-red-100 text-red-800'
    default:          return 'bg-gray-100 text-gray-800'
  }
}