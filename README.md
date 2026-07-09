<img width="1000" height="1429" alt="MV5BOTdkM2M1ZWEtYmYzNi00NDhhLTg1N2QtM2U0ZDEyNzg2ZjNiXkEyXkFqcGc@ _V1_FMjpg_UX1000_" src="https://github.com/user-attachments/assets/c6ba8dfe-7ce4-464a-ad44-0b2d163e7f51" />
<img width="554" height="553" alt="images (1)" src="https://github.com/user-attachments/assets/168d7c0b-f86f-4d19-bfa2-6cf04841ea37" />


Rest macht das Frontend 
die sind ja zu 3

# AutoHaus Müller – Webanwendung

> Schulprojekt AuP · FiSi · Fachinformatiker Systemintegration

---

## Projektbeschreibung

Eine vollständige Webanwendung für ein fiktives Autohaus in Bayreuth.
Das Frontend (Vue 3) kommuniziert ausschließlich über eine REST-API
mit dem Backend (Django). Die Datenbank liegt als SQLite-Datei im Backend-Container.

---

## Technologie-Stack

| Schicht     | Technologie                          |
|-------------|--------------------------------------|
| Frontend    | Vue 3 + TypeScript + Tailwind CSS v4 |
| Build-Tool  | Vite                                 |
| Backend     | Django 5 + Django REST Framework     |
| Auth        | JWT (SimpleJWT)                      |
| Datenbank   | SQLite (Datei: `backend/db.sqlite3`) |
| Container   | Docker + Docker Compose              |

---

## Architektur-Übersicht

```
┌─────────────────────────────────────────────────────┐
│  Browser                                            │
│  Vue 3 SPA (Single Page Application)                │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────────┐ │
│  │  Pages   │ │Components│ │    Composables       │ │
│  │ HomePage │ │ NavBar   │ │ useAuth (JWT-State)  │ │
│  │ Detail   │ │ FzKarte  │ │ useCart (Warenkorb)  │ │
│  │ Login    │ │ Hero     │ │ useFahrzeuge (API)   │ │
│  │ Dashboard│ │ Footer   │ │ useNotification      │ │
│  └──────────┘ └──────────┘ └──────────────────────┘ │
│                    │ HTTP (JSON)                     │
└────────────────────┼────────────────────────────────┘
                     │ Port 5173 → 8000 (Proxy)
┌────────────────────┼────────────────────────────────┐
│  Django Backend    │                                │
│  ┌──────────────────────────────────────────────┐   │
│  │  REST API (Django REST Framework)            │   │
│  │  /api/vehicles/          Fahrzeuge (CRUD)    │   │
│  │  /api/vehicle-images/    Bilder              │   │
│  │  /api/price-history/     Preisverlauf (RO)   │   │
│  │  /api/accounts/login/    JWT-Token           │   │
│  │  /api/accounts/register/ Registrierung       │   │
│  │  /api/accounts/me/       Aktueller User      │   │
│  └──────────────────────────────────────────────┘   │
│                    │                                │
│  ┌─────────────────┴──────────────────────────┐     │
│  │  SQLite-Datenbank (backend/db.sqlite3)      │     │
│  │  Tabellen: vehicles_vehicle, accounts_user  │     │
│  │  Ort im Container: /app/db.sqlite3          │     │
│  └────────────────────────────────────────────┘     │
└────────────────────────────────────────────────────┘
```

---

## Wo liegt was?

```
Autohausv2-main/
├── backend/                    ← Django-Projekt
│   ├── Autohaus/               ← Projekteinstellungen (settings.py, urls.py)
│   ├── vehicles/               ← Fahrzeuge-App (Model, View, Serializer)
│   ├── accounts/               ← User-Authentifizierung (JWT)
│   ├── db.sqlite3              ← DATENBANK (lokal, im Git-ignore)
│   ├── media/                  ← Hochgeladene Bilder (/media/vehicles/)
│   ├── requirements.txt        ← Python-Abhängigkeiten
│   └── dockerfile              ← Backend-Docker-Image
│
├── frontend/                   ← Vue 3-Projekt
│   ├── src/
│   │   ├── pages/              ← Seitenkomponenten (eine pro Route)
│   │   ├── components/         ← Wiederverwendbare UI-Komponenten
│   │   ├── composables/        ← Reaktive Logik (useAuth, useFahrzeuge, …)
│   │   ├── services/api.ts     ← HTTP-Client (alle API-Calls hier)
│   │   ├── data/fahrzeuge.ts   ← TypeScript-Typen & Hilfsfunktionen
│   │   ├── router/index.ts     ← URL-Routing + Auth-Guard
│   │   └── styles/
│   │       ├── theme.css       ← Farben & CSS-Variablen
│   │       ├── tailwind.css    ← Tailwind v4 Import
│   │       └── fonts.css       ← Schriftarten (Barlow)
│   ├── .env                    ← Umgebungsvariablen
│   ├── vite.config.ts          ← Build-Konfiguration + API-Proxy
│   ├── package.json            ← Node.js-Abhängigkeiten
│   └── dockerfile              ← Frontend-Docker-Image
│
└── docker-compose.yaml         ← Startet beide Container zusammen
```

---

## API-Endpunkte (Übersicht)

### Fahrzeuge (öffentlich, read-only aus Frontend-Sicht)
| Methode | Endpunkt                    | Beschreibung                        |
|---------|-----------------------------|-------------------------------------|
| GET     | `/api/vehicles/`            | Alle Fahrzeuge (mit Filterparametern)|
| GET     | `/api/vehicles/{id}/`       | Einzelnes Fahrzeug                  |
| GET     | `/api/vehicles/?brand=BMW`  | Filter: Marke                       |
| GET     | `/api/vehicles/?status=available` | Filter: Status               |
| GET     | `/api/vehicles/?search=GTI` | Freitextsuche                       |
| GET     | `/api/price-history/?vehicle=1` | Preisverlauf für Fahrzeug 1     |

