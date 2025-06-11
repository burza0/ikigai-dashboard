<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
    
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center">
        <div class="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center mr-3">
          <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.196-2.196M17 20H7m10 0v-2c0-2.037-.5-3.948-1.374-5.618M7 20H2v-2a3 3 0 015.196-2.196M7 20v-2c0-2.037.5-3.948 1.374-5.618m0 0A9.015 9.015 0 0115 5c0 .75-.11 1.475-.32 2.152M7 20c-1.657 0-3.158-.672-4.243-1.757A7.963 7.963 0 017 4c.75 0 1.475.11 2.152.32"></path>
          </svg>
        </div>
        <div>
          <h3 class="text-xl font-bold text-gray-900 dark:text-white">🔥 Social Challenges</h3>
          <p class="text-sm text-gray-500 dark:text-gray-400">Join the Gen Z health revolution</p>
        </div>
      </div>
      
      <!-- Streak Counter -->
      <div class="bg-gradient-to-r from-orange-400 to-red-500 rounded-lg px-4 py-2">
        <div class="text-white text-center">
          <div class="text-lg font-bold">{{ currentStreak }}</div>
          <div class="text-xs">Day Streak 🔥</div>
        </div>
      </div>
    </div>

    <!-- Active Challenge Banner -->
    <div class="bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg p-4 mb-6 text-white">
      <div class="flex items-center justify-between">
        <div>
          <h4 class="font-bold text-lg">#SustainabilityWeek Challenge</h4>
          <p class="text-sm opacity-90">Try 5 eco-friendly ingredients • 2 days left</p>
          <div class="mt-2">
            <div class="flex items-center">
              <div class="bg-white/20 rounded-full h-2 w-32 mr-2">
                <div class="bg-white rounded-full h-2" style="width: 60%"></div>
              </div>
              <span class="text-xs">3/5 completed</span>
            </div>
          </div>
        </div>
        <div class="text-right">
          <div class="text-2xl font-bold">🌱</div>
          <div class="text-xs">+50 points</div>
        </div>
      </div>
    </div>

    <!-- Challenge Categories -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
      
      <!-- Daily Challenge -->
      <div class="bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 rounded-lg p-4 border border-green-200 dark:border-green-800">
        <div class="flex items-center justify-between mb-3">
          <h5 class="font-semibold text-green-800 dark:text-green-300">🎯 Daily Goal</h5>
          <span class="bg-green-100 dark:bg-green-800 text-green-800 dark:text-green-200 px-2 py-1 rounded-full text-xs font-medium">
            Active
          </span>
        </div>
        <p class="text-sm text-gray-700 dark:text-gray-300 mb-3">Add 20g protein to your bowl</p>
        <div class="flex items-center justify-between">
          <div class="text-xs text-gray-500 dark:text-gray-400">Progress: 15g/20g</div>
          <div class="text-green-600 dark:text-green-400 text-xs font-medium">+25 XP</div>
        </div>
        <div class="mt-2 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div class="bg-green-500 rounded-full h-2" style="width: 75%"></div>
        </div>
      </div>

      <!-- Social Challenge -->
      <div class="bg-gradient-to-br from-pink-50 to-rose-50 dark:from-pink-900/20 dark:to-rose-900/20 rounded-lg p-4 border border-pink-200 dark:border-pink-800">
        <div class="flex items-center justify-between mb-3">
          <h5 class="font-semibold text-pink-800 dark:text-pink-300">📸 Viral Bowl</h5>
          <span class="bg-pink-100 dark:bg-pink-800 text-pink-800 dark:text-pink-200 px-2 py-1 rounded-full text-xs font-medium">
            Trending
          </span>
        </div>
        <p class="text-sm text-gray-700 dark:text-gray-300 mb-3">Share your colorful bowl on social</p>
        <div class="flex items-center justify-between">
          <div class="text-xs text-gray-500 dark:text-gray-400">{{ socialShares }} shares today</div>
          <div class="text-pink-600 dark:text-pink-400 text-xs font-medium">+100 XP</div>
        </div>
        <button class="mt-2 w-full bg-pink-500 text-white rounded-lg py-2 text-sm font-medium hover:bg-pink-600 transition-colors">
          📱 Share Bowl
        </button>
      </div>

      <!-- Environmental Challenge -->
      <div class="bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-blue-900/20 dark:to-cyan-900/20 rounded-lg p-4 border border-blue-200 dark:border-blue-800">
        <div class="flex items-center justify-between mb-3">
          <h5 class="font-semibold text-blue-800 dark:text-blue-300">🌍 Eco Warrior</h5>
          <span class="bg-blue-100 dark:bg-blue-800 text-blue-800 dark:text-blue-200 px-2 py-1 rounded-full text-xs font-medium">
            Weekly
          </span>
        </div>
        <p class="text-sm text-gray-700 dark:text-gray-300 mb-3">Save 10kg CO₂ this week</p>
        <div class="flex items-center justify-between">
          <div class="text-xs text-gray-500 dark:text-gray-400">{{ co2Saved }}kg saved</div>
          <div class="text-blue-600 dark:text-blue-400 text-xs font-medium">+200 XP</div>
        </div>
        <div class="mt-2 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div class="bg-blue-500 rounded-full h-2" :style="{ width: (co2Saved / 10) * 100 + '%' }"></div>
        </div>
      </div>
    </div>

    <!-- Friends Activity -->
    <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 mb-6">
      <h4 class="font-semibold text-gray-900 dark:text-white mb-3 flex items-center">
        <span class="mr-2">👥</span> Friends Activity
      </h4>
      
      <div class="space-y-3">
        <div v-for="activity in friendsActivity" :key="activity.id" class="flex items-center justify-between">
          <div class="flex items-center">
            <img :src="activity.avatar" :alt="activity.name" class="w-8 h-8 rounded-full mr-3">
            <div>
              <p class="text-sm font-medium text-gray-900 dark:text-white">{{ activity.name }}</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">{{ activity.action }}</p>
            </div>
          </div>
          <div class="text-right">
            <div class="text-sm font-semibold text-purple-600 dark:text-purple-400">{{ activity.points }}</div>
            <div class="text-xs text-gray-500 dark:text-gray-400">{{ activity.time }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Leaderboard Preview -->
    <div class="bg-gradient-to-r from-yellow-50 to-orange-50 dark:from-yellow-900/20 dark:to-orange-900/20 rounded-lg p-4">
      <div class="flex items-center justify-between mb-3">
        <h4 class="font-semibold text-gray-900 dark:text-white flex items-center">
          <span class="mr-2">🏆</span> Campus Leaderboard
        </h4>
        <button class="text-sm text-purple-600 dark:text-purple-400 hover:text-purple-700 font-medium">
          View All
        </button>
      </div>
      
      <div class="space-y-2">
        <div v-for="(leader, index) in leaderboard" :key="leader.id" class="flex items-center justify-between">
          <div class="flex items-center">
            <div class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold mr-3" 
                 :class="index === 0 ? 'bg-yellow-400 text-yellow-900' : 
                        index === 1 ? 'bg-gray-300 text-gray-700' : 
                        index === 2 ? 'bg-orange-400 text-orange-900' : 
                        'bg-gray-100 text-gray-600'">
              {{ index + 1 }}
            </div>
            <div>
              <p class="text-sm font-medium text-gray-900 dark:text-white">{{ leader.name }}</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">{{ leader.university }}</p>
            </div>
          </div>
          <div class="text-right">
            <div class="text-sm font-bold text-purple-600 dark:text-purple-400">{{ leader.totalPoints }}</div>
            <div class="text-xs text-gray-500 dark:text-gray-400">points</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Achievement Badges -->
    <div class="mt-6">
      <h4 class="font-semibold text-gray-900 dark:text-white mb-3 flex items-center">
        <span class="mr-2">🎖️</span> Recent Achievements
      </h4>
      
      <div class="flex flex-wrap gap-2">
        <div v-for="badge in recentBadges" :key="badge.id" 
             class="bg-gradient-to-r from-purple-100 to-pink-100 dark:from-purple-900/30 dark:to-pink-900/30 rounded-lg px-3 py-2 border border-purple-200 dark:border-purple-700">
          <div class="text-center">
            <div class="text-lg">{{ badge.emoji }}</div>
            <div class="text-xs font-medium text-gray-700 dark:text-gray-300">{{ badge.name }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// Reactive data
const currentStreak = ref(7)
const socialShares = ref(23)
const co2Saved = ref(7.2)

// Friends activity
const friendsActivity = ref([
  {
    id: 1,
    name: "Alex",
    avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=32&h=32&fit=crop&crop=face",
    action: "Completed #ProteinChallenge",
    points: "+75 XP",
    time: "2m ago"
  },
  {
    id: 2, 
    name: "Maya",
    avatar: "https://images.unsplash.com/photo-1494790108755-2616b1e8bb24?w=32&h=32&fit=crop&crop=face",
    action: "Shared Rainbow Bowl",
    points: "+100 XP", 
    time: "5m ago"
  },
  {
    id: 3,
    name: "Jake",
    avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=32&h=32&fit=crop&crop=face",
    action: "Unlocked Eco Warrior badge",
    points: "+200 XP",
    time: "12m ago"
  }
])

// Campus leaderboard
const leaderboard = ref([
  {
    id: 1,
    name: "Emma Thompson",
    university: "AGH Kraków",
    totalPoints: 2847
  },
  {
    id: 2,
    name: "Michał Kowalski", 
    university: "Politechnika",
    totalPoints: 2534
  },
  {
    id: 3,
    name: "Sofia Martinez",
    university: "UJ Kraków",
    totalPoints: 2398
  },
  {
    id: 4,
    name: "You",
    university: "Your University",
    totalPoints: 1867
  }
])

// Recent badges
const recentBadges = ref([
  { id: 1, emoji: "🌱", name: "Green Warrior" },
  { id: 2, emoji: "🔥", name: "7-Day Streak" },
  { id: 3, emoji: "💪", name: "Protein Master" },
  { id: 4, emoji: "📸", name: "Social Star" }
])
</script> 