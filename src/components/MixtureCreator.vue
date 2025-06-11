<template>
  <div class="max-w-6xl mx-auto p-6 space-y-8">
    
    <!-- Breadcrumb Navigation -->
    <div class="flex items-center text-sm text-gray-600 dark:text-gray-400 mb-4">
      <button @click="$emit('navigate', 'dashboard')" class="hover:text-purple-600 dark:hover:text-purple-400 transition-colors duration-200">
        🏠 Dashboard
      </button>
      <span class="mx-2">/</span>
      <span class="text-purple-600 dark:text-purple-400 font-medium">🥣 Kreator Mieszanek</span>
    </div>
    
    <!-- Header z filozofią IKIGAI -->
    <div class="bg-gradient-to-r from-purple-500 to-purple-600 rounded-xl p-8 text-white">
      <div class="flex items-center mb-4">
        <div class="w-12 h-12 mr-4 bg-white rounded-full flex items-center justify-center">
          <span class="text-purple-600 text-2xl font-bold">生</span>
        </div>
        <div>
          <h1 class="text-3xl font-bold">🥣 Kreator Mieszanek IKIGAI</h1>
          <p class="text-purple-100 mt-2">Skomponuj swoją idealną mieszankę szczęścia</p>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mt-6">
        <div class="text-center">
          <div class="text-2xl mb-2">🎯</div>
          <div class="text-sm text-purple-100">Co kochasz</div>
        </div>
        <div class="text-center">
          <div class="text-2xl mb-2">💪</div>
          <div class="text-sm text-purple-100">W czym jesteś dobry</div>
        </div>
        <div class="text-center">
          <div class="text-2xl mb-2">🌍</div>
          <div class="text-sm text-purple-100">Czego potrzebuje świat</div>
        </div>
        <div class="text-center">
          <div class="text-2xl mb-2">💰</div>
          <div class="text-sm text-purple-100">Za co możesz otrzymać wynagrodzenie</div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      
      <!-- LEWA KOLUMNA: Wybór składników -->
      <div class="lg:col-span-2 space-y-6">
        
        <!-- STEP 1: Wybierz bazę -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div class="flex items-center mb-6">
            <div class="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center mr-3">
              <span class="text-purple-600 font-bold">1</span>
            </div>
            <h2 class="text-xl font-semibold text-gray-900">🥄 Wybierz bazę</h2>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="base in bases" :key="base.id" 
                 @click="selectBase(base)"
                 :class="['cursor-pointer rounded-lg border-2 p-4 transition-all duration-200', 
                         selectedBase?.id === base.id 
                           ? 'border-purple-500 bg-purple-50' 
                           : 'border-gray-200 hover:border-purple-300 hover:bg-gray-50']">
              <div class="flex items-start">
                <div class="text-3xl mr-3">{{ base.icon }}</div>
                <div class="flex-1">
                  <h3 class="font-semibold text-gray-900">{{ base.name }}</h3>
                  <p class="text-sm text-gray-600 mt-1">{{ base.description }}</p>
                  <div class="flex items-center justify-between mt-3">
                    <span class="text-lg font-bold text-purple-600">{{ base.price.toFixed(2) }}zł</span>
                    <div class="text-xs text-gray-500">{{ base.nutrition.kcal }} kcal</div>
                  </div>
                  <div class="flex flex-wrap gap-1 mt-2">
                    <span v-for="label in base.dietary_labels.slice(0,2)" :key="label"
                          class="px-2 py-1 bg-gray-100 text-gray-600 rounded-full text-xs">
                      {{ label }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- STEP 2: Wybierz dodatki -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div class="flex items-center mb-6">
            <div class="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center mr-3">
              <span class="text-purple-600 font-bold">2</span>
            </div>
            <h2 class="text-xl font-semibold text-gray-900">🍓 Wybierz dodatki</h2>
            <span class="ml-auto text-sm text-gray-500">{{ selectedToppings.length }} wybranych</span>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="topping in toppings" :key="topping.id"
                 @click="toggleTopping(topping)"
                 :class="['cursor-pointer rounded-lg border-2 p-4 transition-all duration-200',
                         selectedToppings.some(t => t.id === topping.id)
                           ? 'border-green-500 bg-green-50'
                           : 'border-gray-200 hover:border-green-300 hover:bg-gray-50']">
              <div class="flex items-start">
                <div class="text-2xl mr-3">{{ topping.icon }}</div>
                <div class="flex-1">
                  <h3 class="font-semibold text-gray-900">{{ topping.name }}</h3>
                  <p class="text-sm text-gray-600 mt-1">{{ topping.description }}</p>
                  <div class="flex items-center justify-between mt-3">
                    <span class="text-lg font-bold text-green-600">+{{ topping.price.toFixed(2) }}zł</span>
                    <div class="text-xs text-gray-500">{{ topping.nutrition.kcal }} kcal</div>
                  </div>
                  <div class="flex flex-wrap gap-1 mt-2">
                    <span v-for="label in topping.dietary_labels.slice(0,2)" :key="label"
                          class="px-2 py-1 bg-gray-100 text-gray-600 rounded-full text-xs">
                      {{ label }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- STEP 3: Nazwa mieszanki -->
        <div v-if="selectedBase" class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div class="flex items-center mb-6">
            <div class="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center mr-3">
              <span class="text-purple-600 font-bold">3</span>
            </div>
            <h2 class="text-xl font-semibold text-gray-900">✨ Nazwij swoją mieszankę</h2>
          </div>
          
          <input v-model="mixtureName" 
                 type="text" 
                 placeholder="np. Moja Poranna Energia"
                 class="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 text-lg">
        </div>
      </div>

      <!-- PRAWA KOLUMNA: Podgląd i podsumowanie -->
      <div class="space-y-6">
        
        <!-- Podgląd mieszanki -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 sticky top-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">🥣 Twoja mieszanka</h3>
          
          <div v-if="!selectedBase" class="text-center py-8 text-gray-500">
            <div class="text-4xl mb-4">🤔</div>
            <p>Wybierz bazę, aby rozpocząć</p>
          </div>
          
          <div v-else class="space-y-4">
            <!-- Nazwa -->
            <div v-if="mixtureName" class="text-center mb-4">
              <h4 class="text-xl font-bold text-purple-600">{{ mixtureName }}</h4>
            </div>
            
            <!-- Baza -->
            <div class="flex items-center p-3 bg-purple-50 rounded-lg">
              <span class="text-2xl mr-3">{{ selectedBase.icon }}</span>
              <div class="flex-1">
                <div class="font-semibold">{{ selectedBase.name }}</div>
                <div class="text-sm text-gray-600">{{ selectedBase.price.toFixed(2) }}zł</div>
              </div>
            </div>
            
            <!-- Dodatki -->
            <div v-if="selectedToppings.length > 0">
              <div class="text-sm font-medium text-gray-700 mb-2">Dodatki:</div>
              <div v-for="topping in selectedToppings" :key="topping.id"
                   class="flex items-center p-2 bg-green-50 rounded-lg mb-2">
                <span class="text-xl mr-2">{{ topping.icon }}</span>
                <div class="flex-1">
                  <div class="text-sm font-medium">{{ topping.name }}</div>
                  <div class="text-xs text-gray-600">+{{ topping.price.toFixed(2) }}zł</div>
                </div>
              </div>
            </div>
            
            <!-- Wartości odżywcze -->
            <div class="bg-gray-50 rounded-lg p-4">
              <h4 class="font-semibold text-gray-900 mb-3">📊 Wartości odżywcze</h4>
              <div class="grid grid-cols-2 gap-3">
                <div class="text-center">
                  <div class="text-lg font-bold text-orange-600">{{ totalNutrition.kcal }}</div>
                  <div class="text-xs text-gray-600">kcal</div>
                </div>
                <div class="text-center">
                  <div class="text-lg font-bold text-blue-600">{{ totalNutrition.protein }}g</div>
                  <div class="text-xs text-gray-600">białko</div>
                </div>
                <div class="text-center">
                  <div class="text-lg font-bold text-green-600">{{ totalNutrition.carbs }}g</div>
                  <div class="text-xs text-gray-600">węglowodany</div>
                </div>
                <div class="text-center">
                  <div class="text-lg font-bold text-yellow-600">{{ totalNutrition.fat }}g</div>
                  <div class="text-xs text-gray-600">tłuszcze</div>
                </div>
              </div>
            </div>
            
            <!-- Etykiety dietetyczne -->
            <div v-if="allDietaryLabels.length > 0">
              <h4 class="font-semibold text-gray-900 mb-2">🏷️ Cechy</h4>
              <div class="flex flex-wrap gap-2">
                <span v-for="label in allDietaryLabels" :key="label"
                      class="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-xs">
                  {{ label }}
                </span>
              </div>
            </div>
            
            <!-- Cena całkowita -->
            <div class="bg-purple-100 rounded-lg p-4 text-center">
              <div class="text-2xl font-bold text-purple-600">{{ totalPrice.toFixed(2) }}zł</div>
              <div class="text-sm text-purple-700">Cena całkowita</div>
            </div>
            
            <!-- Przycisk składania zamówienia -->
            <button @click="createMixture" 
                    :disabled="!selectedBase || isCreating"
                    class="w-full bg-gradient-to-r from-purple-500 to-purple-600 text-white py-4 rounded-lg font-semibold hover:from-purple-600 hover:to-purple-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed">
              <span v-if="isCreating">⏳ Tworzę...</span>
              <span v-else>💾 Zapisz mieszankę</span>
            </button>
          </div>
        </div>
        
        <!-- Alert sukcesu -->
        <div v-if="successMessage" 
             class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded-lg">
          <div class="flex items-center">
            <span class="text-lg mr-2">✅</span>
            <span>{{ successMessage }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Moje Mieszanki -->
    <div v-if="savedMixtures.length > 0" class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h2 class="text-xl font-semibold text-gray-900 mb-6 flex items-center">
        <span class="text-2xl mr-3">💾</span>
        Moje Mieszanki
        <span class="ml-auto text-sm text-gray-500">{{ savedMixtures.length }} zapisanych</span>
      </h2>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="mixture in savedMixtures" :key="mixture.id"
             class="border border-gray-200 rounded-lg p-4 hover:border-purple-300 hover:bg-purple-50 transition-all duration-200">
          <div class="flex items-center justify-between mb-2">
            <h3 class="font-semibold text-gray-900">{{ mixture.name }}</h3>
            <span class="text-sm text-gray-500">{{ new Date(mixture.created_at).toLocaleDateString() }}</span>
          </div>
          <p class="text-sm text-gray-600 mb-3">{{ mixture.description }}</p>
          <div class="flex items-center justify-between mb-3">
            <span class="font-bold text-purple-600">{{ mixture.total_price.toFixed(2) }}zł</span>
            <div class="text-xs text-gray-500">{{ mixture.total_kcal }} kcal</div>
          </div>
          
          <!-- Status zamówienia -->
          <div class="mb-3">
            <div v-if="mixture.order_id && mixture.qr_code" class="text-center">
              <div class="text-xs text-green-600 mb-2">✅ Gotowe do zamówienia</div>
              <img :src="mixture.qr_code" alt="QR Code" class="w-20 h-20 mx-auto border rounded">
              <div class="text-xs text-gray-500 mt-1">ID: {{ mixture.order_id.slice(-8) }}</div>
            </div>
            <div v-else class="text-center">
              <div class="text-xs text-gray-500 mb-2">📋 Zapisano w drafcie</div>
            </div>
          </div>
          
          <!-- Akcje -->
          <div class="flex gap-2">
            <button @click="loadSavedMixture(mixture)" 
                    class="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 py-2 px-3 rounded text-sm font-medium transition-all duration-200">
              📝 Edytuj
            </button>
            <button v-if="!mixture.order_id" 
                    @click="createOrderFromMixture(mixture)" 
                    class="flex-1 bg-orange-100 hover:bg-orange-200 text-orange-700 py-2 px-3 rounded text-sm font-medium transition-all duration-200">
              🎯 Zamów
            </button>
            <button v-else
                    @click="showQrCode(mixture)" 
                    class="flex-1 bg-green-100 hover:bg-green-200 text-green-700 py-2 px-3 rounded text-sm font-medium transition-all duration-200">
              📱 QR
            </button>
            <button @click="deleteMixture(mixture.id)" 
                    class="bg-red-100 hover:bg-red-200 text-red-700 py-2 px-3 rounded text-sm font-medium transition-all duration-200">
              🗑️
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Top 5 Rekomendacji -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h2 class="text-xl font-semibold text-gray-900 mb-6 flex items-center">
        <span class="text-2xl mr-3">⭐</span>
        Top 5 Rekomendacji IKIGAI
      </h2>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="rec in recommendations" :key="rec.id"
             @click="loadRecommendation(rec)"
             class="cursor-pointer border border-gray-200 rounded-lg p-4 hover:border-purple-300 hover:bg-purple-50 transition-all duration-200">
          <h3 class="font-semibold text-gray-900 mb-2">{{ rec.name }}</h3>
          <p class="text-sm text-gray-600 mb-3">{{ rec.description }}</p>
          <div class="flex items-center justify-between">
            <span class="font-bold text-purple-600">{{ rec.total_price.toFixed(2) }}zł</span>
            <div class="flex items-center text-sm text-gray-500">
              <span class="mr-2">❤️ {{ rec.popularity }}%</span>
              <span>💚 {{ rec.health_score }}/100</span>
            </div>
          </div>
          <div class="flex flex-wrap gap-1 mt-2">
            <span v-for="tag in rec.tags" :key="tag"
                  class="px-2 py-1 bg-gray-100 text-gray-600 rounded-full text-xs">
              {{ tag }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- QR Code Modal -->
    <div v-if="showQrModal" 
         @click="showQrModal = false"
         class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div @click.stop class="bg-white rounded-2xl p-8 max-w-md w-full">
        <div class="text-center">
          <h3 class="text-xl font-bold text-gray-900 mb-4">📱 Kod QR do zamówienia</h3>
          <div v-if="selectedQrMixture" class="space-y-4">
            <div class="text-lg font-semibold text-purple-600">{{ selectedQrMixture.name }}</div>
            <div class="flex justify-center">
              <img :src="selectedQrMixture.qr_code" alt="QR Code" class="w-48 h-48 border-2 border-gray-200 rounded-xl">
            </div>
            <div class="text-sm text-gray-600">
              <p>🎯 Zeskanuj ten kod w automacie IKIGAI</p>
              <p>💳 Cena: {{ selectedQrMixture.total_price.toFixed(2) }}zł</p>
              <p>🆔 ID: {{ selectedQrMixture.order_id }}</p>
            </div>
            <div class="flex gap-3">
              <button @click="copyOrderId" 
                      class="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 py-2 px-4 rounded-lg transition-all duration-200">
                📋 Kopiuj ID
              </button>
              <button @click="shareQrCode" 
                      class="flex-1 bg-blue-100 hover:bg-blue-200 text-blue-700 py-2 px-4 rounded-lg transition-all duration-200">
                📤 Udostępnij
              </button>
            </div>
          </div>
          <button @click="showQrModal = false" 
                  class="mt-6 w-full bg-purple-600 hover:bg-purple-700 text-white py-3 px-6 rounded-lg font-semibold transition-all duration-200">
            ✨ Zamknij
          </button>
        </div>
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
const bases = ref([])
const toppings = ref([])
const recommendations = ref([])
const selectedBase = ref(null)
const selectedToppings = ref([])
const mixtureName = ref('')
const isCreating = ref(false)
const successMessage = ref('')
const savedMixtures = ref([])
const showQrModal = ref(false)
const selectedQrMixture = ref(null)

// Computed properties
const totalPrice = computed(() => {
  let price = selectedBase.value?.price || 0
  selectedToppings.value.forEach(topping => {
    price += topping.price
  })
  return price
})

const totalNutrition = computed(() => {
  const nutrition = { protein: 0, carbs: 0, fat: 0, kcal: 0 }
  
  if (selectedBase.value) {
    Object.keys(nutrition).forEach(key => {
      nutrition[key] += selectedBase.value.nutrition[key]
    })
  }
  
  selectedToppings.value.forEach(topping => {
    Object.keys(nutrition).forEach(key => {
      nutrition[key] += topping.nutrition[key]
    })
  })
  
  return nutrition
})

const allDietaryLabels = computed(() => {
  const labels = new Set()
  
  if (selectedBase.value) {
    selectedBase.value.dietary_labels.forEach(label => labels.add(label))
  }
  
  selectedToppings.value.forEach(topping => {
    topping.dietary_labels.forEach(label => labels.add(label))
  })
  
  return Array.from(labels).sort()
})

// Methods
const selectBase = (base) => {
  selectedBase.value = base
}

const toggleTopping = (topping) => {
  const index = selectedToppings.value.findIndex(t => t.id === topping.id)
  if (index === -1) {
    selectedToppings.value.push(topping)
  } else {
    selectedToppings.value.splice(index, 1)
  }
}

const loadRecommendation = async (rec) => {
  try {
    // Znajdź bazę
    const base = bases.value.find(b => b.id === rec.base)
    if (base) {
      selectedBase.value = base
    }
    
    // Znajdź dodatki
    selectedToppings.value = []
    rec.toppings.forEach(toppingId => {
      const topping = toppings.value.find(t => t.id === toppingId)
      if (topping) {
        selectedToppings.value.push(topping)
      }
    })
    
    // Ustaw nazwę
    mixtureName.value = rec.name
    
    // Scroll do góry
    window.scrollTo({ top: 0, behavior: 'smooth' })
    
  } catch (error) {
    console.error('Błąd ładowania rekomendacji:', error)
  }
}

const createMixture = async () => {
  if (!selectedBase.value) return
  
  isCreating.value = true
  
  try {
    // Zapisz mieszankę lokalnie
    const mixture = {
      id: Date.now().toString(),
      name: mixtureName.value || 'Moja Mieszanka',
      description: `${selectedBase.value.name} + ${selectedToppings.value.length} dodatków`,
      base: selectedBase.value,
      toppings: [...selectedToppings.value],
      total_price: totalPrice.value,
      total_kcal: totalNutrition.value.kcal,
      created_at: new Date().toISOString(),
      order_id: null,
      qr_code: null
    }
    
    // Dodaj do zapisanych mieszanek
    savedMixtures.value.unshift(mixture)
    saveMixturesToLocalStorage()
    
    successMessage.value = `Mieszanka "${mixture.name}" została zapisana! 🎉 Możesz teraz utworzyć dla niej zamówienie.`
    
    // Reset formularza po 2 sekundach
    setTimeout(() => {
      selectedBase.value = null
      selectedToppings.value = []
      mixtureName.value = ''
      successMessage.value = ''
    }, 2000)
    
  } catch (error) {
    console.error('Błąd zapisywania mieszanki:', error)
  } finally {
    isCreating.value = false
  }
}

const createOrderFromMixture = async (mixture) => {
  try {
    // Utwórz zamówienie za pomocą API
    const orderResponse = await fetch('http://localhost:5001/api/orders', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: 'web_user',
        vending_machine_id: 'ikigai_central',
        items: [
          {
            id: mixture.base.id,
            name: mixture.base.name,
            type: 'base',
            price: mixture.base.price,
            quantity: 1
          },
          ...mixture.toppings.map(topping => ({
            id: topping.id,
            name: topping.name,
            type: 'topping',
            price: topping.price,
            quantity: 1
          }))
        ]
      })
    })
    
    const orderData = await orderResponse.json()
    
    if (orderData.success) {
      // Wygeneruj QR kod dla zamówienia
      const qrResponse = await fetch(`http://localhost:5001/api/orders/${orderData.order.id}/generate-qr`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      
      const qrData = await qrResponse.json()
      
      if (qrData.success) {
        // Zaktualizuj mieszankę z QR kodem
        const mixtureIndex = savedMixtures.value.findIndex(m => m.id === mixture.id)
        if (mixtureIndex !== -1) {
          savedMixtures.value[mixtureIndex].order_id = orderData.order.id
          savedMixtures.value[mixtureIndex].qr_code = qrData.qr_code
          saveMixturesToLocalStorage()
        }
        
        successMessage.value = `Zamówienie dla "${mixture.name}" utworzone! QR kod jest gotowy do skanowania. 📱`
        setTimeout(() => successMessage.value = '', 3000)
      }
    }
    
  } catch (error) {
    console.error('Błąd tworzenia zamówienia:', error)
  }
}

const loadSavedMixture = (mixture) => {
  selectedBase.value = mixture.base
  selectedToppings.value = [...mixture.toppings]
  mixtureName.value = mixture.name
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const deleteMixture = (mixtureId) => {
  const index = savedMixtures.value.findIndex(m => m.id === mixtureId)
  if (index !== -1) {
    savedMixtures.value.splice(index, 1)
    saveMixturesToLocalStorage()
  }
}

const showQrCode = (mixture) => {
  selectedQrMixture.value = mixture
  showQrModal.value = true
}

const copyOrderId = async () => {
  if (selectedQrMixture.value?.order_id) {
    try {
      await navigator.clipboard.writeText(selectedQrMixture.value.order_id)
      successMessage.value = 'ID zamówienia skopiowane! 📋'
      setTimeout(() => successMessage.value = '', 2000)
    } catch (error) {
      console.error('Błąd kopiowania:', error)
    }
  }
}

const shareQrCode = async () => {
  if (selectedQrMixture.value && navigator.share) {
    try {
      await navigator.share({
        title: `IKIGAI - ${selectedQrMixture.value.name}`,
        text: `Sprawdź moją mieszankę IKIGAI: ${selectedQrMixture.value.name}`,
        url: window.location.href
      })
    } catch (error) {
      console.error('Błąd udostępniania:', error)
    }
  }
}

const saveMixturesToLocalStorage = () => {
  localStorage.setItem('ikigai_mixtures', JSON.stringify(savedMixtures.value))
}

const loadMixturesFromLocalStorage = () => {
  try {
    const saved = localStorage.getItem('ikigai_mixtures')
    if (saved) {
      savedMixtures.value = JSON.parse(saved)
    }
  } catch (error) {
    console.error('Błąd ładowania zapisanych mieszanek:', error)
  }
}

const loadIngredients = async () => {
  try {
    // Pobierz bazy
    const basesResponse = await fetch('http://localhost:5001/api/ingredients/bases')
    const basesData = await basesResponse.json()
    if (basesData.success) {
      bases.value = basesData.bases
    }
    
    // Pobierz dodatki
    const toppingsResponse = await fetch('http://localhost:5001/api/ingredients/toppings')
    const toppingsData = await toppingsResponse.json()
    if (toppingsData.success) {
      toppings.value = toppingsData.toppings
    }
    
    // Pobierz rekomendacje
    const recsResponse = await fetch('http://localhost:5001/api/recommendations')
    const recsData = await recsResponse.json()
    if (recsData.success) {
      recommendations.value = recsData.recommendations
    }
    
  } catch (error) {
    console.error('Błąd ładowania składników:', error)
  }
}

// Lifecycle
onMounted(() => {
  loadIngredients()
  loadMixturesFromLocalStorage()
})
</script>

<style scoped>
/* Custom animations */
.transition-all {
  transition: all 0.2s ease;
}
</style> 