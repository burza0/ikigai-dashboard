<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-40">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center">
            <button 
              @click="$emit('navigate', 'dashboard')"
              class="mr-4 p-2 text-gray-500 hover:text-gray-700 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
            </button>
            <h1 class="text-xl font-bold text-gray-900">🗺️ Mapa automatów IKIGAI</h1>
          </div>
          
          <!-- Stats -->
          <div class="hidden md:flex items-center space-x-6">
            <div class="text-center">
              <div class="text-lg font-bold text-green-600">{{ stats.online }}</div>
              <div class="text-xs text-gray-500">Online</div>
            </div>
            <div class="text-center">
              <div class="text-lg font-bold text-yellow-600">{{ stats.lowStock }}</div>
              <div class="text-xs text-gray-500">Niski stan</div>
            </div>
            <div class="text-center">
              <div class="text-lg font-bold text-red-600">{{ stats.offline }}</div>
              <div class="text-xs text-gray-500">Offline</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="flex h-[calc(100vh-4rem)]">
      
      <!-- Sidebar -->
      <div class="w-full md:w-96 bg-white shadow-lg flex flex-col" 
           :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'"
           style="transition: transform 0.3s ease-in-out">
        
        <!-- Search & Filters -->
        <div class="p-4 border-b border-gray-200">
          <div class="space-y-3">
            <!-- Search -->
            <div class="relative">
              <input 
                v-model="searchQuery"
                type="text" 
                placeholder="🔍 Szukaj lokalizacji..."
                class="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
              </div>
            </div>
            
            <!-- Quick Filters -->
            <div class="flex flex-wrap gap-2">
              <button 
                v-for="filter in quickFilters" 
                :key="filter.key"
                @click="toggleFilter(filter.key)"
                :class="[
                  'px-3 py-1.5 rounded-full text-sm font-medium transition-all duration-200',
                  activeFilters.includes(filter.key)
                    ? 'bg-blue-100 text-blue-700 border border-blue-200'
                    : 'bg-gray-100 text-gray-600 border border-gray-200 hover:bg-gray-200'
                ]"
              >
                {{ filter.icon }} {{ filter.label }}
              </button>
            </div>
            
            <!-- My Location -->
            <button 
              @click="locateUser"
              class="w-full flex items-center justify-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              :disabled="locatingUser"
            >
              <svg v-if="!locatingUser" class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
              </svg>
              <div v-else class="w-5 h-5 mr-2 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              {{ locatingUser ? 'Lokalizowanie...' : '📍 Moja lokalizacja' }}
            </button>
          </div>
        </div>
        
        <!-- Locations List -->
        <div class="flex-1 overflow-y-auto">
          <div class="p-4 space-y-3">
            <div 
              v-for="location in filteredLocations" 
              :key="location.id"
              @click="selectLocation(location)"
              :class="[
                'p-4 rounded-xl border-2 cursor-pointer transition-all duration-200 hover:shadow-md',
                selectedLocation?.id === location.id 
                  ? 'border-blue-500 bg-blue-50 shadow-md' 
                  : 'border-gray-200 hover:border-blue-300'
              ]"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center mb-2">
                    <span class="text-2xl mr-3">{{ getLocationIcon(location) }}</span>
                    <div>
                      <h3 class="font-semibold text-gray-900">{{ location.name }}</h3>
                      <p class="text-sm text-gray-600">{{ location.address }}</p>
                    </div>
                  </div>
                  
                  <!-- Status and Stock -->
                  <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center">
                      <div :class="[
                        'w-3 h-3 rounded-full mr-2',
                        getStatusColor(location.status)
                      ]"></div>
                      <span class="text-sm font-medium" :class="getStatusTextColor(location.status)">
                        {{ getStatusText(location.status) }}
                      </span>
                    </div>
                    <div class="text-sm">
                      <span class="font-medium">Stock: </span>
                      <span :class="getStockColor(location.stock)">{{ location.stock }}%</span>
                    </div>
                  </div>
                  
                  <!-- Distance and Hours -->
                  <div class="flex items-center justify-between text-xs text-gray-500 mb-2">
                    <span v-if="userLocation">📍 {{ getDistance(location) }}km</span>
                    <span>⏰ {{ location.hours }}</span>
                  </div>
                  
                  <!-- Tags -->
                  <div class="flex flex-wrap gap-1 mb-3">
                    <span 
                      v-for="tag in location.tags" 
                      :key="tag"
                      class="px-2 py-1 bg-gray-100 text-gray-600 rounded-full text-xs"
                    >
                      {{ tag }}
                    </span>
                  </div>
                  
                  <!-- Quick Actions -->
                  <div class="grid grid-cols-2 gap-2">
                    <button 
                      @click.stop="openNavigation(location)"
                      class="flex items-center justify-center px-3 py-2 bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition-colors text-sm"
                    >
                      <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-1.447-.894L15 4m0 13V4m-6 3l6-3"></path>
                      </svg>
                      Nawiguj
                    </button>
                    <button 
                      @click.stop="showLocationDetails(location)"
                      class="flex items-center justify-center px-3 py-2 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors text-sm"
                    >
                      <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                      Szczegóły
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Mobile Sidebar Toggle -->
      <button 
        @click="sidebarOpen = !sidebarOpen"
        class="md:hidden fixed top-20 left-4 z-40 p-3 bg-white rounded-full shadow-lg border border-gray-200 hover:bg-gray-50 transition-colors"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
        </svg>
      </button>
      
      <!-- Map Container -->
      <div class="flex-1 relative">
        <div class="w-full h-full bg-gradient-to-br from-green-100 to-blue-100 relative overflow-hidden">
          
          <!-- Interactive Map Mockup -->
          <div class="absolute inset-0 flex items-center justify-center">
            <div class="bg-white rounded-xl shadow-xl p-8 max-w-lg text-center">
              <div class="text-6xl mb-4">🗺️</div>
              <h2 class="text-2xl font-bold text-gray-900 mb-2">Nowa interaktywna mapa</h2>
              <p class="text-gray-600 mb-6">Nowoczesna mapa automatów IKIGAI z lepszymi funkcjonalnościami</p>
              
              <div class="grid grid-cols-2 gap-4 text-sm">
                <div class="bg-green-50 p-3 rounded-lg">
                  <div class="text-green-600 font-semibold">🟢 {{ stats.online }} Online</div>
                  <div class="text-gray-500">Dostępne automaty</div>
                </div>
                <div class="bg-yellow-50 p-3 rounded-lg">
                  <div class="text-yellow-600 font-semibold">🟡 {{ stats.lowStock }} Niski stan</div>
                  <div class="text-gray-500">Wymagają uzupełnienia</div>
                </div>
              </div>
              
              <div class="mt-6 text-xs text-gray-400">
                Kliknij na lokalizację po lewej stronie
              </div>
            </div>
          </div>
          
          <!-- Floating Location Cards -->
          <div 
            v-for="(location, index) in locations" 
            :key="location.id"
            :style="getLocationCardStyle(index)"
            class="absolute bg-white rounded-lg shadow-lg border-2 border-gray-200 p-3 cursor-pointer hover:shadow-xl transition-all duration-300 transform hover:scale-105"
            :class="selectedLocation?.id === location.id ? 'border-blue-500 shadow-blue-200' : ''"
            @click="selectLocation(location)"
          >
            <div class="flex items-center space-x-2">
              <span class="text-xl">{{ getLocationIcon(location) }}</span>
              <div>
                <div class="font-semibold text-sm">{{ location.name }}</div>
                <div class="text-xs text-gray-500">{{ location.stock }}% stock</div>
              </div>
              <div :class="['w-2 h-2 rounded-full', getStatusColor(location.status)]"></div>
            </div>
          </div>
        </div>
        
        <!-- Map Controls -->
        <div class="absolute top-4 right-4 space-y-2">
          <button 
            @click="centerOnUser"
            class="p-3 bg-white rounded-lg shadow-md border border-gray-200 hover:bg-gray-50 transition-colors"
            title="Wyśrodkuj na mojej lokalizacji"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
            </svg>
          </button>
          
          <button 
            @click="refreshLocations"
            class="p-3 bg-white rounded-lg shadow-md border border-gray-200 hover:bg-gray-50 transition-colors"
            :disabled="refreshing"
            title="Odśwież dane"
          >
            <svg class="w-5 h-5" :class="refreshing ? 'animate-spin' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
            </svg>
          </button>
        </div>
        
        <!-- Live Updates Indicator -->
        <div class="absolute bottom-4 right-4 flex items-center space-x-2 bg-white rounded-lg shadow-md border border-gray-200 px-3 py-2">
          <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span class="text-sm text-gray-600">Live updates</span>
        </div>
      </div>
    </div>
    
    <!-- Location Details Modal -->
    <div v-if="detailsModal.show" 
         class="fixed inset-0 z-50 overflow-y-auto"
         @click="detailsModal.show = false">
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
        
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
             @click.stop>
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                  {{ detailsModal.location?.name }}
                </h3>
                
                <div class="space-y-4 text-sm">
                  <div class="flex justify-between">
                    <span class="text-gray-500">Adres:</span>
                    <span>{{ detailsModal.location?.address }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500">Status:</span>
                    <span :class="getStatusTextColor(detailsModal.location?.status)">
                      {{ getStatusText(detailsModal.location?.status) }}
                    </span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500">Stan magazynu:</span>
                    <span :class="getStockColor(detailsModal.location?.stock)">
                      {{ detailsModal.location?.stock }}%
                    </span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500">Godziny:</span>
                    <span>{{ detailsModal.location?.hours }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button 
              @click="openNavigation(detailsModal.location)"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-green-600 text-base font-medium text-white hover:bg-green-700 focus:outline-none sm:ml-3 sm:w-auto sm:text-sm">
              Nawiguj
            </button>
            <button 
              @click="detailsModal.show = false"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
              Zamknij
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

// Define emits
defineEmits<{
  'navigate': (view: string) => void
}>()

// Reactive data
const sidebarOpen = ref(false)
const searchQuery = ref('')
const activeFilters = ref([])
const selectedLocation = ref(null)
const userLocation = ref(null)
const locatingUser = ref(false)
const refreshing = ref(false)

// Modal
const detailsModal = ref({
  show: false,
  location: null
})

// Mock data
const locations = ref([
  {
    id: 1,
    name: 'IKIGAI Campus AGH',
    address: 'al. Mickiewicza 30, 30-059 Kraków',
    lat: 50.0647,
    lng: 19.9450,
    status: 'online',
    stock: 85,
    hours: '06:00-22:00',
    tags: ['Uniwersytet', '24/7', 'WiFi'],
    type: 'university'
  },
  {
    id: 2,
    name: 'IKIGAI Fitness Zone',
    address: 'ul. Karmelicka 45, 31-128 Kraków',
    lat: 50.0619,
    lng: 19.9373,
    status: 'online',
    stock: 92,
    hours: '05:30-23:00',
    tags: ['Fitness', 'Parking', 'Klimatyzacja'],
    type: 'fitness'
  },
  {
    id: 3,
    name: 'IKIGAI Tech Hub',
    address: 'ul. Podole 60, 30-394 Kraków',
    lat: 50.0755,
    lng: 19.9199,
    status: 'online',
    stock: 78,
    hours: '07:00-20:00',
    tags: ['Biurowiec', 'Eco-friendly'],
    type: 'office'
  },
  {
    id: 4,
    name: 'IKIGAI Medical Center',
    address: 'ul. Św. Anny 12, 31-008 Kraków',
    lat: 50.0614,
    lng: 19.9366,
    status: 'maintenance',
    stock: 45,
    hours: '08:00-18:00',
    tags: ['Szpital', 'Ochrona'],
    type: 'medical'
  }
])

// Quick filters
const quickFilters = [
  { key: 'online', label: 'Online', icon: '🟢' },
  { key: 'high_stock', label: 'Pełny stan', icon: '📦' },
  { key: 'nearby', label: 'W pobliżu', icon: '📍' },
  { key: '24h', label: '24/7', icon: '🕒' }
]

// Computed
const filteredLocations = computed(() => {
  let filtered = [...locations.value]
  
  if (searchQuery.value) {
    filtered = filtered.filter(loc => 
      loc.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      loc.address.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }
  
  if (activeFilters.value.includes('online')) {
    filtered = filtered.filter(loc => loc.status === 'online')
  }
  
  if (activeFilters.value.includes('high_stock')) {
    filtered = filtered.filter(loc => loc.stock >= 80)
  }
  
  if (activeFilters.value.includes('24h')) {
    filtered = filtered.filter(loc => loc.tags.includes('24/7'))
  }
  
  if (activeFilters.value.includes('nearby') && userLocation.value) {
    filtered = filtered.filter(loc => getDistance(loc) <= 5)
  }
  
  return filtered
})

const stats = computed(() => {
  const online = locations.value.filter(loc => loc.status === 'online').length
  const lowStock = locations.value.filter(loc => loc.stock < 50).length
  const offline = locations.value.filter(loc => loc.status !== 'online').length
  
  return { online, lowStock, offline }
})

// Methods
const toggleFilter = (filterKey: string) => {
  const index = activeFilters.value.indexOf(filterKey)
  if (index > -1) {
    activeFilters.value.splice(index, 1)
  } else {
    activeFilters.value.push(filterKey)
  }
}

const selectLocation = (location: any) => {
  selectedLocation.value = location
}

const locateUser = async () => {
  if (!navigator.geolocation) {
    alert('Geolokalizacja nie jest dostępna w tej przeglądarce')
    return
  }
  
  locatingUser.value = true
  
  try {
    const position = await new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(resolve, reject, {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 60000
      })
    })
    
    userLocation.value = {
      lat: position.coords.latitude,
      lng: position.coords.longitude
    }
  } catch (error) {
    console.error('Error getting location:', error)
    alert('Nie można określić lokalizacji')
  } finally {
    locatingUser.value = false
  }
}

const centerOnUser = () => {
  if (userLocation.value) {
    console.log('Centering on user location:', userLocation.value)
  } else {
    locateUser()
  }
}

const refreshLocations = async () => {
  refreshing.value = true
  setTimeout(() => {
    refreshing.value = false
    console.log('Locations refreshed')
  }, 1000)
}

const getDistance = (location: any) => {
  if (!userLocation.value) return 0
  
  const R = 6371
  const dLat = (location.lat - userLocation.value.lat) * Math.PI / 180
  const dLng = (location.lng - userLocation.value.lng) * Math.PI / 180
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.cos(userLocation.value.lat * Math.PI / 180) * Math.cos(location.lat * Math.PI / 180) *
            Math.sin(dLng/2) * Math.sin(dLng/2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))
  const distance = R * c
  
  return Math.round(distance * 10) / 10
}

