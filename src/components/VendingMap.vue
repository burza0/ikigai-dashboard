<template>
  <div class="max-w-7xl mx-auto p-6 space-y-6">
    
    <!-- Breadcrumb Navigation -->
    <div class="flex items-center text-sm text-gray-600 dark:text-gray-400 mb-4">
      <button @click="$emit('navigate', 'dashboard')" class="hover:text-purple-600 dark:hover:text-purple-400 transition-colors duration-200">
        🏠 Dashboard
      </button>
      <span class="mx-2">/</span>
      <span class="text-purple-600 dark:text-purple-400 font-medium">🗺️ Mapa Automatów</span>
    </div>
    
    <!-- Header -->
    <div class="bg-gradient-to-r from-green-500 to-green-600 rounded-xl p-8 text-white">
      <div class="flex items-center mb-4">
        <div class="w-12 h-12 mr-4 bg-white rounded-full flex items-center justify-center">
          <span class="text-2xl">🗺️</span>
        </div>
        <div>
          <h1 class="text-3xl font-bold">Mapa Automatów IKIGAI</h1>
          <p class="text-green-100 mt-2">Znajdź najbliższy automat i zaplanuj swoją podróż po zdrowie</p>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
        <div class="text-center bg-green-600 bg-opacity-50 rounded-lg p-4">
          <div class="text-2xl font-bold">{{ vendingMachines.length }}</div>
          <div class="text-sm text-green-100">Automaty IKIGAI</div>
        </div>
        <div class="text-center bg-green-600 bg-opacity-50 rounded-lg p-4">
          <div class="text-2xl font-bold">{{ onlineCount }}</div>
          <div class="text-sm text-green-100">Aktywne teraz</div>
        </div>
        <div class="text-center bg-green-600 bg-opacity-50 rounded-lg p-4">
          <div class="text-2xl font-bold">{{ totalStock }}</div>
          <div class="text-sm text-green-100">Produkty dostępne</div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      
      <!-- LEWA KOLUMNA: Lista automatów i filtry -->
      <div class="lg:col-span-1 space-y-6">
        
        <!-- Filtry -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">🔍 Filtry</h3>
          
          <!-- Status Filter -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Status</label>
            <select v-model="statusFilter" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
              <option value="all">Wszystkie</option>
              <option value="online">Online</option>
              <option value="maintenance">Serwis</option>
            </select>
          </div>
          
          <!-- Stock Filter -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Stan magazynu</label>
            <select v-model="stockFilter" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
              <option value="all">Wszystkie</option>
              <option value="available">Dostępne produkty</option>
              <option value="low">Niski stan</option>
            </select>
          </div>
          
          <!-- User Location -->
          <div class="mb-4">
            <button @click="getUserLocation" 
                    :disabled="gettingLocation"
                    class="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg transition-colors duration-200 disabled:opacity-50">
              <span v-if="gettingLocation">📍 Lokalizuję...</span>
              <span v-else-if="userLocation">📍 Moja lokalizacja</span>
              <span v-else>📍 Znajdź mnie</span>
            </button>
          </div>
        </div>
        
        <!-- Lista automatów -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">🏪 Automaty</h3>
          
          <div class="space-y-3">
            <div v-for="machine in filteredMachines" :key="machine.id"
                 @click="selectMachine(machine)"
                 :class="[
                   'cursor-pointer p-4 rounded-lg border-2 transition-all duration-200',
                   selectedMachine?.id === machine.id 
                     ? 'border-green-500 bg-green-50 dark:bg-green-900/20' 
                     : 'border-gray-200 dark:border-gray-600 hover:border-green-300 hover:bg-gray-50 dark:hover:bg-gray-700'
                 ]">
              
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <h4 class="font-semibold text-gray-900 dark:text-white">{{ machine.name }}</h4>
                  <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">{{ machine.location }}</p>
                  <p class="text-xs text-gray-500 dark:text-gray-500 mt-1">{{ machine.address }}</p>
                </div>
                <div :class="[
                  'px-2 py-1 rounded-full text-xs font-medium',
                  machine.status === 'online' 
                    ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                    : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                ]">
                  {{ machine.status === 'online' ? '🟢 Online' : '🔴 Serwis' }}
                </div>
              </div>
              
              <div class="mt-3 flex items-center justify-between">
                <div class="text-sm text-gray-600 dark:text-gray-400">
                  Stock: {{ machine.current_stock }}/{{ machine.capacity }}
                </div>
                <div class="text-sm text-gray-600 dark:text-gray-400">
                  {{ machine.operating_hours }}
                </div>
              </div>
              
              <div v-if="userLocation" class="mt-2 text-xs text-blue-600 dark:text-blue-400">
                📍 {{ getDistance(machine) }} km od Ciebie
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- PRAWA KOLUMNA: Mapa -->
      <div class="lg:col-span-3">
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">🗺️ Mapa interaktywna</h3>
            <div class="flex items-center space-x-2">
              <button @click="centerOnUser" 
                      v-if="userLocation"
                      class="px-3 py-1 bg-blue-500 text-white rounded-lg text-sm hover:bg-blue-600 transition-colors duration-200">
                📍 Moja lokalizacja
              </button>
              <button @click="centerOnMachines" 
                      class="px-3 py-1 bg-green-500 text-white rounded-lg text-sm hover:bg-green-600 transition-colors duration-200">
                🎯 Wszystkie automaty
              </button>
            </div>
          </div>
          
          <!-- Mapa (placeholder - rzeczywista Google Maps) -->
          <div id="map-container" class="w-full h-96 bg-gray-100 dark:bg-gray-700 rounded-lg flex items-center justify-center relative">
            <div v-if="!mapLoaded" class="text-center">
              <div class="text-4xl mb-4">🗺️</div>
              <p class="text-gray-600 dark:text-gray-400">Ładowanie mapy...</p>
              <div class="mt-4">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-green-500 mx-auto"></div>
              </div>
            </div>
            
            <!-- Symulacja mapy ze statycznymi markerami -->
            <div v-else class="absolute inset-0 bg-gradient-to-br from-green-100 to-blue-100 dark:from-green-900 dark:to-blue-900 rounded-lg overflow-hidden">
              <!-- Grid map background -->
              <div class="absolute inset-0 opacity-20">
                <div class="grid grid-cols-8 grid-rows-6 h-full">
                  <div v-for="i in 48" :key="i" class="border border-gray-300 dark:border-gray-600"></div>
                </div>
              </div>
              
              <!-- Markery automatów -->
              <div v-for="(machine, index) in filteredMachines" :key="machine.id"
                   @click="selectMachine(machine)"
                   :style="getMarkerPosition(index)"
                   class="absolute cursor-pointer transform -translate-x-1/2 -translate-y-1/2">
                
                <!-- Marker -->
                <div :class="[
                  'w-8 h-8 rounded-full flex items-center justify-center text-white font-bold text-sm shadow-lg border-2 border-white hover:scale-110 transition-transform duration-200',
                  machine.status === 'online' 
                    ? 'bg-green-500' 
                    : 'bg-red-500'
                ]">
                  🏪
                </div>
                
                <!-- Tooltip -->
                <div v-if="selectedMachine?.id === machine.id" 
                     class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 bg-white dark:bg-gray-800 rounded-lg shadow-lg p-3 min-w-64 border border-gray-200 dark:border-gray-700">
                  <div class="text-sm font-semibold text-gray-900 dark:text-white">{{ machine.name }}</div>
                  <div class="text-xs text-gray-600 dark:text-gray-400 mt-1">{{ machine.location }}</div>
                  <div class="text-xs text-gray-500 dark:text-gray-500 mt-1">{{ machine.address }}</div>
                  
                  <div class="flex items-center justify-between mt-2">
                    <span :class="[
                      'px-2 py-1 rounded-full text-xs font-medium',
                      machine.status === 'online' 
                        ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                        : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                    ]">
                      {{ machine.status === 'online' ? '🟢 Online' : '🔴 Serwis' }}
                    </span>
                    <span class="text-xs text-gray-600 dark:text-gray-400">
                      {{ machine.current_stock }}/{{ machine.capacity }}
                    </span>
                  </div>
                  
                  <div class="mt-2 text-xs text-gray-600 dark:text-gray-400">
                    🕒 {{ machine.operating_hours }}
                  </div>
                  
                  <div class="flex space-x-2 mt-3">
                    <button @click.stop="getDirections(machine)" 
                            class="flex-1 bg-blue-500 text-white py-1 px-2 rounded text-xs hover:bg-blue-600 transition-colors duration-200">
                      🧭 Dojazd
                    </button>
                    <button @click.stop="callMachine(machine)" 
                            class="flex-1 bg-purple-500 text-white py-1 px-2 rounded text-xs hover:bg-purple-600 transition-colors duration-200">
                      📞 Kontakt
                    </button>
                  </div>
                </div>
              </div>
              
              <!-- User location marker -->
              <div v-if="userLocation"
                   :style="getUserMarkerPosition()"
                   class="absolute cursor-pointer transform -translate-x-1/2 -translate-y-1/2">
                <div class="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center text-white border-2 border-white shadow-lg animate-pulse">
                  📍
                </div>
              </div>
              
              <!-- Map Legend -->
              <div class="absolute top-4 right-4 bg-white dark:bg-gray-800 rounded-lg shadow-lg p-3 border border-gray-200 dark:border-gray-700">
                <h4 class="text-sm font-semibold text-gray-900 dark:text-white mb-2">Legenda</h4>
                <div class="space-y-1 text-xs">
                  <div class="flex items-center">
                    <div class="w-4 h-4 bg-green-500 rounded-full mr-2"></div>
                    <span class="text-gray-600 dark:text-gray-400">Automat online</span>
                  </div>
                  <div class="flex items-center">
                    <div class="w-4 h-4 bg-red-500 rounded-full mr-2"></div>
                    <span class="text-gray-600 dark:text-gray-400">Automat w serwisie</span>
                  </div>
                  <div class="flex items-center">
                    <div class="w-4 h-4 bg-blue-500 rounded-full mr-2"></div>
                    <span class="text-gray-600 dark:text-gray-400">Twoja lokalizacja</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Detale wybranego automatu -->
    <div v-if="selectedMachine" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
        <span class="text-2xl mr-3">🏪</span>
        {{ selectedMachine.name }} - Szczegóły
      </h3>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <!-- Informacje podstawowe -->
        <div>
          <h4 class="font-semibold text-gray-900 dark:text-white mb-3">📍 Lokalizacja</h4>
          <div class="space-y-2 text-sm text-gray-600 dark:text-gray-400">
            <div><strong>Miejsce:</strong> {{ selectedMachine.location }}</div>
            <div><strong>Adres:</strong> {{ selectedMachine.address }}</div>
            <div><strong>Godziny:</strong> {{ selectedMachine.operating_hours }}</div>
          </div>
        </div>
        
        <!-- Status i magazyn -->
        <div>
          <h4 class="font-semibold text-gray-900 dark:text-white mb-3">📊 Status</h4>
          <div class="space-y-2 text-sm">
            <div class="flex items-center">
              <span :class="[
                'px-2 py-1 rounded-full text-xs font-medium mr-2',
                selectedMachine.status === 'online' 
                  ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                  : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
              ]">
                {{ selectedMachine.status === 'online' ? '🟢 Online' : '🔴 Serwis' }}
              </span>
            </div>
            <div class="text-gray-600 dark:text-gray-400">
              <strong>Magazyn:</strong> {{ selectedMachine.current_stock }}/{{ selectedMachine.capacity }}
            </div>
            <div class="text-gray-600 dark:text-gray-400">
              <strong>Ostatnie uzupełnienie:</strong> {{ formatDate(selectedMachine.last_refill) }}
            </div>
          </div>
        </div>
        
        <!-- Dostępne produkty -->
        <div>
          <h4 class="font-semibold text-gray-900 dark:text-white mb-3">🥤 Produkty</h4>
          <div class="space-y-1">
            <div v-for="product in selectedMachine.available_products" :key="product" 
                 class="text-sm text-gray-600 dark:text-gray-400 bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">
              {{ formatProductName(product) }}
            </div>
          </div>
        </div>
        
        <!-- Metody płatności -->
        <div>
          <h4 class="font-semibold text-gray-900 dark:text-white mb-3">💳 Płatność</h4>
          <div class="space-y-1">
            <div v-for="method in selectedMachine.payment_methods" :key="method"
                 class="text-sm text-gray-600 dark:text-gray-400 flex items-center">
              <span class="mr-2">{{ getPaymentIcon(method) }}</span>
              {{ formatPaymentMethod(method) }}
            </div>
          </div>
        </div>
      </div>
      
      <!-- Akcje -->
      <div class="flex flex-wrap gap-3 mt-6">
        <button @click="getDirections(selectedMachine)" 
                class="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg transition-colors duration-200 flex items-center">
          <span class="mr-2">🧭</span> Jak dojechać
        </button>
        <button @click="callMachine(selectedMachine)" 
                class="bg-purple-500 hover:bg-purple-600 text-white py-2 px-4 rounded-lg transition-colors duration-200 flex items-center">
          <span class="mr-2">📞</span> Zgłoś problem
        </button>
        <button @click="$emit('navigate', 'mixer')" 
                class="bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded-lg transition-colors duration-200 flex items-center">
          <span class="mr-2">🥣</span> Skomponuj mieszankę
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

