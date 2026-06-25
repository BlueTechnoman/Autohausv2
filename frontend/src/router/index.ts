/**
 * router/index.ts – Vue Router 4 Konfiguration
 * ══════════════════════════════════════════════
 *
 * Routing = Welche URL zeigt welche Komponente?
 *
 * createWebHistory():
 *   Nutzt die HTML5 History API (saubere URLs ohne # Symbol)
 *   Beispiel: /fahrzeug/3 statt /#/fahrzeug/3
 *   Wichtig: Der Webserver muss alle Pfade auf index.html leiten
 *   (In der Vite-Dev-Umgebung passiert das automatisch)
 *
 * Navigation Guard (beforeEach):
 *   Wird VOR jedem Seitenwechsel ausgeführt.
 *   Prüft ob die Zielseite einen Login erfordert (meta.requiresAuth).
 *   Wenn ja und kein JWT-Token → Weiterleitung zur Login-Seite
 *   mit ?redirect=<ursprüngliche Seite> im Query-Parameter,
 *   damit nach dem Login dorthin weitergeleitet werden kann.
 *
 * Lazy Loading (import()):
 *   Seiten werden erst geladen wenn sie gebraucht werden.
 *   Verbessert die initiale Ladezeit.
 */

import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),

  // scrollBehavior: Wo scrollt die Seite hin bei Navigation?
  scrollBehavior(to, _from, savedPosition) {
    if (savedPosition) return savedPosition           // Browser Zurück/Vor-Button
    if (to.hash) {
      // Hash-Navigation (#fahrzeuge): kleiner Delay wegen Page-Transition
      return new Promise((resolve) => {
        setTimeout(() => resolve({ el: to.hash, behavior: 'smooth', top: 80 }), 100)
      })
    }
    return { top: 0 }  // Neue Seite: immer nach oben scrollen
  },

  routes: [
    // ── Öffentliche Seiten ────────────────────────────────────────
    {
      path: '/',
      name: 'Home',
      component: () => import('../pages/HomePage.vue'),
      // meta: kein requiresAuth → für alle zugänglich
    },
    {
      path: '/ueber-uns',
      name: 'UeberUns',
      component: () => import('../pages/UeberUnsPage.vue'),
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('../pages/LoginPage.vue'),
    },
    {
      path: '/fahrzeug/:id',
      name: 'FahrzeugDetail',
      component: () => import('../pages/FahrzeugDetailPage.vue'),
    },
    {
      path: '/warenkorb',
      name: 'Warenkorb',
      component: () => import('../pages/WarenkorbPage.vue'),
    },
    {
      path: '/impressum',
      name: 'Impressum',
      component: () => import('../pages/ImpressumPage.vue'),
    },
    {
      path: '/datenschutz',
      name: 'Datenschutz',
      component: () => import('../pages/DatenschutzPage.vue'),
    },

    // ── Geschützte Seite (nur für eingeloggte Nutzer) ─────────────
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('../pages/DashboardPage.vue'),
      meta: {
        // requiresAuth: true → der beforeEach-Guard prüft dies
        requiresAuth: true,
      },
    },

    // ── 404 – muss am Ende stehen ─────────────────────────────────
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('../pages/NotFoundPage.vue'),
    },
  ],
})

// ── Navigation Guard ──────────────────────────────────────────────────
/**
 * beforeEach(): Wird VOR JEDEM Seitenwechsel aufgerufen.
 * to  = Ziel-Route
 * from = Herkunfts-Route
 * Rückgabe: undefined = Navigation fortsetzen | { path } = umleiten
 */
router.beforeEach((to, _from) => {
  // Braucht die Seite einen Login?
  if (to.meta.requiresAuth) {
    // JWT-Token aus localStorage prüfen
    const token = localStorage.getItem('auth_access')
    if (!token) {
      // Kein Token → zur Login-Seite, mit redirect-Parameter
      return {
        path: '/login',
        query: { redirect: to.fullPath },
      }
    }
    // Token vorhanden → Navigation erlauben (Server prüft Gültigkeit separat)
  }
  // Navigation erlaubt
})

export default router
