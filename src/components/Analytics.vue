<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 mb-6">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center">
            <button 
              @click="$emit('navigate', 'dashboard')"
              class="mr-4 p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
            </button>
            <div>
              <h1 class="text-2xl font-bold text-gray-900 dark:text-white">📊 Advanced Analytics</h1>
              <p class="text-sm text-gray-600 dark:text-gray-400">Real-time insights & performance metrics</p>
            </div>
          </div>
          
          <!-- Real-time indicator -->
          <div class="flex items-center space-x-4">
            <div class="flex items-center space-x-2">
              <div class="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
              <span class="text-sm text-gray-600 dark:text-gray-400">Live</span>
            </div>
            <button 
              @click="refreshData"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Odśwież
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
      
      <!-- Real-time Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div v-for="(stat, index) in realtimeStats" :key="index" 
          class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6"
        >
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">{{ stat.label }}</p>
              <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ stat.value }}</p>
              <p class="text-xs" :class="stat.trend >= 0 ? 'text-green-600' : 'text-red-600'">
                {{ stat.trend >= 0 ? '+' : '' }}{{ stat.trend }}% vs wczoraj
              </p>
            </div>
            <div class="text-3xl">{{ stat.icon }}</div>
          </div>
        </div>
      </div>

      <!-- Charts Row -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- Daily Sales Chart -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">📈 Sprzedaż tygodniowa</h3>
          <div class="h-64">
            <Line
              v-if="salesChartData.labels.length"
              :data="salesChartData"
              :options="chartOptions"
              :style="{ height: '100%', width: '100%' }"
            />
          </div>
        </div>

        <!-- Monthly Comparison Chart -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">📊 Porównanie miesięczne</h3>
          <div class="h-64">
            <Bar
              v-if="monthlyChartData.labels.length"
              :data="monthlyChartData"
              :options="chartOptions"
              :style="{ height: '100%', width: '100%' }"
            />
          </div>
        </div>
      </div>

      <!-- Ingredients Usage & Sales Funnel -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- Top Ingredients -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">🌟 Najpopularniejsze składniki</h3>
          <div class="space-y-3">
            <div v-for="ingredient in topIngredients" :key="ingredient.name"
              class="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-700"
            >
              <div class="flex-1">
                <p class="font-medium text-gray-900 dark:text-white">{{ ingredient.name }}</p>
                <div class="flex items-center space-x-2 mt-1">
                  <div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                    <div 
                      class="bg-green-600 h-2 rounded-full transition-all duration-500"
                      :style="{ width: ingredient.percentage + '%' }"
                    ></div>
                  </div>
                  <span class="text-sm text-gray-600 dark:text-gray-400">{{ ingredient.percentage }}%</span>
                </div>
              </div>
              <div class="ml-4 text-right">
                <p class="text-sm font-medium text-gray-900 dark:text-white">{{ ingredient.count }}</p>
                <p class="text-xs text-green-600">{{ ingredient.trend }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Sales Funnel -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">🎯 Sales Funnel</h3>
          <div class="space-y-3">
            <div v-for="(stage, index) in salesFunnel" :key="index"
              class="relative"
            >
              <div class="flex items-center justify-between p-3 rounded-lg"
                :class="index === 0 ? 'bg-blue-50 dark:bg-blue-900/20' : 
                       index === salesFunnel.length - 1 ? 'bg-green-50 dark:bg-green-900/20' : 
                       'bg-gray-50 dark:bg-gray-700'"
              >
                <div class="flex-1">
                  <p class="font-medium text-gray-900 dark:text-white">{{ stage.stage }}</p>
                  <div class="flex items-center space-x-2 mt-1">
                    <div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                      <div 
                        class="h-2 rounded-full transition-all duration-500"
                        :class="index === 0 ? 'bg-blue-600' : 
                               index === salesFunnel.length - 1 ? 'bg-green-600' : 
                               'bg-yellow-600'"
                        :style="{ width: stage.percentage + '%' }"
                      ></div>
                    </div>
                    <span class="text-sm text-gray-600 dark:text-gray-400">{{ stage.conversion }}%</span>
                  </div>
                </div>
                <div class="ml-4 text-right">
                  <p class="text-sm font-medium text-gray-900 dark:text-white">{{ stage.count.toLocaleString() }}</p>
                  <p class="text-xs text-gray-600 dark:text-gray-400">{{ stage.percentage }}%</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Machine Status & Recent Orders -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- Machine Status -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">🤖 Status automatów</h3>
          <div class="space-y-3">
            <div v-for="(status, machine) in machineStatus" :key="machine"
              class="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-700"
            >
              <div class="flex items-center space-x-3">
                <div 
                  class="w-3 h-3 rounded-full"
                  :class="status === 'online' ? 'bg-green-500' : 
                         status === 'maintenance' ? 'bg-yellow-500' : 'bg-red-500'"
                ></div>
                <span class="font-medium text-gray-900 dark:text-white">{{ machine }}</span>
              </div>
              <span 
                class="px-3 py-1 rounded-full text-xs font-medium"
                :class="status === 'online' ? 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400' : 
                       status === 'maintenance' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400' : 
                       'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400'"
              >
                {{ status === 'online' ? 'Online' : status === 'maintenance' ? 'Konserwacja' : 'Offline' }}
              </span>
            </div>
          </div>
        </div>

        <!-- Recent Orders -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">🛒 Ostatnie zamówienia</h3>
          <div class="space-y-3">
            <div v-for="order in recentOrders" :key="order.id"
              class="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-700"
            >
              <div>
                <p class="font-medium text-gray-900 dark:text-white">{{ order.id }}</p>
                <p class="text-sm text-gray-600 dark:text-gray-400">{{ order.location }} • {{ order.time }}</p>
              </div>
              <div class="text-right">
                <p class="font-bold text-green-600">{{ order.amount }} PLN</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Ingredients Categories Chart -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">🥗 Wykorzystanie kategorii składników</h3>
        <div class="h-80">
          <Doughnut
            v-if="categoriesChartData.labels.length"
            :data="categoriesChartData"
            :options="doughnutOptions"
            :style="{ height: '100%', width: '100%' }"
          />
        </div>
      </div>

      <!-- Machine Status Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <div 
          v-for="machine in machineStatus" 
          :key="machine.id"
          class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6"
        >
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{{ machine.name }}</h3>
            <div class="flex items-center">
              <div class="w-3 h-3 rounded-full mr-2" :class="machine.statusColor"></div>
              <span class="text-sm font-medium" :class="machine.statusTextColor">{{ machine.status }}</span>
            </div>
          </div>
          
          <div class="space-y-3">
            <div class="flex justify-between text-sm">
              <span class="text-gray-600 dark:text-gray-400">Uptime:</span>
              <span class="font-medium text-gray-900 dark:text-white">{{ machine.uptime }}%</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-600 dark:text-gray-400">Orders Today:</span>
              <span class="font-medium text-gray-900 dark:text-white">{{ machine.ordersToday }}</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-600 dark:text-gray-400">Revenue:</span>
              <span class="font-medium text-green-600 dark:text-green-400">{{ machine.revenue }} PLN</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Performance Monitor Section -->
      <PerformanceMonitor />
      
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import { Line, Bar, Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  ArcElement
} from 'chart.js'
import PerformanceMonitor from './PerformanceMonitor.vue'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  ArcElement
)