// Emits
defineEmits<{
  navigate: (view: string) => void
}>()

// Reactive data
const vendingMachines = ref([])
const selectedMachine = ref(null)
const userLocation = ref(null)
const gettingLocation = ref(false)
const mapLoaded = ref(false)
const statusFilter = ref('all')
const stockFilter = ref('all')

// Computed properties
const filteredMachines = computed(() => {
  let machines = vendingMachines.value

  // Filter by status
  if (statusFilter.value !== 'all') {
    machines = machines.filter(m => m.status === statusFilter.value)
  }

  // Filter by stock
  if (stockFilter.value === 'available') {
    machines = machines.filter(m => m.current_stock > 0)
  } else if (stockFilter.value === 'low') {
    machines = machines.filter(m => m.current_stock < m.capacity * 0.2)
  }

  return machines
})

const onlineCount = computed(() => {
  return vendingMachines.value.filter(m => m.status === 'online').length
})

const totalStock = computed(() => {
  return vendingMachines.value.reduce((sum, m) => sum + m.current_stock, 0)
})

// Methods
const loadVendingMachines = async () => {
  try {
    const response = await fetch('http://localhost:5001/api/vending-machines')
    const data = await response.json()
    if (data.success) {
      vendingMachines.value = data.machines
    }
  } catch (error) {
    console.error('Błąd ładowania automatów:', error)
  }
}

