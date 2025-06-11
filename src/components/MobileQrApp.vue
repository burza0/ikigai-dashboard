<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-indigo-900">
    <!-- Mobile Header -->
    <div class="bg-black/20 backdrop-blur-md sticky top-0 z-50">
      <div class="max-w-md mx-auto px-4 py-3">
        <div class="flex items-center justify-between">
          <button @click="$emit('back')" class="text-white/80 hover:text-white">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
            </svg>
          </button>
          <h1 class="text-xl font-bold text-white">📱 IKIGAI Mobile</h1>
          <div class="relative">
            <button @click="showNotifications = !showNotifications" class="text-white/80 hover:text-white relative">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
              </svg>
              <span v-if="notifications.filter(n => !n.read).length > 0" 
                    class="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                {{ notifications.filter(n => !n.read).length }}
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-md mx-auto px-4 pb-20">


      <!-- Action Tabs -->
      <div class="flex bg-white/10 backdrop-blur-md rounded-xl p-1 mb-6">
        <button v-for="tab in tabs" :key="tab.id"
                @click="activeTab = tab.id"
                :class="[
                  'flex-1 py-3 px-4 rounded-lg font-medium transition-all duration-200',
                  activeTab === tab.id 
                    ? 'bg-white text-gray-900 shadow-lg' 
                    : 'text-white/70 hover:text-white'
                ]">
          {{ tab.icon }} {{ tab.name }}
        </button>
      </div>

      <!-- QR Scanner Tab -->
      <div v-if="activeTab === 'scanner'" class="space-y-6">
        <div class="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
          <h3 class="text-xl font-bold text-white mb-4">🎯 Skaner QR</h3>
          
          <!-- Camera View Simulation -->
          <div class="bg-black rounded-xl mb-4 relative overflow-hidden">
            <div class="aspect-square bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center">
              <div v-if="!scanning" class="text-center">
                <div class="w-48 h-48 border-4 border-white/30 rounded-xl mb-4 relative">
                  <div class="absolute inset-4 border-2 border-purple-400 rounded-lg animate-pulse"></div>
                  <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-white/60">
                    Skieruj kamerę na kod QR
                  </div>
                </div>
              </div>
              <div v-else class="text-center">
                <div class="w-48 h-48 border-4 border-green-400 rounded-xl mb-4 relative">
                  <div class="absolute inset-4 border-2 border-green-400 rounded-lg animate-ping"></div>
                  <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-green-400 text-sm">
                    Skanowanie...
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Manual Input -->
          <div class="space-y-3">
            <input v-model="manualQrCode" 
                   placeholder="Lub wpisz kod QR ręcznie" 
                   class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50">
            <button @click="startScanning" 
                    :disabled="scanning"
                    class="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 text-white font-bold py-3 px-6 rounded-xl transition-all duration-200">
              {{ scanning ? '🔄 Skanowanie...' : '📱 Rozpocznij skanowanie' }}
            </button>
          </div>
        </div>

        <!-- Recent Scans -->
        <div class="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
          <h4 class="text-lg font-bold text-white mb-3">📋 Ostatnie skany</h4>
          <div class="space-y-2">
            <div v-for="scan in recentScans" :key="scan.id" 
                 class="flex items-center justify-between p-3 bg-white/5 rounded-lg">
              <div>
                <div class="text-white font-medium">{{ scan.location }}</div>
                <div class="text-white/60 text-sm">{{ scan.time }}</div>
              </div>
              <div :class="[
                'px-2 py-1 rounded-full text-xs font-medium',
                scan.status === 'success' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
              ]">
                {{ scan.status === 'success' ? '✅ Sukces' : '❌ Błąd' }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- My QR Codes Tab -->
      <div v-if="activeTab === 'my-qr'" class="space-y-6">
        <!-- Generated QR Codes Section -->
        <div class="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-xl font-bold text-white">🎫 Moje kody QR</h3>
            <button @click="refreshQrCodes" class="bg-purple-500/20 hover:bg-purple-500/30 text-purple-400 px-3 py-2 rounded-lg transition-all duration-200">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
              </svg>
            </button>
          </div>
          
          <!-- Active QR Codes -->
          <div v-if="myQrCodes.length > 0" class="space-y-4">
            <div v-for="qr in myQrCodes" :key="qr.id" 
                 class="bg-white/5 rounded-xl p-4 border border-white/10">
              <div class="flex items-center justify-between mb-3">
                <div>
                  <h4 class="text-white font-bold">{{ qr.name }}</h4>
                  <p class="text-white/60 text-sm">{{ qr.description }}</p>
                </div>
                <div class="text-right">
                  <div class="text-white font-bold text-lg">{{ qr.price }}zł</div>
                  <div :class="[
                    'px-2 py-1 rounded-full text-xs font-medium',
                    qr.status === 'active' ? 'bg-green-500/20 text-green-400' :
                    qr.status === 'used' ? 'bg-gray-500/20 text-gray-400' :
                    qr.status === 'expired' ? 'bg-red-500/20 text-red-400' :
                    'bg-yellow-500/20 text-yellow-400'
                  ]">
                    {{ getStatusText(qr.status) }}
                  </div>
                </div>
              </div>
              
              <!-- QR Code Display -->
              <div class="bg-white rounded-lg p-4 mb-3 text-center">
                <div class="w-32 h-32 mx-auto bg-gray-100 rounded border-2 border-gray-300 flex items-center justify-center">
                  <div class="text-xs text-gray-600 text-center">
                    <div class="text-2xl mb-1">🎯</div>
                    <div>QR CODE</div>
                    <div class="font-mono text-xs">{{ qr.code.substring(0, 8) }}...</div>
                  </div>
                </div>
              </div>
              
              <!-- QR Actions -->
              <div class="flex gap-2">
                <button @click="showQrFullscreen(qr)" 
                        class="flex-1 bg-blue-500/20 hover:bg-blue-500/30 text-blue-400 py-2 px-3 rounded-lg text-sm font-medium transition-all duration-200">
                  👁️ Pokaż pełny
                </button>
                <button @click="shareQr(qr)" 
                        class="flex-1 bg-green-500/20 hover:bg-green-500/30 text-green-400 py-2 px-3 rounded-lg text-sm font-medium transition-all duration-200">
                  📤 Udostępnij
                </button>
                <button @click="deleteQr(qr.id)" 
                        v-if="qr.status === 'active'"
                        class="flex-1 bg-red-500/20 hover:bg-red-500/30 text-red-400 py-2 px-3 rounded-lg text-sm font-medium transition-all duration-200">
                  🗑️ Usuń
                </button>
              </div>
              
              <!-- Additional Info -->
              <div class="mt-3 pt-3 border-t border-white/10">
                <div class="flex justify-between text-xs text-white/60">
                  <span>Utworzony: {{ qr.created }}</span>
                  <span v-if="qr.expiresAt">Wygasa: {{ qr.expiresAt }}</span>
                </div>
                <div v-if="qr.usedAt" class="text-xs text-white/60 mt-1">
                  Użyty: {{ qr.usedAt }} w {{ qr.usedLocation }}
                </div>
              </div>
            </div>
          </div>
          
          <!-- Empty State -->
          <div v-else class="text-center py-8">
            <div class="text-6xl mb-4">📱</div>
            <h4 class="text-xl font-bold text-white mb-2">Brak kodów QR</h4>
            <p class="text-white/60 mb-4">Utworz swoją pierwszą mieszankę w Kreatorze, aby wygenerować kod QR</p>
            <button @click="$emit('navigate', 'mixer')" 
                    class="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-bold py-3 px-6 rounded-xl transition-all duration-200">
              🥣 Stwórz mieszankę
            </button>
          </div>
        </div>

        <!-- QR Management Options -->
        <div class="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
          <h4 class="text-lg font-bold text-white mb-4">⚙️ Zarządzanie</h4>
          <div class="space-y-3">
            <button @click="bulkDeleteExpired" 
                    class="w-full bg-orange-500/20 hover:bg-orange-500/30 text-orange-400 py-3 px-4 rounded-xl text-left transition-all duration-200">
              <div class="flex items-center justify-between">
                <div>
                  <div class="font-medium">🧹 Usuń wygasłe kody</div>
                  <div class="text-sm opacity-70">Wyczyść nieaktywne zamówienia</div>
                </div>
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
              </div>
            </button>
            
            <button @click="exportQrHistory" 
                    class="w-full bg-blue-500/20 hover:bg-blue-500/30 text-blue-400 py-3 px-4 rounded-xl text-left transition-all duration-200">
              <div class="flex items-center justify-between">
                <div>
                  <div class="font-medium">📥 Eksportuj historię</div>
                  <div class="text-sm opacity-70">Pobierz historię zamówień</div>
                </div>
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
              </div>
            </button>
            
            <button @click="toggleAutoDelete" 
                    class="w-full bg-purple-500/20 hover:bg-purple-500/30 text-purple-400 py-3 px-4 rounded-xl text-left transition-all duration-200">
              <div class="flex items-center justify-between">
                <div>
                  <div class="font-medium">{{ autoDeleteEnabled ? '🔕' : '🔔' }} Auto-usuwanie</div>
                  <div class="text-sm opacity-70">{{ autoDeleteEnabled ? 'Wyłącz' : 'Włącz' }} automatyczne czyszczenie</div>
                </div>
                <div :class="[
                  'w-6 h-3 rounded-full transition-all duration-200',
                  autoDeleteEnabled ? 'bg-purple-500' : 'bg-white/20'
                ]">
                  <div :class="[
                    'w-3 h-3 rounded-full bg-white transition-transform duration-200',
                    autoDeleteEnabled ? 'translate-x-3' : 'translate-x-0'
                  ]"></div>
                </div>
              </div>
            </button>
          </div>
        </div>
      </div>

      <!-- Payments Tab -->
      <div v-if="activeTab === 'payment'" class="space-y-6">
        <div class="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
          <h3 class="text-xl font-bold text-white mb-4">💳 Płatności Mobilne</h3>
          
          <!-- Payment Methods -->
          <div class="space-y-3 mb-6">
            <div v-for="method in paymentMethods" :key="method.id"
                 @click="selectedPayment = method.id"
                 :class="[
                   'flex items-center p-4 rounded-xl border-2 cursor-pointer transition-all duration-200',
                   selectedPayment === method.id 
                     ? 'border-purple-400 bg-purple-500/20' 
                     : 'border-white/20 bg-white/5 hover:bg-white/10'
                 ]">
              <div class="text-2xl mr-3">{{ method.icon }}</div>
              <div class="flex-1">
                <div class="text-white font-medium">{{ method.name }}</div>
                <div class="text-white/60 text-sm">{{ method.description }}</div>
              </div>
              <div v-if="selectedPayment === method.id" class="text-purple-400">
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"></path>
                </svg>
              </div>
            </div>
          </div>

          <!-- Current Balance -->
          <div class="bg-gradient-to-r from-green-600/20 to-blue-600/20 rounded-xl p-4 mb-4">
            <div class="text-center">
              <div class="text-3xl font-bold text-white">{{ currentBalance }} zł</div>
              <div class="text-white/70">Dostępne środki</div>
            </div>
          </div>

          <!-- Quick Add Money -->
          <div class="grid grid-cols-3 gap-3 mb-4">
            <button v-for="amount in quickAmounts" :key="amount"
                    @click="showPaymentSimulator(amount, `Doładowanie ${amount}zł`)"
                    class="bg-white/10 hover:bg-white/20 border border-white/20 text-white font-bold py-3 rounded-xl transition-all duration-200">
              +{{ amount }}zł
            </button>
          </div>
        </div>

        <!-- Transaction History -->
        <div class="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
          <h4 class="text-lg font-bold text-white mb-3">💸 Historia transakcji</h4>
          <div class="space-y-2">
            <div v-for="transaction in transactions" :key="transaction.id" 
                 class="flex items-center justify-between p-3 bg-white/5 rounded-lg">
              <div>
                <div class="text-white font-medium">{{ transaction.description }}</div>
                <div class="text-white/60 text-sm">{{ transaction.date }}</div>
              </div>
              <div :class="[
                'font-bold',
                transaction.amount > 0 ? 'text-green-400' : 'text-red-400'
              ]">
                {{ transaction.amount > 0 ? '+' : '' }}{{ transaction.amount }}zł
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Orders Tab -->
      <div v-if="activeTab === 'orders'" class="space-y-6">
        <div class="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
          <h3 class="text-xl font-bold text-white mb-4">📦 Śledzenie zamówień</h3>
          
          <!-- Active Order -->
          <div v-if="activeOrder" class="bg-gradient-to-r from-purple-600/20 to-pink-600/20 rounded-xl p-4 mb-4">
            <div class="flex items-center justify-between mb-3">
              <h4 class="text-lg font-bold text-white">Aktualne zamówienie</h4>
              <span class="bg-yellow-500/20 text-yellow-400 px-3 py-1 rounded-full text-sm font-medium">
                {{ activeOrder.status }}
              </span>
            </div>
            
            <!-- Progress Bar -->
            <div class="mb-4">
              <div class="flex justify-between text-sm text-white/70 mb-1">
                <span>Postęp</span>
                <span>{{ activeOrder.progress }}%</span>
              </div>
              <div class="w-full bg-white/10 rounded-full h-2">
                <div class="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full transition-all duration-500" 
                     :style="{ width: activeOrder.progress + '%' }"></div>
              </div>
            </div>

            <!-- Order Details -->
            <div class="space-y-2">
              <div class="flex justify-between text-white">
                <span>Automat:</span>
                <span class="font-medium">{{ activeOrder.machine }}</span>
              </div>
              <div class="flex justify-between text-white">
                <span>Czas pozostały:</span>
                <span class="font-medium text-green-400">{{ activeOrder.timeLeft }}</span>
              </div>
              <div class="flex justify-between text-white">
                <span>Łącznie:</span>
                <span class="font-bold text-lg">{{ activeOrder.total }}zł</span>
              </div>
            </div>
          </div>

          <!-- Quick Order -->
          <div class="bg-white/5 rounded-xl p-4 mb-4">
            <h4 class="text-lg font-bold text-white mb-3">⚡ Szybkie zamówienie</h4>
            <div class="grid grid-cols-2 gap-3">
              <button v-for="quick in quickOrders" :key="quick.id"
                      @click="createQuickOrder(quick)"
                      class="bg-gradient-to-r from-orange-500/20 to-red-500/20 hover:from-orange-500/30 hover:to-red-500/30 border border-orange-500/30 text-white p-4 rounded-xl transition-all duration-200">
                <div class="text-2xl mb-1">{{ quick.icon }}</div>
                <div class="font-medium text-sm">{{ quick.name }}</div>
                <div class="text-orange-400 font-bold">{{ quick.price }}zł</div>
              </button>
            </div>
          </div>
        </div>

        <!-- Order History -->
        <div class="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
          <h4 class="text-lg font-bold text-white mb-3">📋 Historia zamówień</h4>
          <div class="space-y-3">
            <div v-for="order in orderHistory" :key="order.id" 
                 class="p-4 bg-white/5 rounded-xl">
              <div class="flex items-center justify-between mb-2">
                <div class="text-white font-medium">{{ order.name }}</div>
                <div class="text-white font-bold">{{ order.price }}zł</div>
              </div>
              <div class="flex items-center justify-between text-sm">
                <span class="text-white/60">{{ order.date }}</span>
                <span :class="[
                  'px-2 py-1 rounded-full text-xs font-medium',
                  order.status === 'completed' ? 'bg-green-500/20 text-green-400' : 
                  order.status === 'preparing' ? 'bg-yellow-500/20 text-yellow-400' :
                  'bg-gray-500/20 text-gray-400'
                ]">
                  {{ 
                    order.status === 'completed' ? '✅ Ukończone' :
                    order.status === 'preparing' ? '🔄 Przygotowywane' :
                    '📦 Oczekuje'
                  }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Navigation -->
    <div class="fixed bottom-0 left-0 right-0 bg-black/20 backdrop-blur-md border-t border-white/20">
      <div class="max-w-md mx-auto px-4 py-3">
        <div class="flex justify-around">
          <button v-for="tab in tabs" :key="tab.id"
                  @click="activeTab = tab.id"
                  :class="[
                    'flex flex-col items-center py-2 px-4 rounded-lg transition-all duration-200',
                    activeTab === tab.id 
                      ? 'text-purple-400' 
                      : 'text-white/60 hover:text-white'
                  ]">
            <span class="text-xl mb-1">{{ tab.icon }}</span>
            <span class="text-xs font-medium">{{ tab.name }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Notifications Overlay -->
    <div v-if="showNotifications" 
         @click="showNotifications = false"
         class="fixed inset-0 bg-black/50 z-50 flex items-start justify-center pt-16">
      <div @click.stop class="bg-white/10 backdrop-blur-md rounded-2xl p-6 m-4 border border-white/20 max-w-md w-full">
        <h3 class="text-xl font-bold text-white mb-4">🔔 Powiadomienia</h3>
        <div class="space-y-3 max-h-96 overflow-y-auto">
          <div v-for="notification in notifications" :key="notification.id"
               @click="markAsRead(notification.id)"
               :class="[
                 'p-4 rounded-xl cursor-pointer transition-all duration-200',
                 notification.read ? 'bg-white/5' : 'bg-purple-500/20 border border-purple-400/30'
               ]">
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <div class="text-white font-medium">{{ notification.title }}</div>
                <div class="text-white/70 text-sm mt-1">{{ notification.message }}</div>
                <div class="text-white/50 text-xs mt-2">{{ notification.time }}</div>
              </div>
              <div v-if="!notification.read" class="w-3 h-3 bg-purple-400 rounded-full"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Success/Error Toast -->
    <div v-if="toast.show" 
         :class="[
           'fixed top-20 left-4 right-4 max-w-md mx-auto p-4 rounded-xl z-50 transition-all duration-300',
           toast.type === 'success' ? 'bg-green-500/90 text-white' : 'bg-red-500/90 text-white'
         ]">
      <div class="flex items-center">
        <span class="text-xl mr-2">{{ toast.type === 'success' ? '✅' : '❌' }}</span>
        <span class="font-medium">{{ toast.message }}</span>
      </div>
    </div>

    <!-- Payment Simulator -->
    <PaymentSimulator 
      v-if="showPayment" 
      :amount="paymentAmount" 
      :description="paymentDescription"
      @close="showPayment = false"
      @success="handlePaymentSuccess" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import axios from 'axios'
