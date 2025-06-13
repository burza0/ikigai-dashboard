<template>
  <div class="max-w-6xl mx-auto p-6 space-y-8">
    
    <!-- Breadcrumb Navigation -->
    <div class="flex items-center text-sm text-gray-600 dark:text-gray-400 mb-4">
      <button @click="$emit('navigate', 'dashboard')" class="hover:text-purple-600 dark:hover:text-purple-400 transition-colors duration-200">
        🏠 Dashboard
      </button>
      <span class="mx-2">/</span>
      <span class="text-purple-600 dark:text-purple-400 font-medium">🥣 Kreator Bowl</span>
    </div>
    
    <!-- Header z filozofią IKIGAI -->
    <div class="bg-gradient-to-r from-purple-500 to-purple-600 rounded-xl p-8 text-white">
      <div class="flex items-center mb-4">
        <div class="w-12 h-12 mr-4 bg-white rounded-full flex items-center justify-center">
          <span class="text-purple-600 text-2xl font-bold">生</span>
        </div>
        <div>
          <h1 class="text-3xl font-bold">🥣 Kreator Bowl IKIGAI</h1>
          <p class="text-purple-100 mt-2">Skomponuj swój idealny bowl szczęścia</p>
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
                    <span class="text-lg font-bold text-purple-600">{{ formatPrice(base.price) }}zł</span>
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
                    <span class="text-lg font-bold text-green-600">+{{ formatPrice(topping.price) }}zł</span>
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

        <!-- STEP 3: Nazwa bowl -->
        <div v-if="currentStep === 3" class="space-y-8">
          <div class="text-center mb-8">
            <div class="text-6xl mb-4">✨</div>
            <h2 class="text-xl font-semibold text-gray-900">✨ Nazwij swój bowl</h2>
            <p class="text-base text-gray-600 mt-2">Nadaj unikalną nazwę swojej kreacji</p>
          </div>

          <!-- Podgląd bowl -->
          <div class="bg-gradient-to-br from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 rounded-xl p-6 border border-purple-200 dark:border-purple-700">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">🥣 Twój bowl</h3>
            
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
                  <div class="text-sm text-gray-600">{{ formatPrice(selectedBase.price) }}zł</div>
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
                    <div class="text-xs text-gray-600">+{{ formatPrice(topping.price) }}zł</div>
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
                <div class="text-2xl font-bold text-purple-600">{{ formatPrice(totalPrice) }}zł</div>
                <div class="text-sm text-purple-700">Cena całkowita</div>
              </div>
              
              <!-- Przycisk składania zamówienia -->
              <button @click="createMixture" 
                      :disabled="!selectedBase || isCreating"
                      class="w-full bg-gradient-to-r from-purple-500 to-purple-600 text-white py-4 rounded-lg font-semibold hover:from-purple-600 hover:to-purple-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed">
                <span v-if="isCreating">⏳ Tworzę...</span>
                <span v-else>💾 Zapisz bowl</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- PRAWA KOLUMNA: Podgląd i podsumowanie -->
      <div class="space-y-6">
        
        <!-- Podgląd bowl -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 sticky top-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">🥣 Twoj bowl</h3>
          
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
                <div class="text-sm text-gray-600">{{ formatPrice(selectedBase.price) }}zł</div>
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
                  <div class="text-xs text-gray-600">+{{ formatPrice(topping.price) }}zł</div>
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
              <div class="text-2xl font-bold text-purple-600">{{ formatPrice(totalPrice) }}zł</div>
              <div class="text-sm text-purple-700">Cena całkowita</div>
            </div>
            
            <!-- Przycisk składania zamówienia -->
            <button @click="createMixture" 
                    :disabled="!selectedBase || isCreating"
                    class="w-full bg-gradient-to-r from-purple-500 to-purple-600 text-white py-4 rounded-lg font-semibold hover:from-purple-600 hover:to-purple-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed">
              <span v-if="isCreating">⏳ Tworzę...</span>
              <span v-else>💾 Zapisz bowl</span>
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

    <!-- Moje Bowls -->
    <div v-if="savedMixtures.length > 0" class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h2 class="text-xl font-semibold text-gray-900 mb-6 flex items-center">
        <span class="text-2xl mr-3">💾</span>
        Moje Bowls
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
            <span class="font-bold text-purple-600">{{ formatPrice(mixture.total_price) }}zł</span>
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
                    :disabled="isCreatingOrder"
                    :class="[
                      'flex-1 py-2 px-3 rounded text-sm font-medium transition-all duration-200',
                      isCreatingOrder 
                        ? 'bg-gray-100 text-gray-500 cursor-not-allowed' 
                        : 'bg-orange-100 hover:bg-orange-200 text-orange-700'
                    ]">
              <span v-if="isCreatingOrder">⏳ Tworzę...</span>
              <span v-else>🎯 Zamów</span>
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

    <!-- Top 5 Bowl -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
        <span class="text-2xl mr-3">⭐</span>
        Top 5 Bowl IKIGAI
      </h3>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="rec in recommendations" :key="rec.id"
             @click="loadRecommendation(rec)"
             class="cursor-pointer border border-gray-200 rounded-lg p-4 hover:border-purple-300 hover:bg-purple-50 transition-all duration-200">
          <h3 class="font-semibold text-gray-900 mb-2">{{ rec.name }}</h3>
          <p class="text-sm text-gray-600 mb-3">{{ rec.description }}</p>
          <div class="flex items-center justify-between">
            <span class="font-bold text-purple-600">{{ formatPrice(rec.total_price) }}zł</span>
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
              <p>💳 Cena: {{ formatPrice(selectedQrMixture.total_price) }}zł</p>
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

