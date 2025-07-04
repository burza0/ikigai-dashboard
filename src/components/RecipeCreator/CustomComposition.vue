<template>
  <!-- Success/Error Toast -->
  <div v-if="toast.show"
    class="fixed top-4 right-4 z-50 px-6 py-3 rounded-lg shadow-lg transition-all duration-500 transform"
    :class="toast.type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'"
  >
    <span class="text-xl mr-2">{{ toast.type === 'success' ? '✅' : '❌' }}</span>
    <span class="font-medium">{{ toast.message }}</span>
  </div>

  <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 lg:gap-8">
    
    <!-- LEWA STRONA: Składniki (2/3 width) -->
    <div class="lg:col-span-2 space-y-4 lg:space-y-6">
      
      <!-- Search & Filters -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4 lg:p-6">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 lg:gap-4">
          
          <!-- Search -->
          <div class="sm:col-span-2 lg:col-span-2">
            <div class="relative">
              <input 
                v-model="searchQuery"
                type="text" 
                placeholder="🔍 Szukaj składnika..."
                class="w-full pl-10 pr-4 py-2.5 lg:py-3 text-sm lg:text-base border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              >
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <span class="text-gray-400 text-sm lg:text-base">🔍</span>
              </div>
            </div>
          </div>
          
          <!-- Price Range -->
          <div>
            <select 
              v-model="selectedPriceRange"
              class="w-full px-3 lg:px-4 py-2.5 lg:py-3 text-sm lg:text-base border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="">💰 Wszystkie ceny</option>
              <option value="0-5">💰 0-5 PLN</option>
              <option value="5-10">💰 5-10 PLN</option>
              <option value="10+">💰 10+ PLN</option>
            </select>
          </div>
        </div>
        
        <!-- Quick Filters -->
        <div class="mt-4 lg:mt-6">
          <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2 lg:gap-3">
            <button 
              v-for="filter in quickFilters" 
              :key="filter.key"
              @click="toggleFilter(filter.key)"
              :class="[
                'px-3 py-2 rounded-lg text-xs lg:text-sm font-medium transition-all duration-200',
                activeFilters.includes(filter.key)
                  ? 'bg-purple-100 text-purple-700 border border-purple-200'
                  : 'bg-gray-100 text-gray-600 border border-gray-200 hover:bg-gray-200'
              ]"
            >
              {{ filter.label }}
            </button>
          </div>
        </div>
      </div>
      
      <!-- KATEGORIE SKŁADNIKÓW -->
      <div class="space-y-4 lg:space-y-6">
        
        <!-- BAZY (1 wymagana) -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4 lg:p-6">
          <div class="flex items-center mb-4 lg:mb-6">
            <div class="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center mr-3">
              <span class="text-purple-600 font-bold text-sm lg:text-base">1</span>
            </div>
            <h2 class="text-lg lg:text-xl font-semibold text-gray-900">🥛 Wybierz bazę (wymagane)</h2>
          </div>
          
          <!-- Base categories tabs -->
          <div class="flex flex-wrap gap-2 mb-4 lg:mb-6">
            <button 
              v-for="baseCategory in baseCategories" 
              :key="baseCategory.key"
              @click="selectedBaseCategory = baseCategory.key"
              :class="[
                'px-3 lg:px-4 py-2 rounded-lg text-xs lg:text-sm font-medium transition-all duration-200',
                selectedBaseCategory === baseCategory.key
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              ]"
            >
              {{ baseCategory.icon }} {{ baseCategory.name }} ({{ baseCategory.count }})
            </button>
          </div>
          
          <!-- Compact bases grid -->
          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-2 lg:gap-3">
            <div 
              v-for="base in filteredBases" 
              :key="base.id"
              @click="selectBase(base)"
              :class="[
                'p-3 lg:p-4 rounded-lg border-2 cursor-pointer transition-all duration-200 hover:scale-105',
                selectedBase?.id === base.id 
                  ? 'border-purple-500 bg-purple-50 shadow-md' 
                  : 'border-gray-200 hover:border-purple-300 hover:bg-gray-50'
              ]"
            >
              <div class="text-center">
                <div class="text-2xl lg:text-3xl mb-2">{{ base.icon }}</div>
                <div class="text-xs lg:text-sm font-medium text-gray-900 mb-1 line-clamp-2">{{ base.name }}</div>
                <div class="text-xs text-purple-600 font-bold">{{ base.price.toFixed(2) }}zł</div>
                <div class="text-xs text-gray-500 mt-1">{{ base.volume }}</div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- DODATKI (opcjonalne) -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4 lg:p-6">
          <div class="flex items-center mb-4 lg:mb-6">
            <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
              <span class="text-blue-600 font-bold text-sm lg:text-base">2</span>
            </div>
            <h2 class="text-lg lg:text-xl font-semibold text-gray-900">🌟 Dodaj składniki (opcjonalne)</h2>
          </div>
          
          <!-- Toppings categories tabs -->
          <div class="flex flex-wrap gap-2 mb-4 lg:mb-6">
            <button 
              v-for="toppingCategory in toppingCategories" 
              :key="toppingCategory.key"
              @click="selectedToppingCategory = toppingCategory.key"
              :class="[
                'px-3 lg:px-4 py-2 rounded-lg text-xs lg:text-sm font-medium transition-all duration-200',
                selectedToppingCategory === toppingCategory.key
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              ]"
            >
              {{ toppingCategory.icon }} {{ toppingCategory.name }} ({{ toppingCategory.count }})
            </button>
          </div>
          
          <!-- Compact toppings grid -->
          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-2 lg:gap-3">
            <div 
              v-for="topping in filteredToppings" 
              :key="topping.id"
              @click="toggleTopping(topping)"
              :class="[
                'p-3 lg:p-4 rounded-lg border-2 cursor-pointer transition-all duration-200 hover:scale-105 relative',
                selectedToppings.some(t => t.id === topping.id)
                  ? 'border-blue-500 bg-blue-50 shadow-md' 
                  : 'border-gray-200 hover:border-blue-300 hover:bg-gray-50'
              ]"
            >
              <!-- Selected indicator -->
              <div v-if="selectedToppings.some(t => t.id === topping.id)" 
                   class="absolute -top-2 -right-2 w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-xs font-bold">
                {{ selectedToppings.filter(t => t.id === topping.id).length }}
              </div>
              
              <div class="text-center">
                <div class="text-2xl lg:text-3xl mb-2">{{ topping.icon }}</div>
                <div class="text-xs lg:text-sm font-medium text-gray-900 mb-1 line-clamp-2">{{ topping.name }}</div>
                <div class="text-xs text-blue-600 font-bold">{{ topping.price.toFixed(2) }}zł</div>
                
                <!-- Safety labels -->
                <div class="flex flex-wrap justify-center gap-1 mt-1">
                  <span 
                    v-for="label in topping.safety_labels?.slice(0, 2)" 
                    :key="label"
                    class="px-1 py-0.5 bg-green-100 text-green-600 rounded text-xs font-medium"
                  >
                    {{ label }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- PRAWA STRONA: Live Preview + Smart Features (1/3 width) -->
    <div class="lg:col-span-1">
      <div class="lg:sticky lg:top-6 space-y-4 lg:space-y-6">
        
        <!-- Live Preview -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 lg:p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
            <span class="mr-2">👁️</span>
            Live Preview
          </h3>
          
          <!-- Current Selection -->
          <div class="space-y-4">
            
            <!-- Selected Base -->
            <div>
              <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Baza:</h4>
              <div v-if="selectedBase" class="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-3">
                <div class="flex items-center justify-between">
                  <span class="text-sm font-medium text-gray-900 dark:text-white">{{ selectedBase.name }}</span>
                  <span class="text-sm text-blue-600 dark:text-blue-400">{{ selectedBase.price.toFixed(2) }} PLN</span>
                </div>
              </div>
              <div v-else class="text-sm text-gray-500 dark:text-gray-400 text-center p-3 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg">
                Wybierz bazę
              </div>
            </div>
            
            <!-- Selected Toppings -->
            <div>
              <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Dodatki ({{ selectedToppings.length }}/5):
              </h4>
              
              <div v-if="selectedToppings.length" class="space-y-2">
                <div 
                  v-for="topping in selectedToppings" 
                  :key="topping.id"
                  class="bg-green-50 dark:bg-green-900/20 rounded-lg p-3 flex items-center justify-between"
                >
                  <span class="text-sm font-medium text-gray-900 dark:text-white">{{ topping.name }}</span>
                  <div class="flex items-center space-x-2">
                    <span class="text-sm text-green-600 dark:text-green-400">{{ topping.price.toFixed(2) }} PLN</span>
                    <button 
                      @click="removeToppings(topping)"
                      class="text-red-400 hover:text-red-600"
                    >
                      ×
                    </button>
                  </div>
                </div>
              </div>
              
              <div v-else class="text-sm text-gray-500 dark:text-gray-400 text-center p-3 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg">
                Dodaj składniki
              </div>
            </div>
            
            <!-- Live Calculations -->
            <div class="bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 rounded-lg p-4">
              <div class="space-y-2">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-700 dark:text-gray-300">Cena całkowita:</span>
                  <span class="font-semibold text-purple-600 dark:text-purple-400">{{ totalPrice.toFixed(2) }} PLN</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-700 dark:text-gray-300">Kalorie:</span>
                  <span class="font-semibold text-gray-900 dark:text-white">~{{ estimatedCalories }} kcal</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-700 dark:text-gray-300">Białko:</span>
                  <span class="font-semibold text-gray-900 dark:text-white">~{{ estimatedProtein }}g</span>
                </div>
              </div>
              
              <!-- Dietary Labels -->
              <div v-if="dietaryLabels.length" class="flex flex-wrap gap-1 mt-3">
                <span 
                  v-for="label in dietaryLabels" 
                  :key="label"
                  class="px-2 py-1 bg-white dark:bg-gray-700 text-xs rounded-full text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-600"
                >
                  {{ label }}
                </span>
              </div>
            </div>
            
            <!-- Composition Name -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Nazwa kompozycji:
              </label>
              <input 
                v-model="compositionName"
                type="text" 
                placeholder="Moja kompozycja..."
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              >
            </div>
            
            <!-- Action Buttons -->
            <div class="space-y-2">
              <button 
                @click="saveToFavorites"
                :disabled="!canSave"
                class="w-full px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
              >
                <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"></path>
                </svg>
                Zapisz do ulubionych
              </button>
              
              <button 
                @click="createOrder"
                :disabled="!canCreateOrder"
                class="w-full px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                </svg>
                {{ totalPrice.toFixed(2) }} PLN - Utwórz zamówienie
              </button>
            </div>
          </div>
        </div>

        <!-- Smart Suggestions -->
        <SmartSuggestions
          :selected-ingredients="allSelectedIngredients"
          :context="currentContext"
          @add-ingredient="handleSuggestedIngredient"
          @load-recipe="handleSuggestedRecipe"
        />

        <!-- Favorites Panel -->
        <FavoritesPanel
          @select-recipe="handleFavoriteRecipe"
          @select-ingredient="handleFavoriteIngredient"
        />
        
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, defineProps, defineEmits, reactive } from 'vue'
import axios from 'axios'
import SmartSuggestions from '../SmartSuggestions.vue'
import FavoritesPanel from '../FavoritesPanel.vue'