import QRCode from 'qrcode'
import PaymentSimulator from './PaymentSimulator.vue'

const emit = defineEmits(['back'])

// Data
const activeTab = ref('scanner')
const scanning = ref(false)
const manualQrCode = ref('')
const showNotifications = ref(false)
const selectedPayment = ref('blik')
const currentBalance = ref(127.50)
const loyaltyPoints = ref(420)
const completedOrders = ref(27)
const currentLevel = ref('🏆')
const showPayment = ref(false)
const paymentAmount = ref(0)
const paymentDescription = ref('')
const autoDeleteEnabled = ref(true)

// Tabs configuration
const tabs = [
  { id: 'scanner', name: 'Skaner', icon: '📱' },
  { id: 'my-qr', name: 'Moje QR', icon: '🎫' },
  { id: 'payment', name: 'Płatność', icon: '💳' },
  { id: 'orders', name: 'Zamówienia', icon: '📦' }
]

// Toast notification
const toast = reactive({
  show: false,
  type: 'success',
  message: ''
})

// Payment methods
const paymentMethods = [
  { id: 'blik', name: 'BLIK', icon: '📱', description: 'Szybkie płatności telefonem' },
  { id: 'card', name: 'Karta płatnicza', icon: '💳', description: 'Visa, Mastercard, PayPal' },
  { id: 'nfc', name: 'Płatność zbliżeniowa', icon: '📡', description: 'Apple Pay, Google Pay' },
  { id: 'wallet', name: 'Portfel IKIGAI', icon: '💰', description: 'Środki w aplikacji' }
]

