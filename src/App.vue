<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
    <!-- Header -->
    <header class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 transition-colors duration-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-20">
          <!-- Logo/Brand -->
          <div class="flex items-center flex-shrink-0">
            <div class="flex items-center">
              <!-- IKIGAI Logo Icon -->
              <div class="w-10 h-10 sm:w-12 sm:h-12 mr-4 flex items-center justify-center">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="w-8 h-8 sm:w-10 sm:h-10 text-purple-600">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M12 6v12"/>
                  <path d="M6 12h12"/>
                  <circle cx="12" cy="12" r="3" fill="url(#gradient)" stroke="none"/>
                  <defs>
                    <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" style="stop-color:#8B5CF6"/>
                      <stop offset="100%" style="stop-color:#A855F7"/>
                    </linearGradient>
                  </defs>
                </svg>
              </div>
              <h1 class="text-xl sm:text-2xl font-semibold text-gray-900 dark:text-white transition-colors duration-200">
                🌱 IKIGAI Dashboard
            </h1>
            </div>
          </div>
          
          <!-- Header Controls -->
          <div class="flex items-center space-x-2 sm:space-x-4">
            <!-- Navigation Buttons -->
            <div class="hidden sm:flex items-center space-x-3">
              <!-- Dostępne dla wszystkich -->
              <button 
                @click="navigateTo('dashboard')"
                :class="[
                  'px-4 py-2 text-base font-medium rounded-lg transition-colors duration-200',
                  currentView === 'dashboard' 
                    ? 'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300' 
                    : 'text-gray-600 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400'
                ]"
              >
                🏠 Dashboard
              </button>
              <button 
                @click="navigateTo('mixer')"
                :class="[
                  'px-4 py-2 text-base font-medium rounded-lg transition-colors duration-200',
                  currentView === 'mixer' 
                    ? 'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300' 
                    : 'text-gray-600 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400'
                ]"
              >
                🥣 Kreator
              </button>
              <button 
                @click="navigateTo('map')"
                :class="[
                  'px-4 py-2 text-base font-medium rounded-lg transition-colors duration-200',
                  currentView === 'map' 
                    ? 'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300' 
                    : 'text-gray-600 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400'
                ]"
              >
                🗺️ Mapa
              </button>
              <button
                @click="navigateTo('mobile')"
                :class="[
                  'px-4 py-2 text-base font-medium rounded-lg transition-colors duration-200',
                  currentView === 'mobile' 
                    ? 'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300' 
                    : 'text-gray-600 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400'
                ]"
              >
                📱 Mobile QR
              </button>
              
              <!-- Dostępne tylko dla zalogowanych użytkowników -->
              <button 
                v-if="currentUser"
                @click="navigateTo('social')"
                :class="[
                  'px-4 py-2 text-base font-medium rounded-lg transition-colors duration-200',
                  currentView === 'social' 
                    ? 'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300' 
                    : 'text-gray-600 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400'
                ]"
              >
                🎯 Social Challenges
              </button>
              <button 
                v-if="currentUser"
                @click="navigateTo('loyalty')"
                :class="[
                  'px-4 py-2 text-base font-medium rounded-lg transition-colors duration-200',
                  currentView === 'loyalty' 
                    ? 'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300' 
                    : 'text-gray-600 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400'
                ]"
              >
                🏆 Loyalty
              </button>
              
              <!-- Dostępne tylko dla administratorów -->
              <button 
                v-if="isAdmin"
                @click="navigateTo('analytics')"
                :class="[
                  'px-4 py-2 text-base font-medium rounded-lg transition-colors duration-200',
                  currentView === 'analytics' 
                    ? 'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300' 
                    : 'text-gray-600 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400'
                  ]"
              >
                📊 Analytics
              </button>
            </div>

            
            <!-- Dark Mode Toggle -->
            <button 
              @click="toggleDarkMode"
              class="p-2 sm:p-3 text-gray-400 dark:text-gray-300 hover:text-purple-500 dark:hover:text-purple-400 transition-colors duration-200"
              :title="darkMode ? 'Przełącz na tryb jasny' : 'Przełącz na tryb ciemny'"
            >
              <svg v-if="darkMode" class="h-6 w-6 sm:h-7 sm:w-7" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="12" cy="12" r="5"/>
                <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
              </svg>
                              <svg v-else class="h-6 w-6 sm:h-7 sm:w-7" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
                </svg>
            </button>
            
            <!-- User Menu -->
            <div class="relative">
              <!-- User Avatar / Login Button -->
              <button
                @click="toggleUserMenu"
                :class="[
                  'w-9 h-9 sm:w-10 sm:h-10 rounded-full flex items-center justify-center transition-all duration-200',
                  currentUser ? 'bg-gradient-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700' : 'bg-gray-400 hover:bg-gray-500'
                ]"
                :title="currentUser ? `Zalogowany jako: ${currentUser.name}` : 'Kliknij aby się zalogować'"
              >
                <svg v-if="currentUser" class="w-5 h-5 sm:w-6 sm:h-6 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
                <svg v-else class="w-5 h-5 sm:w-6 sm:h-6 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
                  <polyline points="10,17 15,12 10,7"/>
                  <line x1="15" y1="12" x2="3" y2="12"/>
                </svg>
              </button>

              <!-- User Dropdown Menu -->
              <div
                v-if="showUserMenu && currentUser"
                class="absolute right-0 mt-2 w-64 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-50"
                @click.stop
              >
                <!-- User Info -->
                <div class="p-4 border-b border-gray-200 dark:border-gray-700">
                  <div class="flex items-center">
                    <div class="w-10 h-10 bg-gradient-to-r from-purple-500 to-purple-600 rounded-full flex items-center justify-center">
                      <span class="text-white font-medium text-sm">
                        {{ currentUser.name.split(' ').map(n => n[0]).join('').toUpperCase() }}
                      </span>
                    </div>
                    <div class="ml-3">
                      <p class="text-sm font-medium text-gray-900 dark:text-white">{{ currentUser.name }}</p>
                      <p class="text-xs text-gray-500 dark:text-gray-400">{{ currentUser.email }}</p>
                      <p class="text-xs text-purple-600 dark:text-purple-400 font-medium">
                        {{ currentUser.role === 'admin' ? '👑 Administrator' : '👤 Użytkownik' }}
                      </p>
                    </div>
                  </div>
                </div>

                <!-- Menu Items -->
                <div class="py-2">
                  <button
                    @click="navigateTo('social'); toggleUserMenu()"
                    class="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center"
                  >
                    🎯 Social Challenges
                  </button>
                  <button
                    @click="navigateTo('loyalty'); toggleUserMenu()"
                    class="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center"
                  >
                    🏆 Program lojalnościowy
                  </button>
                  <button
                    v-if="currentUser.role === 'admin'"
                    @click="navigateTo('analytics'); toggleUserMenu()"
                    class="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center"
                  >
                    📊 Panel administracyjny
                  </button>
                  <hr class="my-2 border-gray-200 dark:border-gray-600">
                  <button
                    @click="handleLogout"
                    class="w-full px-4 py-2 text-left text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 flex items-center"
                  >
                    🚪 Wyloguj się
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Dashboard Content -->
    <main class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <IkigaiDashboard v-if="currentView === 'dashboard'" :isAdmin="isAdmin" :currentUser="currentUser" @navigate="navigateTo" />
      <RecipeCreator v-else-if="currentView === 'mixer'" @navigate="navigateTo" />
      <VendingMap v-else-if="currentView === 'map'" @navigate="navigateTo" />
      <SocialChallenges v-else-if="currentView === 'social' && currentUser" @navigate="navigateTo" />
      <LoyaltyProgram v-else-if="currentView === 'loyalty' && currentUser" @navigate="navigateTo" />
      <MobileQrApp v-else-if="currentView === 'mobile'" @back="navigateTo('dashboard')" />
      <Analytics v-else-if="currentView === 'analytics' && isAdmin" @navigate="navigateTo" />
      <!-- Fallback dla nieprawomocnego dostępu -->
      <div v-else-if="!currentUser && (currentView === 'social' || currentView === 'loyalty')" class="text-center py-12">
        <div class="text-6xl mb-4">🔒</div>
        <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">Zaloguj się aby kontynuować</h3>
        <p class="text-gray-600 dark:text-gray-400 mb-6">Ta sekcja wymaga zalogowania</p>
        <button 
          @click="showLoginForm = true" 
          class="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
        >
          🔐 Zaloguj się
        </button>
      </div>
      <div v-else-if="!isAdmin && currentView === 'analytics'" class="text-center py-12">
        <div class="text-6xl mb-4">⚠️</div>
        <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">Brak uprawnień</h3>
        <p class="text-gray-600 dark:text-gray-400 mb-6">Ta sekcja dostępna tylko dla administratorów</p>
        <button 
          @click="navigateTo('dashboard')" 
          class="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
        >
          🏠 Powrót do Dashboard
        </button>
      </div>
    </main>

    <!-- Login Modal -->
    <LoginForm
      v-if="showLoginForm"
      @close="showLoginForm = false"
      @login="handleLogin"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, defineAsyncComponent, onMounted } from 'vue'

