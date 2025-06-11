<template>
  <div class="bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 rounded-xl shadow-sm border border-green-200 dark:border-green-700 p-6">
    
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center">
        <div class="w-10 h-10 bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl flex items-center justify-center mr-3">
          <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
        <div>
          <h3 class="text-xl font-bold text-green-800 dark:text-green-300">🌍 Eco Impact Dashboard</h3>
          <p class="text-sm text-green-600 dark:text-green-400">Your positive environmental footprint</p>
        </div>
      </div>
      
      <!-- Eco Level -->
      <div class="bg-green-100 dark:bg-green-800 rounded-lg px-4 py-2">
        <div class="text-green-800 dark:text-green-200 text-center">
          <div class="text-lg font-bold">Eco Warrior</div>
          <div class="text-xs">Level {{ ecoLevel }}</div>
        </div>
      </div>
    </div>

    <!-- This Week's Impact -->
    <div class="bg-white dark:bg-gray-800 rounded-lg p-4 mb-6 border border-green-200 dark:border-green-700">
      <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
        <span class="mr-2">📊</span> This Week's Impact
      </h4>
      
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <!-- CO2 Saved -->
        <div class="text-center">
          <div class="text-2xl font-bold text-green-600 dark:text-green-400">{{ co2Saved }}kg</div>
          <div class="text-xs text-gray-500 dark:text-gray-400">CO₂ Saved</div>
          <div class="text-xs text-green-600 dark:text-green-400">vs fast food</div>
        </div>
        
        <!-- Water Saved -->
        <div class="text-center">
          <div class="text-2xl font-bold text-blue-600 dark:text-blue-400">{{ waterSaved }}L</div>
          <div class="text-xs text-gray-500 dark:text-gray-400">Water Saved</div>
          <div class="text-xs text-blue-600 dark:text-blue-400">sustainable farming</div>
        </div>
        
        <!-- Local Sourcing -->
        <div class="text-center">
          <div class="text-2xl font-bold text-orange-600 dark:text-orange-400">{{ localSourcing }}%</div>
          <div class="text-xs text-gray-500 dark:text-gray-400">Local Ingredients</div>
          <div class="text-xs text-orange-600 dark:text-orange-400">< 50km radius</div>
        </div>
        
        <!-- Plastic Avoided -->
        <div class="text-center">
          <div class="text-2xl font-bold text-purple-600 dark:text-purple-400">{{ plasticAvoided }}</div>
          <div class="text-xs text-gray-500 dark:text-gray-400">Plastic Items</div>
          <div class="text-xs text-purple-600 dark:text-purple-400">biodegradable only</div>
        </div>
      </div>
    </div>

    <!-- Sustainability Challenges -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
      
      <!-- Weekly Challenge -->
      <div class="bg-gradient-to-br from-green-100 to-emerald-100 dark:from-green-800/50 dark:to-emerald-800/50 rounded-lg p-4 border border-green-300 dark:border-green-600">
        <div class="flex items-center justify-between mb-3">
          <h5 class="font-semibold text-green-800 dark:text-green-300">🌱 Weekly Challenge</h5>
          <span class="bg-green-200 dark:bg-green-700 text-green-800 dark:text-green-200 px-2 py-1 rounded-full text-xs font-medium">
            {{ daysLeft }} days left
          </span>
        </div>
        <p class="text-sm text-green-700 dark:text-green-300 mb-3">Try 5 seasonal ingredients this week</p>
        <div class="flex items-center justify-between">
          <div class="text-xs text-green-600 dark:text-green-400">Progress: {{ seasonalProgress }}/5</div>
          <div class="text-green-700 dark:text-green-300 text-xs font-medium">🏆 +150 XP</div>
        </div>
        <div class="mt-2 bg-green-200 dark:bg-green-700 rounded-full h-2">
          <div class="bg-green-500 rounded-full h-2" :style="{ width: (seasonalProgress / 5) * 100 + '%' }"></div>
        </div>
      </div>

      <!-- Carbon Footprint Challenge -->
      <div class="bg-gradient-to-br from-blue-100 to-cyan-100 dark:from-blue-800/50 dark:to-cyan-800/50 rounded-lg p-4 border border-blue-300 dark:border-blue-600">
        <div class="flex items-center justify-between mb-3">
          <h5 class="font-semibold text-blue-800 dark:text-blue-300">⚡ Carbon Challenge</h5>
          <span class="bg-blue-200 dark:bg-blue-700 text-blue-800 dark:text-blue-200 px-2 py-1 rounded-full text-xs font-medium">
            Monthly
          </span>
        </div>
        <p class="text-sm text-blue-700 dark:text-blue-300 mb-3">Reduce your footprint by 25kg CO₂</p>
        <div class="flex items-center justify-between">
          <div class="text-xs text-blue-600 dark:text-blue-400">Progress: {{ carbonProgress }}kg/25kg</div>
          <div class="text-blue-700 dark:text-blue-300 text-xs font-medium">🌍 +300 XP</div>
        </div>
        <div class="mt-2 bg-blue-200 dark:bg-blue-700 rounded-full h-2">
          <div class="bg-blue-500 rounded-full h-2" :style="{ width: (carbonProgress / 25) * 100 + '%' }"></div>
        </div>
      </div>
    </div>

    <!-- Ingredient Impact Tracker -->
    <div class="bg-white dark:bg-gray-800 rounded-lg p-4 mb-6 border border-green-200 dark:border-green-700">
      <h4 class="font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
        <span class="mr-2">🌾</span> Your Sustainable Choices This Month
      </h4>
      
      <div class="space-y-3">
        <div v-for="choice in sustainableChoices" :key="choice.id" class="flex items-center justify-between">
          <div class="flex items-center">
            <div class="w-10 h-10 rounded-lg mr-3 flex items-center justify-center" :class="choice.bgColor">
              <span class="text-lg">{{ choice.emoji }}</span>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-900 dark:text-white">{{ choice.ingredient }}</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">{{ choice.impact }}</p>
            </div>
          </div>
          <div class="text-right">
            <div class="text-sm font-semibold text-green-600 dark:text-green-400">{{ choice.savings }}</div>
            <div class="text-xs text-gray-500 dark:text-gray-400">CO₂ saved</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Environmental Tips -->
    <div class="bg-gradient-to-r from-emerald-100 to-green-100 dark:from-emerald-800/30 dark:to-green-800/30 rounded-lg p-4 border border-emerald-200 dark:border-emerald-700">
      <h4 class="text-sm font-medium text-emerald-800 dark:text-emerald-300 mb-3 flex items-center">
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
        </svg>
        Eco Tips for Today
      </h4>
      <div class="space-y-2">
        <p v-for="tip in ecoTips" :key="tip" class="text-xs text-emerald-700 dark:text-emerald-300">
          • {{ tip }}
        </p>
      </div>
    </div>

    <!-- Social Impact -->
    <div class="mt-6 bg-gradient-to-r from-purple-100 to-pink-100 dark:from-purple-800/30 dark:to-pink-800/30 rounded-lg p-4 border border-purple-200 dark:border-purple-700">
      <h4 class="font-semibold text-gray-900 dark:text-white mb-3 flex items-center">
        <span class="mr-2">🤝</span> Community Impact
      </h4>
      
      <div class="grid grid-cols-3 gap-4 text-center">
        <div>
          <div class="text-lg font-bold text-purple-600 dark:text-purple-400">{{ communityOrders }}</div>
          <div class="text-xs text-gray-500 dark:text-gray-400">Community Orders</div>
        </div>
        <div>
          <div class="text-lg font-bold text-pink-600 dark:text-pink-400">{{ farmersSupported }}</div>
          <div class="text-xs text-gray-500 dark:text-gray-400">Local Farmers</div>
        </div>
        <div>
          <div class="text-lg font-bold text-indigo-600 dark:text-indigo-400">{{ treesPlanted }}</div>
          <div class="text-xs text-gray-500 dark:text-gray-400">Trees Planted</div>
        </div>
      </div>
      
      <div class="mt-3 text-center">
        <p class="text-xs text-gray-600 dark:text-gray-400">
          Your choices help support sustainable agriculture and local communities! 🌱
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// Reactive data
const ecoLevel = ref(7)
const co2Saved = ref(23.7)
const waterSaved = ref(145)
const localSourcing = ref(73)
const plasticAvoided = ref(12)
const daysLeft = ref(4)
const seasonalProgress = ref(3)
const carbonProgress = ref(18.3)
const communityOrders = ref(1247)
const farmersSupported = ref(15)
const treesPlanted = ref(89)

