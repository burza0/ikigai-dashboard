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

    <!-- MAPA NA GÓRZE -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
      <div class="p-6 border-b border-gray-200 dark:border-gray-700">
        <h2 class="text-lg font-semibold text-gray-900 dark:text-white">🗺️ Mapa interaktywna</h2>
        <p class="text-gray-600 dark:text-gray-400">Znajdź najbliższy automat IKIGAI w Warszawie</p>
      </div>
      
      <div class="p-6">
        <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <!-- FILTRY (PO LEWEJ) -->
          <div class="lg:col-span-1">
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">🔍 Filtry</label>
                
                <div class="space-y-3">
                  <div>
                    <label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">Status</label>
                    <select v-model="statusFilter" class="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
                      <option value="all">Wszystkie</option>
                      <option value="online">Online</option>
                      <option value="maintenance">Serwis</option>
                    </select>
                  </div>
                  
                  <div>
                    <label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">Stan magazynu</label>
                    <select v-model="stockFilter" class="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
                      <option value="all">Wszystkie</option>
                      <option value="available">Dostępne produkty</option>
                      <option value="low">Niski stan</option>
                    </select>
                  </div>
                  
                  <button @click="getUserLocation" 
                          :disabled="gettingLocation"
                          class="w-full mt-4 px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50">
                    <span v-if="gettingLocation">📍 Lokalizuję...</span>
                    <span v-else-if="userLocation">📍 Moja lokalizacja</span>
                    <span v-else>🔍 Znajdź mnie</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
          
                     <!-- MAPA (NA ŚRODKU) -->
           <div class="lg:col-span-2">
             <div class="relative bg-gradient-to-br from-green-100 to-blue-100 dark:from-green-900/20 dark:to-blue-900/20 rounded-lg h-80 border border-gray-200 dark:border-gray-600">
               <!-- Symulacja mapy Warszawy (w tle) -->
               <div class="absolute inset-0 flex items-center justify-center z-0">
                 <div class="text-center opacity-50">
                   <div class="text-2xl mb-2">🗺️</div>
                   <div class="text-sm text-gray-600 dark:text-gray-400">Warszawa</div>
                 </div>
               </div>
               
               <!-- Dynamiczne markery automatów -->
               <div 
                 v-for="(machine, index) in vendingMachines" 
                 :key="machine.id"
                 :style="getMarkerStyle(index)"
                 class="absolute cursor-pointer transition-all duration-200 hover:scale-110 z-10"
                 @click="selectMachine(machine)"
                 :title="machine.name">
                 
                 <!-- Główny marker -->
                 <div :class="[
                   'w-8 h-8 rounded-full border-3 border-white shadow-lg flex items-center justify-center text-white font-bold text-lg relative',
                   machine.status === 'online' ? 'bg-green-500' : 'bg-red-500'
                 ]">
                   {{ machine.status === 'online' ? '🏪' : '🔧' }}
                   
                   <!-- Etykieta z nazwą -->
                   <div class="absolute -bottom-8 left-1/2 transform -translate-x-1/2 bg-black bg-opacity-75 text-white text-xs px-2 py-1 rounded whitespace-nowrap">
                     {{ machine.name }}
                   </div>
                   
                   <!-- Pulsujący efekt dla aktywnych automatów -->
                   <div v-if="machine.status === 'online'" 
                        class="absolute inset-0 bg-green-500 rounded-full animate-ping opacity-30"></div>
                 </div>
               </div>
               
               <!-- Marker użytkownika (jeśli lokalizacja jest dostępna) -->
               <div v-if="userLocation" 
                    :style="getUserMarkerStyle()"
                    class="absolute cursor-pointer z-10">
                 <div class="w-6 h-6 bg-blue-500 rounded-full border-2 border-white shadow-lg flex items-center justify-center relative">
                   <div class="w-2 h-2 bg-white rounded-full"></div>
                   <div class="absolute inset-0 bg-blue-500 rounded-full animate-ping opacity-40"></div>
                   
                   <!-- Etykieta -->
                   <div class="absolute -bottom-6 left-1/2 transform -translate-x-1/2 bg-blue-600 text-white text-xs px-2 py-1 rounded whitespace-nowrap">
                     Twoja lokalizacja
                   </div>
                 </div>
               </div>
               
               <!-- Kontrolki mapy -->
               <div class="absolute top-4 right-4 flex flex-col space-y-2">
                 <button class="w-8 h-8 bg-white dark:bg-gray-800 rounded border border-gray-300 dark:border-gray-600 flex items-center justify-center text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700">📍</button>
                 <button class="w-8 h-8 bg-white dark:bg-gray-800 rounded border border-gray-300 dark:border-gray-600 flex items-center justify-center text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700">🏠</button>
               </div>
             </div>
           </div>
           
           <!-- LEGENDA (PO PRAWEJ) -->
           <div class="lg:col-span-1">
             <div class="space-y-4">
               <div>
                 <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">🗺️ Wszystkie automaty</label>
                 <div class="text-xs text-gray-600 dark:text-gray-400 mb-3">Warszawa</div>
                 
                 <div class="space-y-3 text-sm">
                   <div class="flex items-center space-x-2">
                     <div class="w-3 h-3 bg-green-500 rounded-full"></div>
                     <span class="text-gray-700 dark:text-gray-300">Automat online</span>
                   </div>
                   <div class="flex items-center space-x-2">
                     <div class="w-3 h-3 bg-red-500 rounded-full"></div>
                     <span class="text-gray-700 dark:text-gray-300">Automat w serwisie</span>
                   </div>
                   <div class="flex items-center space-x-2">
                     <div class="w-3 h-3 bg-blue-500 rounded-full"></div>
                     <span class="text-gray-700 dark:text-gray-300">Twoja lokalizacja</span>
                   </div>
                 </div>
               </div>
             </div>
           </div>
         </div>
       </div>
     </div>

     <!-- POZIOMA LISTA AUTOMATÓW POD MAPĄ -->
     <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
       <div class="p-6 border-b border-gray-200 dark:border-gray-700">
         <h2 class="text-lg font-semibold text-gray-900 dark:text-white">🏪 Szczegóły automatów</h2>
       </div>
       
       <div class="p-6">
         <!-- Poziomy scroll kontener -->
         <div class="overflow-x-auto">
           <div class="flex gap-4 pb-4" style="min-width: max-content;">
             <div v-for="machine in filteredMachines" :key="machine.id"
                  @click="selectMachine(machine)"
                  :class="[
                    'cursor-pointer p-6 border border-gray-200 dark:border-gray-700 rounded-lg min-w-80 transition-all duration-200',
                    selectedMachine?.id === machine.id 
                      ? 'border-green-500 bg-green-50 dark:bg-green-900/20' 
                      : 'hover:border-green-300 hover:bg-gray-50 dark:hover:bg-gray-700',
                    machine.status === 'online' 
                      ? 'bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 border-green-200 dark:border-green-700'
                      : 'bg-gradient-to-br from-red-50 to-red-100 dark:from-red-900/20 dark:to-red-800/20 border-red-200 dark:border-red-700'
                  ]">
               
               <div class="flex items-center justify-between mb-4">
                 <h3 class="font-semibold text-gray-900 dark:text-white text-lg">{{ machine.name }}</h3>
                 <span :class="[
                   'inline-flex items-center px-3 py-1 rounded-full text-sm font-medium',
                   machine.status === 'online' 
                     ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                     : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                 ]">
                   {{ machine.status === 'online' ? '🟢 Online' : '🔧 Serwis' }}
                 </span>
               </div>
               <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">{{ machine.location }}</p>
               <div class="text-xs text-gray-500 dark:text-gray-500">{{ machine.address }}</div>
               <div class="mt-4 flex items-center justify-between">
                 <div :class="[
                   'text-sm font-medium',
                   machine.status === 'online' 
                     ? 'text-green-600 dark:text-green-400'
                     : 'text-red-600 dark:text-red-400'
                 ]">
                   Stock: {{ machine.current_stock }}/{{ machine.capacity }}
                 </div>
                 <div class="text-xs text-gray-500 dark:text-gray-500">{{ machine.operating_hours }}</div>
               </div>
               
               <div v-if="userLocation" class="mt-2 text-xs text-blue-600 dark:text-blue-400">
                 📍 {{ getDistance(machine) }} km od Ciebie
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
  // Pozycje dla wszystkich 5 automatów na mapie Warszawy
  const positions = [
    { top: '40%', left: '50%' },  // IKIGAI Central - centrum
    { top: '60%', left: '30%' },  // IKIGAI Fitness - południowy zachód
    { top: '30%', left: '70%' },  // IKIGAI Office - północny wschód
    { top: '25%', left: '45%' },  // IKIGAI University - północ centrum
    { top: '70%', left: '60%' }   // IKIGAI Park - południe wschód
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

const getMarkerStyle = (index) => {
  const position = getMarkerPosition(index)
  return {
    top: position.top,
    left: position.left
  }
}

const getUserMarkerStyle = () => {
  const position = getUserMarkerPosition()
  return {
    top: position.top,
    left: position.left
  }
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