// Core components - always loaded
import IkigaiDashboard from './components/IkigaiDashboard.vue'
import LoginForm from './components/LoginForm.vue'

// Lazy-loaded components with loading states
const RecipeCreator = defineAsyncComponent({
  loader: () => import('./components/RecipeCreator.vue'),
  loadingComponent: {
    template: `
      <div class="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div class="text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p class="text-gray-600 dark:text-gray-400">Ładowanie kreatora...</p>
        </div>
      </div>
    `
  },
  errorComponent: {
    template: `
      <div class="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div class="text-center p-8">
          <div class="text-red-500 text-4xl mb-4">⚠️</div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Błąd ładowania</h3>
          <p class="text-gray-600 dark:text-gray-400 mb-4">Nie udało się załadować kreatora</p>
          <button @click="window.location.reload()" class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700">
            Odśwież stronę
          </button>
        </div>
      </div>
    `
  },
  delay: 200,
  timeout: 10000
})

const VendingMap = defineAsyncComponent({
  loader: () => import('./components/VendingMap.vue'),
  loadingComponent: {
    template: `
      <div class="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div class="text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p class="text-gray-600 dark:text-gray-400">Ładowanie mapy...</p>
        </div>
      </div>
    `
  },
  delay: 200,
  timeout: 10000
})