const openNavigation = (location: any) => {
  const url = `https://www.google.com/maps/dir/?api=1&destination=${location.lat},${location.lng}`
  window.open(url, '_blank')
}

const showLocationDetails = (location: any) => {
  detailsModal.value = {
    show: true,
    location
  }
}

const getLocationIcon = (location: any) => {
  const icons = {
    university: '🎓',
    fitness: '💪',
    office: '🏢',
    medical: '🏥',
    shopping: '🛒'
  }
  return icons[location.type] || '🏪'
}

const getStatusColor = (status: string) => {
  const colors = {
    online: 'bg-green-500',
    maintenance: 'bg-yellow-500',
    offline: 'bg-red-500'
  }
  return colors[status] || 'bg-gray-500'
}

const getStatusTextColor = (status: string) => {
  const colors = {
    online: 'text-green-600',
    maintenance: 'text-yellow-600', 
    offline: 'text-red-600'
  }
  return colors[status] || 'text-gray-600'
}

const getStatusText = (status: string) => {
  const texts = {
    online: 'Online',
    maintenance: 'Serwis',
    offline: 'Offline'
  }
  return texts[status] || 'Nieznany'
}

const getStockColor = (stock: number) => {
  if (stock >= 80) return 'text-green-600 font-semibold'
  if (stock >= 50) return 'text-yellow-600 font-semibold'
  return 'text-red-600 font-semibold'
}

const getLocationCardStyle = (index: number) => {
  const positions = [
    { top: '20%', left: '65%' },
    { top: '45%', left: '55%' },
    { top: '30%', left: '75%' },
    { top: '60%', left: '70%' }
  ]
  return positions[index] || { top: '50%', left: '50%' }
}

onMounted(() => {
  console.log('Interactive Map component mounted')
})
</script>

<style scoped>
.transition-all {
  transition: all 0.3s ease;
}
</style> 