<template>
  <div class="max-w-7xl mx-auto p-6 space-y-6">
    
    <!-- Breadcrumb Navigation -->
    <div class="flex items-center text-sm text-gray-600 dark:text-gray-400 mb-4">
      <button @click="$emit('navigate', 'dashboard')" class="hover:text-purple-600 dark:hover:text-purple-400 transition-colors duration-200">
        🏠 Dashboard
      </button>
      <span class="mx-2">/</span>
      <span class="text-purple-600 dark:text-purple-400 font-medium">🏆 Program Lojalnościowy</span>
    </div>
    
    <!-- Header -->
    <div class="bg-gradient-to-r from-orange-500 to-orange-600 rounded-xl p-8 text-white">
      <div class="flex items-center mb-4">
        <div class="w-12 h-12 mr-4 bg-white rounded-full flex items-center justify-center">
          <span class="text-2xl">🏆</span>
        </div>
        <div>
          <h1 class="text-3xl font-bold">Program Lojalnościowy IKIGAI</h1>
          <p class="text-orange-100 mt-2">Zbieraj punkty, podejmuj wyzwania, zyskuj nagrody za zdrowy styl życia</p>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <!-- LEWA KOLUMNA: Profil i Postęp -->
      <div class="lg:col-span-1 space-y-6">
        
        <!-- Profil Użytkownika -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
            <span class="text-2xl mr-3">👤</span>
            Twój Profil IKIGAI
          </h3>
          
          <div v-if="loyaltyProfile" class="space-y-4">
            <!-- Aktualny poziom -->
            <div class="text-center p-4 bg-gradient-to-r from-purple-100 to-orange-100 dark:from-purple-900 dark:to-orange-900 rounded-lg">
              <div class="text-3xl mb-2">{{ currentLevel?.badge }}</div>
              <div class="font-bold text-gray-900 dark:text-white">{{ currentLevel?.name }}</div>
              <div class="text-sm text-gray-600 dark:text-gray-400 mt-2">
                {{ loyaltyProfile.points }} / {{ nextLevel?.points_required || '∞' }} punktów
              </div>
            </div>
            
            <!-- Pasek postępu do następnego poziomu -->
            <div v-if="nextLevel" class="space-y-2">
              <div class="flex justify-between text-sm text-gray-600 dark:text-gray-400">
                <span>Postęp do następnego poziomu</span>
                <span>{{ pointsToNextLevel }} punktów</span>
              </div>
              <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                <div class="bg-gradient-to-r from-orange-500 to-purple-500 h-3 rounded-full transition-all duration-300" 
                     :style="{ width: `${levelProgress}%` }">
                </div>
              </div>
            </div>
            
            <!-- Korzyści aktualnego poziomu -->
            <div>
              <h4 class="font-semibold text-gray-900 dark:text-white mb-2">🎁 Twoje korzyści</h4>
              <div class="space-y-1">
                <div v-for="benefit in currentLevel?.benefits" :key="benefit"
                     class="text-sm text-gray-600 dark:text-gray-400 bg-green-50 dark:bg-green-900/20 px-3 py-2 rounded-lg flex items-center">
                  <span class="text-green-600 mr-2">✓</span>
                  {{ benefit }}
                </div>
              </div>
            </div>
            
            <!-- Odznaki -->
            <div>
              <h4 class="font-semibold text-gray-900 dark:text-white mb-2">🏅 Odznaki</h4>
              <div class="flex flex-wrap gap-2">
                <span v-for="badge in loyaltyProfile.badges" :key="badge"
                      class="text-2xl p-2 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-700">
                  {{ badge }}
                </span>
              </div>
            </div>
            
            <!-- Statystyki -->
            <div class="grid grid-cols-2 gap-4 pt-4 border-t border-gray-200 dark:border-gray-700">
              <div class="text-center">
                <div class="text-xl font-bold text-gray-900 dark:text-white">{{ loyaltyProfile.total_orders }}</div>
                <div class="text-xs text-gray-600 dark:text-gray-400">Zamówienia</div>
              </div>
              <div class="text-center">
                <div class="text-xl font-bold text-gray-900 dark:text-white">{{ loyaltyProfile.total_spent?.toFixed(2) }}zł</div>
                <div class="text-xs text-gray-600 dark:text-gray-400">Wydane</div>
              </div>
            </div>
          </div>
          
          <div v-else class="text-center py-8 text-gray-500">
            <div class="text-4xl mb-4">🔄</div>
            <p>Ładowanie profilu...</p>
          </div>
        </div>
        
        <!-- Szybkie akcje -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">⚡ Szybkie akcje</h3>
          
          <div class="space-y-3">
            <li class="flex items-center text-base text-gray-700 dark:text-gray-300">
              <span class="mr-2">🥣</span> Skomponuj bowl (+punkty)
            </li>
            <button @click="simulateOrder" 
                    class="w-full bg-green-500 hover:bg-green-600 text-white py-3 px-4 rounded-lg transition-colors duration-200 flex items-center justify-center">
              <span class="mr-2">🎯</span> Symuluj zamówienie
            </button>
            <button @click="refreshData" 
                    class="w-full bg-blue-500 hover:bg-blue-600 text-white py-3 px-4 rounded-lg transition-colors duration-200 flex items-center justify-center">
              <span class="mr-2">🔄</span> Odśwież dane
            </button>
          </div>
        </div>
      </div>
      
      <!-- ŚRODKOWA KOLUMNA: Wyzwania -->
      <div class="lg:col-span-1 space-y-6">
        
        <!-- Wyzwania tygodniowe -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
            <span class="text-2xl mr-3">🎯</span>
            Wyzwania Tygodniowe
          </h3>
          
          <div v-if="userChallenges.length > 0" class="space-y-4">
            <div v-for="challengeData in userChallenges" :key="challengeData.challenge.id"
                 class="border border-gray-200 dark:border-gray-600 rounded-lg p-4">
              
              <div class="flex items-start justify-between mb-3">
                <div class="flex-1">
                  <div class="flex items-center mb-2">
                    <span class="text-2xl mr-2">{{ challengeData.challenge.icon }}</span>
                    <h4 class="font-semibold text-gray-900 dark:text-white">{{ challengeData.challenge.name }}</h4>
                  </div>
                  <p class="text-sm text-gray-600 dark:text-gray-400">{{ challengeData.challenge.description }}</p>
                </div>
                <div :class="[
                  'px-2 py-1 rounded-full text-xs font-medium',
                  challengeData.challenge.difficulty === 'easy' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' :
                  challengeData.challenge.difficulty === 'medium' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200' :
                  'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                ]">
                  {{ challengeData.challenge.difficulty }}
                </div>
              </div>
              
              <!-- Postęp -->
              <div class="space-y-2">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600 dark:text-gray-400">
                    Postęp: {{ challengeData.progress }}/{{ challengeData.challenge.target }}
                  </span>
                  <span class="text-orange-600 dark:text-orange-400 font-medium">
                    {{ challengeData.challenge.reward_points }} punktów
                  </span>
                </div>
                
                <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div :class="[
                    'h-2 rounded-full transition-all duration-300',
                    challengeData.completed ? 'bg-green-500' : 'bg-orange-500'
                  ]" :style="{ width: `${(challengeData.progress / challengeData.challenge.target) * 100}%` }">
                  </div>
                </div>
                
                <div v-if="challengeData.completed" class="flex items-center text-green-600 dark:text-green-400 text-sm">
                  <span class="mr-1">✅</span> Ukończone!
                </div>
                
                <div v-else class="text-xs text-gray-500 dark:text-gray-500">
                  Wygasa: {{ formatDate(challengeData.expires_date) }}
                </div>
              </div>
            </div>
          </div>
          
          <div v-else class="text-center py-8 text-gray-500">
            <div class="text-4xl mb-4">🎯</div>
            <p>Brak aktywnych wyzwań</p>
            <button @click="loadChallenges" class="mt-4 text-orange-600 hover:text-orange-700 text-sm">
              Wczytaj wyzwania
            </button>
          </div>
        </div>
      </div>
      
      <!-- PRAWA KOLUMNA: Sklep nagród -->
      <div class="lg:col-span-1 space-y-6">
        
        <!-- Sklep nagród -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
            <span class="text-2xl mr-3">🏪</span>
            Sklep Nagród
          </h3>
          
          <div v-if="rewardsShop.length > 0" class="space-y-4">
            <div v-for="reward in rewardsShop" :key="reward.id"
                 class="border border-gray-200 dark:border-gray-600 rounded-lg p-4">
              
              <div class="flex items-start justify-between mb-3">
                <div class="flex items-center">
                  <span class="text-2xl mr-3">{{ reward.icon }}</span>
                  <div>
                    <h4 class="font-semibold text-gray-900 dark:text-white">{{ reward.name }}</h4>
                    <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">{{ reward.description }}</p>
                  </div>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <div class="text-lg font-bold text-orange-600 dark:text-orange-400">
                  {{ reward.points_cost }} punktów
                </div>
                <button @click="redeemReward(reward)" 
                        :disabled="!loyaltyProfile || loyaltyProfile.points < reward.points_cost"
                        :class="[
                          'px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200',
                          loyaltyProfile && loyaltyProfile.points >= reward.points_cost
                            ? 'bg-orange-500 hover:bg-orange-600 text-white'
                            : 'bg-gray-300 dark:bg-gray-600 text-gray-500 dark:text-gray-400 cursor-not-allowed'
                        ]">
                  <span v-if="loyaltyProfile && loyaltyProfile.points >= reward.points_cost">🎁 Wymień</span>
                  <span v-else>💸 Za mało punktów</span>
                </button>
              </div>
            </div>
          </div>
          
          <div v-else class="text-center py-8 text-gray-500">
            <div class="text-4xl mb-4">🏪</div>
            <p>Ładowanie sklepu...</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Alert sukcesu -->
    <div v-if="successMessage" 
         class="fixed bottom-6 right-6 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 flex items-center">
      <span class="text-xl mr-3">🎉</span>
      <span>{{ successMessage }}</span>
      <button @click="successMessage = ''" class="ml-4 text-white hover:text-gray-200">✕</button>
    </div>
    
    <!-- Alert poziomu -->
    <div v-if="levelUpMessage" 
         class="fixed top-6 left-1/2 transform -translate-x-1/2 bg-gradient-to-r from-purple-500 to-orange-500 text-white px-6 py-4 rounded-lg shadow-lg z-50 flex items-center">
      <span class="text-2xl mr-3">🎊</span>
      <div>
        <div class="font-bold">Gratulacje! Awans na poziom {{ newLevel }}!</div>
        <div class="text-sm opacity-90">{{ levelUpMessage }}</div>
      </div>
      <button @click="levelUpMessage = ''" class="ml-4 text-white hover:text-gray-200">✕</button>
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
const loyaltyProfile = ref(null)
const currentLevel = ref(null)
const nextLevel = ref(null)
const userChallenges = ref([])
const rewardsShop = ref([])
const successMessage = ref('')
const levelUpMessage = ref('')
const newLevel = ref(0)