const selectMachine = (machine) => {
  selectedMachine.value = machine
}

const getUserLocation = () => {
  if (navigator.geolocation) {
    gettingLocation.value = true
    navigator.geolocation.getCurrentPosition(
      (position) => {
        userLocation.value = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        }
        gettingLocation.value = false
      },
      (error) => {
        console.error('Błąd lokalizacji:', error)
        // Fallback na lokalizację w Warszawie
        userLocation.value = {
          lat: 52.2297,
          lng: 21.0122
        }
        gettingLocation.value = false
      }
    )
  }
}

const getDistance = (machine) => {
  if (!userLocation.value) return 0
  
  const R = 6371 // Radius of the Earth in km
  const dLat = (machine.coordinates.lat - userLocation.value.lat) * Math.PI / 180
  const dLng = (machine.coordinates.lng - userLocation.value.lng) * Math.PI / 180
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
           Math.cos(userLocation.value.lat * Math.PI / 180) * Math.cos(machine.coordinates.lat * Math.PI / 180) *
           Math.sin(dLng/2) * Math.sin(dLng/2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))
  const distance = R * c
  
  return distance.toFixed(1)
}

const getMarkerPosition = (index) => {
  // Symulowane pozycje markerów na mapie
  const positions = [
    { top: '40%', left: '50%' },  // IKIGAI Central
    { top: '60%', left: '30%' },  // IKIGAI Fitness  
    { top: '30%', left: '70%' }   // IKIGAI Office
  ]
  return positions[index] || { top: '50%', left: '50%' }
}

