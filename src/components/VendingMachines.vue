<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <!-- Machines Icon -->
        <div class="w-8 h-8 bg-gradient-to-r from-green-500 to-green-600 rounded-lg flex items-center justify-center">
          <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <rect x="4" y="2" width="16" height="20" rx="2" ry="2"/>
            <rect x="7" y="6" width="4" height="2" rx="1"/>
            <rect x="13" y="6" width="4" height="2" rx="1"/>
            <circle cx="12" cy="18" r="1"/>
          </svg>
        </div>
        <div>
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white">🏪 Automaty IKIGAI</h1>
          <p class="text-gray-600 dark:text-gray-400">Zarządzanie automatami vendingowymi</p>
        </div>
      </div>
      
      <div class="flex items-center space-x-3">
        <a href="http://localhost:5001/api/vending-machines" target="_blank" 
           class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors duration-200 flex items-center space-x-2">
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
            <polyline points="15,3 21,3 21,9"/>
            <line x1="10" y1="14" x2="21" y2="3"/>
          </svg>
          <span>Machines API</span>
        </a>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Wszystkie</p>
            <p class="text-2xl font-bold text-gray-900 dark:text-white">3</p>
          </div>
          <div class="w-12 h-12 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-green-600 dark:text-green-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="4" y="2" width="16" height="20" rx="2" ry="2"/>
              <circle cx="12" cy="18" r="1"/>
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Online</p>
            <p class="text-2xl font-bold text-gray-900 dark:text-white">2</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-blue-600 dark:text-blue-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="12" cy="12" r="10"/>
              <path d="M9 12l2 2 4-4"/>
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Konserwacja</p>
            <p class="text-2xl font-bold text-gray-900 dark:text-white">1</p>
          </div>
          <div class="w-12 h-12 bg-orange-100 dark:bg-orange-900 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-orange-600 dark:text-orange-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Machines -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
      <div class="p-6 border-b border-gray-200 dark:border-gray-700">
        <h2 class="text-lg font-semibold text-gray-900 dark:text-white">🏪 Automaty Vendingowe</h2>
        <p class="text-gray-600 dark:text-gray-400">Status automatów IKIGAI w czasie rzeczywistym</p>
      </div>
      
      <div class="p-6">
        <!-- Poziomy scroll kontener -->
        <div class="overflow-x-auto">
          <div class="flex gap-4 pb-4" style="min-width: max-content;">
            <!-- IKIGAI Central -->
            <div class="p-6 border border-gray-200 dark:border-gray-700 rounded-lg min-w-80 bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 border-green-200 dark:border-green-700">
              <div class="flex items-center justify-between mb-4">
                <h3 class="font-semibold text-gray-900 dark:text-white text-lg">IKIGAI Central</h3>
                <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                  🟢 Online
                </span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">Centrum Handlowe - Poziom 1</p>
              <div class="text-xs text-gray-500 dark:text-gray-500">ul. Główna 123, Warszawa</div>
              <div class="mt-4 flex items-center justify-between">
                <div class="text-sm text-green-600 dark:text-green-400 font-medium">Stock: 42/50</div>
                <div class="text-xs text-gray-500 dark:text-gray-500">06:00-22:00</div>
              </div>
            </div>

            <!-- IKIGAI Fitness -->
            <div class="p-6 border border-gray-200 dark:border-gray-700 rounded-lg min-w-80 bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 border-blue-200 dark:border-blue-700">
              <div class="flex items-center justify-between mb-4">
                <h3 class="font-semibold text-gray-900 dark:text-white text-lg">IKIGAI Fitness</h3>
                <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                  🟢 Online
                </span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">Siłownia FitZone</p>
              <div class="text-xs text-gray-500 dark:text-gray-500">ul. Sportowa 45, Warszawa</div>
              <div class="mt-4 flex items-center justify-between">
                <div class="text-sm text-green-600 dark:text-green-400 font-medium">Stock: 28/30</div>
                <div class="text-xs text-gray-500 dark:text-gray-500">05:00-23:00</div>
              </div>
            </div>

            <!-- IKIGAI Office -->
            <div class="p-6 border border-gray-200 dark:border-gray-700 rounded-lg min-w-80 bg-gradient-to-br from-orange-50 to-orange-100 dark:from-orange-900/20 dark:to-orange-800/20 border-orange-200 dark:border-orange-700">
              <div class="flex items-center justify-between mb-4">
                <h3 class="font-semibold text-gray-900 dark:text-white text-lg">IKIGAI Office</h3>
                <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200">
                  🔧 Serwis
                </span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">Biurowiec Alpha Tower</p>
              <div class="text-xs text-gray-500 dark:text-gray-500">ul. Biznesowa 78, Warszawa</div>
              <div class="mt-4 flex items-center justify-between">
                <div class="text-sm text-orange-600 dark:text-orange-400 font-medium">Stock: 0/40</div>
                <div class="text-xs text-gray-500 dark:text-gray-500">07:00-19:00</div>
              </div>
            </div>

            <!-- Więcej automatów dla demonstracji przewijania -->
            <div class="p-6 border border-gray-200 dark:border-gray-700 rounded-lg min-w-80 bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/20 border-purple-200 dark:border-purple-700">
              <div class="flex items-center justify-between mb-4">
                <h3 class="font-semibold text-gray-900 dark:text-white text-lg">IKIGAI Mall</h3>
                <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                  🟢 Online
                </span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">Galeria Centrum</p>
              <div class="text-xs text-gray-500 dark:text-gray-500">ul. Handlowa 12, Warszawa</div>
              <div class="mt-4 flex items-center justify-between">
                <div class="text-sm text-green-600 dark:text-green-400 font-medium">Stock: 35/50</div>
                <div class="text-xs text-gray-500 dark:text-gray-500">10:00-22:00</div>
              </div>
            </div>

            <div class="p-6 border border-gray-200 dark:border-gray-700 rounded-lg min-w-80 bg-gradient-to-br from-teal-50 to-teal-100 dark:from-teal-900/20 dark:to-teal-800/20 border-teal-200 dark:border-teal-700">
              <div class="flex items-center justify-between mb-4">
                <h3 class="font-semibold text-gray-900 dark:text-white text-lg">IKIGAI University</h3>
                <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                  🟢 Online
                </span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">Kampus Główny</p>
              <div class="text-xs text-gray-500 dark:text-gray-500">ul. Uniwersytecka 1, Warszawa</div>
              <div class="mt-4 flex items-center justify-between">
                <div class="text-sm text-green-600 dark:text-green-400 font-medium">Stock: 18/30</div>
                <div class="text-xs text-gray-500 dark:text-gray-500">06:00-20:00</div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Wskazówka przewijania -->
        <div class="mt-4 flex items-center justify-center text-sm text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-700 rounded-lg py-2">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"></path>
          </svg>
          Przewiń w prawo aby zobaczyć więcej automatów →
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Komponent IKIGAI VendingMachines
</script>

<style scoped>
/* Custom styles */
</style> 