// Emits
defineEmits<{
  navigate: (page: string) => void
}>()

// Reactive data
const loading = ref(false)
const refreshInterval = ref(null)

// Analytics data
const realtimeStats = ref([
  { label: 'Użytkownicy online', value: '0', trend: 0, icon: '👥' },
  { label: 'Zamówienia/godz', value: '0', trend: 0, icon: '🛒' },
  { label: 'Przychód dziś', value: '0 PLN', trend: 0, icon: '💰' },
  { label: 'Konwersja', value: '0%', trend: 0, icon: '📈' }
])

const topIngredients = ref([])
const salesFunnel = ref([])
const machineStatus = ref([
  {
    id: 1,
    name: 'IKIGAI Central',
    status: 'Online',
    statusColor: 'bg-green-500',
    statusTextColor: 'text-green-600 dark:text-green-400',
    uptime: 99.2,
    ordersToday: 24,
    revenue: 387.50
  },
  {
    id: 2,
    name: 'IKIGAI Fitness',
    status: 'Online', 
    statusColor: 'bg-green-500',
    statusTextColor: 'text-green-600 dark:text-green-400',
    uptime: 98.7,
    ordersToday: 18,
    revenue: 295.80
  },
  {
    id: 3,
    name: 'IKIGAI Office',
    status: 'Maintenance',
    statusColor: 'bg-yellow-500',
    statusTextColor: 'text-yellow-600 dark:text-yellow-400',
    uptime: 95.3,
    ordersToday: 12,
    revenue: 198.20
  },
  {
    id: 4,
    name: 'IKIGAI University',
    status: 'Online',
    statusColor: 'bg-green-500', 
    statusTextColor: 'text-green-600 dark:text-green-400',
    uptime: 97.8,
    ordersToday: 31,
    revenue: 478.90
  },
  {
    id: 5,
    name: 'IKIGAI Park',
    status: 'Online',
    statusColor: 'bg-green-500',
    statusTextColor: 'text-green-600 dark:text-green-400',
    uptime: 98.1,
    ordersToday: 15,
    revenue: 267.30
  }
])

