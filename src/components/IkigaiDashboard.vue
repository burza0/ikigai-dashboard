<template>
  <div class="space-y-8">
    <!-- Tools & Quick Actions -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
            <svg class="w-5 h-5 mr-2 text-purple-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
              <path d="M9 9h6v6H9z"/>
            </svg>
            Your tools / data
          </h2>
          <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Szybki dostęp do kluczowych funkcji IKIGAI
          </p>
        </div>
      </div>
      
      <div class="grid grid-cols-6 md:grid-cols-12 gap-4">
        <a href="http://localhost:5001/api/products" target="_blank" 
           class="flex flex-col items-center p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg hover:scale-105 transition-transform duration-200 border border-purple-200 dark:border-purple-700">
          <svg class="w-6 h-6 text-purple-600 mb-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
            <circle cx="9" cy="9" r="2"/>
          </svg>
          <span class="text-xs text-purple-700 dark:text-purple-300 text-center">Products API</span>
        </a>
        
        <a href="http://localhost:5001/api/orders" target="_blank"
           class="flex flex-col items-center p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg hover:scale-105 transition-transform duration-200 border border-blue-200 dark:border-blue-700">
          <svg class="w-6 h-6 text-blue-600 mb-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M9 12l2 2 4-4"/>
            <circle cx="12" cy="12" r="10"/>
          </svg>
          <span class="text-xs text-blue-700 dark:text-blue-300 text-center">Orders API</span>
        </a>
        
        <a href="http://localhost:5001/api/vending-machines" target="_blank"
           class="flex flex-col items-center p-3 bg-green-50 dark:bg-green-900/20 rounded-lg hover:scale-105 transition-transform duration-200 border border-green-200 dark:border-green-700">
          <svg class="w-6 h-6 text-green-600 mb-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <rect x="4" y="2" width="16" height="20" rx="2" ry="2"/>
            <circle cx="12" cy="18" r="1"/>
          </svg>
          <span class="text-xs text-green-700 dark:text-green-300 text-center">Machines API</span>
        </a>
        
        <a href="http://localhost:5001/automat" target="_blank"
           class="flex flex-col items-center p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg hover:scale-105 transition-transform duration-200 border border-orange-200 dark:border-orange-700">
          <svg class="w-6 h-6 text-orange-600 mb-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <rect x="3" y="3" width="5" height="5"/>
            <rect x="16" y="3" width="5" height="5"/>
            <rect x="3" y="16" width="5" height="5"/>
          </svg>
          <span class="text-xs text-orange-700 dark:text-orange-300 text-center">Demo Automat</span>
        </a>
        
        <button class="flex flex-col items-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg hover:scale-105 transition-transform duration-200 border border-gray-200 dark:border-gray-600">
          <svg class="w-6 h-6 text-gray-600 dark:text-gray-400 mb-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
          </svg>
          <span class="text-xs text-gray-700 dark:text-gray-300 text-center">Settings</span>
        </button>
        
        <button class="flex flex-col items-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg hover:scale-105 transition-transform duration-200 border border-gray-200 dark:border-gray-600">
          <svg class="w-6 h-6 text-gray-600 dark:text-gray-400 mb-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="7,10 12,15 17,10"/>
            <line x1="12" y1="15" x2="12" y2="3"/>
          </svg>
          <span class="text-xs text-gray-700 dark:text-gray-300 text-center">Export</span>
        </button>
      </div>
    </div>

    <!-- Main Dashboard Grid -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
      <div class="flex items-center mb-6">
        <svg class="w-6 h-6 mr-3 text-gray-700 dark:text-gray-300" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
          <path d="M7 16l3-3 3 3 4-6"/>
        </svg>
        <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Visualization</h2>
      </div>
      
      <!-- Dashboard Cards Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Kreator Mieszanek - Purple (GŁÓWNA FUNKCJA) -->
        <div @click="$emit('navigate', 'mixer')" class="md:col-span-1 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl p-6 text-white hover:scale-[1.02] transition-transform duration-200 cursor-pointer">
          <div class="flex items-center mb-4">
            <svg class="w-8 h-8 mr-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 6v12"/>
              <path d="M6 12h12"/>
              <circle cx="12" cy="12" r="3"/>
            </svg>
            <h3 class="text-lg font-semibold">🥣 Kreator Mieszanek</h3>
          </div>
          <p class="text-purple-100 mb-4">Skomponuj swoją idealną mieszankę szczęścia IKIGAI</p>
          <div class="text-2xl font-bold mb-2">4 bazy + 6 dodatków</div>
          <div class="text-purple-200 text-sm">Rozpocznij podróż! ✨</div>
        </div>

        <!-- Orders & QR Workflow - Blue -->
        <div class="md:col-span-1 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white hover:scale-[1.02] transition-transform duration-200 cursor-pointer">
          <div class="flex items-center mb-4">
            <svg class="w-8 h-8 mr-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M9 12l2 2 4-4"/>
              <circle cx="12" cy="12" r="10"/>
            </svg>
            <h3 class="text-lg font-semibold">📦 Orders</h3>
          </div>
          <p class="text-blue-100 mb-4">QR workflow management system</p>
          <div class="text-2xl font-bold mb-2">847 zamówień</div>
          <div class="text-blue-200 text-sm">+12% ten miesiąc ↗</div>
        </div>

        <!-- Mapa Automatów - Green -->
        <div @click="$emit('navigate', 'map')" class="md:col-span-1 bg-gradient-to-br from-green-500 to-green-600 rounded-xl p-6 text-white hover:scale-[1.02] transition-transform duration-200 cursor-pointer">
          <div class="flex items-center mb-4">
            <svg class="w-8 h-8 mr-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
              <circle cx="12" cy="10" r="3"/>
            </svg>
            <h3 class="text-lg font-semibold">🗺️ Mapa Automatów</h3>
          </div>
          <p class="text-green-100 mb-4">Interaktywna mapa z lokalizacjami automatów IKIGAI</p>
          <div class="text-2xl font-bold mb-2">3 lokalizacje</div>
          <div class="text-green-200 text-sm">Znajdź najbliższy automat 📍</div>
        </div>

        <!-- Program Lojalnościowy - Orange -->
        <div @click="$emit('navigate', 'loyalty')" class="md:col-span-1 bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl p-6 text-white hover:scale-[1.02] transition-transform duration-200 cursor-pointer">
          <div class="flex items-center mb-4">
            <svg class="w-8 h-8 mr-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M12 6v6l4 2"/>
              <circle cx="12" cy="12" r="10"/>
            </svg>
            <h3 class="text-lg font-semibold">🏆 Program Lojalnościowy</h3>
          </div>
          <p class="text-orange-100 mb-4">Zbieraj punkty, podejmuj wyzwania, zyskuj nagrody</p>
          <div class="text-2xl font-bold mb-2">5 wyzwań</div>
          <div class="text-orange-200 text-sm">Zacznij zbierać punkty! 🌟</div>
        </div>

        <!-- Mobile QR App - Pink/Purple -->
        <div @click="$emit('navigate', 'mobile')" class="md:col-span-1 bg-gradient-to-br from-pink-500 to-purple-600 rounded-xl p-6 text-white hover:scale-[1.02] transition-transform duration-200 cursor-pointer">
          <div class="flex items-center mb-4">
            <svg class="w-8 h-8 mr-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="5" y="2" width="14" height="20" rx="2" ry="2"/>
              <path d="M12 18h.01"/>
              <rect x="8" y="6" width="8" height="8"/>
            </svg>
            <h3 class="text-lg font-semibold">📱 Mobile QR App</h3>
          </div>
          <p class="text-pink-100 mb-4">Skanowanie QR, płatności mobilne, push notifications</p>
          <div class="text-2xl font-bold mb-2">3 funkcje</div>
          <div class="text-pink-200 text-sm">Zaawansowane możliwości mobilne 🚀</div>
        </div>

        <!-- Analytics - Orange (Admin only) -->
        <div v-if="isAdmin" class="md:col-span-2 lg:col-span-3 bg-gradient-to-br from-red-500 to-red-600 rounded-xl p-6 text-white hover:scale-[1.02] transition-transform duration-200 cursor-pointer">
          <div class="flex items-center mb-4">
            <svg class="w-8 h-8 mr-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
              <path d="M7 16l3-3 3 3 4-6"/>
            </svg>
            <h3 class="text-xl font-semibold">📊 Analytics & Insights</h3>
            <span class="ml-auto px-2 py-1 bg-red-400 rounded-full text-xs font-medium">ADMIN</span>
          </div>
          <p class="text-red-100 mb-4">Zaawansowane analizy sprzedaży, KPI i trendy zdrowotne</p>
          <div class="grid grid-cols-3 gap-4">
            <div>
              <div class="text-2xl font-bold">12,456zł</div>
              <div class="text-red-200 text-sm">Przychód</div>
            </div>
            <div>
              <div class="text-2xl font-bold">94%</div>
              <div class="text-red-200 text-sm">Satysfakcja</div>
            </div>
            <div>
              <div class="text-2xl font-bold">234</div>
              <div class="text-red-200 text-sm">Aktywni klienci</div>
            </div>
          </div>
        </div>

        <!-- IKIGAI Philosophy - Yellow -->
        <div :class="[isAdmin ? 'md:col-span-2 lg:col-span-3' : 'md:col-span-2 lg:col-span-3']" class="bg-gradient-to-br from-yellow-400 to-yellow-500 rounded-xl p-6 text-gray-900 hover:scale-[1.02] transition-transform duration-200 cursor-pointer">
          <div class="flex items-center mb-4">
            <div class="w-8 h-8 mr-3 bg-gray-900 rounded-full flex items-center justify-center">
              <span class="text-yellow-400 text-sm font-bold">生</span>
            </div>
            <h3 class="text-xl font-semibold">🌱 IKIGAI Philosophy</h3>
          </div>
          <p class="text-gray-800 mb-4">
            <strong>IKIGAI</strong> (生き甲斐) - "powód istnienia". Łączymy zdrowe odżywianie z nowoczesną technologią.
          </p>
          <div class="text-lg font-semibold">Healthy choices made easy</div>
        </div>
      </div>
    </div>

    <!-- Health Environment Status -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Environment Status -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
          <svg class="w-5 h-5 mr-2 text-green-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M20 6L9 17l-5-5"/>
          </svg>
          Your environment
        </h3>
        <p class="text-gray-600 dark:text-gray-400 mb-4">
          Połączenia z systemami zdrowotnymi i aplikacjami fitness
        </p>
        
        <div class="space-y-3">
          <div class="flex items-center justify-between p-3 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-700">
            <span class="text-green-700 dark:text-green-300">MyFitnessPal Integration</span>
            <span class="text-green-600 text-sm">✓ Connected</span>
          </div>
          <div class="flex items-center justify-between p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-700">
            <span class="text-blue-700 dark:text-blue-300">Apple Health Sync</span>
            <span class="text-blue-600 text-sm">✓ Active</span>
          </div>
          <div class="flex items-center justify-between p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-700">
            <span class="text-purple-700 dark:text-purple-300">Strava Workouts</span>
            <span class="text-purple-600 text-sm">✓ Synced</span>
          </div>
        </div>
      </div>

      <!-- No Lock-in / Open Standards -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
          <svg class="w-5 h-5 mr-2 text-blue-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
            <polyline points="15,3 21,3 21,9"/>
            <line x1="10" y1="14" x2="21" y2="3"/>
          </svg>
          No lock-in
        </h3>
        <p class="text-gray-600 dark:text-gray-400 mb-4">
          Otwarte standardy i API
        </p>
        
        <div class="space-y-3">
          <div class="text-sm text-gray-700 dark:text-gray-300">
            <strong>Open standards:</strong> REST API, JSON, WebSockets
          </div>
          <div class="text-sm text-gray-700 dark:text-gray-300">
            <strong>Export możliwości:</strong> CSV, JSON, PDF raporty
          </div>
          <div class="text-sm text-gray-700 dark:text-gray-300">
            <strong>Integracje:</strong> Webhooks, third-party apps
          </div>
        </div>
        
        <div class="mt-4 flex space-x-2">
          <span class="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded text-xs">REST API</span>
          <span class="px-2 py-1 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 rounded text-xs">WebSockets</span>
          <span class="px-2 py-1 bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200 rounded text-xs">JSON</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  isAdmin: boolean
}

defineProps<Props>()
defineEmits<{
  navigate: (view: string) => void
}>()
</script>

<style scoped>
/* Custom hover effects */
</style> 