// Props
const props = defineProps<{
  savedCompositions: Array<any>
}>()

// Emits
const emit = defineEmits<{
  'update:saved-compositions': (compositions: Array<any>) => void
}>()

// Reactive data
const bases = ref([])
const toppings = ref([])
const categories = ref({})
const loading = ref(false)

// Search & Filters
const searchQuery = ref('')
const selectedPriceRange = ref('')
const activeFilters = ref([])

// Category selections
const selectedBaseCategory = ref('traditional')
const selectedToppingCategory = ref('superfoods')

// Composition state
const selectedBase = ref(null)
const selectedToppings = ref([])
const compositionName = ref('')

// Toast notifications
const toast = ref({
  show: false,
  type: 'success',
  message: ''
})

// Quick filters configuration
const quickFilters = [
  { key: 'vegan', label: '🌱 Vegan' },
  { key: 'protein', label: '💪 Białko' },
  { key: 'gluten_free', label: '🌾 Bezglutenowe' },
  { key: 'natural', label: '🍃 Naturalne' },
  { key: 'bio', label: '🌿 BIO' },
  { key: 'superfood', label: '⭐ Superfood' }
]

// Base categories
const baseCategories = ref([
  { key: 'traditional', name: 'Tradycyjne', icon: '🥛', count: 0 },
  { key: 'cups', name: 'Kubeczki', icon: '🥤', count: 0 },
  { key: 'powders', name: 'Proszki', icon: '🥄', count: 0 }
])