const quickAmounts = [10, 25, 50]

// Recent scans
const recentScans = ref([
  { id: 1, location: 'IKIGAI Central', time: '2 minuty temu', status: 'success' },
  { id: 2, location: 'IKIGAI Fitness', time: '15 minut temu', status: 'success' },
  { id: 3, location: 'IKIGAI Office', time: '1 godzinę temu', status: 'error' }
])

// Transactions
const transactions = ref([
  { id: 1, description: 'Smoothie Bowl Energy', amount: -18.50, date: 'Dzisiaj 10:30' },
  { id: 2, description: 'Doładowanie BLIK', amount: 50.00, date: 'Wczoraj 15:20' },
  { id: 3, description: 'Granola Power Mix', amount: -12.00, date: 'Wczoraj 14:15' },
  { id: 4, description: 'Bonus lojalnościowy', amount: 5.00, date: '2 dni temu' }
])

// Active order
const activeOrder = ref({
  id: 'ORD_12345',
  machine: 'IKIGAI Central',
  status: 'Przygotowywane',
  progress: 75,
  timeLeft: '2:30',
  total: 18.50,
  items: ['Smoothie Bowl', 'Mix Jagód', 'Granola']
})

// Quick orders
const quickOrders = [
  { id: 1, name: 'Energy Bowl', icon: '⚡', price: 15.50 },
  { id: 2, name: 'Protein Power', icon: '💪', price: 18.00 },
  { id: 3, name: 'Green Detox', icon: '🥬', price: 16.50 },
  { id: 4, name: 'Berry Boost', icon: '🫐', price: 14.00 }
]

