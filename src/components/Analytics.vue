<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <!-- Analytics Icon -->
        <div class="w-8 h-8 bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg flex items-center justify-center">
          <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
            <path d="M7 16l3-3 3 3 4-6"/>
            <circle cx="7" cy="16" r="1" fill="currentColor"/>
            <circle cx="10" cy="13" r="1" fill="currentColor"/>
            <circle cx="13" cy="16" r="1" fill="currentColor"/>
            <circle cx="17" cy="10" r="1" fill="currentColor"/>
          </svg>
        </div>
        <div>
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white">📊 Analityka IKIGAI</h1>
          <p class="text-gray-600 dark:text-gray-400">Statystyki i wykres sprzedaży</p>
        </div>
      </div>
      
      <div class="flex items-center space-x-3">
        <button class="px-4 py-2 bg-gradient-to-r from-purple-500 to-purple-600 text-white rounded-lg hover:scale-105 transition-transform duration-200 flex items-center space-x-2">
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="7,10 12,15 17,10"/>
            <line x1="12" y1="15" x2="12" y2="3"/>
          </svg>
          <span>Eksportuj Raport</span>
        </button>
      </div>
    </div>

    <!-- KPI Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Sprzedaż dzisiaj</p>
            <p class="text-2xl font-bold text-gray-900 dark:text-white">47</p>
            <p class="text-sm text-green-600 dark:text-green-400 font-medium">+12% ↗</p>
          </div>
          <div class="w-12 h-12 bg-purple-100 dark:bg-purple-900 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-purple-600 dark:text-purple-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17M17 13v6a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2v-6.001"/>
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Przychód</p>
            <p class="text-2xl font-bold text-gray-900 dark:text-white">428zł</p>
            <p class="text-sm text-green-600 dark:text-green-400 font-medium">+8% ↗</p>
          </div>
          <div class="w-12 h-12 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-green-600 dark:text-green-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <line x1="12" y1="1" x2="12" y2="23"/>
              <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Średnia na zamówienie</p>
            <p class="text-2xl font-bold text-gray-900 dark:text-white">9.11zł</p>
            <p class="text-sm text-blue-600 dark:text-blue-400 font-medium">-3% ↘</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-blue-600 dark:text-blue-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 6v6l4 2"/>
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Popularność IKIGAI</p>
            <p class="text-2xl font-bold text-gray-900 dark:text-white">94%</p>
            <p class="text-sm text-green-600 dark:text-green-400 font-medium">+5% ↗</p>
          </div>
          <div class="w-12 h-12 bg-emerald-100 dark:bg-emerald-900 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-emerald-600 dark:text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M20 6L9 17l-5-5"/>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Sales Chart -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
        <div class="p-6 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
            <svg class="w-5 h-5 mr-2 text-purple-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M7 16l3-3 3 3 4-6"/>
            </svg>
            Sprzedaż w czasie
          </h3>
          <p class="text-gray-600 dark:text-gray-400">Ostatnie 7 dni</p>
        </div>
        <div class="p-6">
          <!-- Simple Chart Representation -->
          <div class="flex items-end justify-between h-48 space-x-2">
            <div class="flex flex-col items-center space-y-2">
              <div class="w-8 bg-gradient-to-t from-purple-500 to-purple-600 rounded-t" style="height: 60%"></div>
              <span class="text-xs text-gray-600 dark:text-gray-400">Pon</span>
            </div>
            <div class="flex flex-col items-center space-y-2">
              <div class="w-8 bg-gradient-to-t from-purple-500 to-purple-600 rounded-t" style="height: 45%"></div>
              <span class="text-xs text-gray-600 dark:text-gray-400">Wt</span>
            </div>
            <div class="flex flex-col items-center space-y-2">
              <div class="w-8 bg-gradient-to-t from-purple-500 to-purple-600 rounded-t" style="height: 80%"></div>
              <span class="text-xs text-gray-600 dark:text-gray-400">Śr</span>
            </div>
            <div class="flex flex-col items-center space-y-2">
              <div class="w-8 bg-gradient-to-t from-purple-500 to-purple-600 rounded-t" style="height: 65%"></div>
              <span class="text-xs text-gray-600 dark:text-gray-400">Czw</span>
            </div>
            <div class="flex flex-col items-center space-y-2">
              <div class="w-8 bg-gradient-to-t from-purple-500 to-purple-600 rounded-t" style="height: 90%"></div>
              <span class="text-xs text-gray-600 dark:text-gray-400">Pt</span>
            </div>
            <div class="flex flex-col items-center space-y-2">
              <div class="w-8 bg-gradient-to-t from-purple-500 to-purple-600 rounded-t" style="height: 75%"></div>
              <span class="text-xs text-gray-600 dark:text-gray-400">Sob</span>
            </div>
            <div class="flex flex-col items-center space-y-2">
              <div class="w-8 bg-gradient-to-t from-purple-500 to-purple-600 rounded-t" style="height: 55%"></div>
              <span class="text-xs text-gray-600 dark:text-gray-400">Ndz</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Top Products -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
        <div class="p-6 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
            <svg class="w-5 h-5 mr-2 text-green-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M20 6L9 17l-5-5"/>
            </svg>
            Najpopularniejsze produkty
          </h3>
          <p class="text-gray-600 dark:text-gray-400">Top 5 tego tygodnia</p>
        </div>
        <div class="p-6">
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="w-8 h-8 bg-gradient-to-r from-green-500 to-green-600 rounded-lg flex items-center justify-center text-white text-sm font-bold">1</div>
                <span class="font-medium text-gray-900 dark:text-white">Protein Shake</span>
              </div>
              <span class="text-green-600 dark:text-green-400 font-medium">23 szt</span>
            </div>
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg flex items-center justify-center text-white text-sm font-bold">2</div>
                <span class="font-medium text-gray-900 dark:text-white">Green Smoothie</span>
              </div>
              <span class="text-blue-600 dark:text-blue-400 font-medium">18 szt</span>
            </div>
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="w-8 h-8 bg-gradient-to-r from-orange-500 to-orange-600 rounded-lg flex items-center justify-center text-white text-sm font-bold">3</div>
                <span class="font-medium text-gray-900 dark:text-white">Energy Bar</span>
              </div>
              <span class="text-orange-600 dark:text-orange-400 font-medium">15 szt</span>
            </div>
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="w-8 h-8 bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg flex items-center justify-center text-white text-sm font-bold">4</div>
                <span class="font-medium text-gray-900 dark:text-white">Vitamin Water</span>
              </div>
              <span class="text-purple-600 dark:text-purple-400 font-medium">12 szt</span>
            </div>
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="w-8 h-8 bg-gradient-to-r from-pink-500 to-pink-600 rounded-lg flex items-center justify-center text-white text-sm font-bold">5</div>
                <span class="font-medium text-gray-900 dark:text-white">Berry Bowl</span>
              </div>
              <span class="text-pink-600 dark:text-pink-400 font-medium">9 szt</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Additional Analytics -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
      <div class="p-6 border-b border-gray-200 dark:border-gray-700">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">🎯 IKIGAI Analytics</h3>
        <p class="text-gray-600 dark:text-gray-400">Filozofia zdrowych wyborów w liczbach</p>
      </div>
      
      <div class="p-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="text-center">
            <div class="w-16 h-16 bg-gradient-to-r from-green-500 to-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M20 6L9 17l-5-5"/>
              </svg>
            </div>
            <h4 class="font-semibold text-gray-900 dark:text-white mb-2">94% Satysfakcji</h4>
            <p class="text-sm text-gray-600 dark:text-gray-400">Klienci wybierają zdrowe opcje</p>
          </div>

          <div class="text-center">
            <div class="w-16 h-16 bg-gradient-to-r from-blue-500 to-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 6v6l4 2"/>
              </svg>
            </div>
            <h4 class="font-semibold text-gray-900 dark:text-white mb-2">45s Średni Czas</h4>
            <p class="text-sm text-gray-600 dark:text-gray-400">Od skanowania QR do odbioru</p>
          </div>

          <div class="text-center">
            <div class="w-16 h-16 bg-gradient-to-r from-purple-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
              </svg>
            </div>
            <h4 class="font-semibold text-gray-900 dark:text-white mb-2">+24% Wzrost</h4>
            <p class="text-sm text-gray-600 dark:text-gray-400">Miesięczny wzrost sprzedaży</p>
          </div>
        </div>

        <div class="flex items-center justify-center mt-8">
          <p class="text-center text-gray-600 dark:text-gray-400">
            <span class="font-semibold text-purple-600 dark:text-purple-400">IKIGAI</span> - 
            Czynienie zdrowych wyborów łatwymi i dostępnymi
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Komponent placeholder dla Analityki IKIGAI
</script>

<style scoped>
/* Custom styles */
</style> 