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
            </div>

            
            <!-- Dark Mode Toggle -->
            <button 
              @click="toggleDarkMode"
              class="p-2 sm:p-3 text-gray-400 dark:text-gray-300 hover:text-purple-500 dark:hover:text-purple-400 transition-colors duration-200"
              :title="isDarkMode ? 'Przełącz na tryb jasny' : 'Przełącz na tryb ciemny'"
            >
              <svg v-if="isDarkMode" class="h-6 w-6 sm:h-7 sm:w-7" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="12" cy="12" r="5"/>
                <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
              </svg>
              <svg v-else class="h-6 w-6 sm:h-7 sm:w-7" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
              </svg>
            </button>
            
            <!-- User Avatar -->
            <div class="w-9 h-9 sm:w-10 sm:h-10 bg-gradient-to-r from-purple-500 to-purple-600 rounded-full flex items-center justify-center">
              <svg class="w-5 h-5 sm:w-6 sm:h-6 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Dashboard Content -->
    <main class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
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
const isAdmin = ref(false)
const isDarkMode = ref(localStorage.getItem('darkMode') === 'true')
const currentView = ref('dashboard') // 'dashboard' lub 'mixer'

// Methods
const navigateTo = (view: string) => {
  currentView.value = view
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