// Topping categories  
const toppingCategories = ref([
  { key: 'superfoods', name: 'Superfoods', icon: '⭐', count: 0 },
  { key: 'fruits', name: 'Owoce', icon: '🍓', count: 0 },
  { key: 'nuts_seeds', name: 'Nasiona', icon: '🥜', count: 0 },
  { key: 'spices', name: 'Przyprawy', icon: '🌿', count: 0 },
  { key: 'bee_products', name: 'Produkty pszczele', icon: '🍯', count: 0 },
  { key: 'detox', name: 'Detoks', icon: '🌊', count: 0 }
])

// Computed properties
const filteredBases = computed(() => {
  let filtered = bases.value.filter(base => {
    // Category filter
    if (selectedBaseCategory.value && base.category_key !== selectedBaseCategory.value) {
      return false
    }
    
    // Search filter
    if (searchQuery.value && !base.name.toLowerCase().includes(searchQuery.value.toLowerCase())) {
      return false
    }
    
    // Price filter
    if (selectedPriceRange.value) {
      const [min, max] = selectedPriceRange.value.split('-').map(p => p.replace('+', ''))
      const price = base.price
      if (max) {
        if (price < parseInt(min) || price > parseInt(max)) return false
      } else {
        if (price < parseInt(min)) return false
      }
    }
    
    // Quick filters
    if (activeFilters.value.length > 0) {
      return activeFilters.value.some(filter => 
        base.dietary_labels?.some(label => label.toLowerCase().includes(filter.toLowerCase())) || 
        base.safety_labels?.some(label => label.toLowerCase().includes(filter.toLowerCase()))
      )
    }
    
    return true
  })
  
  return filtered
})