const LoyaltyProgram = defineAsyncComponent({
  loader: () => import('./components/LoyaltyProgram.vue'),
  loadingComponent: {
    template: `
      <div class="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div class="text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto mb-4"></div>
          <p class="text-gray-600 dark:text-gray-400">Ładowanie programu lojalnościowego...</p>
        </div>
      </div>
    `
  },
  delay: 200,
  timeout: 10000
})

const MobileQrApp = defineAsyncComponent({
  loader: () => import('./components/MobileQrApp.vue'),
  loadingComponent: {
    template: `
      <div class="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div class="text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p class="text-gray-600 dark:text-gray-400">Ładowanie aplikacji mobile...</p>
        </div>
      </div>
    `
  },
  delay: 200,
  timeout: 10000
})

const Analytics = defineAsyncComponent({
  loader: () => import('./components/Analytics.vue'),
  loadingComponent: {
    template: `
      <div class="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div class="text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-600 mx-auto mb-4"></div>
          <p class="text-gray-600 dark:text-gray-400">Ładowanie analityki...</p>
        </div>
      </div>
    `
  },
  delay: 200,
  timeout: 10000
})

const SocialChallenges = defineAsyncComponent({
  loader: () => import('./components/SocialChallenges.vue'),
  loadingComponent: {
    template: `
      <div class="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div class="text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-pink-600 mx-auto mb-4"></div>
          <p class="text-gray-600 dark:text-gray-400">Ładowanie wyzwań społecznych...</p>
        </div>
      </div>
    `
  },
  delay: 200,
  timeout: 10000
})

// Authentication state
const currentUser = ref(null)
const showLoginForm = ref(false)
const showUserMenu = ref(false)

// Reactive state
const currentView = ref('dashboard')
const isAdmin = ref(false)
const darkMode = ref(localStorage.getItem('darkMode') === 'true')

// Authentication methods
const checkAuthStatus = async () => {
  try {
    const response = await fetch('http://localhost:5001/api/auth/profile', {
      credentials: 'include'
    })
    
    if (response.ok) {
      const data = await response.json()
      if (data.status === 'success') {
        currentUser.value = data.data
        isAdmin.value = data.data.role === 'admin'
      }
    }
  } catch (error) {
    console.log('Nie zalogowano')
  }
}

const handleLogin = (user) => {
  currentUser.value = user
  isAdmin.value = user.role === 'admin'
  showLoginForm.value = false
  showUserMenu.value = false
  
  // Show success notification
  console.log('Zalogowano pomyślnie:', user.name)
}

const handleLogout = async () => {
  try {
    await fetch('http://localhost:5001/api/auth/logout', {
      method: 'POST',
      credentials: 'include'
    })
  } catch (error) {
    console.log('Błąd podczas wylogowania')
  }
  
  currentUser.value = null
  isAdmin.value = false
  showUserMenu.value = false
  
  // Redirect to dashboard
  currentView.value = 'dashboard'
}

const toggleUserMenu = () => {
  if (currentUser.value) {
    showUserMenu.value = !showUserMenu.value
  } else {
    showLoginForm.value = true
  }
}

// Close user menu when clicking outside
const handleClickOutside = (event) => {
  if (showUserMenu.value && !event.target.closest('.relative')) {
    showUserMenu.value = false
  }
}

// Performance: Preload next likely component
const preloadComponent = (componentName) => {
  if (componentName === 'mixer') RecipeCreator
  else if (componentName === 'map') VendingMap
  else if (componentName === 'social') SocialChallenges
  else if (componentName === 'loyalty') LoyaltyProgram
  else if (componentName === 'mobile') MobileQrApp
  else if (componentName === 'analytics') Analytics
}

// Navigation with preloading
const navigateTo = (view) => {
  // Preload component before switching (performance optimization)
  preloadComponent(view)
  
  // Small delay to allow preloading
  setTimeout(() => {
    currentView.value = view
  }, 50)
}

// Theme management with performance optimization
const toggleDarkMode = () => {
  darkMode.value = !darkMode.value
  
  // Use requestAnimationFrame for smooth transition
  requestAnimationFrame(() => {
    if (darkMode.value) {
      document.documentElement.classList.add('dark')
      localStorage.setItem('darkMode', 'true')
    } else {
      document.documentElement.classList.remove('dark')
      localStorage.setItem('darkMode', 'false')
    }
  })
}

// Initialize theme
const initializeTheme = () => {
  const savedTheme = localStorage.getItem('darkMode')
  if (savedTheme === 'true') {
    darkMode.value = true
    document.documentElement.classList.add('dark')
  }
}

// Lifecycle
onMounted(() => {
  initializeTheme()
  checkAuthStatus()
  document.addEventListener('click', handleClickOutside)
})
</script>

<style>
/* Custom styles */
</style> 