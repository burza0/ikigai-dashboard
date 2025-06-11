<template>
  <div class="space-y-8">
    <!-- Tools & Quick Actions -->
    <div v-if="isAdmin" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-8">
      <div class="flex items-center justify-between mb-8">
        <div>
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white flex items-center">
            <svg class="w-6 h-6 mr-3 text-purple-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
              <path d="M9 9h6v6H9z"/>
            </svg>
            Your tools / data
          </h2>
          <p class="text-base text-gray-600 dark:text-gray-400 mt-1">
            Szybki dostęp do kluczowych funkcji IKIGAI
          </p>
        </div>
      </div>
      
      <div class="grid grid-cols-6 md:grid-cols-12 gap-6">
        <a href="http://localhost:5001/api/products" target="_blank" 
           class="flex flex-col items-center p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg hover:scale-105 transition-transform duration-200 border border-purple-200 dark:border-purple-700">
          <svg class="w-8 h-8 text-purple-600 mb-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
            <circle cx="9" cy="9" r="2"/>
          </svg>
          <span class="text-sm text-purple-700 dark:text-purple-300 text-center">Products API</span>
        </a>
        
        <a href="http://localhost:5001/api/orders" target="_blank"
           class="flex flex-col items-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg hover:scale-105 transition-transform duration-200 border border-blue-200 dark:border-blue-700">
          <svg class="w-8 h-8 text-blue-600 mb-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M9 12l2 2 4-4"/>
            <circle cx="12" cy="12" r="10"/>
          </svg>
          <span class="text-sm text-blue-700 dark:text-blue-300 text-center">Orders API</span>
        </a>
        
        <a href="http://localhost:5001/api/vending-machines" target="_blank"
           class="flex flex-col items-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg hover:scale-105 transition-transform duration-200 border border-green-200 dark:border-green-700">
          <svg class="w-8 h-8 text-green-600 mb-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <rect x="4" y="2" width="16" height="20" rx="2" ry="2"/>
            <circle cx="12" cy="18" r="1"/>
          </svg>
          <span class="text-sm text-green-700 dark:text-green-300 text-center">Machines API</span>
        </a>
        
        <a href="http://localhost:5001/automat" target="_blank"
           class="flex flex-col items-center p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg hover:scale-105 transition-transform duration-200 border border-orange-200 dark:border-orange-700">
          <svg class="w-8 h-8 text-orange-600 mb-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <rect x="3" y="3" width="5" height="5"/>
            <rect x="16" y="3" width="5" height="5"/>
            <rect x="3" y="16" width="5" height="5"/>
          </svg>
          <span class="text-sm text-orange-700 dark:text-orange-300 text-center">Demo Automat</span>
        </a>
        
        <button class="flex flex-col items-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg hover:scale-105 transition-transform duration-200 border border-gray-200 dark:border-gray-600">
          <svg class="w-8 h-8 text-gray-600 dark:text-gray-400 mb-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
          </svg>
          <span class="text-sm text-gray-700 dark:text-gray-300 text-center">Settings</span>
        </button>
        
        <button class="flex flex-col items-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg hover:scale-105 transition-transform duration-200 border border-gray-200 dark:border-gray-600">
          <svg class="w-8 h-8 text-gray-600 dark:text-gray-400 mb-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="7,10 12,15 17,10"/>
            <line x1="12" y1="15" x2="12" y2="3"/>
          </svg>
          <span class="text-sm text-gray-700 dark:text-gray-300 text-center">Export</span>
        </button>
             </div>
    </div>

    <!-- IKIGAI Philosophy Section -->
    <div class="bg-gradient-to-br from-yellow-400 to-yellow-500 rounded-xl p-8 text-gray-900 hover:scale-[1.02] transition-transform duration-200 cursor-pointer shadow-sm border border-yellow-300">
      <div class="flex items-center mb-6">
        <div class="w-10 h-10 mr-4 bg-gray-900 rounded-full flex items-center justify-center">
          <span class="text-yellow-400 text-lg font-bold">生</span>
        </div>
        <h3 class="text-2xl font-semibold">🌱 IKIGAI Philosophy</h3>
      </div>
      <div class="space-y-4">
        <p class="text-xl text-gray-800 font-bold leading-relaxed">
          Wybierz zdrowie z automatu – łączymy zdrowe odżywianie z technologią, by dbać o Ciebie każdego dnia!
        </p>
      </div>
    </div>

    <!-- Main Dashboard Grid -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-8">
      <!-- Dashboard Cards Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <!-- Kreator Mieszanek - Purple (GŁÓWNA FUNKCJA) -->
        <div @click="$emit('navigate', 'mixer')" class="md:col-span-1 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl p-8 text-white hover:scale-[1.02] transition-transform duration-200 cursor-pointer">
          <div class="flex items-center mb-6">
            <svg class="w-10 h-10 mr-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 6v12"/>
              <path d="M6 12h12"/>
              <circle cx="12" cy="12" r="3"/>
            </svg>
            <h3 class="text-xl font-semibold">🥣 Kreator Mieszanek</h3>
          </div>
          <p class="text-lg text-purple-100 mb-6">Skomponuj swoją idealną mieszankę szczęścia IKIGAI</p>
          <div class="text-3xl font-bold mb-3">4 bazy + 6 dodatków</div>
          <div class="text-purple-200 text-base">Rozpocznij podróż! ✨</div>
        </div>

        <!-- Orders & QR Workflow - Blue (Admin only) -->
        <div v-if="isAdmin" class="md:col-span-1 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-8 text-white hover:scale-[1.02] transition-transform duration-200 cursor-pointer">
          <div class="flex items-center mb-6">
            <svg class="w-10 h-10 mr-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M9 12l2 2 4-4"/>
              <circle cx="12" cy="12" r="10"/>
            </svg>
            <h3 class="text-xl font-semibold">📦 Orders</h3>
          </div>
          <p class="text-lg text-blue-100 mb-6">QR workflow management system</p>
          <div class="text-3xl font-bold mb-3">847 zamówień</div>
          <div class="text-blue-200 text-base">+12% ten miesiąc ↗</div>
        </div>

        <!-- Mapa Automatów - Green -->
        <div @click="$emit('navigate', 'map')" class="md:col-span-1 bg-gradient-to-br from-green-500 to-green-600 rounded-xl p-8 text-white hover:scale-[1.02] transition-transform duration-200 cursor-pointer">
          <div class="flex items-center mb-6">
            <svg class="w-10 h-10 mr-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
              <circle cx="12" cy="10" r="3"/>
            </svg>
            <h3 class="text-xl font-semibold">🗺️ Mapa Automatów</h3>
          </div>
          <p class="text-lg text-green-100 mb-6">Interaktywna mapa z lokalizacjami automatów IKIGAI</p>
          <div class="text-3xl font-bold mb-3">3 lokalizacje</div>
          <div class="text-green-200 text-base">Znajdź najbliższy automat 📍</div>
        </div>

        <!-- Program Lojalnościowy - Orange -->
        <div @click="$emit('navigate', 'loyalty')" class="md:col-span-1 bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl p-8 text-white hover:scale-[1.02] transition-transform duration-200 cursor-pointer">
          <div class="flex items-center mb-6">
            <svg class="w-10 h-10 mr-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M12 6v6l4 2"/>
              <circle cx="12" cy="12" r="10"/>
            </svg>
            <h3 class="text-xl font-semibold">🏆 Program Lojalnościowy</h3>
          </div>
          <p class="text-lg text-orange-100 mb-6">Zbieraj punkty, podejmuj wyzwania, zyskuj nagrody</p>
          <div class="text-3xl font-bold mb-3">5 wyzwań</div>
          <div class="text-orange-200 text-base">Zacznij zbierać punkty! 🌟</div>
        </div>

        <!-- Mobile QR App - Pink/Purple -->
        <div @click="$emit('navigate', 'mobile')" class="md:col-span-1 bg-gradient-to-br from-pink-500 to-purple-600 rounded-xl p-8 text-white hover:scale-[1.02] transition-transform duration-200 cursor-pointer">
          <div class="flex items-center mb-6">
            <svg class="w-10 h-10 mr-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="5" y="2" width="14" height="20" rx="2" ry="2"/>
              <path d="M12 18h.01"/>
              <rect x="8" y="6" width="8" height="8"/>
            </svg>
            <h3 class="text-xl font-semibold">📱 Mobile QR App</h3>
          </div>
          <p class="text-lg text-pink-100 mb-6">Skanowanie QR, płatności mobilne, push notifications</p>
          <div class="text-3xl font-bold mb-3">3 funkcje</div>
          <div class="text-pink-200 text-base">Zaawansowane możliwości mobilne 🚀</div>
        </div>

        <!-- Analytics - Orange (Admin only) -->
        <div v-if="isAdmin" class="md:col-span-2 lg:col-span-3 bg-gradient-to-br from-red-500 to-red-600 rounded-xl p-8 text-white hover:scale-[1.02] transition-transform duration-200 cursor-pointer">
          <div class="flex items-center mb-6">
            <svg class="w-10 h-10 mr-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
              <path d="M7 16l3-3 3 3 4-6"/>
            </svg>
            <h3 class="text-2xl font-semibold">📊 Analytics & Insights</h3>
            <span class="ml-auto px-3 py-1.5 bg-red-400 rounded-full text-sm font-medium">ADMIN</span>
          </div>
          <p class="text-lg text-red-100 mb-6">Zaawansowane analizy sprzedaży, KPI i trendy zdrowotne</p>
          <div class="grid grid-cols-3 gap-6">
            <div>
              <div class="text-3xl font-bold">12,456zł</div>
              <div class="text-red-200 text-base">Przychód</div>
            </div>
            <div>
              <div class="text-3xl font-bold">94%</div>
              <div class="text-red-200 text-base">Satysfakcja</div>
            </div>
            <div>
              <div class="text-3xl font-bold">234</div>
              <div class="text-red-200 text-base">Aktywni klienci</div>
            </div>
          </div>
        </div>


      </div>
    </div>

    <!-- Top 5 Rekomendacji IKIGAI -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-8">
      <div class="flex items-center justify-between mb-8">
        <h2 class="text-2xl font-semibold text-gray-900 dark:text-white flex items-center">
          <svg class="w-7 h-7 mr-4 text-yellow-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"/>
          </svg>
          🌟 Top 5 Rekomendacji IKIGAI
        </h2>
        <p class="text-base text-gray-600 dark:text-gray-400">
          Najpopularniejsze i najzdrowsze mieszanki - zamów jednym kliknięciem
        </p>
      </div>

      <div v-if="loadingRecommendations" class="flex justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>



      <div v-if="!loadingRecommendations" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div 
          v-for="(rec, index) in recommendations" 
          :key="rec.id"
          class="bg-gradient-to-br from-gray-50 to-white dark:from-gray-700 dark:to-gray-800 rounded-xl p-8 border border-gray-200 dark:border-gray-600 hover:shadow-lg transition-all duration-200 cursor-pointer hover:scale-[1.02]"
          @click="orderRecommendation(rec)"
        >


          <!-- Name & Description -->
          <h3 class="font-semibold text-gray-900 dark:text-white mb-4 text-lg">{{ rec.name || 'Ładowanie...' }}</h3>
          <p class="text-base text-gray-600 dark:text-gray-400 mb-6">{{ rec.description || 'Opis produktu...' }}</p>

          <!-- Tags -->
          <div class="flex flex-wrap gap-3 mb-6">
            <span 
              v-for="tag in (rec.tags || []).slice(0, 2)" 
              :key="tag"
              class="inline-flex items-center px-3 py-1.5 rounded-full text-base bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-200"
            >
              {{ tag }}
            </span>
          </div>

          <!-- Price & Order Button -->
          <div class="flex items-center justify-between">
            <div class="text-2xl font-bold text-purple-600 dark:text-purple-400">
              {{ (rec.total_price || 0).toFixed(2) }}zł
            </div>
            <button class="bg-purple-600 hover:bg-purple-700 text-white text-base px-6 py-3 rounded-lg font-medium transition-colors duration-200">
              Zamów
            </button>
          </div>
        </div>
      </div>

      <!-- Quick Order Alert -->
      <div 
        v-if="orderAlert.show" 
        :class="[
          'mt-6 p-5 rounded-lg border transition-all duration-500',
          orderAlert.type === 'success' ? 'bg-green-50 border-green-200 text-green-800 dark:bg-green-900/20 dark:border-green-700 dark:text-green-200' :
          'bg-red-50 border-red-200 text-red-800 dark:bg-red-900/20 dark:border-red-700 dark:text-red-200'
        ]"
      >
        <div class="flex items-center">
          <svg class="w-6 h-6 mr-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path v-if="orderAlert.type === 'success'" d="M9 12l2 2 4-4"/>
            <circle cx="12" cy="12" r="10"/>
          </svg>
          <span class="text-base">{{ orderAlert.message }}</span>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Props {
  isAdmin: boolean
}