// Order history
const orderHistory = ref([
  { id: 1, name: 'Smoothie Bowl Energy', price: 18.50, date: 'Dzisiaj 10:30', status: 'completed' },
  { id: 2, name: 'Granola Power Mix', price: 12.00, date: 'Wczoraj 14:15', status: 'completed' },
  { id: 3, name: 'Protein Shake', price: 15.50, date: '2 dni temu', status: 'completed' }
])

// Notifications
const notifications = ref([
  { 
    id: 1, 
    title: '🎉 Zamówienie gotowe!', 
    message: 'Twój Smoothie Bowl Energy jest gotowy do odbioru w IKIGAI Central',
    time: '2 minuty temu',
    read: false
  },
  { 
    id: 2, 
    title: '💰 Bonus punktów!', 
    message: 'Otrzymałeś 25 punktów lojalnościowych za dzisiejsze zamówienie',
    time: '10 minut temu',
    read: false
  },
  { 
    id: 3, 
    title: '🔥 Promocja!', 
    message: '20% zniżki na wszystkie Protein Bowls do końca tygodnia',
    time: '1 godzinę temu',
    read: true
  }
])

// My QR Codes data
const myQrCodes = ref([
  {
    id: 1,
    name: 'Energizing Morning Bowl',
    description: 'Smoothie z mango, bananem i szpinakiem + granola',
    price: 18.50,
    status: 'active',
    code: 'IKIGAI:ORDER:EM001:2024-12-11T10:30:00Z',
    created: 'Dzisiaj 10:30',
    expiresAt: 'Dzisiaj 18:30',
    usedAt: null,
    usedLocation: null
  },
  {
    id: 2,
    name: 'Protein Power Mix',
    description: 'Shake białkowy z jagodami i orzechami',
    price: 16.00,
    status: 'used',
    code: 'IKIGAI:ORDER:PP002:2024-12-10T14:15:00Z',
    created: 'Wczoraj 14:15',
    expiresAt: 'Wczoraj 22:15',
    usedAt: 'Wczoraj 15:30',
    usedLocation: 'IKIGAI Central'
  },
  {
    id: 3,
    name: 'Green Detox Delight',
    description: 'Sok z kale, ogórka, jabłka i imbiru',
    price: 14.50,
    status: 'expired',
    code: 'IKIGAI:ORDER:GD003:2024-12-09T16:00:00Z',
    created: '2 dni temu',
    expiresAt: '2 dni temu',
    usedAt: null,
    usedLocation: null
  }
])