const recentOrders = ref([])

// Chart data
const salesChartData = ref({ labels: [], datasets: [] })
const monthlyChartData = ref({ labels: [], datasets: [] })
const categoriesChartData = ref({ labels: [], datasets: [] })

// Chart options
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
    },
  },
  scales: {
    y: {
      beginAtZero: true,
    },
  },
}

const doughnutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right',
    },
  },
}

// Methods
const fetchDashboardData = async () => {
  try {
    // Temporary mock data - will work after backend restart
    const mockData = {
      orders: { today: 89, completion_rate: 96.1 },
      sales: { today: 2847.50, growth_daily: 32.1 },
      machines: { uptime: 98.7 }
    }
    
    // Update stats
    realtimeStats.value = [
      { 
        label: 'Zamówienia dziś', 
        value: mockData.orders.today.toString(), 
        trend: mockData.sales.growth_daily, 
        icon: '🛒' 
      },
      { 
        label: 'Przychód dziś', 
        value: `${mockData.sales.today.toLocaleString()} PLN`, 
        trend: mockData.sales.growth_daily, 
        icon: '💰' 
      },
      { 
        label: 'Realizacja', 
        value: `${mockData.orders.completion_rate}%`, 
        trend: 2.3, 
        icon: '📈' 
      },
      { 
        label: 'Uptime', 
        value: `${mockData.machines.uptime}%`, 
        trend: 0.5, 
        icon: '🤖' 
      }
    ]
    
    // Try real API (will work after backend restart)
    try {
      const response = await axios.get('http://localhost:5001/api/analytics/dashboard')
      const data = response.data.data
      
      realtimeStats.value = [
        { 
          label: 'Zamówienia dziś', 
          value: data.orders.today.toString(), 
          trend: data.sales.growth_daily, 
          icon: '🛒' 
        },
        { 
          label: 'Przychód dziś', 
          value: `${data.sales.today.toLocaleString()} PLN`, 
          trend: data.sales.growth_daily, 
          icon: '💰' 
        },
        { 
          label: 'Realizacja', 
          value: `${data.orders.completion_rate}%`, 
          trend: 2.3, 
          icon: '📈' 
        },
        { 
          label: 'Uptime', 
          value: `${data.machines.uptime}%`, 
          trend: 0.5, 
          icon: '🤖' 
        }
      ]
    } catch (apiError) {
      console.log('Using mock data - restart backend for real API')
    }
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  }
}

const fetchChartsData = async () => {
  try {
    // Mock data for charts
    salesChartData.value = {
      labels: ["Pon", "Wt", "Śr", "Czw", "Pt", "Sob", "Nie"],
      datasets: [{
        label: "Sprzedaż (PLN)",
        data: [2847, 3156, 2890, 3247, 3456, 2234, 1890],
        backgroundColor: "rgba(34, 197, 94, 0.1)",
        borderColor: "rgba(34, 197, 94, 1)",
        borderWidth: 2,
        fill: true
      }]
    }
    
    monthlyChartData.value = {
      labels: ["Sty", "Lut", "Mar", "Kwi", "Maj", "Cze"],
      datasets: [{
        label: "Ten rok",
        data: [45678, 52345, 58234, 62890, 69456, 78549],
        backgroundColor: "rgba(59, 130, 246, 0.8)"
      }, {
        label: "Zeszły rok", 
        data: [38234, 41567, 47890, 52345, 58234, 63456],
        backgroundColor: "rgba(156, 163, 175, 0.8)"
      }]
    }
    
    // Try real API
    try {
      const response = await axios.get('http://localhost:5001/api/analytics/charts/sales')
      const data = response.data.data
      salesChartData.value = data.daily_sales
      monthlyChartData.value = data.monthly_comparison
    } catch (apiError) {
      console.log('Using mock chart data - restart backend for real API')
    }
  } catch (error) {
    console.error('Error fetching charts data:', error)
  }
}

