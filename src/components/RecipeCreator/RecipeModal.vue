<template>
  <div 
    @click="$emit('close')"
    class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4"
  >
    <div 
      @click.stop 
      class="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto"
    >
      <!-- Header -->
      <div class="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 rounded-t-2xl">
        <div class="flex items-center justify-between">
          <h2 class="text-2xl font-bold text-gray-900">{{ recipe.name }}</h2>
          <button 
            @click="$emit('close')"
            class="w-8 h-8 rounded-full bg-gray-100 hover:bg-gray-200 flex items-center justify-center transition-colors duration-200"
          >
            ✕
          </button>
        </div>
      </div>

      <!-- Content -->
      <div class="p-6 space-y-6">
        
        <!-- Quick Stats -->
        <div class="grid grid-cols-4 gap-4">
          <div class="text-center p-3 bg-purple-50 rounded-lg">
            <div class="text-lg font-bold text-purple-600">{{ recipe.total_price.toFixed(2) }}zł</div>
            <div class="text-xs text-gray-600">Cena</div>
          </div>
          <div class="text-center p-3 bg-green-50 rounded-lg">
            <div class="text-lg font-bold text-green-600">{{ recipe.health_score }}/100</div>
            <div class="text-xs text-gray-600">Health Score</div>
          </div>
          <div class="text-center p-3 bg-blue-50 rounded-lg">
            <div class="text-lg font-bold text-blue-600">{{ recipe.popularity }}%</div>
            <div class="text-xs text-gray-600">Popularność</div>
          </div>
          <div class="text-center p-3 bg-orange-50 rounded-lg">
            <div class="text-lg font-bold text-orange-600">{{ recipe.prep_time }}</div>
            <div class="text-xs text-gray-600">Czas przygot.</div>
          </div>
        </div>

        <!-- Description -->
        <div>
          <h3 class="font-semibold text-gray-900 mb-2">📝 Opis</h3>
          <p class="text-gray-700 leading-relaxed">{{ recipe.description }}</p>
        </div>

        <!-- Nutrition -->
        <div>
          <h3 class="font-semibold text-gray-900 mb-3">📊 Wartości odżywcze</h3>
          <div class="grid grid-cols-4 gap-3">
            <div class="text-center p-3 bg-gray-50 rounded-lg">
              <div class="text-lg font-bold text-orange-600">{{ recipe.nutrition.kcal }}</div>
              <div class="text-xs text-gray-600">kcal</div>
            </div>
            <div class="text-center p-3 bg-gray-50 rounded-lg">
              <div class="text-lg font-bold text-blue-600">{{ recipe.nutrition.protein }}g</div>
              <div class="text-xs text-gray-600">białko</div>
            </div>
            <div class="text-center p-3 bg-gray-50 rounded-lg">
              <div class="text-lg font-bold text-green-600">{{ recipe.nutrition.carbs }}g</div>
              <div class="text-xs text-gray-600">węglowodany</div>
            </div>
            <div class="text-center p-3 bg-gray-50 rounded-lg">
              <div class="text-lg font-bold text-yellow-600">{{ recipe.nutrition.fat }}g</div>
              <div class="text-xs text-gray-600">tłuszcze</div>
            </div>
          </div>
        </div>

        <!-- Ingredients -->
        <div>
          <h3 class="font-semibold text-gray-900 mb-3">🥄 Składniki</h3>
          
          <!-- Base -->
          <div class="mb-4">
            <h4 class="text-sm font-medium text-gray-700 mb-2">Baza:</h4>
            <div class="bg-purple-50 rounded-lg p-3">
              <span class="font-medium text-purple-700">{{ getBaseIngredientName(recipe.base) }}</span>
            </div>
          </div>
          
          <!-- Toppings -->
          <div>
            <h4 class="text-sm font-medium text-gray-700 mb-2">Dodatki ({{ recipe.toppings.length }}):</h4>
            <div class="grid grid-cols-2 gap-2">
              <div 
                v-for="topping in recipe.toppings" 
                :key="topping"
                class="bg-green-50 rounded-lg p-3 text-sm"
              >
                <span class="font-medium text-green-700">{{ getToppingName(topping) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Health Benefits -->
        <div>
          <h3 class="font-semibold text-gray-900 mb-3">💚 Korzyści zdrowotne</h3>
          <div class="flex flex-wrap gap-2">
            <span 
              v-for="benefit in recipe.health_benefits" 
              :key="benefit"
              class="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium"
            >
              {{ benefit }}
            </span>
          </div>
        </div>

        <!-- Best For -->
        <div v-if="recipe.best_for">
          <h3 class="font-semibold text-gray-900 mb-3">🎯 Idealne dla</h3>
          <div class="flex flex-wrap gap-2">
            <span 
              v-for="purpose in recipe.best_for" 
              :key="purpose"
              class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium"
            >
              {{ purpose }}
            </span>
          </div>
        </div>

        <!-- Preparation Instructions -->
        <div v-if="recipe.preparation">
          <h3 class="font-semibold text-gray-900 mb-3">👨‍🍳 Instrukcja przygotowania</h3>
          <div class="bg-gray-50 rounded-lg p-4">
            <p class="text-gray-700 leading-relaxed">{{ recipe.preparation }}</p>
          </div>
        </div>

        <!-- Difficulty Level -->
        <div>
          <h3 class="font-semibold text-gray-900 mb-3">📈 Poziom trudności</h3>
          <div class="flex items-center space-x-3">
            <div 
              :class="[
                'px-3 py-1 rounded-full text-sm font-medium',
                recipe.difficulty === 'easy' ? 'bg-green-100 text-green-700' :
                recipe.difficulty === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                'bg-red-100 text-red-700'
              ]"
            >
              {{ getDifficultyLabel(recipe.difficulty) }}
            </div>
            <span class="text-sm text-gray-600">
              {{ getDifficultyDescription(recipe.difficulty) }}
            </span>
          </div>
        </div>

      </div>

      <!-- Footer -->
      <div class="sticky bottom-0 bg-white border-t border-gray-200 px-6 py-4 rounded-b-2xl">
        <div class="flex items-center justify-between">
          <div class="text-sm text-gray-600">
            🏷️ {{ getCategoryName(recipe.category) }} • {{ recipe.prep_time }}
          </div>
          <div class="flex space-x-3">
            <button 
              @click="$emit('close')"
              class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg font-medium hover:bg-gray-200 transition-colors duration-200"
            >
              Zamknij
            </button>
            <button 
              @click="handleOrder"
              class="px-6 py-2 bg-purple-600 text-white rounded-lg font-medium hover:bg-purple-700 transition-colors duration-200"
            >
              🛒 Zamów za {{ recipe.total_price.toFixed(2) }}zł
            </button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

// Props
const props = defineProps<{
  recipe: any
}>()

// Emits
const emits = defineEmits<{
  close: () => void
  order: (recipe: any) => void
}>()

// Methods
const handleOrder = () => {
  emits('order', props.recipe)
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

const getDifficultyLabel = (difficulty: string) => {
  const labels = {
    easy: '🟢 Łatwy',
    medium: '🟡 Średni',
    hard: '🔴 Trudny'
  }
  return labels[difficulty] || difficulty
}

const getDifficultyDescription = (difficulty: string) => {
  const descriptions = {
    easy: 'Proste mieszanie składników',
    medium: 'Wymaga kolejności dodawania',
    hard: 'Precyzyjne proporcje i technika'
  }
  return descriptions[difficulty] || ''
}

const getBaseIngredientName = (baseId: string) => {
  const baseNames = {
    protein_vanilla: 'Protein Vanilla',
    spirulina_powder: 'Spirulina Powder',
    coconut_water: 'Woda Kokosowa Premium',
    golden_milk: 'Złote Mleko Kurkumowe',
    matcha_premium: 'Matcha Premium Grade A',
    kombucha_ginger: 'Kombucha Imbirowa BIO',
    collagen_marine: 'Kolagen Morski',
    aloe_vera_juice: 'Sok z Aloesu Vera',
    yogurt_greek: 'Jogurt Grecki',
    oatmeal_base: 'Owsianka BIO',
    lemon_ginger_water: 'Woda Cytrynowo-Imbirowa',
    smoothie_bowl: 'Smoothie Bowl Base'
  }
  return baseNames[baseId] || baseId
}

const getToppingName = (toppingId: string) => {
  const toppingNames = {
    goji_berries: 'Jagody Goji',
    maca_powder: 'Maca Powder',
    nuts_almonds: 'Migdały',
    honey_raw: 'Miód Surowy',
    cinnamon_ceylon: 'Cynamon Cejloński',
    chlorella_tablets: 'Chlorella w tabletkach',
    barley_grass: 'Trawa Jęczmienna',
    flax_seeds: 'Siemię Lniane',
    acai_powder: 'Acai Powder',
    coconut_flakes: 'Płatki Kokosowe',
    lucuma_powder: 'Lucuma Powder',
    banana_sliced: 'Plasterki Banana',
    bee_pollen: 'Pyłek Pszczeli',
    ashwagandha_powder: 'Ashwagandha Powder',
    turmeric_powder: 'Kurkuma BIO',
    ginger_dried: 'Imbir Kandyzowany',
    mct_oil: 'MCT Oil',
    moringa_powder: 'Moringa Powder',
    propolis_powder: 'Propolis Powder',
    pumpkin_seeds: 'Pestki Dyni',
    sunflower_seeds: 'Nasiona Słonecznika',
    chia_seeds: 'Nasiona Chia',
    hemp_hearts: 'Konopie Hearts',
    cacao_nibs: 'Ziarna Kakao',
    activated_charcoal: 'Węgiel Aktywny',
    baobab_powder: 'Baobab Powder',
    mulberries_white: 'Morwa Biała'
  }
  return toppingNames[toppingId] || toppingId
}
</script>

<style scoped>
/* Custom scrollbar for modal */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style> 