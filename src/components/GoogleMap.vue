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
            <h1 class="text-xl font-bold text-gray-900">🗺️ Mapa automatów IKIGAI (Google Maps)</h1>
          </div>
        </div>
      </div>
    </div>

    <div class="flex h-[calc(100vh-4rem)]">
      
      <!-- Sidebar -->
      <div class="w-full md:w-96 bg-white shadow-lg flex flex-col">
        
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
              v-for="location in locations" 
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
                  
                  <!-- Quick Actions -->
                  <div class="grid grid-cols-2 gap-2">
                    <button 
                      @click.stop="openNavigation(location)"
                      class="flex items-center justify-center px-3 py-2 bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition-colors text-sm"
                    >
                      🧭 Nawiguj
                    </button>
                    <button 
                      @click.stop="showLocationDetails(location)"
                      class="flex items-center justify-center px-3 py-2 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors text-sm"
                    >
                      ℹ️ Szczegóły
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Google Maps Container -->
      <div class="flex-1 relative">
        <div ref="mapContainer" class="w-full h-full">
          <!-- Loading State -->
          <div v-if="mapLoading" class="absolute inset-0 bg-gray-100 flex items-center justify-center z-10">
            <div class="text-center">
              <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <p class="text-gray-600">Ładowanie Google Maps...</p>
            </div>
          </div>
          
          <!-- Error State -->
          <div v-if="mapError" class="absolute inset-0 bg-gray-100 flex items-center justify-center z-10">
            <div class="text-center p-8">
              <div class="text-red-500 text-4xl mb-4">⚠️</div>
              <h3 class="text-lg font-semibold text-gray-900 mb-2">Błąd ładowania mapy</h3>
              <p class="text-gray-600 mb-4">{{ mapError }}</p>
              <button @click="initializeMap" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                Spróbuj ponownie
              </button>
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
            🎯
          </button>
          
          <button 
            @click="refreshLocations"
            class="p-3 bg-white rounded-lg shadow-md border border-gray-200 hover:bg-gray-50 transition-colors"
            :disabled="refreshing"
            title="Odśwież dane"
          >
            🔄
          </button>
        </div>
      </div>
    </div>

    <!-- Location Details Modal -->
    <div v-if="detailsModal.show" 
         class="fixed inset-0 z-50 overflow-y-auto"
         @click="detailsModal.show = false">
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
        
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
             @click.stop>
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
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
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { Loader } from '@googlemaps/js-api-loader'

// Define emits
defineEmits<{
  'navigate': (view: string) => void
}>()

// Reactive data
const searchQuery = ref('')
const selectedLocation = ref(null)
const userLocation = ref(null)
const locatingUser = ref(false)
const refreshing = ref(false)
const mapContainer = ref(null)
const mapLoading = ref(true)
const mapError = ref('')

// Google Maps
let map = null
let markers = []
let userMarker = null
let infoWindow = null

// Modal
const detailsModal = ref({
  show: false,
  location: null
})

// Real locations in Kraków
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
    type: 'medical'
  },
  {
    id: 5,
    name: 'IKIGAI Galeria Kazimierz',
    address: 'ul. Podgórska 34, 30-306 Kraków',
    lat: 50.0489,
    lng: 19.9578,
    status: 'online',
    stock: 67,
    hours: '09:00-21:00',
    type: 'shopping'
  }
])

// Google Maps configuration  
const GOOGLE_MAPS_API_KEY = 'AIzaSyB41DRUbKWJHPxaFjMAwdrzWzbVKartNGg' // Demo key
const mapOptions = {
  center: { lat: 50.0647, lng: 19.9450 }, // Kraków center
  zoom: 13,
  mapTypeId: 'roadmap'
}

// Google Maps Methods
const initializeMap = async () => {
  try {
    mapLoading.value = true
    mapError.value = ''
    
    const loader = new Loader({
      apiKey: GOOGLE_MAPS_API_KEY,
      version: 'weekly'
    })
    
    await loader.load()
    await nextTick()
    
    if (!mapContainer.value) {
      throw new Error('Map container not found')
    }
    
    // Initialize map
    map = new google.maps.Map(mapContainer.value, mapOptions)
    
    // Initialize InfoWindow
    infoWindow = new google.maps.InfoWindow()
    
    // Add markers for all locations
    createLocationMarkers()
    
    mapLoading.value = false
    console.log('Google Maps initialized successfully')
    
  } catch (error) {
    console.error('Error initializing Google Maps:', error)
    mapError.value = error.message || 'Błąd ładowania Google Maps'
    mapLoading.value = false
  }
}

