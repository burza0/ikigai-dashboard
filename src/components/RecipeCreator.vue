<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 mb-6 lg:mb-8">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16 lg:h-20">
          <div class="flex items-center">
            <button 
              @click="$emit('navigate', 'dashboard')"
              class="mr-4 p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
            </button>
            <h1 class="text-xl lg:text-2xl font-bold text-gray-900 dark:text-white">🍽️ Kreator Przepisów IKIGAI</h1>
          </div>
          
          <!-- Header Stats -->
          <div class="hidden sm:flex items-center space-x-4 lg:space-x-6">
            <div class="text-center">
              <div class="text-lg lg:text-xl font-bold text-purple-600">{{ recipeStats.ready }}</div>
              <div class="text-xs lg:text-sm text-gray-500">Gotowe przepisy</div>
            </div>
            <div class="text-center">
              <div class="text-lg lg:text-xl font-bold text-blue-600">{{ recipeStats.ingredients }}</div>
              <div class="text-xs lg:text-sm text-gray-500">Składniki</div>
            </div>
            <div class="text-center">
              <div class="text-lg lg:text-xl font-bold text-green-600">{{ savedCompositions.length }}</div>
              <div class="text-xs lg:text-sm text-gray-500">Zapisane</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tab Navigation -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-6 lg:mb-8">
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-2">
        <div class="grid grid-cols-2 gap-2">
          <button 
            @click="activeTab = 'recipes'"
            :class="[
              'flex items-center justify-center py-3 lg:py-4 px-4 lg:px-6 rounded-lg font-medium text-sm lg:text-base transition-all duration-200',
              activeTab === 'recipes' 
                ? 'bg-purple-100 text-purple-700 shadow-sm' 
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700'
            ]"
          >
            <span class="text-xl lg:text-2xl mr-2 lg:mr-3">🍽️</span>
            <span>Gotowe Przepisy</span>
            <span v-if="recipeStats.ready > 0" class="ml-2 px-2 py-1 bg-white rounded-full text-xs lg:text-sm">{{ recipeStats.ready }}</span>
          </button>
          
          <button 
            @click="activeTab = 'custom'"
            :class="[
              'flex items-center justify-center py-3 lg:py-4 px-4 lg:px-6 rounded-lg font-medium text-sm lg:text-base transition-all duration-200',
              activeTab === 'custom' 
                ? 'bg-blue-100 text-blue-700 shadow-sm' 
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700'
            ]"
          >
            <span class="text-xl lg:text-2xl mr-2 lg:mr-3">🎨</span>
            <span>Własna Kompozycja</span>
            <span v-if="savedCompositions.length > 0" class="ml-2 px-2 py-1 bg-white rounded-full text-xs lg:text-sm">{{ savedCompositions.length }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Tab Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-8">
      <!-- Ready Recipes Tab -->
      <div v-if="activeTab === 'recipes'">
        <RecipeGrid 
          :recipes="recipes"
          :categories="recipeCategories"
          :loading="loadingRecipes"
          @select-recipe="showRecipeModal"
          @order-recipe="handleOrderRecipe"
        />
      </div>

      <!-- Custom Composition Tab -->
      <div v-if="activeTab === 'custom'">
        <CustomComposition 
          v-model:saved-compositions="savedCompositions"
        />
      </div>
    </div>

    <!-- Recipe Modal -->
    <RecipeModal 
      v-if="selectedRecipe"
      :recipe="selectedRecipe"
      @close="selectedRecipe = null"
      @order="handleOrderRecipe"
    />

    <!-- Success Toast -->
    <div v-if="toast.show" 
         :class="[
           'fixed top-4 right-4 z-50 p-4 rounded-xl shadow-lg transition-all duration-300',
           toast.type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
         ]">
      <div class="flex items-center">
        <span class="text-xl mr-2">{{ toast.type === 'success' ? '✅' : '❌' }}</span>
        <span class="font-medium">{{ toast.message }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive, computed } from 'vue'
import axios from 'axios'
import RecipeGrid from './RecipeCreator/RecipeGrid.vue'
import CustomComposition from './RecipeCreator/CustomComposition.vue'
import RecipeModal from './RecipeCreator/RecipeModal.vue'

// Define emits
defineEmits<{
  'navigate': (view: string) => void
}>()

// Reactive state
const activeTab = ref('recipes')
const recipes = ref([])
const recipeCategories = ref({})
const loadingRecipes = ref(false)
const selectedRecipe = ref(null)
const savedCompositions = ref([])

// Toast notifications
const toast = reactive({
  show: false,
  type: 'success',
  message: ''
})

// Computed stats
const recipeStats = computed(() => ({
  ready: recipes.value.length,
  ingredients: 41, // Static for now, could be dynamic
  categories: Object.keys(recipeCategories.value).length
}))

// Methods
const showToast = (type: 'success' | 'error', message: string) => {
  toast.type = type
  toast.message = message
  toast.show = true
  
  setTimeout(() => {
    toast.show = false
  }, 4000)
}

const showRecipeModal = (recipe: any) => {
  selectedRecipe.value = recipe
}

const handleOrderRecipe = async (recipe: any) => {
  try {
    console.log('🛒 Zamawianie przepisu:', recipe.name)
    
    const orderData = {
      type: 'meal_recipe',
      recipe_id: recipe.id,
      name: recipe.name,
      total_price: recipe.total_price,
      total_calories: recipe.calories,
      base: recipe.base,
      toppings: recipe.toppings,
      custom_composition: false
    }
    
    const response = await axios.post('http://localhost:5001/api/orders', orderData)
    
    if (response.data.success) {
      showToast('success', `Zamówienie "${recipe.name}" zostało utworzone! QR: ${response.data.qr_code}`)
      selectedRecipe.value = null // Close modal
    } else {
      throw new Error(response.data.message || 'Błąd tworzenia zamówienia')
    }
  } catch (error) {
    console.error('❌ Błąd zamówienia:', error)
    showToast('error', `Błąd tworzenia zamówienia: ${error.message}`)
  }
}

const fetchRecipes = async () => {
  try {
    loadingRecipes.value = true
    
    // Fetch recipes and categories in parallel
    const [recipesResponse, categoriesResponse] = await Promise.all([
      axios.get('http://localhost:5001/api/meal-recipes'),
      axios.get('http://localhost:5001/api/meal-recipes/categories')
    ])
    
    recipes.value = recipesResponse.data.recipes || []
    recipeCategories.value = categoriesResponse.data.categories || {}
    
    console.log('📋 Przepisy załadowane:', {
      recipes: recipes.value.length,
      categories: Object.keys(recipeCategories.value).length
    })
    
  } catch (error) {
    console.error('❌ Błąd ładowania przepisów:', error)
    showToast('error', 'Błąd ładowania przepisów')
  } finally {
    loadingRecipes.value = false
  }
}

const loadSavedCompositions = () => {
  try {
    const saved = localStorage.getItem('ikigai_compositions')
    if (saved) {
      savedCompositions.value = JSON.parse(saved)
      console.log('💾 Wczytano kompozycje:', savedCompositions.value.length)
    }
  } catch (error) {
    console.error('❌ Błąd ładowania kompozycji:', error)
  }
}

// Lifecycle
onMounted(() => {
  fetchRecipes()
  loadSavedCompositions()
})
</script>

<style scoped>
.transition-all {
  transition: all 0.3s ease;
}
</style> 