defineProps<Props>()
defineEmits<{
  navigate: (view: string) => void
}>()

// Reactive data
const recommendations = ref([])
const loadingRecommendations = ref(false)
const orderAlert = ref({
  show: false,
  type: 'success',
  message: ''
})

// Fetch recommendations
const fetchRecommendations = async () => {
  loadingRecommendations.value = true
  try {
    console.log('Fetching recommendations...')
    const response = await fetch('http://localhost:5001/api/recommendations')
    const data = await response.json()
    
    console.log('API Response:', data)
    
    if (data.success) {
      recommendations.value = data.recommendations
      console.log('Recommendations loaded:', recommendations.value)
    } else {
      console.error('API returned success: false')
    }
  } catch (error) {
    console.error('Error fetching recommendations:', error)
  } finally {
    loadingRecommendations.value = false
  }
}

// Order recommendation function
const orderRecommendation = async (recommendation: any) => {
  try {
    // Create order for this recommendation
    const orderData = {
      mixture_name: recommendation.name,
      base_id: recommendation.base,
      topping_ids: recommendation.toppings,
      total_price: recommendation.total_price,
      user_id: 'web_user',
      quick_order: true
    }

    const response = await fetch('http://localhost:5001/api/orders', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(orderData)
    })

    const result = await response.json()
    
    if (result.success) {
      showAlert('success', `✨ Zamówiono ${recommendation.name}! ID: ${result.order.id.substring(0, 8)}...`)
    } else {
      showAlert('error', 'Błąd podczas składania zamówienia')
    }
  } catch (error) {
    console.error('Error creating order:', error)
    showAlert('error', 'Błąd podczas składania zamówienia')
  }
}

// Show alert function
const showAlert = (type: string, message: string) => {
  orderAlert.value = {
    show: true,
    type,
    message
  }
  
  setTimeout(() => {
    orderAlert.value.show = false
  }, 4000)
}

// Initialize
onMounted(() => {
  fetchRecommendations()
})
</script>

<style scoped>
/* Custom hover effects */
</style> 