### Authentifizierung
| Methode | Endpunkt                        | Beschreibung                    |
|---------|---------------------------------|---------------------------------|
| POST    | `/api/accounts/login/`          | Login → JWT-Token erhalten      |
| POST    | `/api/accounts/register/`       | Neues Konto anlegen             |
| POST    | `/api/accounts/refresh/`        | Access-Token erneuern           |
| GET     | `/api/accounts/me/`             | Aktuell eingeloggter Benutzer   |

### Login-Payload
```json
POST /api/accounts/login/
{ "username": "max", "password": "sicherespasswort" }

Antwort:
{ "access": "eyJ...", "refresh": "eyJ..." }
```

### Register-Payload
```json
POST /api/accounts/register/
{
  "username": "max_mustermann",
  "email": "max@beispiel.de",
  "password": "sicherespasswort123",
  "role": "customer"
}
```

---

## Docker-Setup

### Voraussetzungen
- Docker Desktop installiert (https://www.docker.com/)
- Port 8000 und 5173 frei

### Projekt starten

```bash
# 1. Repository/ZIP entpacken
cd Autohausv2-main

# 2. Alle Container bauen und starten
docker compose up --build

# 3. Datenbank initialisieren (nur beim ersten Start!)
# In einem neuen Terminal:
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
# → Benutzername, E-Mail und Passwort eingeben

# 4. Browser öffnen
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000/api/
# Django Admin: http://localhost:8000/admin/
```

### Nur Backend starten (z.B. für API-Tests)
```bash
docker compose up backend
```

### Container stoppen
```bash
docker compose down

# Mit Datenbankbereinigung (VORSICHT: Daten weg!)
docker compose down -v
```

### Testdaten eingeben (Django Admin)
1. http://localhost:8000/admin/ öffnen
2. Mit Superuser-Konto anmelden
3. Unter "Fahrzeuge" → Fahrzeug hinzufügen
4. Bilder unter "Fahrzeugbilder" hochladen
5. Preishistorie unter "Preisverlauf-Einträge" anlegen

---

## Lokale Entwicklung (ohne Docker)

### Backend
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
# → läuft auf http://localhost:8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# → läuft auf http://localhost:5173
```

---

## Umgebungsvariablen

### Frontend (frontend/.env)
| Variable             | Beschreibung                          | Standard             |
|----------------------|---------------------------------------|----------------------|
| `VITE_API_BASE_URL`  | URL der Django API                    | http://localhost:8000|
| `VITE_API_TARGET`    | Docker-interner Proxy-Target          | http://backend:8000  |

---

## Seitenstruktur

| Route          | Seite               | Auth erforderlich | Beschreibung                        |
|----------------|---------------------|-------------------|-------------------------------------|
| `/`            | Startseite          | Nein              | Hero, Fahrzeugkatalog, Kontakt      |
| `/fahrzeug/:id`| Fahrzeugdetail      | Nein              | Einzelfahrzeug mit Galerie          |
| `/ueber-uns`   | Über uns            | Nein              | Geschichte, Team, Leistungen        |
| `/login`       | Login/Registrierung | Nein              | JWT-Login, Registrierung            |
| `/warenkorb`   | Warenkorb/Checkout  | Nein              | 3-Schritt-Checkout                  |
| `/dashboard`   | Benutzer-Dashboard  | **JA** (JWT)      | Erweiterte Infos, Preisverlauf      |
| `/impressum`   | Impressum           | Nein              | Rechtliche Angaben (§5 TMG)         |
| `/datenschutz` | Datenschutz         | Nein              | DSGVO-Datenschutzerklärung          |

---

## Fachgespräch – Wichtige Konzepte

### Wo liegt die Datenbank?
SQLite-Datei: `backend/db.sqlite3`  
Im Docker-Container: `/app/db.sqlite3`  
Gesichert als Docker-Volume in `docker-compose.yaml`.

### Wie funktioniert die Authentifizierung?
1. Benutzer gibt Username + Passwort im Formular ein
2. Frontend sendet POST an `/api/accounts/login/`
3. Django prüft Passwort (bcrypt-Hash)
4. Bei Erfolg: Django gibt JWT-Access-Token + Refresh-Token zurück
5. Frontend speichert Tokens im `localStorage`
6. Alle weiteren API-Requests haben `Authorization: Bearer <token>` im Header
7. Geschützte Seite `/dashboard` prüft Token im Router-Guard (router/index.ts)

### Warum kein Vuex/Pinia?
Das Singleton-Composable-Pattern (Module-Level refs) reicht für diese Anwendung.
`useAuth`, `useCart` etc. halten ihren State auf Modul-Ebene → geteilt in der gesamten App.

### Was macht der Vite-Proxy?
Der Browser läuft auf Port 5173. API-Calls an `/api/*` werden vom
Vite-Dev-Server transparent an Port 8000 weitergeleitet → kein CORS-Problem.

### Wie werden Bilder ausgeliefert?
1. Admin lädt Bild im Django-Admin hoch
2. Django speichert Datei unter `backend/media/vehicles/`
3. Django-Media-Server liefert: `http://localhost:8000/media/vehicles/datei.jpg`
4. Serializer baut `image_url` mit `request.build_absolute_uri()` → absolute URL
5. Frontend zeigt `<img :src="image_url">` direkt

---

*Erstellt: 2026 · AutoHaus Müller GmbH · Bayreuth*
