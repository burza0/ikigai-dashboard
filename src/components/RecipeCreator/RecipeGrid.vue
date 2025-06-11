<template>
  <div class="space-y-6">
    
    <!-- Filters & Search -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        
        <!-- Search -->
        <div class="md:col-span-2">
          <div class="relative">
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="🔍 Szukaj przepisu..."
              class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <span class="text-gray-400">🔍</span>
            </div>
          </div>
        </div>
        
        <!-- Category Filter -->
        <div>
          <select 
            v-model="selectedCategory"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          >
            <option value="">🍽️ Wszystkie kategorie</option>
            <option value="breakfast">🌅 Śniadania</option>
            <option value="lunch">🌞 Obiady</option>
            <option value="dinner">🌙 Kolacje</option>
            <option value="snacks">🥨 Przekąski</option>
            <option value="specialty">🎯 Specjalistyczne</option>
          </select>
        </div>
        
        <!-- Price Range -->
        <div>
          <select 
            v-model="selectedPriceRange"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          >
            <option value="">💰 Wszystkie ceny</option>
            <option value="0-15">💰 0-15 PLN</option>
            <option value="15-20">💰 15-20 PLN</option>
            <option value="20-25">💰 20-25 PLN</option>
            <option value="25+">💰 25+ PLN</option>
          </select>
        </div>
      </div>
      
      <!-- Quick Filters -->
      <div class="flex flex-wrap gap-2 mt-4">
        <button 
          v-for="filter in quickFilters" 
          :key="filter.id"
          @click="toggleQuickFilter(filter.id)"
          :class="[
            'px-3 py-1 rounded-full text-sm font-medium transition-all duration-200',
            activeQuickFilters.includes(filter.id)
              ? 'bg-purple-100 text-purple-700 border border-purple-300'
              : 'bg-gray-100 text-gray-600 border border-gray-300 hover:bg-purple-50'
          ]"
        >
          {{ filter.icon }} {{ filter.name }}
        </button>
      </div>
      
      <!-- Results Count -->
      <div class="flex justify-between items-center mt-4 pt-4 border-t border-gray-200">
        <span class="text-sm text-gray-600">
          Znaleziono {{ filteredRecipes.length }} z {{ recipes.length }} przepisów
        </span>
        <button 
          @click="clearFilters"
          class="text-sm text-purple-600 hover:text-purple-700 font-medium"
        >
          🔄 Wyczyść filtry
        </button>
      </div>
    </div>

    <!-- Categories Overview -->
    <div v-if="!hasActiveFilters" class="grid grid-cols-2 md:grid-cols-5 gap-4">
      <div 
        v-for="(category, key) in categories" 
        :key="key"
        @click="selectedCategory = key"
        class="bg-white rounded-lg border border-gray-200 p-4 hover:border-purple-300 hover:bg-purple-50 transition-all duration-200 cursor-pointer"
      >
        <div class="text-center">
          <div class="text-2xl mb-2">{{ getCategoryIcon(key) }}</div>
          <div class="font-semibold text-gray-900">{{ getCategoryName(key) }}</div>
          <div class="text-sm text-gray-600">{{ category.count }} przepisów</div>
          <div class="text-xs text-purple-600 mt-1">
            {{ category.price_range.min.toFixed(0) }}-{{ category.price_range.max.toFixed(0) }} PLN
          </div>
        </div>
      </div>
    </div>

    <!-- Recipe Grid -->
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="n in 6" :key="n" class="bg-gray-100 rounded-xl p-6 animate-pulse">
        <div class="h-4 bg-gray-300 rounded mb-4"></div>
        <div class="h-3 bg-gray-300 rounded mb-2"></div>
        <div class="h-3 bg-gray-300 rounded mb-4"></div>
        <div class="h-8 bg-gray-300 rounded"></div>
      </div>
    </div>

    <div v-else-if="filteredRecipes.length === 0" class="text-center py-12">
      <div class="text-6xl mb-4">🤔</div>
      <h3 class="text-xl font-semibold text-gray-900 mb-2">Brak przepisów</h3>
      <p class="text-gray-600">Spróbuj zmienić filtry lub wyszukiwanie</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div 
        v-for="recipe in filteredRecipes" 
        :key="recipe.id"
        class="bg-white rounded-xl border border-gray-200 overflow-hidden hover:border-purple-300 hover:shadow-lg transition-all duration-200 cursor-pointer"
        @click="$emit('select-recipe', recipe)"
      >
        <!-- Header -->
        <div class="p-6 pb-4">
          <div class="flex items-start justify-between mb-3">
            <h3 class="font-bold text-lg text-gray-900 leading-tight">{{ recipe.name }}</h3>
            <div class="text-right ml-4">
              <div class="text-lg font-bold text-purple-600">{{ recipe.total_price.toFixed(2) }}zł</div>
              <div class="text-xs text-gray-500">⏱️ {{ recipe.prep_time }}</div>
            </div>
          </div>
          
          <!-- Health Score & Popularity -->
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center space-x-3">
              <div class="flex items-center">
                <span class="text-green-600 font-medium">💚 {{ recipe.health_score }}/100</span>
              </div>
              <div class="flex items-center">
                <span class="text-blue-600 font-medium">👥 {{ recipe.popularity }}%</span>
              </div>
            </div>
            <div class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
              {{ getCategoryName(recipe.category) }}
            </div>
          </div>
          
          <!-- Description -->
          <p class="text-sm text-gray-600 mb-4 line-clamp-2">{{ recipe.description }}</p>
          
          <!-- Health Benefits Tags -->
          <div class="flex flex-wrap gap-1 mb-4">
            <span 
              v-for="benefit in recipe.health_benefits.slice(0, 3)" 
              :key="benefit"
              class="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium"
            >
              {{ benefit }}
            </span>
            <span 
              v-if="recipe.health_benefits.length > 3"
              class="px-2 py-1 bg-gray-100 text-gray-600 rounded-full text-xs"
            >
              +{{ recipe.health_benefits.length - 3 }} więcej
            </span>
          </div>
        </div>
        
        <!-- Footer -->
        <div class="px-6 py-4 bg-gray-50 border-t border-gray-100">
          <div class="flex items-center justify-between">
            <div class="text-sm text-gray-600">
              🥄 {{ getBaseIngredientName(recipe.base) }} + {{ recipe.toppings.length }} dodatków
            </div>
            <div class="flex space-x-2">
              <button 
                @click.stop="$emit('select-recipe', recipe)"
                class="px-3 py-1 bg-purple-100 text-purple-700 rounded-lg text-sm font-medium hover:bg-purple-200 transition-colors duration-200"
              >
                👁️ Szczegóły
              </button>
              <button 
                @click.stop="$emit('order-recipe', recipe)"
                class="px-3 py-1 bg-purple-600 text-white rounded-lg text-sm font-medium hover:bg-purple-700 transition-colors duration-200"
              >
                🛒 Zamów
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, defineProps, defineEmits } from 'vue'

