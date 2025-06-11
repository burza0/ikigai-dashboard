<template>
  <div class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" @click="$emit('close')">
    <div @click.stop class="bg-white/10 backdrop-blur-md rounded-2xl p-6 m-4 border border-white/20 max-w-md w-full">
      <div class="flex items-center justify-between mb-6">
        <h3 class="text-xl font-bold text-white">💳 Symulator Płatności</h3>
        <button @click="$emit('close')" class="text-white/60 hover:text-white">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>

      <!-- Payment Method Selection -->
      <div v-if="step === 'select'" class="space-y-4">
        <div class="text-center mb-6">
          <div class="text-3xl font-bold text-white mb-2">{{ amount }}zł</div>
          <div class="text-white/70">{{ description }}</div>
        </div>

        <div class="space-y-3">
          <button @click="startPayment('blik')" 
                  class="w-full flex items-center p-4 bg-gradient-to-r from-blue-500/20 to-blue-600/20 border border-blue-400/30 rounded-xl text-white hover:bg-blue-500/30 transition-all duration-200">
            <div class="text-3xl mr-4">📱</div>
            <div class="flex-1 text-left">
              <div class="font-bold">BLIK</div>
              <div class="text-sm text-blue-200">Szybka płatność telefonem</div>
            </div>
            <div class="text-blue-400">→</div>
          </button>

          <button @click="startPayment('nfc')" 
                  class="w-full flex items-center p-4 bg-gradient-to-r from-green-500/20 to-green-600/20 border border-green-400/30 rounded-xl text-white hover:bg-green-500/30 transition-all duration-200">
            <div class="text-3xl mr-4">📡</div>
            <div class="flex-1 text-left">
              <div class="font-bold">Płatność zbliżeniowa</div>
              <div class="text-sm text-green-200">Apple Pay, Google Pay, NFC</div>
            </div>
            <div class="text-green-400">→</div>
          </button>

          <button @click="startPayment('card')" 
                  class="w-full flex items-center p-4 bg-gradient-to-r from-purple-500/20 to-purple-600/20 border border-purple-400/30 rounded-xl text-white hover:bg-purple-500/30 transition-all duration-200">
            <div class="text-3xl mr-4">💳</div>
            <div class="flex-1 text-left">
              <div class="font-bold">Karta płatnicza</div>
              <div class="text-sm text-purple-200">Visa, Mastercard</div>
            </div>
            <div class="text-purple-400">→</div>
          </button>
        </div>
      </div>

      <!-- BLIK Payment -->
      <div v-else-if="step === 'blik'" class="space-y-6">
        <div class="text-center">
          <div class="text-6xl mb-4">📱</div>
          <h4 class="text-lg font-bold text-white mb-2">Płatność BLIK</h4>
          <div class="text-white/70 mb-4">Wpisz 6-cyfrowy kod BLIK z aplikacji bankowej</div>
        </div>

        <div class="relative">
          <input v-model="blikCode" 
                 @input="handleBlikInput"
                 maxlength="6" 
                 placeholder="000000"
                 class="w-full text-center text-3xl font-mono bg-white/10 border border-white/30 rounded-xl py-4 px-6 text-white placeholder-white/40 focus:border-blue-400 focus:outline-none tracking-wider">
          <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
            <div class="flex space-x-2">
              <div v-for="i in 6" :key="i" 
                   :class="[
                     'w-8 h-1 rounded-full',
                     blikCode.length >= i ? 'bg-blue-400' : 'bg-white/20'
                   ]"></div>
            </div>
          </div>
        </div>

        <div v-if="blikCode.length === 6" class="text-center">
          <button @click="processBlik" 
                  class="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-bold py-3 px-8 rounded-xl transition-all duration-200">
            💳 Zapłać {{ amount }}zł
          </button>
        </div>
      </div>

      <!-- NFC Payment -->
      <div v-else-if="step === 'nfc'" class="space-y-6">
        <div class="text-center">
          <div class="text-6xl mb-4 animate-pulse">📡</div>
          <h4 class="text-lg font-bold text-white mb-2">Płatność zbliżeniowa</h4>
          <div class="text-white/70 mb-4">Przyłóż telefon lub kartę do czytnika</div>
        </div>

        <div class="relative bg-gradient-to-br from-green-500/20 to-green-600/20 rounded-xl p-8 border border-green-400/30">
          <div class="absolute inset-0 bg-green-400/20 rounded-xl animate-ping"></div>
          <div class="relative text-center">
            <div class="text-4xl mb-4">📱 ↔️ 📡</div>
            <div class="text-white font-medium">Wykrywanie urządzenia...</div>
            <div class="text-green-400 text-sm mt-2">{{ nfcStatus }}</div>
          </div>
        </div>

        <div class="text-center">
          <button @click="simulateNfcTap" 
                  class="bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-bold py-3 px-8 rounded-xl transition-all duration-200">
            📡 Symuluj dotknięcie
          </button>
        </div>
      </div>

      <!-- Card Payment -->
      <div v-else-if="step === 'card'" class="space-y-6">
        <div class="text-center">
          <div class="text-6xl mb-4">💳</div>
          <h4 class="text-lg font-bold text-white mb-2">Płatność kartą</h4>
          <div class="text-white/70 mb-4">Wprowadź dane karty płatniczej</div>
        </div>

        <div class="space-y-4">
          <div>
            <label class="block text-white/70 text-sm mb-2">Numer karty</label>
            <input v-model="cardNumber" 
                   @input="formatCardNumber"
                   placeholder="1234 5678 9012 3456"
                   maxlength="19"
                   class="w-full bg-white/10 border border-white/30 rounded-xl py-3 px-4 text-white placeholder-white/40 focus:border-purple-400 focus:outline-none font-mono">
          </div>
          
          <div class="flex space-x-4">
            <div class="flex-1">
              <label class="block text-white/70 text-sm mb-2">Data ważności</label>
              <input v-model="cardExpiry" 
                     @input="formatExpiry"
                     placeholder="MM/YY"
                     maxlength="5"
                     class="w-full bg-white/10 border border-white/30 rounded-xl py-3 px-4 text-white placeholder-white/40 focus:border-purple-400 focus:outline-none font-mono">
            </div>
            <div class="flex-1">
              <label class="block text-white/70 text-sm mb-2">CVV</label>
              <input v-model="cardCvv" 
                     placeholder="123"
                     maxlength="3"
                     class="w-full bg-white/10 border border-white/30 rounded-xl py-3 px-4 text-white placeholder-white/40 focus:border-purple-400 focus:outline-none font-mono">
            </div>
          </div>
        </div>

        <div v-if="isCardValid" class="text-center">
          <button @click="processCard" 
                  class="bg-gradient-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700 text-white font-bold py-3 px-8 rounded-xl transition-all duration-200">
            💳 Zapłać {{ amount }}zł
          </button>
        </div>
      </div>

      <!-- Processing -->
      <div v-else-if="step === 'processing'" class="space-y-6">
        <div class="text-center">
          <div class="text-6xl mb-4 animate-spin">⚡</div>
          <h4 class="text-lg font-bold text-white mb-2">Przetwarzanie płatności</h4>
          <div class="text-white/70 mb-4">{{ processingMessage }}</div>
        </div>

        <div class="w-full bg-white/10 rounded-full h-2">
          <div class="bg-gradient-to-r from-yellow-400 to-orange-500 h-2 rounded-full transition-all duration-300" 
               :style="{ width: progress + '%' }"></div>
        </div>

        <div class="text-center text-white/60 text-sm">
          {{ Math.round(progress) }}% ukończone
        </div>
      </div>

      <!-- Success -->
      <div v-else-if="step === 'success'" class="space-y-6">
        <div class="text-center">
          <div class="text-6xl mb-4 animate-bounce">✅</div>
          <h4 class="text-xl font-bold text-green-400 mb-2">Płatność zakończona!</h4>
          <div class="text-white/70 mb-4">Transakcja przebiegła pomyślnie</div>
        </div>

        <div class="bg-green-500/20 border border-green-400/30 rounded-xl p-4">
          <div class="flex justify-between text-white mb-2">
            <span>Kwota:</span>
            <span class="font-bold">{{ amount }}zł</span>
          </div>
          <div class="flex justify-between text-white mb-2">
            <span>Metoda:</span>
            <span class="font-bold">{{ paymentMethodName }}</span>
          </div>
          <div class="flex justify-between text-white">
            <span>ID transakcji:</span>
            <span class="font-mono text-sm">{{ transactionId }}</span>
          </div>
        </div>

        <div class="text-center">
          <button @click="$emit('success', { amount, method: currentMethod, transactionId })" 
                  class="bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-bold py-3 px-8 rounded-xl transition-all duration-200">
            ✨ Ukończ
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