// Methods
const startScanning = async () => {
  scanning.value = true
  
  // Simulate scanning delay
  setTimeout(() => {
    if (manualQrCode.value) {
      processQrCode(manualQrCode.value)
    } else {
      // Simulate successful scan
      const simulatedQr = 'IKIGAI:ORDER:12345:ikigai_central:18.50'
      processQrCode(simulatedQr)
    }
    scanning.value = false
  }, 2000)
}

const processQrCode = async (qrString: string) => {
  try {
    const response = await axios.post('/api/orders/scan-qr', {
      qr_string: qrString,
      machine_id: 'ikigai_central'
    })
    
    if (response.data.success) {
      showToast('success', '✅ QR kod zeskanowany pomyślnie!')
      // Update active order
      activeOrder.value = {
        ...activeOrder.value,
        status: 'Przygotowywane',
        progress: 25
      }
      
      // Add to recent scans
      recentScans.value.unshift({
        id: Date.now(),
        location: 'IKIGAI Central',
        time: 'Teraz',
        status: 'success'
      })
      
      // Send push notification
      sendPushNotification('🎯 Skanowanie udane!', 'Zamówienie zostało przekazane do realizacji')
      
    } else {
      showToast('error', '❌ Błąd skanowania: ' + response.data.error)
    }
  } catch (error) {
    showToast('error', '❌ Błąd połączenia z serwerem')
  }
}