// Props
const props = defineProps<{
  recipes: Array<any>
  categories: Record<string, any>
  loading: boolean
}>()

// Emits
defineEmits<{
  'select-recipe': (recipe: any) => void
  'order-recipe': (recipe: any) => void
}>()

// Reactive state
const searchQuery = ref('')
const selectedCategory = ref('')
const selectedPriceRange = ref('')
const activeQuickFilters = ref([])

// Quick filters
const quickFilters = [
  { id: 'High-Protein', name: 'Wysokobiałkowe', icon: '💪' },
  { id: 'Detox', name: 'Detoks', icon: '🌿' },
  { id: 'Vegan', name: 'Vegan', icon: '🌱' },
  { id: 'Anti-inflammatory', name: 'Przeciwzapalne', icon: '🔥' },
  { id: 'Energy-Boost', name: 'Energia', icon: '⚡' },
  { id: 'Stress-Relief', name: 'Antystres', icon: '🧘' }
]

// Computed
const hasActiveFilters = computed(() => 
  searchQuery.value || selectedCategory.value || selectedPriceRange.value || activeQuickFilters.value.length > 0
)

const filteredRecipes = computed(() => {
  let filtered = [...props.recipes]
  
  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(recipe => 
      recipe.name.toLowerCase().includes(query) ||
      recipe.description.toLowerCase().includes(query) ||
      recipe.health_benefits.some(benefit => benefit.toLowerCase().includes(query))
    )
  }
  
  // Category filter
  if (selectedCategory.value) {
    filtered = filtered.filter(recipe => recipe.category === selectedCategory.value)
  }
  
  // Price range filter
  if (selectedPriceRange.value) {
    filtered = filtered.filter(recipe => {
      const price = recipe.total_price
      switch (selectedPriceRange.value) {
        case '0-15': return price <= 15
        case '15-20': return price > 15 && price <= 20
        case '20-25': return price > 20 && price <= 25
        case '25+': return price > 25
        default: return true
      }
    })
  }
  
  // Quick filters
  if (activeQuickFilters.value.length > 0) {
    filtered = filtered.filter(recipe => 
      activeQuickFilters.value.some(filter => 
        recipe.health_benefits.includes(filter)
      )
    )
  }
  
  return filtered
})

// Methods
const toggleQuickFilter = (filterId: string) => {
  const index = activeQuickFilters.value.indexOf(filterId)
  if (index === -1) {
    activeQuickFilters.value.push(filterId)
  } else {
    activeQuickFilters.value.splice(index, 1)
  }
}

const clearFilters = () => {
  searchQuery.value = ''
  selectedCategory.value = ''
  selectedPriceRange.value = ''
  activeQuickFilters.value = []
}

const getCategoryIcon = (category: string) => {
  const icons = {
    breakfast: '🌅',
    lunch: '🌞', 
    dinner: '🌙',
    snacks: '🥨',
    specialty: '🎯'
  }
  return icons[category] || '🍽️'
}

const getCategoryName = (category: string) => {
  const names = {
    breakfast: 'Śniadania',
    lunch: 'Obiady',
    dinner: 'Kolacje', 
    snacks: 'Przekąski',
    specialty: 'Specjalistyczne'
  }
  return names[category] || 'Przepisy'
}

const getBaseIngredientName = (baseId: string) => {
  // Simplified - w rzeczywistej implementacji pobierzemy z API
  const baseNames = {
    protein_vanilla: 'Protein Vanilla',
    spirulina_powder: 'Spirulina',
    coconut_water: 'Woda Kokosowa',
    golden_milk: 'Złote Mleko',
    matcha_premium: 'Matcha Premium',
    kombucha_ginger: 'Kombucha Imbir',
    collagen_marine: 'Kolagen Morski',
    aloe_vera_juice: 'Sok Aloe Vera',
    yogurt_greek: 'Jogurt Grecki',
    oatmeal_base: 'Owsianka',
    lemon_ginger_water: 'Woda Cytryna-Imbir',
    smoothie_bowl: 'Smoothie Bowl'
  }
  return baseNames[baseId] || baseId
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 