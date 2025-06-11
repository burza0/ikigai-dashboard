<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 lg:p-6">
    
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center">
        <div class="w-8 h-8 bg-purple-100 dark:bg-purple-900 rounded-lg flex items-center justify-center mr-3">
          <svg class="w-4 h-4 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
          </svg>
        </div>
        <div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">🤖 Smart Suggestions</h3>
          <p class="text-sm text-gray-500 dark:text-gray-400">AI-powered recommendations dla Twojej kompozycji</p>
        </div>
      </div>
      
      <!-- Refresh Button -->
      <button 
        @click="refreshSuggestions"
        :disabled="loading"
        class="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
      >
        <svg class="w-5 h-5" :class="{ 'animate-spin': loading }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
        </svg>
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="space-y-4">
      <div class="animate-pulse">
        <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/4 mb-2"></div>
        <div class="space-y-2">
          <div class="h-3 bg-gray-200 dark:bg-gray-700 rounded w-full"></div>
          <div class="h-3 bg-gray-200 dark:bg-gray-700 rounded w-3/4"></div>
        </div>
      </div>
    </div>

    <!-- Suggestions Content -->
    <div v-else-if="suggestions" class="space-y-6">
      
      <!-- AI Tips -->
      <div v-if="suggestions.ai_tips?.length" class="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-lg p-4">
        <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-3 flex items-center">
          <span class="mr-2">🧠</span>
          AI Tips & Insights
        </h4>
        <div class="space-y-2">
          <div 
            v-for="(tip, index) in suggestions.ai_tips" 
            :key="index"
            class="text-sm text-gray-700 dark:text-gray-300 flex items-start"
          >
            <span class="text-blue-500 mr-2 mt-0.5">•</span>
            <span>{{ tip }}</span>
          </div>
        </div>
      </div>

      <!-- Complementary Ingredients -->
      <div v-if="suggestions.complementary_ingredients?.length">
        <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-3 flex items-center">
          <span class="mr-2">✨</span>
          Polecane składniki
          <span class="ml-2 px-2 py-1 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 text-xs rounded-full">
            AI Powered
          </span>
        </h4>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div 
            v-for="ingredient in suggestions.complementary_ingredients" 
            :key="ingredient.id"
            class="bg-gray-50 dark:bg-gray-700 rounded-lg p-3 border border-gray-200 dark:border-gray-600 hover:shadow-md transition-shadow cursor-pointer"
            @click="addIngredient(ingredient)"
          >
            <div class="flex items-center justify-between mb-2">
              <h5 class="font-medium text-gray-900 dark:text-white text-sm">{{ ingredient.name }}</h5>
              <div class="flex items-center text-xs text-gray-500 dark:text-gray-400">
                <span class="mr-1">🎯</span>
                {{ ingredient.confidence }}%
              </div>
            </div>
            
            <p class="text-xs text-gray-600 dark:text-gray-400 mb-2">{{ ingredient.reason }}</p>
            
            <div class="flex items-center justify-between">
              <span class="text-sm font-semibold text-green-600 dark:text-green-400">{{ ingredient.price.toFixed(2) }} PLN</span>
              <button class="px-2 py-1 bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300 text-xs rounded hover:bg-purple-200 dark:hover:bg-purple-800 transition-colors">
                + Dodaj
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Similar Recipes -->
      <div v-if="suggestions.similar_recipes?.length">
        <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-3 flex items-center">
          <span class="mr-2">🔄</span>
          Podobne przepisy
        </h4>
        
        <div class="space-y-3">
          <div 
            v-for="recipe in suggestions.similar_recipes" 
            :key="recipe.id"
            class="bg-gray-50 dark:bg-gray-700 rounded-lg p-3 border border-gray-200 dark:border-gray-600 hover:shadow-md transition-shadow cursor-pointer"
            @click="loadRecipe(recipe)"
          >
            <div class="flex items-center justify-between mb-2">
              <h5 class="font-medium text-gray-900 dark:text-white">{{ recipe.name }}</h5>
              <div class="flex items-center space-x-2 text-xs">
                <span class="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 rounded">
                  {{ recipe.similarity }}% match
                </span>
                <span class="px-2 py-1 bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 rounded">
                  Health {{ recipe.health_score }}
                </span>
              </div>
            </div>
            
            <div class="flex items-center justify-between">
              <span class="text-sm font-semibold text-green-600 dark:text-green-400">{{ recipe.price.toFixed(2) }} PLN</span>
              <button class="px-3 py-1 bg-indigo-100 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-300 text-xs rounded hover:bg-indigo-200 dark:hover:bg-indigo-800 transition-colors">
                Użyj przepisu
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-8">
      <div class="w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
        </svg>
      </div>
      <p class="text-gray-500 dark:text-gray-400 text-sm">Zacznij dodawać składniki aby otrzymać inteligentne sugestie</p>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, defineProps, defineEmits } from 'vue'
import axios from 'axios'

// Props
const props = defineProps<{
  selectedIngredients: Array<any>
  context: string
}>()

// Emits
const emit = defineEmits<{
  'add-ingredient': (ingredient: any) => void
  'load-recipe': (recipe: any) => void
}>()

// Reactive data
const suggestions = ref(null)
const loading = ref(false)

// Watch for ingredient changes
watch(() => props.selectedIngredients, async (newIngredients) => {
  if (newIngredients.length > 0) {
    await fetchSuggestions()
  } else {
    suggestions.value = null
  }
}, { deep: true })

// Methods
const fetchSuggestions = async () => {
  if (props.selectedIngredients.length === 0) {
    suggestions.value = null
    return
  }

  try {
    loading.value = true
    
    const response = await axios.post('http://localhost:5001/api/suggestions/smart', {
      ingredients: props.selectedIngredients.map(ing => ing.id),
      context: props.context
    })
    
    if (response.data.status === 'success') {
      suggestions.value = response.data.data
    }
  } catch (error) {
    console.error('Error fetching suggestions:', error)
    // Mock data jako fallback
    suggestions.value = {
      complementary_ingredients: [
        {
          id: "spirulina_powder",
          name: "Spirulina Powder BIO", 
          reason: "Doskonale komponuje się z proteinami",
          confidence: 92,
          price: 4.50
        }
      ],
      similar_recipes: [
        {
          id: "energetic_morning",
          name: "Energetyczny Start Dnia",
          similarity: 89,
          health_score: 94,
          price: 16.60
        }
      ],
      ai_tips: [
        "💡 Dodaj spirulinę dla dodatkowych witamin B12",
        "🌱 Ta kombinacja zapewni energię na 4-5 godzin"
      ]
    }
  } finally {
    loading.value = false
  }
}

const refreshSuggestions = async () => {
  await fetchSuggestions()
}

const addIngredient = (ingredient: any) => {
  emit('add-ingredient', ingredient)
}

const loadRecipe = (recipe: any) => {
  emit('load-recipe', recipe)
}
</script> 