const addMoney = (amount: number) => {
  currentBalance.value += amount
  transactions.value.unshift({
    id: Date.now(),
    description: `Doładowanie ${selectedPayment.value.toUpperCase()}`,
    amount: amount,
    date: 'Teraz'
  })
  showToast('success', `💰 Dodano ${amount}zł do portfela`)
}

const createQuickOrder = async (order: any) => {
  try {
    if (currentBalance.value < order.price) {
      showToast('error', '❌ Niewystarczające środki')
      return
    }
    
    currentBalance.value -= order.price
    completedOrders.value += 1
    loyaltyPoints.value += Math.floor(order.price)
    
    // Add to transactions
    transactions.value.unshift({
      id: Date.now(),
      description: order.name,
      amount: -order.price,
      date: 'Teraz'
    })
    
    // Add to order history
    orderHistory.value.unshift({
      id: Date.now(),
      name: order.name,
      price: order.price,
      date: 'Teraz',
      status: 'preparing'
    })
    
    showToast('success', `🚀 Zamówienie ${order.name} złożone!`)
    sendPushNotification('📦 Nowe zamówienie!', `${order.name} zostało przekazane do realizacji`)
    
    activeTab.value = 'orders'
  } catch (error) {
    showToast('error', '❌ Błąd składania zamówienia')
  }
}