// Sustainable choices this month
const sustainableChoices = ref([
  {
    id: 1,
    ingredient: "Quinoa Organic",
    impact: "Low water usage, regenerative farming",
    savings: "2.3kg",
    emoji: "🌾",
    bgColor: "bg-yellow-100 dark:bg-yellow-800"
  },
  {
    id: 2,
    ingredient: "Local Spinach",
    impact: "15km transport, seasonal",
    savings: "1.8kg",
    emoji: "🥬",
    bgColor: "bg-green-100 dark:bg-green-800"
  },
  {
    id: 3,
    ingredient: "Hemp Seeds",
    impact: "Carbon-negative crop, soil restoration",
    savings: "3.1kg",
    emoji: "🌱",
    bgColor: "bg-emerald-100 dark:bg-emerald-800"
  },
  {
    id: 4,
    ingredient: "Coconut Water",
    impact: "Sustainable packaging, fair trade",
    savings: "1.2kg",
    emoji: "🥥",
    bgColor: "bg-blue-100 dark:bg-blue-800"
  }
])

// Eco tips
const ecoTips = ref([
  "Choose seasonal ingredients for lower carbon footprint",
  "Local sourcing reduces transportation emissions by 60%",
  "Plant-based proteins use 90% less water than animal proteins",
  "Biodegradable packaging breaks down in 90 days vs 1000 years",
  "Supporting local farmers strengthens community resilience"
])
</script> 