const getUserMarkerPosition = () => {
  return { top: '50%', left: '40%' } // Symulowana pozycja użytkownika
}

const centerOnUser = () => {
  // W rzeczywistej implementacji przesunie mapę na lokalizację użytkownika
  console.log('Centrowanie mapy na użytkowniku')
}

const centerOnMachines = () => {
  // W rzeczywistej implementacji pokaże wszystkie automaty
  console.log('Centrowanie mapy na automatach')
}

const getDirections = (machine) => {
  // Otwiera Google Maps z nawigacją
  const url = `https://www.google.com/maps/dir/?api=1&destination=${machine.coordinates.lat},${machine.coordinates.lng}`
  window.open(url, '_blank')
}

const callMachine = (machine) => {
  alert(`Kontakt dla automatu ${machine.name}\nID: ${machine.id}\nLokalizacja: ${machine.location}`)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('pl-PL', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatProductName = (product) => {
  const names = {
    'protein_shake': '🥤 Shake Proteinowy',
    'green_smoothie': '🥬 Zielone Smoothie',
    'energy_bar': '🍫 Baton Energetyczny',
    'vitamin_water': '💧 Woda Witaminowa',
    'fresh_juice': '🧃 Świeży Sok',
    'berry_bowl': '🫐 Berry Bowl'
  }
  return names[product] || product
}

const formatPaymentMethod = (method) => {
  const methods = {
    'card': 'Karta płatnicza',
    'mobile': 'Płatność mobilna',
    'qr_code': 'Kod QR'
  }
  return methods[method] || method
}

const getPaymentIcon = (method) => {
  const icons = {
    'card': '💳',
    'mobile': '📱',
    'qr_code': '📱'
  }
  return icons[method] || '💰'
}

// Lifecycle
onMounted(async () => {
  await loadVendingMachines()
  
  // Symulacja ładowania mapy
  setTimeout(() => {
    mapLoaded.value = true
  }, 1500)
  
  // Auto-select pierwszy automat
  if (vendingMachines.value.length > 0) {
    selectedMachine.value = vendingMachines.value[0]
  }
})
</script>

<style scoped>
/* Custom animations */
.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: .5;
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style> 