const markAsRead = (notificationId: number) => {
  const notification = notifications.value.find(n => n.id === notificationId)
  if (notification) {
    notification.read = true
  }
}

const showToast = (type: 'success' | 'error', message: string) => {
  toast.show = true
  toast.type = type
  toast.message = message
  
  setTimeout(() => {
    toast.show = false
  }, 3000)
}

const sendPushNotification = (title: string, message: string) => {
  // Simulate push notification
  setTimeout(() => {
    notifications.value.unshift({
      id: Date.now(),
      title: title,
      message: message,
      time: 'Teraz',
      read: false
    })
  }, 1000)
}

const showPaymentSimulator = (amount: number, description: string) => {
  paymentAmount.value = amount
  paymentDescription.value = description
  showPayment.value = true
}

const handlePaymentSuccess = (result: any) => {
  showPayment.value = false
  
  // Add money to balance
  currentBalance.value += result.amount
  
  // Add transaction
  transactions.value.unshift({
    id: Date.now(),
    description: paymentDescription.value,
    amount: result.amount,
    date: 'Teraz'
  })
  
  showToast('success', `💳 Płatność ${result.amount}zł zakończona pomyślnie!`)
  sendPushNotification('💰 Doładowanie udane!', `Środki ${result.amount}zł zostały dodane do portfela`)
}

