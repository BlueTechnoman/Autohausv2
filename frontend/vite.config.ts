/**
 * vite.config.ts – Vite Build- & Dev-Server-Konfiguration
 * ══════════════════════════════════════════════════════════
 *
 * Was macht dieser File?
 *   • Vite ist der Build-Tool für Vue 3 (ersetzt Webpack)
 *   • Kompiliert .vue, .ts → JavaScript (im Build)
 *   • Dev-Server mit Hot-Module-Replacement (HMR)
 *
 * server.proxy (wichtig für Docker!):
 *   Im Browser läuft alles auf localhost:5173.
 *   API-Calls an /api/* werden vom Vite-Dev-Server
 *   transparent an den Django-Backend-Container
 *   (http://backend:8000 in Docker, http://localhost:8000 lokal) weitergeleitet.
 *   → Kein CORS-Problem, da Requests vom Server kommen.
 *
 * @alias '@':
 *   Erlaubt Imports wie: import X from '@/components/X.vue'
 *   Statt relativen Pfaden: import X from '../../../components/X.vue'
 */

import { defineConfig } from 'vite'
import path from 'path'
import tailwindcss from '@tailwindcss/vite'
import vue from '@vitejs/plugin-vue'

// API-Target: In Docker heißt der Backend-Container "backend"
// Lokal ohne Docker: http://localhost:8000
const API_TARGET = process.env.VITE_API_TARGET ?? 'http://localhost:8000'

export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
  ],

  resolve: {
    alias: {
      // @ zeigt auf den src-Ordner
      '@': path.resolve(__dirname, './src'),
    },
  },

  assetsInclude: ['**/*.svg', '**/*.csv'],

  server: {
    // In Docker: Host 0.0.0.0 damit der Container von außen erreichbar ist
    host: '0.0.0.0',
    port: 5173,

    proxy: {
      // Alle Requests an /api/* → Django-Backend
      '/api': {
        target: API_TARGET,
        changeOrigin: true,
        // rewrite: (path) => path  // Pfad bleibt unverändert
      },
      // Bilder/Uploads werden vom Django-Media-Server geliefert
      '/media': {
        target: API_TARGET,
        changeOrigin: true,
      },
    },
  },
})
