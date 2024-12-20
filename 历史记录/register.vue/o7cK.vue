<template>
    <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-700 to-indigo-900 p-4">
      <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-xl shadow-2xl transform transition-all hover:scale-105">
        <div>
          <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
            创建您的账户
          </h2>
        </div>
        <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
          <div class="rounded-md shadow-sm space-y-4">
            <div>
              <label for="username" class="sr-only">用户名</label>
              <input id="username" name="username" type="text" required
                     v-model="form.username"
                     :class="{'border-red-500': v$.form.username.$error}"
                     class="appearance-none rounded-lg relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                     placeholder="用户名" />
              <p v-if="v$.form.username.$error" class="text-red-500 text-xs mt-1">
                {{ v$.form.username.$errors[0].$message }}
              </p>
            </div>
            <div>
              <label for="email" class="sr-only">电子邮箱</label>
              <input id="email" name="email" type="email" required
                     v-model="form.email"
                     :class="{'border-red-500': v$.form.email.$error}"
                     class="appearance-none rounded-lg relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                     placeholder="电子邮箱" />
              <p v-if="v$.form.email.$error" class="text-red-500 text-xs mt-1">
                {{ v$.form.email.$errors[0].$message }}
              </p>
            </div>
            <div>
              <label for="password" class="sr-only">密码</label>
              <input id="password" name="password" type="password" required
                     v-model="form.password"
                     :class="{'border-red-500': v$.form.password.$error}"
                     class="appearance-none rounded-lg relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                     placeholder="密码" />
              <p v-if="v$.form.password.$error" class="text-red-500 text-xs mt-1">
                {{ v$.form.password.$errors[0].$message }}
              </p>
            </div>
            <div>
              <div class="flex items-center">
                <div class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
                  <div class="bg-blue-600 h-2.5 rounded-full" :style="{ width: `${passwordStrength}%` }"></div>
                </div>
                <span class="ml-2 text-sm" :class="passwordStrengthColor">{{ passwordStrengthText }}</span>
              </div>
            </div>
          </div>
  
          <div>
            <button type="submit"
                    :disabled="v$.$invalid"
                    class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed">
              <span class="absolute left-0 inset-y-0 flex items-center pl-3">
                <LockClosedIcon class="h-5 w-5 text-indigo-500 group-hover:text-indigo-400" aria-hidden="true" />
              </span>
              注册
            </button>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import { useVuelidate } from '@vuelidate/core'
  import { required, email, minLength } from '@vuelidate/validators'
  import { LockClosedIcon } from '@heroicons/vue/solid'
  
  const form = ref({
    username: '',
    email: '',
    password: ''
  })
  
  const rules = {
    form: {
      username: { required, minLength: minLength(3) },
      email: { required, email },
      password: { required, minLength: minLength(8) }
    }
  }
  
  const v$ = useVuelidate(rules, { form })
  
  const passwordStrength = computed(() => {
    const password = form.value.password
    if (!password) return 0
    let strength = 0
    if (password.match(/[a-z]+/)) strength += 25
    if (password.match(/[A-Z]+/)) strength += 25
    if (password.match(/[0-9]+/)) strength += 25
    if (password.match(/[$@#&!]+/)) strength += 25
    return Math.min(strength, 100)
  })
  
  const passwordStrengthText = computed(() => {
    if (passwordStrength.value < 25) return '弱'
    if (passwordStrength.value < 50) return '一般'
    if (passwordStrength.value < 75) return '强'
    return '非常强'
  })
  
  const passwordStrengthColor = computed(() => {
    if (passwordStrength.value < 25) return 'text-red-500'
    if (passwordStrength.value < 50) return 'text-yellow-500'
    if (passwordStrength.value < 75) return 'text-blue-500'
    return 'text-green-500'
  })
  
  const handleSubmit = async () => {
    const isFormCorrect = await v$.value.$validate()
    if (isFormCorrect) {
      // 在这里处理表单提交逻辑
      console.log('Form submitted:', form.value)
    }
  }
  </script>