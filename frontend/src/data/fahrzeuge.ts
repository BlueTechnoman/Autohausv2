// ── Typ-Definition ───────────────────────────────────────────────────
export interface Fahrzeug {
  id: number
  marke: string
  modell: string
  baujahr: number
  km: number
  kraftstoff: string
  preis: number
  bild: string
}

// ── Fahrzeugdaten ────────────────────────────────────────────────────
export const FAHRZEUGE: Fahrzeug[] = [
  {
    id: 1,
    marke: 'BMW',
    modell: '3er Touring 320d',
    baujahr: 2021,
    km: 48200,
    kraftstoff: 'Diesel',
    preis: 32900,
    bild: 'https://images.unsplash.com/photo-1569021476330-3545605d7062?w=800&h=500&fit=crop&auto=format',
  },
  {
    id: 2,
    marke: 'Volkswagen',
    modell: 'Golf 8 GTI',
    baujahr: 2022,
    km: 21500,
    kraftstoff: 'Benzin',
    preis: 38500,
    bild: 'https://images.unsplash.com/photo-1565786089437-496904c48734?w=800&h=500&fit=crop&auto=format',
  },
  {
    id: 3,
    marke: 'Volkswagen',
    modell: 'Passat Variant 2.0 TDI',
    baujahr: 2020,
    km: 67800,
    kraftstoff: 'Diesel',
    preis: 24900,
    bild: 'https://images.unsplash.com/photo-1572811298797-9eecadf6cb24?w=800&h=500&fit=crop&auto=format',
  },
  {
    id: 4,
    marke: 'Mercedes-Benz',
    modell: 'C 220 d Avantgarde',
    baujahr: 2021,
    km: 39100,
    kraftstoff: 'Diesel',
    preis: 41200,
    bild: 'https://images.unsplash.com/photo-1624085568108-36410cfe4d24?w=800&h=500&fit=crop&auto=format',
  },
  {
    id: 5,
    marke: 'BMW',
    modell: 'X3 xDrive20d M Sport',
    baujahr: 2022,
    km: 29400,
    kraftstoff: 'Diesel',
    preis: 47800,
    bild: 'https://images.unsplash.com/photo-1691111375360-81227c67d093?w=800&h=500&fit=crop&auto=format',
  },
  {
    id: 6,
    marke: 'Audi',
    modell: 'A4 Avant 35 TDI',
    baujahr: 2020,
    km: 55600,
    kraftstoff: 'Diesel',
    preis: 28900,
    bild: 'https://images.unsplash.com/photo-1585390062628-be8608aa7d83?w=800&h=500&fit=crop&auto=format',
  },
]

// ── Filter-Optionen ──────────────────────────────────────────────────
export const MARKEN = ['Alle Marken', 'Audi', 'BMW', 'Mercedes-Benz', 'Volkswagen']

export const KRAFTSTOFFE = ['Alle', 'Benzin', 'Diesel', 'Elektro', 'Hybrid']

export const MAX_PREISE: { label: string; value: number }[] = [
  { label: 'Alle Preise',  value: 100000 },
  { label: 'bis 25.000 €', value: 25000 },
  { label: 'bis 30.000 €', value: 30000 },
  { label: 'bis 40.000 €', value: 40000 },
  { label: 'bis 50.000 €', value: 50000 },
]

// ── Hilfsfunktionen ──────────────────────────────────────────────────
export function formatKm(km: number): string {
  return km.toLocaleString('de-DE') + ' km'
}

export function formatPreis(preis: number): string {
  return preis.toLocaleString('de-DE') + ' €'
}
