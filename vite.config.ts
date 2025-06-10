import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const config = {
    plugins: [vue()],
    build: {
      // OPTYMALIZACJA BUNDLE SIZE dla QR komponentów
      rollupOptions: {
        output: {
          manualChunks: {
            // Vendor chunks - oddzielne chunki dla dużych bibliotek
            'vue-vendor': ['vue'],
            'axios-vendor': ['axios'],
            'heroicons': ['@heroicons/vue/24/outline'],
            'qrcode': ['qrcode']
          }
        }
      },
      // Kompresja i minifikacja
      minify: 'terser',
      terserOptions: {
        compress: {
          drop_console: mode === 'production', // Usuń console.log w produkcji
          drop_debugger: true
        }
      },
      // Zwiększ limity dla analizy bundle size
      chunkSizeWarningLimit: 500
    },
    // Optymalizacje dev server
    optimizeDeps: {
      include: [
        'vue',
        'axios',
        '@heroicons/vue/24/outline',
        'qrcode'
      ]
    }
  }

  // Proxy tylko w developmencie
  if (mode === 'development') {
    config.server = {
      proxy: {
        '/api': {
          target: 'http://localhost:5001',
          changeOrigin: true
        }
      }
    }
  }

  return config
}) 