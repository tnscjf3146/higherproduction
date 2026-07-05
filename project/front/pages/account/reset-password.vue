<template>
  <div class="reset-container">
    <h2>새 비밀번호 설정</h2>
    
    <div v-if="!uid || !token" class="error-box">
      잘못된 접근입니다. 재설정 링크가 유효하지 않습니다.
    </div>
    
    <form v-else @submit.prevent="handleReset" class="reset-form">
      <p class="desc">새롭게 사용할 비밀번호를 입력해 주세요.</p>
      
      <div class="form-group">
        <label for="password">새 비밀번호</label>
        <input 
          id="password" 
          v-model="password" 
          type="password" 
          required 
          placeholder="대문자, 특수기호 포함 8자 이상" 
        />
      </div>

      <div class="form-group">
        <label for="passwordConfirm">비밀번호 확인</label>
        <input 
          id="passwordConfirm" 
          v-model="passwordConfirm" 
          type="password" 
          required 
          placeholder="비밀번호를 다시 한 번 입력하세요" 
        />
      </div>
      
      <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>
      
      <button type="submit" :disabled="isLoading">
        {{ isLoading ? '변경 중...' : '비밀번호 변경하기' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const uid = ref('')
const token = ref('')
const password = ref('')
const passwordConfirm = ref('')
const errorMsg = ref('')
const isLoading = ref(false)

onMounted(() => {
  // URL 쿼리 파라미터에서 uid와 token 추출 (?uid=...&token=...)
  uid.value = route.query.uid
  token.value = route.query.token
})

const handleReset = async () => {
  errorMsg.value = ''
  
  if (password.value !== passwordConfirm.value) {
    errorMsg.value = '비밀번호가 일치하지 않습니다.'
    return
  }
  
  isLoading.value = true
  
  try {
    const response = await $fetch('http://127.0.0.1:8000/account/password-reset/confirm/', {
      method: 'POST',
      body: {
        uid: uid.value,
        token: token.value,
        password: password.value
      }
    })
    
    alert(response.message)
    router.push('/account/login')
    
  } catch (error) {
    errorMsg.value = error.response?._data?.error || '비밀번호 변경에 실패했습니다. 링크가 만료되었을 수 있습니다.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.reset-container {
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
  margin-bottom: 20px;
  font-weight: 700;
  color: #222;
}

.desc {
  text-align: center;
  font-size: 14px;
  color: #666;
  margin-bottom: 25px;
}

.error-box {
  background-color: #ffebee;
  color: #c62828;
  padding: 20px;
  border-radius: 6px;
  text-align: center;
  font-size: 15px;
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
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
  box-sizing: border-box;
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
  margin-top: 10px;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error-msg {
  color: #c62828;
  font-size: 13.5px;
  margin-bottom: 15px;
}
</style>