const fetchIngredientsData = async () => {
  try {
    // Mock data for ingredients
    topIngredients.value = [
      {"name": "Spirulina Powder BIO", "count": 387, "percentage": 15.8, "trend": "+12%"},
      {"name": "Protein Vanilla Premium", "count": 342, "percentage": 14.1, "trend": "+8%"},
      {"name": "Woda Kokosowa Premium", "count": 298, "percentage": 12.3, "trend": "+15%"},
      {"name": "Matcha Premium Grade A", "count": 267, "percentage": 11.0, "trend": "+5%"},
      {"name": "Goji Berries BIO", "count": 234, "percentage": 9.6, "trend": "+18%"},
      {"name": "Chia Seeds Premium", "count": 189, "percentage": 7.8, "trend": "+3%"}
    ]
    
    categoriesChartData.value = {
      labels: ["Superfoods", "Proteiny", "Bazy płynne", "Nasiona", "Przyprawy", "Detoks"],
      datasets: [{
        data: [1247, 987, 756, 534, 398, 234],
        backgroundColor: ["#10B981", "#3B82F6", "#8B5CF6", "#F59E0B", "#EF4444", "#6B7280"],
        borderWidth: 0
      }]
    }
    
    // Try real API
    try {
      const response = await axios.get('http://localhost:5001/api/analytics/ingredients/usage')
      const data = response.data.data
      topIngredients.value = data.top_ingredients.slice(0, 6)
      
      categoriesChartData.value = {
        labels: data.categories_usage.labels,
        datasets: [{
          data: data.categories_usage.data,
          backgroundColor: data.categories_usage.colors,
          borderWidth: 0
        }]
      }
    } catch (apiError) {
      console.log('Using mock ingredients data - restart backend for real API')
    }
  } catch (error) {
    console.error('Error fetching ingredients data:', error)
  }
}

const fetchFunnelData = async () => {
  try {
    // Mock funnel data
    salesFunnel.value = [
      {"stage": "Wizyta strony", "count": 15678, "percentage": 100, "conversion": 100},
      {"stage": "Otworzył kreator", "count": 8934, "percentage": 57.0, "conversion": 57.0},
      {"stage": "Wybrał składniki", "count": 6234, "percentage": 39.8, "conversion": 69.8},
      {"stage": "Dodał do koszyka", "count": 3456, "percentage": 22.0, "conversion": 55.4},
      {"stage": "Rozpoczął płatność", "count": 2789, "percentage": 17.8, "conversion": 80.7},
      {"stage": "Ukończył zamówienie", "count": 2234, "percentage": 14.2, "conversion": 80.1}
    ]
    
    // Try real API
    try {
      const response = await axios.get('http://localhost:5001/api/analytics/funnel')
      const data = response.data.data
      salesFunnel.value = data.funnel_stages.slice(0, 6)
    } catch (apiError) {
      console.log('Using mock funnel data - restart backend for real API')
    }
  } catch (error) {
    console.error('Error fetching funnel data:', error)
  }
}

const fetchRealtimeData = async () => {
  try {
    // Mock real-time data
    machineStatus.value = {
      "IKIGAI Central": "online",
      "IKIGAI Fitness": "online", 
      "IKIGAI Office": "maintenance",
      "IKIGAI University": "online",
      "IKIGAI Park": "online"
    }
    
    recentOrders.value = [
      {"id": "ORD-2024-1247", "time": "2 min ago", "amount": 24.50, "location": "Central"},
      {"id": "ORD-2024-1246", "time": "5 min ago", "amount": 18.20, "location": "Fitness"},
      {"id": "ORD-2024-1245", "time": "8 min ago", "amount": 31.70, "location": "University"}
    ]
    
    // Update real-time stats with random variations
    realtimeStats.value[0].value = (45 + Math.floor(Math.random() * 33)).toString()
    realtimeStats.value[1].value = (8 + Math.floor(Math.random() * 7)).toString()
    realtimeStats.value[2].value = `${(2847.50 + (Math.random() - 0.5) * 100).toFixed(2)} PLN`
    
    // Try real API
    try {
      const response = await axios.get('http://localhost:5001/api/analytics/realtime')
      const data = response.data.data
      
      realtimeStats.value[0].value = data.current_users.toString()
      realtimeStats.value[1].value = data.orders_last_hour.toString()
      realtimeStats.value[2].value = `${data.revenue_today.toFixed(2)} PLN`
      
      machineStatus.value = data.machine_status
      recentOrders.value = data.last_orders
    } catch (apiError) {
      console.log('Using mock realtime data - restart backend for real API')
    }
  } catch (error) {
    console.error('Error fetching realtime data:', error)
  }
}

const refreshData = async () => {
  loading.value = true
  try {
    await Promise.all([
      fetchDashboardData(),
      fetchChartsData(),
      fetchIngredientsData(),
      fetchFunnelData(),
      fetchRealtimeData()
    ])
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(async () => {
  await refreshData()
  
  // Set up auto-refresh every 30 seconds
  refreshInterval.value = setInterval(fetchRealtimeData, 30000)
})

onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
})
</script>

<style scoped>
/* Custom styles */
</style> 