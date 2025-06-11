import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue({
      // Performance: Enable Vue 3 optimizations
      reactivityTransform: true,
      script: {
        defineModel: true
      }
    })
  ],
  
  // Performance: Resolve aliases for better bundling
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
      '@components': resolve(__dirname, './src/components'),
      '@assets': resolve(__dirname, './src/assets')
    }
  },
  
  // Performance: Build optimizations
  build: {
    // Code splitting configuration
    rollupOptions: {
      output: {
        // Chunk splitting strategy
        manualChunks: {
          // Vendor chunks
          'vendor-vue': ['vue'],
          'vendor-charts': ['chart.js', 'vue-chartjs'],
          'vendor-http': ['axios'],
          
          // Feature chunks
          'feature-analytics': [
            './src/components/Analytics.vue',
            './src/components/SmartSuggestions.vue'
          ],
          'feature-creator': [
            './src/components/RecipeCreator.vue',
            './src/components/RecipeCreator/CustomComposition.vue',
            './src/components/RecipeCreator/RecipeGrid.vue',
            './src/components/RecipeCreator/RecipeModal.vue'
          ],
          'feature-maps': [
            './src/components/VendingMap.vue'
          ],
          'feature-loyalty': [
            './src/components/LoyaltyProgram.vue'
          ],
          'feature-mobile': [
            './src/components/MobileQrApp.vue'
          ]
        },
        
        // Asset optimization
        assetFileNames: (assetInfo) => {
          const info = assetInfo.name.split('.')
          const ext = info[info.length - 1]
          
          if (/\.(png|jpe?g|svg|gif|tiff|bmp|ico)$/i.test(assetInfo.name)) {
            return `assets/images/[name]-[hash][extname]`
          }
          if (/\.(woff2?|eot|ttf|otf)$/i.test(assetInfo.name)) {
            return `assets/fonts/[name]-[hash][extname]`
          }
          return `assets/[name]-[hash][extname]`
        },
        
        chunkFileNames: 'assets/js/[name]-[hash].js',
        entryFileNames: 'assets/js/[name]-[hash].js'
      }
    },
    
    // Performance settings
    target: 'esnext',
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
        pure_funcs: ['console.log', 'console.info']
      },
      format: {
        comments: false
      }
    },
    
    // Bundle size optimization
    chunkSizeWarningLimit: 1000,
    
    // Source maps for debugging (disabled in production)
    sourcemap: false
  },
  
  // Performance: CSS optimization
  css: {
    devSourcemap: true,
    preprocessorOptions: {
      scss: {
        additionalData: `@import "@/assets/styles/variables.scss";`
      }
    }
  },
  
  // Performance: Dependencies optimization
  optimizeDeps: {
    include: [
      'vue',
      'axios',
      'chart.js',
      'vue-chartjs'
    ],
    exclude: [
      // Large dependencies that should be lazy loaded
    ]
  },
  
  // Development server optimization
  server: {
    hmr: {
      overlay: false
    },
    host: true,
    port: 5173
  },
  
  // Performance: Preview server
  preview: {
    port: 4173,
    host: true
  },
  
  // Performance: Environment variables
  define: {
    __VUE_OPTIONS_API__: false,
    __VUE_PROD_DEVTOOLS__: false
  }
}) 