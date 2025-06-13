<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 mb-8">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">🛒 Koszyk Zamówień</h1>
            <p class="text-gray-600 dark:text-gray-400 mt-2">Zarządzaj wszystkimi zamówieniami w systemie</p>
          </div>
          <div class="flex items-center space-x-4">
            <!-- Status Filter -->
            <select
              v-model="statusFilter"
              class="px-4 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg text-sm font-medium text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
            >
              <option value="">Wszystkie statusy</option>
              <option value="pending">⏳ Oczekuje</option>
              <option value="preparing">👨‍🍳 Przygotowywane</option>
              <option value="ready">✅ Gotowe</option>
              <option value="completed">🎉 Zakończone</option>
              <option value="cancelled">❌ Anulowane</option>
            </select>
            
            <!-- Refresh Button -->
            <button
              @click="loadOrders"
              :disabled="loading"
              class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 transition-all duration-200 flex items-center space-x-2"
            >
              <span>{{ loading ? 'Ładowanie...' : 'Odśwież' }}</span>
            </button>
            
            <!-- Stats -->
            <div class="bg-purple-100 dark:bg-purple-900 px-4 py-2 rounded-lg">
              <span class="text-purple-800 dark:text-purple-200 font-medium">{{ filteredOrders.length }} zamówień</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Loading State -->
      <div v-if="loading && orders.length === 0" class="flex items-center justify-center py-12">
        <div class="text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p class="text-gray-600 dark:text-gray-400">Ładowanie zamówień...</p>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredOrders.length === 0" class="text-center py-12">
        <div class="text-gray-400 text-6xl mb-4">🛒</div>
        <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
          {{ statusFilter ? 'Brak zamówień z tym statusem' : 'Brak zamówień' }}
        </h3>
        <p class="text-gray-600 dark:text-gray-400 mb-6">
          {{ statusFilter ? 'Zmień filtr statusu lub dodaj nowe zamówienia' : 'Nie ma jeszcze żadnych zamówień w systemie' }}
        </p>
        <button 
          @click="$emit('navigate', 'mixer')" 
          class="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
        >
          🥣 Utwórz pierwsze zamówienie
        </button>
      </div>

      <!-- Orders Grid -->
      <div v-else class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="order in filteredOrders"
          :key="order.id"
          class="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 overflow-hidden hover:shadow-xl transition-all duration-200"
        >
          <!-- Order Header -->
          <div class="p-6 border-b border-gray-200 dark:border-gray-700">
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center space-x-3">
                <div class="w-12 h-12 bg-gradient-to-r from-purple-500 to-purple-600 rounded-full flex items-center justify-center">
                  <span class="text-white text-lg">{{ getOrderIcon(order.status) }}</span>
                </div>
                <div>
                  <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Zamówienie #{{ order.id.slice(-4) }}</h3>
                  <p class="text-sm text-gray-600 dark:text-gray-400">{{ formatDate(order.created_at) }}</p>
                </div>
              </div>
              <div :class="getStatusColor(order.status)" class="px-3 py-1 rounded-full text-xs font-medium">
                {{ getStatusText(order.status) }}
              </div>
            </div>
          </div>

          <!-- Order Details -->
          <div class="p-6">
            <div class="space-y-3">
              <!-- User -->
              <div class="flex items-center justify-between">
                <span class="text-gray-600 dark:text-gray-400">Użytkownik:</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ order.user_id }}</span>
              </div>
              
              <!-- Machine -->
              <div class="flex items-center justify-between">
                <span class="text-gray-600 dark:text-gray-400">Automat:</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ order.machine_id }}</span>
              </div>
              
              <!-- Price -->
              <div class="flex items-center justify-between">
                <span class="text-gray-600 dark:text-gray-400">Cena:</span>
                <span class="font-bold text-purple-600 dark:text-purple-400">{{ order.total_price }} PLN</span>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="mt-6 flex space-x-2">
              <!-- Payment Button -->
              <button
                @click="processPayment(order)"
                :disabled="order.status === 'completed' || order.status === 'cancelled'"
                :class="[
                  'flex-1 px-4 py-2 rounded-lg font-medium text-sm transition-colors',
                  order.status === 'completed' || order.status === 'cancelled'
                    ? 'bg-gray-300 dark:bg-gray-600 text-gray-500 dark:text-gray-400 cursor-not-allowed'
                    : 'bg-green-600 text-white hover:bg-green-700'
                ]"
              >
                {{ order.status === 'completed' ? '✅ Opłacone' : order.status === 'cancelled' ? '❌ Anulowane' : '💳 Opłać' }}
              </button>
              
              <!-- QR Code Button -->
              <button
                @click="showQRCode(order)"
                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
              >
                📱 QR
              </button>
              
              <!-- Delete Button -->
              <button
                @click="confirmDeleteOrder(order)"
                :disabled="order.status === 'preparing' || order.status === 'ready'"
                :class="[
                  'px-4 py-2 rounded-lg font-medium text-sm transition-colors',
                  order.status === 'preparing' || order.status === 'ready'
                    ? 'bg-gray-300 dark:bg-gray-600 text-gray-500 dark:text-gray-400 cursor-not-allowed'
                    : 'bg-red-600 text-white hover:bg-red-700'
                ]"
                :title="order.status === 'preparing' || order.status === 'ready' ? 'Nie można usunąć zamówienia w trakcie przygotowania' : 'Usuń zamówienie'"
              >
                🗑️
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- QR Code Modal -->
    <div v-if="showQRModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="showQRModal = false">
      <div class="bg-white dark:bg-gray-800 rounded-xl p-8 max-w-md w-full mx-4" @click.stop>
        <div class="text-center">
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Kod QR dla zamówienia #{{ selectedOrder?.id.slice(-4) }}
          </h3>
          
          <div v-if="qrCodeLoading" class="flex justify-center py-12">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
          </div>
          
          <div v-else-if="qrCodeData" class="mb-6">
            <img :src="qrCodeData" alt="QR Code" class="mx-auto max-w-full h-auto" />
          </div>
          
          <button
            @click="showQRModal = false"
            class="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
          >
            Zamknij
          </button>
        </div>
      </div>
    </div>

    <!-- Payment Modal -->
    <div v-if="showPaymentModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="showPaymentModal = false">
      <div class="bg-white dark:bg-gray-800 rounded-xl p-8 max-w-md w-full mx-4" @click.stop>
        <div class="text-center">
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            💳 Płatność za zamówienie #{{ selectedOrder?.id.slice(-4) }}
          </h3>
          
          <div class="mb-6">
            <div class="bg-purple-100 dark:bg-purple-900 p-4 rounded-lg mb-4">
              <p class="text-lg font-bold text-purple-800 dark:text-purple-200">
                {{ selectedOrder?.total_price }} PLN
              </p>
            </div>
            
            <div class="space-y-3">
              <button
                @click="payWithCard"
                class="w-full px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                💳 Płać kartą
              </button>
              
              <button
                @click="payWithBlik"
                class="w-full px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium"
              >
                📱 Płać BLIK
              </button>
              
              <button
                @click="payWithPayU"
                class="w-full px-4 py-3 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-colors font-medium"
              >
                🏦 PayU
              </button>
            </div>
          </div>
          
          <button
            @click="showPaymentModal = false"
            class="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
          >
            Anuluj
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="showDeleteModal = false">
      <div class="bg-white dark:bg-gray-800 rounded-xl p-8 max-w-md w-full mx-4" @click.stop>
        <div class="text-center">
          <div class="text-red-500 text-6xl mb-4">⚠️</div>
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Usunąć zamówienie?
          </h3>
          
          <div class="mb-6">
            <p class="text-gray-600 dark:text-gray-400 mb-4">
              Czy na pewno chcesz usunąć zamówienie #{{ orderToDelete?.id.slice(-4) }}?
            </p>
            <div class="bg-red-50 dark:bg-red-900 p-4 rounded-lg">
              <p class="text-red-800 dark:text-red-200 text-sm font-medium">
                ⚠️ Ta operacja jest nieodwracalna!
              </p>
            </div>
          </div>
          
          <div class="flex space-x-3">
            <button
              @click="showDeleteModal = false"
              class="flex-1 px-4 py-2 bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-400 dark:hover:bg-gray-500 transition-colors font-medium"
            >
              Anuluj
            </button>
            <button
              @click="deleteOrder"
              :disabled="deleting"
              class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 transition-colors font-medium"
            >
              {{ deleting ? 'Usuwanie...' : 'Usuń' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'

const orders = ref([])
const loading = ref(false)
const statusFilter = ref('')

const showQRModal = ref(false)
const showPaymentModal = ref(false)
const selectedOrder = ref(null)
const qrCodeData = ref(null)
const qrCodeLoading = ref(false)

const showDeleteModal = ref(false)
const orderToDelete = ref(null)
const deleting = ref(false)

const emit = defineEmits(['navigate'])

// Computed property for filtered orders
const filteredOrders = computed(() => {
  if (!statusFilter.value) {
    return orders.value
  }
  return orders.value.filter(order => order.status === statusFilter.value)
})

const loadOrders = async () => {
  loading.value = true
  
  try {
    const response = await fetch('http://localhost:5001/api/orders?limit=50')
    const data = await response.json()
    
    if (data.status === 'success') {
      orders.value = data.data
    }
  } catch (err) {
    console.error('Error loading orders:', err)
  } finally {
    loading.value = false
  }
}

const processPayment = (order) => {
  selectedOrder.value = order
  showPaymentModal.value = true
}

const payWithCard = () => {
  // Przekierowanie do płatności kartą
  window.open('https://payment.example.com/card', '_blank')
  showPaymentModal.value = false
}

const payWithBlik = () => {
  // Przekierowanie do płatności BLIK
  window.open('https://payment.example.com/blik', '_blank')
  showPaymentModal.value = false
}

const payWithPayU = () => {
  // Przekierowanie do płatności PayU
  window.open('https://payment.example.com/payu', '_blank')
  showPaymentModal.value = false
}

const showQRCode = async (order) => {
  selectedOrder.value = order
  showQRModal.value = true
  qrCodeLoading.value = true
  
  try {
    const response = await fetch(`http://localhost:5001/api/orders/${order.id}/qr`)
    const data = await response.json()
    
    if (data.status === 'success' && data.qr_code) {
      qrCodeData.value = data.qr_code
    }
  } catch (err) {
    console.error('Error loading QR code:', err)
  } finally {
    qrCodeLoading.value = false
  }
}

const confirmDeleteOrder = (order) => {
  orderToDelete.value = order
  showDeleteModal.value = true
}

const deleteOrder = async () => {
  deleting.value = true
  
  try {
    const response = await fetch(`http://localhost:5001/api/orders/${orderToDelete.value.id}`, {
      method: 'DELETE'
    })
    const data = await response.json()
    
    if (data.status === 'success') {
      orders.value = orders.value.filter(o => o.id !== orderToDelete.value.id)
      showDeleteModal.value = false
    }
  } catch (err) {
    console.error('Error deleting order:', err)
  } finally {
    deleting.value = false
  }
}

const getOrderIcon = (status) => {
  const icons = { pending: '⏳', preparing: '👨‍🍳', ready: '✅', completed: '🎉', cancelled: '❌' }
  return icons[status] || '📦'
}

const getStatusColor = (status) => {
  const colors = {
    pending: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
    preparing: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200', 
    ready: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    completed: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
    cancelled: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
  }
  return colors[status] || 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200'
}

const getStatusText = (status) => {
  const texts = { pending: 'Oczekuje', preparing: 'Przygotowywane', ready: 'Gotowe', completed: 'Zakończone', cancelled: 'Anulowane' }
  return texts[status] || status
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('pl-PL', {
    year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit'
  })
}

onMounted(() => {
  loadOrders()
})
</script>
