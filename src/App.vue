<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
    <!-- Header -->
    <header class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 transition-colors duration-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo/Brand -->
          <div class="flex items-center flex-shrink-0">
            <div class="flex items-center">
              <!-- IKIGAI Logo Icon -->
              <div class="w-8 h-8 sm:w-10 sm:h-10 mr-3 flex items-center justify-center">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="w-6 h-6 sm:w-8 sm:h-8 text-purple-600">
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
              <h1 class="text-lg sm:text-xl font-semibold text-gray-900 dark:text-white transition-colors duration-200">
                🌱 IKIGAI Dashboard
                <span v-if="isAdmin" class="ml-1 sm:ml-2 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200">
                  <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 15l-3-3h6l-3 3z"/>
                    <path d="M17 8l-5-5-5 5"/>
                  </svg>
                  <span class="hidden sm:inline ml-1">ADMIN</span>
                </span>
              </h1>
            </div>
          </div>
          
          <!-- Header Controls -->
          <div class="flex items-center space-x-2 sm:space-x-4">
            <!-- Navigation Buttons -->
            <div class="hidden sm:flex items-center space-x-2">
              <button 
                @click="navigateTo('dashboard')"
                :class="[
                  'px-3 py-1.5 text-sm font-medium rounded-lg transition-colors duration-200',
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
                  'px-3 py-1.5 text-sm font-medium rounded-lg transition-colors duration-200',
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
                  'px-3 py-1.5 text-sm font-medium rounded-lg transition-colors duration-200',
                  currentView === 'map' 
                    ? 'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300' 
                    : 'text-gray-600 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400'
                ]"
              >
                🗺️ Mapa
              </button>
              <button 
                @click="navigateTo('loyalty')"
                :class="[
                  'px-3 py-1.5 text-sm font-medium rounded-lg transition-colors duration-200',
                  currentView === 'loyalty' 
                    ? 'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300' 
                    : 'text-gray-600 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400'
                ]"
              >
                🏆 Loyalty
              </button>
              <button 
                @click="navigateTo('mobile')"
                :class="[
                  'px-3 py-1.5 text-sm font-medium rounded-lg transition-colors duration-200',
                  currentView === 'mobile' 
                    ? 'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300' 
                    : 'text-gray-600 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400'
                ]"
              >
                📱 Mobile QR
              </button>
            </div>
            <!-- Admin Toggle -->
            <div class="flex items-center space-x-1 sm:space-x-2">
              <label class="text-xs sm:text-sm text-gray-600 dark:text-gray-300 hidden sm:inline">Admin:</label>
              <button
                @click="toggleAdminMode"
                :class="[
                  'relative inline-flex h-5 w-9 sm:h-6 sm:w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2',
                  isAdmin ? 'bg-gradient-to-r from-purple-500 to-purple-600' : 'bg-gray-200 dark:bg-gray-600'
                ]"
              >
                <span
                  :class="[
                    'pointer-events-none inline-block h-4 w-4 sm:h-5 sm:w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                    isAdmin ? 'translate-x-4 sm:translate-x-5' : 'translate-x-0'
                  ]"
                />
              </button>
            </div>
            
            <!-- Dark Mode Toggle -->
            <button 
              @click="toggleDarkMode"
              class="p-1 sm:p-2 text-gray-400 dark:text-gray-300 hover:text-purple-500 dark:hover:text-purple-400 transition-colors duration-200"
              :title="isDarkMode ? 'Przełącz na tryb jasny' : 'Przełącz na tryb ciemny'"
            >
              <svg v-if="isDarkMode" class="h-5 w-5 sm:h-6 sm:w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="12" cy="12" r="5"/>
                <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
              </svg>
              <svg v-else class="h-5 w-5 sm:h-6 sm:w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
              </svg>
            </button>
            
            <!-- User Avatar -->
            <div class="w-7 h-7 sm:w-8 sm:h-8 bg-gradient-to-r from-purple-500 to-purple-600 rounded-full flex items-center justify-center">
              <span class="text-white text-xs sm:text-sm font-medium">{{ isAdmin ? 'A' : 'U' }}</span>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Dashboard Content -->
    <main class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <IkigaiDashboard v-if="currentView === 'dashboard'" :isAdmin="isAdmin" @navigate="navigateTo" />
      <MixtureCreator v-else-if="currentView === 'mixer'" @navigate="navigateTo" />
      <VendingMap v-else-if="currentView === 'map'" @navigate="navigateTo" />
      <LoyaltyProgram v-else-if="currentView === 'loyalty'" @navigate="navigateTo" />
      <MobileQrApp v-else-if="currentView === 'mobile'" @back="navigateTo('dashboard')" />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import IkigaiDashboard from './components/IkigaiDashboard.vue'
import MixtureCreator from './components/MixtureCreator.vue'
import VendingMap from './components/VendingMap.vue'
import LoyaltyProgram from './components/LoyaltyProgram.vue'
import MobileQrApp from './components/MobileQrApp.vue'

// Reactive variables
const isAdmin = ref(true)
const isDarkMode = ref(localStorage.getItem('darkMode') === 'true')
const currentView = ref('dashboard') // 'dashboard' lub 'mixer'

// Methods
const navigateTo = (view: string) => {
  currentView.value = view
}

const toggleAdminMode = () => {
  isAdmin.value = !isAdmin.value
}

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
  localStorage.setItem("darkMode", isDarkMode.value.toString())
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

// Lifecycle
onMounted(() => {
  if (isDarkMode.value) {
    document.documentElement.classList.add("dark")
  } else {
    document.documentElement.classList.remove("dark")
  }
})
</script>

<style>
/* Custom styles */
</style> 