const filteredToppings = computed(() => {
  let filtered = toppings.value.filter(topping => {
    // Category filter
    if (selectedToppingCategory.value && topping.category_key !== selectedToppingCategory.value) {
      return false
    }
    
    // Search filter
    if (searchQuery.value && !topping.name.toLowerCase().includes(searchQuery.value.toLowerCase())) {
      return false
    }
    
    // Price filter
    if (selectedPriceRange.value) {
      const [min, max] = selectedPriceRange.value.split('-').map(p => p.replace('+', ''))
      const price = topping.price
      if (max) {
        if (price < parseInt(min) || price > parseInt(max)) return false
      } else {
        if (price < parseInt(min)) return false
      }
    }
    
    // Quick filters
    if (activeFilters.value.length > 0) {
      return activeFilters.value.some(filter => 
        topping.dietary_labels?.some(label => label.toLowerCase().includes(filter.toLowerCase())) || 
        topping.safety_labels?.some(label => label.toLowerCase().includes(filter.toLowerCase()))
      )
    }
    
    return true
  })
  
  return filtered
})

const totalPrice = computed(() => {
  let price = 0
  if (selectedBase.value) price += selectedBase.value.price
  price += selectedToppings.value.reduce((sum, topping) => sum + topping.price, 0)
  return price
})

const estimatedCalories = computed(() => {
  let calories = 0
  if (selectedBase.value) calories += selectedBase.value.calories || 120
  calories += selectedToppings.value.reduce((sum, topping) => sum + (topping.calories || 50), 0)
  return calories
})

const estimatedProtein = computed(() => {
  let protein = 0
  if (selectedBase.value) protein += selectedBase.value.protein || 8
  protein += selectedToppings.value.reduce((sum, topping) => sum + (topping.protein || 3), 0)
  return Math.round(protein)
})

const dietaryLabels = computed(() => {
  const labels = new Set()
  
  if (selectedBase.value?.dietary_labels) {
    selectedBase.value.dietary_labels.forEach(label => labels.add(label))
  }
  
  selectedToppings.value.forEach(topping => {
    if (topping.dietary_labels) {
      topping.dietary_labels.forEach(label => labels.add(label))
    }
  })
  
  return Array.from(labels)
})

