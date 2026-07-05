<template>
  <div class="signup-container">
    <h2>회원가입</h2>
    <form @submit.prevent="handleSignup" class="signup-form">
      <div class="form-group">
        <label for="username">아이디 (Username) *</label>
        <input 
          id="username" 
          v-model="form.username" 
          type="text" 
          required 
          placeholder="아이디를 입력하세요" 
        />
      </div>

      <div class="form-group">
        <label for="password">비밀번호 (Password) *</label>
        <input 
          id="password" 
          v-model="form.password" 
          type="password" 
          required 
          placeholder="대문자, 특수기호 포함 8자 이상" 
        />
      </div>

      <div class="form-group">
        <label for="email">이메일 (Email)</label>
        <input 
          id="email" 
          v-model="form.email" 
          type="email" 
          placeholder="이메일을 입력하세요 (선택)" 
        />
      </div>

      <div class="form-group">
        <label for="phone">전화번호 (Phone)</label>
        <input 
          id="phone" 
          v-model="form.phone_number" 
          type="text" 
          placeholder="전화번호를 입력하세요 (선택)" 
        />
      </div>
      
      <!-- 백엔드에서 넘어오는 여러 에러 메시지를 렌더링 -->
      <div v-if="errorMessages.length > 0" class="error-msg">
        <p v-for="(msg, idx) in errorMessages" :key="idx">• {{ msg }}</p>
      </div>
      
      <button type="submit" :disabled="isLoading">
        {{ isLoading ? '회원가입 처리 중...' : '가입하기' }}
      </button>

      <div class="login-link">
        이미 계정이 있으신가요? <NuxtLink to="/account/login">로그인하기</NuxtLink>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '~/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// 폼 데이터 (모델에 정의된 필드들과 동일하게 맞춤)
const form = reactive({
  username: '',
  email: '',
  phone_number: '',
  password: ''
})

const errorMessages = ref([])
const isLoading = ref(false)

const handleSignup = async () => {
  errorMessages.value = []
  isLoading.value = true
  
  try {
    const response = await $fetch('http://127.0.0.1:8000/account/signup/', {
      method: 'POST',
      body: {
        username: form.username,
        email: form.email || null,               // 빈 값이면 null로 처리
        phone_number: form.phone_number || null, // 빈 값이면 null로 처리
        password: form.password
      }
    })
    
    // 성공 시: 스토어를 통한 자동 로그인 처리
    const loginResult = await authStore.login(form.username, form.password)
    
    if (loginResult.success) {
      alert('회원가입 및 자동 로그인이 완료되었습니다!')
      router.push('/')
    } else {
      alert('회원가입은 완료되었으나 자동 로그인에 실패했습니다. 직접 로그인해주세요.')
      router.push('/account/login')
    }
    
  } catch (error) {
    console.error('Signup error:', error)
    const errData = error.response?._data
    
    if (errData) {
      // DRF는 에러를 객체 형태로 반환합니다. (예: { password: ["비밀번호가 너무 짧습니다."], username: ["이미 존재합니다."] })
      if (typeof errData === 'object' && !errData.error) {
        for (const [field, messages] of Object.entries(errData)) {
          if (Array.isArray(messages)) {
            // 필드명을 한글로 매핑하여 표시
            const fieldName = field === 'password' ? '비밀번호' : field === 'username' ? '아이디' : field;
            errorMessages.value.push(`[${fieldName}] ${messages[0]}`)
          } else {
            errorMessages.value.push(messages)
          }
        }
      } else if (errData.error) {
        errorMessages.value.push(errData.error)
      } else {
        errorMessages.value.push('회원가입에 실패했습니다.')
      }
    } else {
      errorMessages.value.push('서버와 통신할 수 없습니다.')
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.signup-container {
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
  margin-bottom: 30px;
  font-weight: 700;
  color: #222;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #444;
}

input {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

input:focus {
  outline: none;
  border-color: #111;
}

button {
  width: 100%;
  padding: 14px;
  background-color: #111;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  margin-top: 15px;
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
  background-color: #ffebee;
  color: #c62828;
  padding: 12px;
  border-radius: 6px;
  font-size: 13.5px;
  margin-bottom: 20px;
}

.error-msg p {
  margin: 4px 0;
}

.login-link {
  text-align: center;
  margin-top: 25px;
  font-size: 14px;
  color: #666;
}

.login-link a {
  color: #111;
  font-weight: 600;
  text-decoration: underline;
  margin-left: 5px;
}
</style>
