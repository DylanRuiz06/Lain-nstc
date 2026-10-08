import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// El proxy evita problemas de CORS/cookies en desarrollo:
// el navegador pide a :5173/api/... y Vite lo reenvía a Django :8000
// como mismo origen, así las cookies de sesión y CSRF funcionan solas.
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})