interface Props {
  amount: number
  description: string
}

const props = defineProps<Props>()
const emit = defineEmits(['close', 'success'])

// State
const step = ref('select')
const currentMethod = ref('')
const blikCode = ref('')
const cardNumber = ref('')
const cardExpiry = ref('')
const cardCvv = ref('')
const nfcStatus = ref('Przygotowywanie...')
const progress = ref(0)
const processingMessage = ref('')
const transactionId = ref('')

// Computed
const isCardValid = computed(() => {
  return cardNumber.value.replace(/\s/g, '').length === 16 &&
         cardExpiry.value.length === 5 &&
         cardCvv.value.length === 3
})

const paymentMethodName = computed(() => {
  const names: { [key: string]: string } = {
    'blik': 'BLIK',
    'nfc': 'Płatność zbliżeniowa',
    'card': 'Karta płatnicza'
  }
  return names[currentMethod.value] || ''
})

// Methods
const startPayment = (method: string) => {
  currentMethod.value = method
  step.value = method
  
  if (method === 'nfc') {
    simulateNfcDetection()
  }
}

const handleBlikInput = (event: any) => {
  const value = event.target.value.replace(/\D/g, '')
  blikCode.value = value
}

const formatCardNumber = (event: any) => {
  let value = event.target.value.replace(/\s/g, '').replace(/\D/g, '')
  value = value.replace(/(.{4})/g, '$1 ').trim()
  cardNumber.value = value
}