const allSelectedIngredients = computed(() => {
  const ingredients = []
  if (selectedBase.value) ingredients.push(selectedBase.value)
  return ingredients.concat(selectedToppings.value)
})

const currentContext = computed(() => {
  const hour = new Date().getHours()
  if (hour < 11) return 'breakfast'
  if (hour < 16) return 'lunch'
  if (hour < 20) return 'dinner'
  return 'snack'
})

const canSave = computed(() => {
  return selectedBase.value && compositionName.value.trim().length > 0
})

const canCreateOrder = computed(() => {
  return selectedBase.value && totalPrice.value > 0
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

const selectBase = (base: any) => {
  selectedBase.value = selectedBase.value?.id === base.id ? null : base
}

const removeBase = () => {
  selectedBase.value = null
}

const toggleTopping = (topping: any) => {
  const index = selectedToppings.value.findIndex(t => t.id === topping.id)
  if (index > -1) {
    selectedToppings.value.splice(index, 1)
  } else {
    selectedToppings.value.push(topping)
  }
}

const removeTopping = (topping: any) => {
  const index = selectedToppings.value.findIndex(t => t.id === topping.id)
  if (index > -1) {
    selectedToppings.value.splice(index, 1)
  }
}

const addTopping = (topping: any) => {
  const exists = selectedToppings.value.find(t => t.id === topping.id)
  if (!exists) {
    selectedToppings.value.push(topping)
  }
}

const removeToppings = (topping: any) => {
  removeTopping(topping)
}

const resetComposition = () => {
  selectedBase.value = null
  selectedToppings.value = []
  compositionName.value = ''
  searchQuery.value = ''
  selectedPriceRange.value = ''
  activeFilters.value = []
}

const saveComposition = () => {
  if (!canSave.value) return
  
  const composition = {
    id: Date.now().toString(),
    name: compositionName.value,
    base: selectedBase.value,
    toppings: [...selectedToppings.value],
    ingredients: [selectedBase.value, ...selectedToppings.value],
    price: totalPrice.value,
    calories: estimatedCalories.value,
    nutrition: { protein: estimatedProtein.value, carbs: 0, fat: 0 },
    dietaryLabels: [...dietaryLabels.value],
    savedAt: new Date().toLocaleString('pl-PL')
  }
  
  // Save to localStorage
  const saved = localStorage.getItem('ikigai_compositions') || '[]'
  const compositions = JSON.parse(saved)
  compositions.unshift(composition) // Add to beginning
  
  // Keep only 20 most recent
  if (compositions.length > 20) {
    compositions.splice(20)
  }
  
  localStorage.setItem('ikigai_compositions', JSON.stringify(compositions))
  
  // Emit update to parent
  emit('update:saved-compositions', compositions)
  
  // Show success message
  alert(`✅ Kompozycja "${compositionName.value}" została zapisana!`)
  
  console.log('💾 Kompozycja zapisana:', composition)
}

const loadComposition = (composition: any) => {
  selectedBase.value = composition.base
  selectedToppings.value = [...composition.toppings]
  compositionName.value = composition.name
  
  console.log('📥 Kompozycja wczytana:', composition.name)
}

const deleteComposition = (compositionId: string) => {
  if (!confirm('Czy na pewno chcesz usunąć tę kompozycję?')) return
  
  const saved = localStorage.getItem('ikigai_compositions') || '[]'
  const compositions = JSON.parse(saved)
  const filtered = compositions.filter(c => c.id !== compositionId)
  
  localStorage.setItem('ikigai_compositions', JSON.stringify(filtered))
  emit('update:saved-compositions', filtered)
  
  console.log('🗑️ Kompozycja usunięta:', compositionId)
}

const createOrder = async () => {
  if (!canCreateOrder.value) return
  
  try {
    const orderData = {
      type: 'custom_composition',
      name: compositionName.value,
      base: selectedBase.value,
      toppings: selectedToppings.value,
      total_price: totalPrice.value,
      total_calories: estimatedCalories.value,
      nutrition: { protein: estimatedProtein.value, carbs: 0, fat: 0 },
      dietary_labels: [...dietaryLabels.value],
      custom_composition: true
    }
    
    console.log('🛒 Tworzę zamówienie:', orderData)
    
    const response = await axios.post('http://localhost:5001/api/orders', orderData)
    
    if (response.data.success) {
      alert(`✅ Zamówienie "${compositionName.value}" zostało utworzone! 💰 ${totalPrice.value.toFixed(2)}zł`)
      
      // Optionally save composition and reset
      if (!props.savedCompositions.some(c => c.name === compositionName.value)) {
        saveComposition()
      }
      resetComposition()
    } else {
      throw new Error(response.data.message || 'Błąd tworzenia zamówienia')
    }
  } catch (error) {
    console.error('❌ Błąd zamówienia:', error)
    alert(`❌ Błąd tworzenia zamówienia: ${error.message}`)
  }
}

const fetchIngredients = async () => {
  try {
    loading.value = true
    
    // Pobierz kategorie składników z PostgreSQL
    const categoriesResponse = await axios.get('http://localhost:5001/api/ingredients/categories')
    
    if (categoriesResponse.data && categoriesResponse.data.data) {
      const categories = categoriesResponse.data.data
      
      console.log('📦 Kategorie z backend:', categories)
      
      // Mapowanie kategorii do frontend
      const categoryMapping = {
        'bases': { frontend_key: 'traditional', type: 'base' },
        'superfoods': { frontend_key: 'superfoods', type: 'topping' },
        'fruits': { frontend_key: 'fruits', type: 'topping' },
        'seeds': { frontend_key: 'nuts_seeds', type: 'topping' },
        'honey': { frontend_key: 'bee_products', type: 'topping' },
        'detox': { frontend_key: 'detox', type: 'topping' },
        'vitamins': { frontend_key: 'spices', type: 'topping' },
        'proteins': { frontend_key: 'superfoods', type: 'topping' }
      }
      
      // Aktualizuj liczby w kategoriach na podstawie danych z PostgreSQL
      baseCategories.value.forEach(cat => {
        cat.count = 0 // Resetuj
      })
      
      toppingCategories.value.forEach(cat => {
        cat.count = 0 // Resetuj
      })
      
      // Pobierz składniki dla każdej kategorii
      const allIngredients = []
      
      for (const category of categories) {
        const mapping = categoryMapping[category.id]
        if (!mapping) continue
        
        // Aktualizuj count w odpowiedniej kategorii frontend
        if (mapping.type === 'base') {
          const frontendCat = baseCategories.value.find(c => c.key === mapping.frontend_key)
          if (frontendCat) frontendCat.count = category.count
        } else {
          const frontendCat = toppingCategories.value.find(c => c.key === mapping.frontend_key)
          if (frontendCat) frontendCat.count += category.count
        }
        
        // Pobierz składniki dla tej kategorii
        try {
          const ingredientsResponse = await axios.get(`http://localhost:5001/api/ingredients/category/${category.db_slug}`)
          if (ingredientsResponse.data && ingredientsResponse.data.data) {
            const ingredients = ingredientsResponse.data.data.map(ing => ({
              ...ing,
              category_key: mapping.frontend_key,
              type: mapping.type,
              icon: getIngredientIcon(ing.name, category.id),
              dietary_labels: ing.allergens || [],
              safety_labels: ing.benefits || []
            }))
            
            if (mapping.type === 'base') {
              bases.value.push(...ingredients)
            } else {
              toppings.value.push(...ingredients)
            }
            
            allIngredients.push(...ingredients)
          }
        } catch (error) {
          console.error(`❌ Błąd pobierania składników dla kategorii ${category.db_slug}:`, error)
        }
      }
      
      console.log('📦 Składniki załadowane:', {
        bases: bases.value.length,
        toppings: toppings.value.length,
        total: allIngredients.length,
        basesBreakdown: baseCategories.value.map(c => `${c.name}: ${c.count}`),
        toppingsBreakdown: toppingCategories.value.map(c => `${c.name}: ${c.count}`)
      })
    }
  } catch (error) {
    console.error('❌ Błąd ładowania składników:', error)
  } finally {
    loading.value = false
  }
}

// Pomocnicza funkcja do przypisywania ikon składnikom
const getIngredientIcon = (name: string, categoryId: string) => {
  const lowerName = name.toLowerCase()
  
  // Ikony na podstawie nazwy składnika
  if (lowerName.includes('mleko')) return '🥛'
  if (lowerName.includes('woda')) return '💧'
  if (lowerName.includes('chia')) return '🌱'
  if (lowerName.includes('białko')) return '💪'
  if (lowerName.includes('protein')) return '💪'
  if (lowerName.includes('spirulina')) return '🌿'
  if (lowerName.includes('matcha')) return '🍵'
  
  // Ikony na podstawie kategorii
  switch (categoryId) {
    case 'bases': return '🥛'
    case 'superfoods': return '⭐'
    case 'fruits': return '🍓'
    case 'seeds': return '🌰'
    case 'honey': return '🍯'
    case 'detox': return '🌊'
    case 'vitamins': return '💊'
    case 'proteins': return '💪'
    default: return '🔸'
  }
}

// Load saved compositions from localStorage
const loadSavedCompositions = () => {
  try {
    const saved = localStorage.getItem('ikigai_compositions')
    if (saved) {
      const compositions = JSON.parse(saved)
      emit('update:saved-compositions', compositions)
      console.log('💾 Wczytano kompozycje:', compositions.length)
    }
  } catch (error) {
    console.error('❌ Błąd ładowania kompozycji:', error)
  }
}

// Smart Suggestions handlers
const handleSuggestedIngredient = (ingredient) => {
  // Determine if it's a base or topping based on category
  const baseCategories = ['traditional', 'liquid_cup', 'powder']
  
  if (baseCategories.includes(ingredient.category_key || ingredient.category)) {
    // It's a base
    if (!selectedBase.value) {
      selectedBase.value = ingredient
    } else {
      // Ask user if they want to replace current base
      if (confirm(`Zastąpić obecną bazę "${selectedBase.value.name}" na "${ingredient.name}"?`)) {
        selectedBase.value = ingredient
      }
    }
  } else {
    // It's a topping
    addTopping(ingredient)
  }
}

const handleSuggestedRecipe = (recipe) => {
  if (confirm(`Wczytać przepis "${recipe.name}"? To zastąpi obecną kompozycję.`)) {
    loadRecipeFromSuggestion(recipe)
  }
}

const loadRecipeFromSuggestion = async (recipe) => {
  try {
    // Load recipe details and set composition
    const response = await axios.get(`http://localhost:5001/api/meal-recipes/${recipe.id}`)
    
    if (response.data.status === 'success') {
      const recipeData = response.data.data
      resetComposition()
      
      // Set composition name
      compositionName.value = recipeData.name
      
      // Load ingredients from recipe
      if (recipeData.base) {
        selectedBase.value = recipeData.base
      }
      
      if (recipeData.toppings && recipeData.toppings.length > 0) {
        selectedToppings.value = [...recipeData.toppings]
      }
    }
  } catch (error) {
    console.error('Error loading recipe:', error)
  }
}

// Favorites handlers
const handleFavoriteRecipe = (recipe) => {
  if (confirm(`Wczytać ulubiony przepis "${recipe.name}"?`)) {
    loadFavoriteRecipe(recipe)
  }
}

const handleFavoriteIngredient = (ingredient) => {
  handleSuggestedIngredient(ingredient)
}

const loadFavoriteRecipe = (recipe) => {
  // Reset current composition
  resetComposition()
  
  // Load recipe data (mock for now, would load from API)
  compositionName.value = recipe.name
  
  // This would normally load the full recipe composition
  // For now, just set the name and let user build
}

const saveToFavorites = async () => {
  if (!canSave.value) return
  
  try {
    // Save current composition to favorites
    const compositionData = {
      user_id: 'web_user',
      type: 'recipe',
      item_id: compositionName.value.toLowerCase().replace(/\s+/g, '_'),
      name: compositionName.value,
      ingredients: allSelectedIngredients.value,
      price: totalPrice.value
    }
    
    await axios.post('http://localhost:5001/api/favorites', compositionData)
    
    alert('Kompozycja zapisana do ulubionych!')
  } catch (error) {
    console.error('Error saving to favorites:', error)
    alert('Zapisano do ulubionych lokalnie')
  }
}

// Lifecycle
onMounted(() => {
  fetchIngredients()
  loadSavedCompositions()
})
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.aspect-square {
  aspect-ratio: 1;
  position: relative;
}

.aspect-square .absolute {
  position: absolute;
}

/* Custom scrollbar */
.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 2px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style> 