// Helper function for safe price formatting
const formatPrice = (price: any): string => {
  const numPrice = parseFloat(price) || 0
  return numPrice.toFixed(2)
}

// Reactive data
const bases = ref([])
const toppings = ref([])
const recommendations = ref([])
const selectedBase = ref(null)
const selectedToppings = ref([])
const mixtureName = ref('')
const isCreating = ref(false)
const isCreatingOrder = ref(false)
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
    // Generuj unikalne ID
    const uniqueId = `mixture_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    
    // Zapisz bowl lokalnie
    const mixture = {
      id: uniqueId,
      name: mixtureName.value || 'Moj Bowl',
      description: `${selectedBase.value.name} + ${selectedToppings.value.length} dodatków`,
      base: { ...selectedBase.value }, // Skopiuj obiekt żeby uniknąć referencji
      toppings: selectedToppings.value.map(t => ({ ...t })), // Skopiuj tablicę obiektów
      total_price: totalPrice.value,
      total_kcal: totalNutrition.value.kcal,
      created_at: new Date().toISOString(),
      order_id: null,
      qr_code: null
    }
    
    console.log('Zapisuję nowy bowl:', mixture.name, 'ID:', mixture.id)
    
    // Stwórz kopię aktualnych bowls i dodaj nowy na początku
    const updatedMixtures = [mixture, ...savedMixtures.value]
    savedMixtures.value = updatedMixtures
    saveMixturesToLocalStorage()
    
    successMessage.value = `Bowl "${mixture.name}" został zapisany! 🎉 Możesz teraz utworzyć dla niego zamówienie.`
    
    // Reset formularza po 2 sekundach
    setTimeout(() => {
      selectedBase.value = null
      selectedToppings.value = []
      mixtureName.value = ''
      successMessage.value = ''
    }, 2000)
    
  } catch (error) {
    console.error('Błąd zapisywania bowl:', error)
    successMessage.value = 'Błąd podczas zapisywania bowl. Spróbuj ponownie.'
    setTimeout(() => successMessage.value = '', 3000)
  } finally {
    isCreating.value = false
  }
}

const createOrderFromMixture = async (mixture) => {
  // Zabezpieczenie przed wielokrotnym kliknięciem
  if (isCreatingOrder.value) {
    console.log('Zamówienie już w trakcie tworzenia...')
    return
  }

  isCreatingOrder.value = true
  
  try {
    console.log('🎯 Rozpoczynam tworzenie zamówienia dla bowl:', mixture.name)
    console.log('📦 Składniki:', {
      base: mixture.base.name,
      toppings: mixture.toppings.map(t => t.name),
      total_price: mixture.total_price
    })
    
    successMessage.value = `⏳ Tworzę zamówienie dla "${mixture.name}"...`
    
    // Utwórz zamówienie za pomocą API
    const orderPayload = {
      mixture_name: mixture.name,
      user_id: 'web_user',
      vending_machine_id: 'vm001',
      items: [
        {
          id: mixture.base.id,
          type: 'base',
          quantity: 1
        },
        ...mixture.toppings.map(topping => ({
          id: topping.id,
          type: 'topping',
          quantity: 1
        }))
      ],
      total_price: mixture.total_price,
      quick_order: true
    }
    
    console.log('📤 Wysyłam dane zamówienia:', orderPayload)
    
    const orderResponse = await fetch('http://localhost:5001/api/orders', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(orderPayload)
    })
    
    if (!orderResponse.ok) {
      throw new Error(`HTTP ${orderResponse.status}: ${orderResponse.statusText}`)
    }
    
    const orderData = await orderResponse.json()
    console.log('📥 Odpowiedź API zamówienia:', orderData)
    
    if (orderData.success) {
      successMessage.value = `⚡ Generuję QR kod dla "${mixture.name}"...`
      
      // Wygeneruj QR kod dla zamówienia
      const qrResponse = await fetch(`http://localhost:5001/api/orders/${orderData.order.id}/generate-qr`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      
      if (!qrResponse.ok) {
        throw new Error(`HTTP QR ${qrResponse.status}: ${qrResponse.statusText}`)
      }
      
      const qrData = await qrResponse.json()
      console.log('📥 Odpowiedź API QR:', qrData.success ? 'Sukces!' : qrData.error)
      
      if (qrData.success) {
        // Stwórz kopię aktualnych bowls
        const updatedMixtures = [...savedMixtures.value]
        
        // Znajdź i zaktualizuj konkretny bowl
        const mixtureIndex = updatedMixtures.findIndex(m => m.id === mixture.id)
        if (mixtureIndex !== -1) {
          updatedMixtures[mixtureIndex] = {
            ...updatedMixtures[mixtureIndex],
            order_id: orderData.order.id,
            qr_code: qrData.qr_code
          }
          
          // Zaktualizuj stan i zapisz do localStorage
          savedMixtures.value = updatedMixtures
          saveMixturesToLocalStorage()
          
          console.log('✅ Bowl zaktualizowany z QR kodem:', orderData.order.id.slice(-8))
        }
        
        successMessage.value = `🎉 Zamówienie dla "${mixture.name}" utworzone! QR kod jest gotowy do skanowania. 📱`
        setTimeout(() => successMessage.value = '', 5000)
      } else {
        console.error('❌ Błąd generowania QR kodu:', qrData.error)
        successMessage.value = `❌ Błąd generowania QR kodu: ${qrData.error || 'Nieznany błąd'}`
        setTimeout(() => successMessage.value = '', 5000)
      }
    } else {
      console.error('❌ Błąd tworzenia zamówienia:', orderData.error)
      successMessage.value = `❌ Błąd tworzenia zamówienia: ${orderData.error || 'Nieznany błąd'}`
      setTimeout(() => successMessage.value = '', 5000)
    }
    
  } catch (error) {
    console.error('❌ Błąd tworzenia zamówienia:', error)
    
    if (error.message.includes('Failed to fetch')) {
      successMessage.value = '❌ Błąd połączenia z serwerem. Sprawdź czy backend działa na porcie 5001.'
    } else {
      successMessage.value = `❌ Błąd: ${error.message}`
    }
    
    setTimeout(() => successMessage.value = '', 5000)
  } finally {
    isCreatingOrder.value = false
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
        text: `Sprawdź mój bowl IKIGAI: ${selectedQrMixture.value.name}`,
        url: window.location.href
      })
    } catch (error) {
      console.error('Błąd udostępniania:', error)
    }
  }
}