const userId = 'web_user' // ID użytkownika

// Computed properties
const pointsToNextLevel = computed(() => {
  if (!nextLevel.value || !loyaltyProfile.value) return 0
  return nextLevel.value.points_required - loyaltyProfile.value.points
})

const levelProgress = computed(() => {
  if (!nextLevel.value || !loyaltyProfile.value || !currentLevel.value) return 100
  
  const currentPoints = loyaltyProfile.value.points
  const currentLevelPoints = currentLevel.value.points_required
  const nextLevelPoints = nextLevel.value.points_required
  
  const progress = ((currentPoints - currentLevelPoints) / (nextLevelPoints - currentLevelPoints)) * 100
  return Math.min(Math.max(progress, 0), 100)
})

// Methods
const loadLoyaltyProfile = async () => {
  try {
    const response = await fetch(`http://localhost:5001/api/loyalty/profile/${userId}`)
    const data = await response.json()
    if (data.success) {
      loyaltyProfile.value = data.profile
      currentLevel.value = data.current_level
      nextLevel.value = data.next_level
    }
  } catch (error) {
    console.error('Błąd ładowania profilu lojalnościowego:', error)
  }
}

const loadChallenges = async () => {
  try {
    const response = await fetch(`http://localhost:5001/api/loyalty/challenges/${userId}`)
    const data = await response.json()
    if (data.success) {
      userChallenges.value = data.challenges
    }
  } catch (error) {
    console.error('Błąd ładowania wyzwań:', error)
  }
}

