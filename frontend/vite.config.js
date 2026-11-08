import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// El proxy evita problemas de CORS/cookies en desarrollo:
// el navegador pide a :5173/api/... y Vite lo reenvía a Django :8000
// como mismo origen, así las cookies de sesión y CSRF funcionan solas.
export default defineConfig(({ command }) => ({
  // En producción Django/WhiteNoise sirve el build bajo /static/.
  base: command === 'build' ? '/static/' : '/',
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
}))
