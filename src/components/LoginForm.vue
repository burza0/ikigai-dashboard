<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
    <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl w-full max-w-md mx-auto">
      <!-- Header -->
      <div class="p-6 border-b border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <div class="w-8 h-8 mr-3 flex items-center justify-center">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="w-6 h-6 text-purple-600">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 6v12"/>
                <path d="M6 12h12"/>
                <circle cx="12" cy="12" r="3" fill="url(#gradient)" stroke="none"/>
                <defs>
                  <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#8B5CF6"/>
                    <stop offset="100%" style="stop-color:#A855F7"/>
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <h2 class="text-xl font-semibold text-gray-900 dark:text-white">
              {{ isLogin ? '🔐 Logowanie' : '📝 Rejestracja' }}
            </h2>
          </div>
          <button @click="emit('close')" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
        <!-- Błędy -->
        <div v-if="error" class="bg-red-50 dark:bg-red-900/50 border border-red-200 dark:border-red-700 rounded-lg p-3">
          <div class="flex items-center">
            <svg class="w-5 h-5 text-red-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"/>
            </svg>
            <span class="text-red-700 dark:text-red-400 text-sm">{{ error }}</span>
          </div>
        </div>

        <!-- Sukces -->
        <div v-if="success" class="bg-green-50 dark:bg-green-900/50 border border-green-200 dark:border-green-700 rounded-lg p-3">
          <div class="flex items-center">
            <svg class="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"/>
            </svg>
            <span class="text-green-700 dark:text-green-400 text-sm">{{ success }}</span>
          </div>
        </div>

        <!-- Pola formularza -->
        <div v-if="!isLogin" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              👤 Imię i nazwisko
            </label>
            <input
              v-model="form.name"
              type="text"
              required
              class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
              placeholder="Wprowadź swoje imię i nazwisko"
            />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            🏷️ Login {{ isLogin ? 'lub Email' : '' }}
          </label>
          <input
            v-model="form.username"
            type="text"
            required
            class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
            :placeholder="isLogin ? 'Wprowadź login lub email' : 'Wybierz unikalny login'"
          />
        </div>

        <div v-if="!isLogin">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            📧 Email
          </label>
          <input
            v-model="form.email"
            type="email"
            required
            class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
            placeholder="twoj@email.com"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            🔒 Hasło
          </label>
          <div class="relative">
            <input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              required
              :minlength="isLogin ? 1 : 6"
              class="w-full px-4 py-3 pr-12 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
              :placeholder="isLogin ? 'Wprowadź hasło' : 'Min. 6 znaków'"
            />
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            >
              <svg v-if="showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"/>
              </svg>
              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Przyciski -->
        <div class="pt-4 space-y-3">
          <button
            type="submit"
            :disabled="loading"
            class="w-full flex items-center justify-center px-6 py-3 bg-gradient-to-r from-purple-600 to-purple-700 text-white font-medium rounded-lg hover:from-purple-700 hover:to-purple-800 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
          >
            <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
            </svg>
            {{ loading ? 'Przetwarzanie...' : (isLogin ? '🚀 Zaloguj się' : '✨ Utwórz konto') }}
          </button>

          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300 dark:border-gray-600"/>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 bg-white dark:bg-gray-800 text-gray-500 dark:text-gray-400">lub</span>
            </div>
          </div>

          <button
            type="button"
            @click="toggleMode"
            class="w-full text-center text-purple-600 dark:text-purple-400 hover:text-purple-700 dark:hover:text-purple-300 font-medium transition-colors duration-200"
          >
            {{ isLogin ? '📝 Nie masz konta? Zarejestruj się' : '🔐 Masz już konto? Zaloguj się' }}
          </button>
        </div>

        <!-- Demo accounts info -->
        <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4 text-sm">
          <h4 class="font-medium text-gray-900 dark:text-white mb-2">🎯 Konta demo:</h4>
          <div class="space-y-1 text-gray-600 dark:text-gray-400">
            <div><strong>Admin:</strong> admin / admin123</div>
            <div><strong>User:</strong> web_user / demo123</div>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

// Define emits
// Emit events
const emit = defineEmits<{
  close: []
  login: [user: any]
}>()

// State
const isLogin = ref(true)
const loading = ref(false)
const error = ref('')
const success = ref('')
const showPassword = ref(false)

const form = reactive({
  username: '',
  email: '',
  password: '',
  name: ''
})

// Methods
const toggleMode = () => {
  isLogin.value = !isLogin.value
  error.value = ''
  success.value = ''
  
  // Reset form
  Object.keys(form).forEach(key => {
    form[key] = ''
  })
}

const handleSubmit = async () => {
  loading.value = true
  error.value = ''
  success.value = ''

  try {
    const endpoint = isLogin.value ? '/api/auth/login' : '/api/auth/register'
    const payload = isLogin.value 
      ? { username: form.username, password: form.password }
      : { username: form.username, email: form.email, password: form.password, name: form.name }

    const response = await fetch(`http://localhost:5001${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify(payload)
    })

    const data = await response.json()

    if (data.status === 'success') {
      if (isLogin.value) {
        success.value = data.message
        // Emit login event with user data
        setTimeout(() => {
          emit('login', data.user)
        }, 1000)
      } else {
        success.value = `${data.message}. Możesz się teraz zalogować.`
        setTimeout(() => {
          isLogin.value = true
          form.username = payload.username
          form.password = ''
        }, 2000)
      }
    } else {
      error.value = data.message || 'Wystąpił błąd'
    }
  } catch (err) {
    error.value = 'Błąd połączenia z serwerem'
  } finally {
    loading.value = false
  }
}
</script> 