const loadRewardsShop = async () => {
  try {
    const response = await fetch('http://localhost:5001/api/loyalty/rewards')
    const data = await response.json()
    if (data.success) {
      rewardsShop.value = data.rewards
    }
  } catch (error) {
    console.error('Błąd ładowania sklepu nagród:', error)
  }
}

const redeemReward = async (reward) => {
  if (!loyaltyProfile.value || loyaltyProfile.value.points < reward.points_cost) {
    return
  }
  
  try {
    const response = await fetch('http://localhost:5001/api/loyalty/redeem', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: userId,
        reward_id: reward.id
      })
    })
    
    const data = await response.json()
    
    if (data.success) {
      successMessage.value = data.message
      loyaltyProfile.value.points = data.remaining_points
      
      // Ukryj komunikat po 3 sekundach
      setTimeout(() => {
        successMessage.value = ''
      }, 3000)
    } else {
      console.error('Błąd wymiany nagrody:', data.error)
    }
    
  } catch (error) {
    console.error('Błąd połączenia:', error)
  }
}

const simulateOrder = async () => {
  try {
    const orderAmount = Math.floor(Math.random() * 15) + 5 // 5-20 PLN
    
    const response = await fetch('http://localhost:5001/api/loyalty/points/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: userId,
        order_amount: orderAmount,
        reason: 'Symulowane zamówienie'
      })
    })
    
    const data = await response.json()
    
    if (data.success) {
      successMessage.value = `${data.message}! (${orderAmount}zł)`
      
      // Sprawdź awans na wyższy poziom
      if (data.level_up) {
        newLevel.value = data.new_level
        levelUpMessage.value = `Osiągnięto nowy poziom: ${data.new_level}!`
        
        setTimeout(() => {
          levelUpMessage.value = ''
        }, 5000)
      }
      
      // Odśwież profil
      await loadLoyaltyProfile()
      
      // Aktualizuj postęp wyzwań
      await updateChallengeProgress('healthy_week')
      
      setTimeout(() => {
        successMessage.value = ''
      }, 3000)
    }
    
  } catch (error) {
    console.error('Błąd symulacji zamówienia:', error)
  }
}