// Auto-update order progress
onMounted(() => {
  setInterval(() => {
    if (activeOrder.value && activeOrder.value.progress < 100) {
      activeOrder.value.progress += 5
      
      if (activeOrder.value.progress >= 100) {
        activeOrder.value.status = 'Gotowe do odbioru'
        sendPushNotification('🎉 Zamówienie gotowe!', 'Możesz odebrać swoje zamówienie')
      }
    }
  }, 3000)
})

// QR Management Functions
const refreshQrCodes = async () => {
  try {
    // Symulacja odświeżania kodów QR z API
    showToast('success', '🔄 Kody QR zostały odświeżone')
  } catch (error) {
    showToast('error', '❌ Błąd odświeżania kodów QR')
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'active':
      return '✅ Aktywny'
    case 'used':
      return '✔️ Użyty'
    case 'expired':
      return '⏰ Wygasły'
    case 'preparing':
      return '🔄 W przygotowaniu'
    default:
      return '❓ Nieznany'
  }
}

const showQrFullscreen = (qr: any) => {
  // Tutaj można dodać modal z pełnoekranowym kodem QR
  showToast('success', `📱 Pokazuję kod QR dla: ${qr.name}`)
}

const shareQr = (qr: any) => {
  if (navigator.share) {
    navigator.share({
      title: `IKIGAI QR - ${qr.name}`,
      text: `Mój kod QR do zamówienia: ${qr.description}`,
      url: `ikigai://qr/${qr.code}`
    })
  } else {
    // Fallback - kopiowanie do schowka
    navigator.clipboard.writeText(qr.code)
    showToast('success', '📋 Kod QR skopiowany do schowka')
  }
}

const deleteQr = async (qrId: number) => {
  if (confirm('Czy na pewno chcesz usunąć ten kod QR? Ta akcja jest nieodwracalna.')) {
    try {
      // Symulacja usuwania z API
      await new Promise(resolve => setTimeout(resolve, 500))
      
      const index = myQrCodes.value.findIndex(qr => qr.id === qrId)
      if (index > -1) {
        const deletedQr = myQrCodes.value.splice(index, 1)[0]
        showToast('success', `🗑️ Kod QR "${deletedQr.name}" został usunięty`)
      }
    } catch (error) {
      showToast('error', '❌ Błąd podczas usuwania kodu QR')
    }
  }
}

const bulkDeleteExpired = async () => {
  const expiredCodes = myQrCodes.value.filter(qr => qr.status === 'expired')
  
  if (expiredCodes.length === 0) {
    showToast('info', '📋 Brak wygasłych kodów do usunięcia')
    return
  }
  
  if (confirm(`Czy chcesz usunąć ${expiredCodes.length} wygasłych kodów QR?`)) {
    try {
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      myQrCodes.value = myQrCodes.value.filter(qr => qr.status !== 'expired')
      showToast('success', `🧹 Usunięto ${expiredCodes.length} wygasłych kodów QR`)
    } catch (error) {
      showToast('error', '❌ Błąd podczas usuwania kodów QR')
    }
  }
}

const exportQrHistory = async () => {
  try {
    // Symulacja eksportu danych
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    const data = myQrCodes.value.map(qr => ({
      name: qr.name,
      price: qr.price,
      status: qr.status,
      created: qr.created,
      used: qr.usedAt || 'Nie użyty'
    }))
    
    // W rzeczywistej aplikacji tutaj byłby eksport do CSV/PDF
    console.log('Eksportowane dane:', data)
    showToast('success', '📥 Historia została wyeksportowana')
  } catch (error) {
    showToast('error', '❌ Błąd eksportu danych')
  }
}

const toggleAutoDelete = () => {
  autoDeleteEnabled.value = !autoDeleteEnabled.value
  const status = autoDeleteEnabled.value ? 'włączone' : 'wyłączone'
  showToast('success', `🔔 Auto-usuwanie ${status}`)
  
  // Zapisanie preferencji w localStorage
  localStorage.setItem('ikigai_auto_delete', autoDeleteEnabled.value.toString())
}
</script> 