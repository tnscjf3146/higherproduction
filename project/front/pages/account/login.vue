<template>
  <div class="login-container">
    <h2>로그인</h2>
    <form @submit.prevent="handleLogin" class="login-form">
      <div class="form-group">
        <label for="username">아이디</label>
        <input 
          id="username" 
          v-model="username" 
          type="text" 
          required 
          placeholder="아이디를 입력하세요" 
        />
      </div>
      
      <div class="form-group">
        <label for="password">비밀번호</label>
        <input 
          id="password" 
          v-model="password" 
          type="password" 
          required 
          placeholder="비밀번호를 입력하세요" 
        />
      </div>
      
      <div v-if="errorMessage" class="error-msg">
        {{ errorMessage }}
      </div>
      
      <button type="submit" :disabled="isLoading">
        {{ isLoading ? '로그인 중...' : '로그인' }}
      </button>

      <div class="extra-links">
        <NuxtLink to="/account/find">아이디/비밀번호 찾기</NuxtLink>
        <span class="divider">|</span>
        <NuxtLink to="/account/signup">회원가입</NuxtLink>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

const authStore = useAuthStore()
const router = useRouter()

const handleLogin = async () => {
  errorMessage.value = ''
  isLoading.value = true
  
  // stores/auth.js 에 정의한 login 함수 호출
  const result = await authStore.login(username.value, password.value)
  
  if (result.success) {
    // 로그인 성공 시 메인 페이지로 이동
    alert('로그인 성공!')
    router.push('/')
  } else {
    // 실패 시 에러 메시지 렌더링
    errorMessage.value = result.message
  }
  
  isLoading.value = false
}
</script>

<style scoped>
.login-container {
  max-width: 450px;
  margin: 80px auto;
  padding: 40px 30px;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  background-color: white;
  border: 1px solid #eaeaea;
}

h2 {
  text-align: center;
  margin-bottom: 24px;
  font-weight: 600;
}

.form-group {
  margin-bottom: 16px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

button {
  width: 100%;
  padding: 14px;
  background-color: #111;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  margin-top: 10px;
  transition: background-color 0.2s;
}

button:hover:not(:disabled) {
  background-color: #333;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error-msg {
  color: #e74c3c;
  font-size: 13px;
  margin-bottom: 15px;
}

.extra-links {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
}

.extra-links a {
  color: #666;
  text-decoration: none;
  transition: color 0.2s;
}

.extra-links a:hover {
  color: #111;
  text-decoration: underline;
}

.divider {
  margin: 0 10px;
  color: #ccc;
}
</style>