const saveMixturesToLocalStorage = () => {
  try {
    console.log('Zapisuję bowls do localStorage:', savedMixtures.value.length)
    const mixturesData = savedMixtures.value.map(mixture => ({
      ...mixture,
      // Upewnij się, że wszystkie ważne pola są zachowane
      id: mixture.id,
      name: mixture.name,
      order_id: mixture.order_id || null,
      qr_code: mixture.qr_code || null,
      created_at: mixture.created_at
    }))
    localStorage.setItem('ikigai_mixtures', JSON.stringify(mixturesData))
    console.log('Bowls zapisane pomyślnie')
  } catch (error) {
    console.error('Błąd zapisywania bowls do localStorage:', error)
  }
}

const loadMixturesFromLocalStorage = () => {
  try {
    const saved = localStorage.getItem('ikigai_mixtures')
    if (saved) {
      const parsedMixtures = JSON.parse(saved)
      console.log('Ładuję bowls z localStorage:', parsedMixtures.length)
      
      // Sprawdź czy każdy bowl ma wszystkie wymagane pola
      savedMixtures.value = parsedMixtures.map(mixture => ({
        ...mixture,
        // Upewnij się, że ID istnieje
        id: mixture.id || Date.now().toString() + Math.random(),
        // Zachowaj kody QR i order_id jeśli istnieją
        order_id: mixture.order_id || null,
        qr_code: mixture.qr_code || null
      }))
      
      console.log('Bowls załadowane:', savedMixtures.value.map(m => ({ 
        name: m.name, 
        hasQR: !!m.qr_code, 
        orderId: m.order_id?.slice(-8) 
      })))
    }
  } catch (error) {
    console.error('Błąd ładowania zapisanych bowls:', error)
    savedMixtures.value = []
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

// Debug functions
const debugMixtures = () => {
  console.log('=== DEBUG BOWLS ===')
  console.log('Liczba bowls:', savedMixtures.value.length)
  savedMixtures.value.forEach((mixture, index) => {
    console.log(`${index + 1}. ${mixture.name}:`, {
      id: mixture.id,
      hasOrderId: !!mixture.order_id,
      hasQRCode: !!mixture.qr_code,
      orderId: mixture.order_id?.slice(-8),
      created: mixture.created_at
    })
  })
  console.log('localStorage content:', localStorage.getItem('ikigai_mixtures'))
}

const clearAllMixtures = () => {
  if (confirm('Czy na pewno chcesz usunąć wszystkie zapisane bowls?')) {
    savedMixtures.value = []
    localStorage.removeItem('ikigai_mixtures')
    console.log('Wszystkie bowls zostały usunięte')
  }
}

// Expose debug functions globally (tylko do debugowania)
if (typeof window !== 'undefined') {
  window.debugMixtures = debugMixtures
  window.clearAllMixtures = clearAllMixtures
  window.testOrderCreation = (mixtureIndex = 0) => {
    if (savedMixtures.value[mixtureIndex]) {
      console.log('🧪 Test tworzenia zamówienia dla:', savedMixtures.value[mixtureIndex].name)
      createOrderFromMixture(savedMixtures.value[mixtureIndex])
    } else {
      console.log('❌ Brak bowl o indeksie', mixtureIndex)
    }
  }
}

// Lifecycle
onMounted(() => {
  loadIngredients()
  loadMixturesFromLocalStorage()
  
  // Debug info przy załadowaniu
  setTimeout(() => {
    console.log('=== STAN PO ZAŁADOWANIU ===')
    debugMixtures()
  }, 1000)
})
</script>

<style scoped>
/* Custom animations */
.transition-all {
  transition: all 0.2s ease;
}
</style> 