<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
    
    <!-- Header -->
    <div class="p-4 lg:p-6 border-b border-gray-200 dark:border-gray-700">
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center">
          <div class="w-8 h-8 bg-red-100 dark:bg-red-900 rounded-lg flex items-center justify-center mr-3">
            <svg class="w-4 h-4 text-red-600 dark:text-red-400" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"></path>
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">⭐ Ulubione</h3>
            <p class="text-sm text-gray-500 dark:text-gray-400">Twoje ulubione przepisy i składniki</p>
          </div>
        </div>
        
        <!-- View Toggle -->
        <div class="flex bg-gray-100 dark:bg-gray-700 rounded-lg p-1">
          <button 
            @click="activeView = 'recipes'"
            :class="[
              'px-3 py-1 text-sm rounded-md transition-colors',
              activeView === 'recipes' 
                ? 'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow-sm' 
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
            ]"
          >
            Przepisy
          </button>
          <button 
            @click="activeView = 'ingredients'"
            :class="[
              'px-3 py-1 text-sm rounded-md transition-colors',
              activeView === 'ingredients' 
                ? 'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow-sm' 
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
            ]"
          >
            Składniki
          </button>
        </div>
      </div>
      
      <!-- Quick Stats -->
      <div class="grid grid-cols-3 gap-4 text-center">
        <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
          <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ favorites?.recipes?.length || 0 }}</div>
          <div class="text-xs text-gray-500 dark:text-gray-400">Przepisy</div>
        </div>
        <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
          <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ favorites?.ingredients?.length || 0 }}</div>
          <div class="text-xs text-gray-500 dark:text-gray-400">Składniki</div>
        </div>
        <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
          <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ totalOrders }}</div>
          <div class="text-xs text-gray-500 dark:text-gray-400">Zamówienia</div>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="p-4 lg:p-6">
      
      <!-- Loading State -->
      <div v-if="loading" class="space-y-4">
        <div v-for="i in 3" :key="i" class="animate-pulse">
          <div class="flex items-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <div class="w-12 h-12 bg-gray-200 dark:bg-gray-600 rounded-lg mr-3"></div>
            <div class="flex-1 space-y-2">
              <div class="h-4 bg-gray-200 dark:bg-gray-600 rounded w-3/4"></div>
              <div class="h-3 bg-gray-200 dark:bg-gray-600 rounded w-1/2"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Favorite Recipes -->
      <div v-else-if="activeView === 'recipes'">
        <div v-if="favorites?.recipes?.length" class="space-y-3">
          <div 
            v-for="recipe in favorites.recipes" 
            :key="recipe.id"
            class="group bg-gray-50 dark:bg-gray-700 rounded-lg p-4 hover:shadow-md transition-all duration-200 cursor-pointer border border-gray-200 dark:border-gray-600"
            @click="selectRecipe(recipe)"
          >
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center">
                <div class="w-10 h-10 bg-gradient-to-br from-orange-400 to-red-500 rounded-lg flex items-center justify-center mr-3">
                  <span class="text-white text-lg">{{ getCategoryIcon(recipe.category) }}</span>
                </div>
                <div>
                  <h4 class="font-medium text-gray-900 dark:text-white group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors">
                    {{ recipe.name }}
                  </h4>
                  <p class="text-xs text-gray-500 dark:text-gray-400 capitalize">{{ recipe.category }}</p>
                </div>
              </div>
              
              <button 
                @click.stop="removeFromFavorites(recipe.id, 'recipe')"
                class="opacity-0 group-hover:opacity-100 p-1 text-red-400 hover:text-red-600 transition-all"
              >
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"></path>
                </svg>
              </button>
            </div>
            
            <div class="flex items-center justify-between text-sm">
              <div class="flex items-center space-x-3">
                <span class="text-green-600 dark:text-green-400 font-semibold">{{ recipe.price.toFixed(2) }} PLN</span>
                <span class="px-2 py-1 bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 text-xs rounded">
                  Health {{ recipe.health_score }}
                </span>
              </div>
              <div class="text-xs text-gray-500 dark:text-gray-400">
                Zamówiono {{ recipe.order_count }} razy
              </div>
            </div>
            
            <div class="text-xs text-gray-400 dark:text-gray-500 mt-2">
              Ostatnio: {{ formatDate(recipe.last_ordered) }}
            </div>
          </div>
        </div>
        
        <div v-else class="text-center py-8">
          <div class="w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-gray-400" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"></path>
            </svg>
          </div>
          <p class="text-gray-500 dark:text-gray-400 text-sm">Brak ulubionych przepisów</p>
          <p class="text-gray-400 dark:text-gray-500 text-xs mt-1">Kliknij ⭐ przy przepisie aby dodać do ulubionych</p>
        </div>
      </div>

      <!-- Favorite Ingredients -->
      <div v-else-if="activeView === 'ingredients'">
        
        <!-- Category Filter -->
        <div class="flex flex-wrap gap-2 mb-4">
          <button 
            @click="selectedCategory = ''"
            :class="[
              'px-3 py-1 text-xs rounded-full border transition-colors',
              selectedCategory === '' 
                ? 'bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300 border-purple-300 dark:border-purple-600' 
                : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 border-gray-300 dark:border-gray-600'
            ]"
          >
            Wszystkie
          </button>
          <button 
            v-for="category in favoriteCategories" 
            :key="category.name"
            @click="selectedCategory = category.name"
            :class="[
              'px-3 py-1 text-xs rounded-full border transition-colors',
              selectedCategory === category.name 
                ? 'bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300 border-purple-300 dark:border-purple-600' 
                : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 border-gray-300 dark:border-gray-600'
            ]"
          >
            {{ getCategoryName(category.name) }} ({{ category.count }})
          </button>
        </div>
        
        <div v-if="filteredIngredients?.length" class="space-y-3">
          <div 
            v-for="ingredient in filteredIngredients" 
            :key="ingredient.id"
            class="group bg-gray-50 dark:bg-gray-700 rounded-lg p-4 hover:shadow-md transition-all duration-200 cursor-pointer border border-gray-200 dark:border-gray-600"
            @click="selectIngredient(ingredient)"
          >
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center">
                <div class="w-10 h-10 bg-gradient-to-br from-green-400 to-blue-500 rounded-lg flex items-center justify-center mr-3">
                  <span class="text-white text-lg">{{ getCategoryIcon(ingredient.category) }}</span>
                </div>
                <div>
                  <h4 class="font-medium text-gray-900 dark:text-white group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors">
                    {{ ingredient.name }}
                  </h4>
                  <p class="text-xs text-gray-500 dark:text-gray-400 capitalize">{{ getCategoryName(ingredient.category) }}</p>
                </div>
              </div>
              
              <button 
                @click.stop="removeFromFavorites(ingredient.id, 'ingredient')"
                class="opacity-0 group-hover:opacity-100 p-1 text-red-400 hover:text-red-600 transition-all"
              >
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"></path>
                </svg>
              </button>
            </div>
            
            <div class="flex items-center justify-between text-sm">
              <span class="text-green-600 dark:text-green-400 font-semibold">{{ ingredient.price.toFixed(2) }} PLN</span>
              <span class="text-xs text-gray-500 dark:text-gray-400">
                Użyto {{ ingredient.usage_count }} razy
              </span>
            </div>
          </div>
        </div>
        
        <div v-else class="text-center py-8">
          <div class="w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
            </svg>
          </div>
          <p class="text-gray-500 dark:text-gray-400 text-sm">Brak ulubionych składników</p>
          <p class="text-gray-400 dark:text-gray-500 text-xs mt-1">Dodaj składniki do ulubionych podczas tworzenia kompozycji</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, defineEmits } from 'vue'
