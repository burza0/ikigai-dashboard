import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

// Performance: Preload critical resources
const preloadCriticalResources = () => {
  // Preload fonts
  const fontLink = document.createElement('link')
  fontLink.rel = 'preload'
  fontLink.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap'
  fontLink.as = 'style'
  fontLink.onload = function() { this.rel = 'stylesheet' }
  document.head.appendChild(fontLink)
}

// Performance: Initialize performance monitoring
const initPerformanceMonitoring = () => {
  // Measure Core Web Vitals
  if ('performance' in window && 'PerformanceObserver' in window) {
    // Largest Contentful Paint (LCP)
    new PerformanceObserver((entryList) => {
      for (const entry of entryList.getEntries()) {
        console.log('[Performance] LCP:', entry.startTime)
      }
    }).observe({entryTypes: ['largest-contentful-paint']})

    // First Input Delay (FID)
    new PerformanceObserver((entryList) => {
      for (const entry of entryList.getEntries()) {
        console.log('[Performance] FID:', entry.processingStart - entry.startTime)
      }
    }).observe({entryTypes: ['first-input']})

    // Cumulative Layout Shift (CLS)
    new PerformanceObserver((entryList) => {
      for (const entry of entryList.getEntries()) {
        if (!entry.hadRecentInput) {
          console.log('[Performance] CLS:', entry.value)
        }
      }
    }).observe({entryTypes: ['layout-shift']})
  }
}

// Performance: App initialization with optimization
const initializeApp = async () => {
  try {
    // Preload critical resources
    preloadCriticalResources()
    
    // Initialize performance monitoring
    initPerformanceMonitoring()
    
    // Create Vue app with performance config
    const app = createApp(App)
    
    // Performance: Configure Vue for production
    if (import.meta.env.PROD) {
      app.config.performance = true
      app.config.silent = true
    } else {
      app.config.performance = true
      console.log('[IKIGAI] Development mode with performance monitoring')
    }
    
    // Global error handler for better UX
    app.config.errorHandler = (err, vm, info) => {
      console.error('[IKIGAI Error]:', err, info)
      // In production, send to error tracking service
      if (import.meta.env.PROD) {
        // Could integrate with Sentry, LogRocket, etc.
      }
    }
    
    // Mount app
    app.mount('#app')
    
    console.log('🌱 IKIGAI Dashboard v3.0 - Ready!')
    console.log('📊 Performance monitoring enabled')
    console.log('🎯 Week 4: Advanced Analytics + Performance')
    
  } catch (error) {
    console.error('[IKIGAI] Failed to initialize app:', error)
  }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeApp)
} else {
  initializeApp()
} 