const updateChallengeProgress = async (challengeType) => {
  try {
    const response = await fetch('http://localhost:5001/api/loyalty/challenge/progress', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: userId,
        challenge_type: challengeType
      })
    })
    
    const data = await response.json()
    
    if (data.success && data.completed_challenges.length > 0) {
      for (const completed of data.completed_challenges) {
        successMessage.value = `🎯 Ukończono wyzwanie: ${completed.challenge.name}! +${completed.reward_points} punktów`
      }
      
      // Odśwież wyzwania
      await loadChallenges()
    }
    
  } catch (error) {
    console.error('Błąd aktualizacji wyzwań:', error)
  }
}

const refreshData = async () => {
  await Promise.all([
    loadLoyaltyProfile(),
    loadChallenges(),
    loadRewardsShop()
  ])
  successMessage.value = 'Dane zostały odświeżone!'
  setTimeout(() => {
    successMessage.value = ''
  }, 2000)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('pl-PL', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Lifecycle
onMounted(async () => {
  await Promise.all([
    loadLoyaltyProfile(),
    loadChallenges(),
    loadRewardsShop()
  ])
})
</script>

<style scoped>
/* Custom animations */
.transition-all {
  transition: all 0.2s ease;
}

/* Gradient text */
.bg-clip-text {
  -webkit-background-clip: text;
  background-clip: text;
}
</style> 