import axios from 'axios'

// Emits
const emit = defineEmits<{
  'select-recipe': (recipe: any) => void
  'select-ingredient': (ingredient: any) => void
}>()

// Reactive data
const favorites = ref(null)
const loading = ref(false)
const activeView = ref('recipes')
const selectedCategory = ref('')

// Computed
const totalOrders = computed(() => {
  if (!favorites.value?.recipes) return 0
  return favorites.value.recipes.reduce((sum, recipe) => sum + recipe.order_count, 0)
})

const favoriteCategories = computed(() => {
  return favorites.value?.categories || []
})

const filteredIngredients = computed(() => {
  if (!favorites.value?.ingredients) return []
  if (!selectedCategory.value) return favorites.value.ingredients
  return favorites.value.ingredients.filter(ing => ing.category === selectedCategory.value)
})

// Methods
const fetchFavorites = async () => {
  try {
    loading.value = true
    const response = await axios.get('http://localhost:5001/api/favorites?user_id=web_user')
    
    if (response.data.status === 'success') {
      favorites.value = response.data.data
    }
  } catch (error) {
    console.error('Error fetching favorites:', error)
    // Mock data jako fallback
    favorites.value = {
      recipes: [
        {
          id: "energetic_morning",
          name: "Energetyczny Start Dnia",
          category: "breakfast",
          price: 16.60,
          health_score: 94,
          last_ordered: "2024-06-10",
          order_count: 12
        }
      ],
      ingredients: [
        {
          id: "spirulina_powder",
          name: "Spirulina Powder BIO",
          category: "superfoods",
          price: 4.50,
          usage_count: 18
        }
      ],
      categories: [
        {"name": "breakfast", "count": 1},
        {"name": "superfoods", "count": 1}
      ]
    }
  } finally {
    loading.value = false
  }
}