const formatExpiry = (event: any) => {
  let value = event.target.value.replace(/\D/g, '')
  if (value.length >= 2) {
    value = value.substring(0, 2) + '/' + value.substring(2, 4)
  }
  cardExpiry.value = value
}

const processBlik = () => {
  step.value = 'processing'
  processingMessage.value = 'Autoryzacja w banku...'
  simulateProcessing()
}

const simulateNfcTap = () => {
  step.value = 'processing'
  processingMessage.value = 'Komunikacja NFC...'
  simulateProcessing()
}

const processCard = () => {
  step.value = 'processing'
  processingMessage.value = 'Weryfikacja karty...'
  simulateProcessing()
}

const simulateNfcDetection = () => {
  const statuses = [
    'Przygotowywanie...',
    'Skanowanie urządzeń...',
    'Gotowy do płatności'
  ]
  
  let index = 0
  const interval = setInterval(() => {
    nfcStatus.value = statuses[index]
    index++
    if (index >= statuses.length) {
      clearInterval(interval)
    }
  }, 1000)
}

const simulateProcessing = () => {
  const messages = [
    'Łączenie z bankiem...',
    'Weryfikacja tożsamości...',
    'Autoryzacja płatności...',
    'Finalizacja transakcji...'
  ]
  
  let messageIndex = 0
  progress.value = 0
  
  const interval = setInterval(() => {
    progress.value += 25
    
    if (messageIndex < messages.length) {
      processingMessage.value = messages[messageIndex]
      messageIndex++
    }
    
    if (progress.value >= 100) {
      clearInterval(interval)
      transactionId.value = 'TXN_' + Math.random().toString(36).substr(2, 9).toUpperCase()
      step.value = 'success'
    }
  }, 800)
}

onMounted(() => {
  // Auto-close after 2 minutes
  setTimeout(() => {
    if (step.value !== 'success') {
      emit('close')
    }
  }, 120000)
})
</script> 