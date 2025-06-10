<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
    <!-- Header -->
    <header class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 transition-colors duration-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Main Header Row -->
        <div class="flex justify-between items-center h-16">
          <!-- Logo/Brand -->
          <div class="flex items-center flex-shrink-0">
            <h1 class="text-lg sm:text-xl font-semibold text-gray-900 dark:text-white transition-colors duration-200">
              <span class="hidden sm:inline">SKATECROSS - Centrum Startu & QR</span>
              <span class="sm:hidden">SKATECROSS</span>
              <span v-if="isAdmin" class="ml-1 sm:ml-2 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200">
                🔧
                <span class="hidden sm:inline ml-1">ADMIN</span>
              </span>
            </h1>
          </div>
          
          <!-- Header Controls -->
          <div class="flex items-center space-x-2 sm:space-x-4">
            <!-- Admin Toggle -->
            <div class="flex items-center space-x-1 sm:space-x-2">
              <label class="text-xs sm:text-sm text-gray-600 dark:text-gray-300 hidden sm:inline">Admin:</label>
              <button
                @click="toggleAdminMode"
                :class="[
                  'relative inline-flex h-5 w-9 sm:h-6 sm:w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2',
                  isAdmin ? 'bg-indigo-600' : 'bg-gray-200 dark:bg-gray-600'
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
              class="p-1 sm:p-2 text-gray-400 dark:text-gray-300 hover:text-gray-500 dark:hover:text-gray-200 transition-colors duration-200"
              :title="isDarkMode ? 'Przełącz na tryb jasny' : 'Przełącz na tryb ciemny'"
            >
              <SunIcon v-if="isDarkMode" class="h-5 w-5 sm:h-6 sm:w-6" />
              <MoonIcon v-else class="h-5 w-5 sm:h-6 sm:w-6" />
            </button>
            
            <!-- User Avatar -->
            <div class="w-7 h-7 sm:w-8 sm:h-8 bg-indigo-500 rounded-full flex items-center justify-center">
              <span class="text-white text-xs sm:text-sm font-medium">{{ isAdmin ? 'A' : 'U' }}</span>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Navigation Tabs -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="border-b border-gray-200 dark:border-gray-700">
        <nav class="-mb-px flex flex-wrap gap-x-4 gap-y-2 sm:space-x-8 sm:gap-y-0" aria-label="Tabs">
          <button
            v-for="tab in availableTabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              activeTab === tab.id
                ? 'border-indigo-500 text-indigo-600 dark:text-indigo-400'
                : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600',
              'whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm transition-colors duration-200 flex items-center'
            ]"
          >
            <component :is="tab.icon" class="h-4 w-4 sm:h-5 sm:w-5 mr-1 sm:mr-2" />
            <span class="text-xs sm:text-sm">{{ tab.name }}</span>
          </button>
        </nav>
      </div>
    </div>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Centrum Startu -->
      <div v-if="activeTab === 'start-line'">
        <StartLineScanner />
      </div>

      <!-- Drukowanie QR -->
      <div v-if="activeTab === 'qr-print'">
        <QrPrint />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { 
  SunIcon, 
  MoonIcon,
  QrCodeIcon,
  PrinterIcon
} from '@heroicons/vue/24/outline'
import StartLineScanner from './components/StartLineScanner.vue'
import QrPrint from './components/QrPrint.vue'

// Reactive variables
const isAdmin = ref(true)
const isDarkMode = ref(localStorage.getItem('darkMode') === 'true')
const activeTab = ref('start-line')

// Tabs configuration - tylko Centrum Startu i Drukowanie QR
const tabs = [
  { id: 'start-line', name: 'Centrum Startu', icon: QrCodeIcon, adminOnly: true },
  { id: 'qr-print', name: 'Drukowanie QR', icon: PrinterIcon, adminOnly: true }
]

// Computed
const availableTabs = computed(() => {
  return tabs.filter(tab => !tab.adminOnly || isAdmin.value)
})

// Methods
const toggleAdminMode = () => {
  isAdmin.value = !isAdmin.value
  // Jeśli nie admin i jesteśmy na admin-only tabie, przełącz na pierwszą dostępną
  if (!isAdmin.value && !availableTabs.value.find(t => t.id === activeTab.value)) {
    activeTab.value = availableTabs.value[0]?.id || 'start-line'
  }
}

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
  // Zapisz preferencje w localStorage
  localStorage.setItem("darkMode", isDarkMode.value.toString())
  // Aplikuj dark mode do dokumentu
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

// Lifecycle
onMounted(() => {
  // Inicjalizacja dark mode na podstawie localStorage
  if (isDarkMode.value) {
    document.documentElement.classList.add("dark")
  } else {
    document.documentElement.classList.remove("dark")
  }
})
</script>

<style>
/* Custom styles if needed */
</style> 