const removeFromFavorites = async (itemId: string, type: string) => {
  try {
    await axios.delete(`http://localhost:5001/api/favorites/${itemId}?user_id=web_user`)
    
    // Update local state
    if (type === 'recipe') {
      favorites.value.recipes = favorites.value.recipes.filter(r => r.id !== itemId)
    } else {
      favorites.value.ingredients = favorites.value.ingredients.filter(i => i.id !== itemId)
    }
  } catch (error) {
    console.error('Error removing from favorites:', error)
  }
}

const selectRecipe = (recipe: any) => {
  emit('select-recipe', recipe)
}

const selectIngredient = (ingredient: any) => {
  emit('select-ingredient', ingredient)
}

const getCategoryIcon = (category: string) => {
  const icons = {
    breakfast: '☀️',
    lunch: '🍽️',
    dinner: '🌙',
    snacks: '🍓',
    specialty: '✨',
    superfoods: '⭐',
    traditional: '🥛',
    liquid_cup: '🥤',
    powder: '🥄',
    fruits_berries: '🍓',
    seeds_nuts: '🥜',
    spices_herbs: '🌿',
    bee_products: '🍯',
    detox: '🌊'
  }
  return icons[category] || '🔹'
}

const getCategoryName = (category: string) => {
  const names = {
    breakfast: 'Śniadania',
    lunch: 'Obiady', 
    dinner: 'Kolacje',
    snacks: 'Przekąski',
    specialty: 'Specjalistyczne',
    superfoods: 'Superfoods',
    traditional: 'Tradycyjne',
    liquid_cup: 'Płynne kubeczki',
    powder: 'Proszki',
    fruits_berries: 'Owoce',
    seeds_nuts: 'Nasiona',
    spices_herbs: 'Przyprawy',
    bee_products: 'Produkty pszczele',
    detox: 'Detoks'
  }
  return names[category] || category
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now.getTime() - date.getTime())
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 1) return 'wczoraj'
  if (diffDays === 2) return '2 dni temu'
  if (diffDays < 7) return `${diffDays} dni temu`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} tygodni temu`
  return date.toLocaleDateString('pl-PL')
}

// Lifecycle
onMounted(() => {
  fetchFavorites()
})
</script> 