const createLocationMarkers = () => {
  // Clear existing markers
  markers.forEach(marker => marker.setMap(null))
  markers = []
  
  locations.value.forEach(location => {
    const marker = new google.maps.Marker({
      position: { lat: location.lat, lng: location.lng },
      map: map,
      title: location.name,
      icon: {
        url: getMarkerIcon(location),
        scaledSize: new google.maps.Size(40, 40),
        anchor: new google.maps.Point(20, 40)
      }
    })
    
    // Info window content
    const infoContent = `
      <div style="padding: 12px; max-width: 300px;">
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
          <span style="font-size: 24px; margin-right: 8px;">${getLocationIcon(location)}</span>
          <div>
            <h3 style="margin: 0; font-weight: bold; color: #111;">${location.name}</h3>
            <p style="margin: 4px 0 0 0; font-size: 14px; color: #666;">${location.address}</p>
          </div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
          <span style="display: inline-flex; align-items: center; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: 500; ${getStatusBadgeStyle(location.status)}">
            ${getStatusText(location.status)}
          </span>
          <span style="font-size: 14px; font-weight: 500;">Stock: ${location.stock}%</span>
        </div>
        <p style="margin: 0 0 8px 0; font-size: 12px; color: #666;">⏰ ${location.hours}</p>
        <div style="display: flex; gap: 8px;">
          <a href="https://www.google.com/maps/dir/?api=1&destination=${location.lat},${location.lng}" 
             target="_blank" 
             style="padding: 6px 12px; background: #dcfce7; color: #166534; border-radius: 6px; text-decoration: none; font-size: 14px;">
            🧭 Nawiguj
          </a>
          <button onclick="window.showLocationDetails(${location.id})" 
                  style="padding: 6px 12px; background: #dbeafe; color: #1d4ed8; border: none; border-radius: 6px; cursor: pointer; font-size: 14px;">
            ℹ️ Szczegóły
          </button>
        </div>
      </div>
    `
    
    marker.addListener('click', () => {
      infoWindow.setContent(infoContent)
      infoWindow.open(map, marker)
      selectLocation(location)
    })
    
    markers.push(marker)
  })
  
  console.log(`Created ${markers.length} markers`)
}

const getMarkerIcon = (location) => {
  const status = location.status
  let color = '#10B981' // green
  let emoji = '🏪'
  
  if (status === 'maintenance') {
    color = '#F59E0B' // yellow
    emoji = '🔧'
  } else if (status === 'offline') {
    color = '#EF4444' // red
    emoji = '❌'
  }
  
  return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(`
    <svg width="40" height="40" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
      <circle cx="20" cy="20" r="18" fill="${color}" stroke="white" stroke-width="2"/>
      <text x="20" y="26" text-anchor="middle" fill="white" font-size="14">${emoji}</text>
    </svg>
  `)}`
}

// Global function for InfoWindow
window.showLocationDetails = (locationId) => {
  const location = locations.value.find(loc => loc.id === locationId)
  if (location) showLocationDetails(location)
}

// Methods
const selectLocation = (location: any) => {
  selectedLocation.value = location
  
  if (map) {
    map.panTo({ lat: location.lat, lng: location.lng })
    map.setZoom(15)
  }
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
    
    // Add user marker to map
    if (map) {
      if (userMarker) {
        userMarker.setMap(null)
      }
      
      userMarker = new google.maps.Marker({
        position: userLocation.value,
        map: map,
        title: 'Twoja lokalizacja',
        icon: {
          url: `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(`
            <svg width="30" height="30" viewBox="0 0 30 30" xmlns="http://www.w3.org/2000/svg">
              <circle cx="15" cy="15" r="13" fill="#3B82F6" stroke="white" stroke-width="2"/>
              <circle cx="15" cy="15" r="6" fill="white"/>
              <circle cx="15" cy="15" r="3" fill="#3B82F6"/>
            </svg>
          `)}`,
          scaledSize: new google.maps.Size(30, 30),
          anchor: new google.maps.Point(15, 15)
        }
      })
      
      map.panTo(userLocation.value)
      map.setZoom(15)
    }
    
  } catch (error) {
    console.error('Error getting location:', error)
    alert('Nie można określić lokalizacji')
  } finally {
    locatingUser.value = false
  }
}

const centerOnUser = () => {
  if (userLocation.value && map) {
    map.panTo(userLocation.value)
    map.setZoom(15)
  } else {
    locateUser()
  }
}

const refreshLocations = async () => {
  refreshing.value = true
  
  setTimeout(() => {
    if (map) {
      createLocationMarkers()
    }
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

const getStatusBadgeStyle = (status: string) => {
  const styles = {
    online: 'background: #dcfce7; color: #166534;',
    maintenance: 'background: #fef3c7; color: #92400e;',
    offline: 'background: #fee2e2; color: #991b1b;'
  }
  return styles[status] || 'background: #f3f4f6; color: #374151;'
}

const getStockColor = (stock: number) => {
  if (stock >= 80) return 'text-green-600 font-semibold'
  if (stock >= 50) return 'text-yellow-600 font-semibold'
  return 'text-red-600 font-semibold'
}

// Lifecycle
onMounted(() => {
  console.log('Google Maps component mounted')
  initializeMap()
})

onUnmounted(() => {
  // Cleanup
  if (markers) {
    markers.forEach(marker => marker.setMap(null))
  }
  if (userMarker) {
    userMarker.setMap(null)
  }
})
</script>

<style scoped>
.transition-all {
  transition: all 0.3s ease;
}
</style> 