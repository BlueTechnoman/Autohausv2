import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior(to, _from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.hash) {
      return new Promise((resolve) => {
        setTimeout(() => resolve({ el: to.hash, behavior: 'smooth', top: 80 }), 100)
      })
    }
    return { top: 0 }
  },
  routes: [
    // ── Öffentliche Seiten ──────────────────────────────────────────
    { path: '/',            name: 'Home',        component: () => import('../pages/HomePage.vue') },
    { path: '/ueber-uns',   name: 'UeberUns',    component: () => import('../pages/UeberUnsPage.vue') },
    { path: '/login',       name: 'Login',       component: () => import('../pages/LoginPage.vue') },
    { path: '/fahrzeug/:id',name: 'FahrzeugDetail', component: () => import('../pages/FahrzeugDetailPage.vue') },
    { path: '/warenkorb',   name: 'Warenkorb',   component: () => import('../pages/WarenkorbPage.vue') },
    { path: '/impressum',   name: 'Impressum',   component: () => import('../pages/ImpressumPage.vue') },
    { path: '/datenschutz', name: 'Datenschutz', component: () => import('../pages/DatenschutzPage.vue') },
    { path: '/agb',         name: 'AGB',         component: () => import('../pages/AgbPage.vue') },

    // ── Geschützte Seiten (Login erforderlich) ──────────────────────
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('../pages/DashboardPage.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/termine',
      name: 'Termine',
      component: () => import('../pages/TerminePage.vue'),
      meta: { requiresAuth: true },
    },

    // ── Nur Admin + Employee ────────────────────────────────────────
    {
      path: '/anfragen',
      name: 'Anfragen',
      component: () => import('../pages/AnfragenPage.vue'),
      meta: { requiresAuth: true, requiresRole: ['admin', 'employee'] },
    },
    {
      path: '/fahrzeug-anlegen',
      name: 'FahrzeugAnlegen',
      component: () => import('../pages/FahrzeugAnlegenPage.vue'),
      meta: { requiresAuth: true, requiresRole: ['admin', 'employee'] },
    },

    // ── 404 ─────────────────────────────────────────────────────────
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import('../pages/NotFoundPage.vue') },
  ],
})

router.beforeEach((to, _from) => {
  const token    = localStorage.getItem('auth_access')
  const userRaw  = localStorage.getItem('auth_user')
  const userRole = userRaw ? JSON.parse(userRaw)?.role : null

  // Login erforderlich?
  if (to.meta.requiresAuth && !token) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }

  // Rolle erforderlich?
  const roles = to.meta.requiresRole as string[] | undefined
  if (roles && token && !roles.includes(userRole)) {
    return { path: '/dashboard' }
  }
})

export default router
