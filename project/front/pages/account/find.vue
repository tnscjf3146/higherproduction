<template>
  <div class="find-container">
    <div class="tabs">
      <button :class="{ active: activeTab === 'id' }" @click="activeTab = 'id'">아이디 찾기</button>
      <button :class="{ active: activeTab === 'password' }" @click="activeTab = 'password'">비밀번호 찾기</button>
    </div>

    <!-- 아이디 찾기 폼 -->
    <div v-if="activeTab === 'id'" class="form-section">
      <h3>가입 시 등록한 이메일로 찾기</h3>
      <form @submit.prevent="handleFindId">
        <div class="form-group">
          <label for="find-id-email">이메일</label>
          <input id="find-id-email" v-model="idForm.email" type="email" required placeholder="가입하신 이메일을 입력하세요" />
        </div>
        
        <div v-if="foundId" class="success-box">
          회원님의 아이디는 <strong>{{ foundId }}</strong> 입니다.
        </div>
        <div v-if="idError" class="error-msg">{{ idError }}</div>

        <button type="submit" :disabled="isLoading">
          {{ isLoading ? '조회 중...' : '아이디 찾기' }}
        </button>
      </form>
    </div>

    <!-- 비밀번호 찾기 폼 -->
    <div v-if="activeTab === 'password'" class="form-section">
      <h3>아이디와 이메일로 비밀번호 재설정</h3>
      <p class="desc">가입하신 이메일로 비밀번호 재설정 링크를 보내드립니다.</p>
      <form @submit.prevent="handleFindPassword">
        <div class="form-group">
          <label for="find-pw-username">아이디</label>
          <input id="find-pw-username" v-model="pwForm.username" type="text" required placeholder="가입하신 아이디를 입력하세요" />
        </div>
        
        <div class="form-group">
          <label for="find-pw-email">이메일</label>
          <input id="find-pw-email" v-model="pwForm.email" type="email" required placeholder="가입하신 이메일을 입력하세요" />
        </div>
        
        <div v-if="pwSuccess" class="success-box">{{ pwSuccess }}</div>
        <div v-if="pwError" class="error-msg">{{ pwError }}</div>

        <button type="submit" :disabled="isLoading">
          {{ isLoading ? '발송 중...' : '재설정 링크 받기' }}
        </button>
      </form>
    </div>

    <div class="login-link">
      <NuxtLink to="/account/login">로그인으로 돌아가기</NuxtLink>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const activeTab = ref('id') // 'id' 또는 'password'
const isLoading = ref(false)

// 아이디 찾기 관련 상태
const idForm = reactive({ email: '' })
const foundId = ref('')
const idError = ref('')

const handleFindId = async () => {
  idError.value = ''
  foundId.value = ''
  isLoading.value = true
  
  try {
    const response = await $fetch(useRuntimeConfig().public.apiBaseUrl + '/account/find-id/', {
      method: 'POST',
      body: { email: idForm.email }
    })
    foundId.value = response.username
  } catch (error) {
    idError.value = error.response?._data?.error || '서버 통신 오류가 발생했습니다.'
  } finally {
    isLoading.value = false
  }
}

// 비밀번호 찾기 관련 상태
const pwForm = reactive({ username: '', email: '' })
const pwSuccess = ref('')
const pwError = ref('')

const handleFindPassword = async () => {
  pwError.value = ''
  pwSuccess.value = ''
  isLoading.value = true
  
  try {
    const response = await $fetch(useRuntimeConfig().public.apiBaseUrl + '/account/password-reset/', {
      method: 'POST',
      body: { username: pwForm.username, email: pwForm.email }
    })
    pwSuccess.value = response.message
  } catch (error) {
    pwError.value = error.response?._data?.error || '서버 통신 오류가 발생했습니다.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.find-container {
  max-width: 450px;
  margin: 80px auto;
  padding: 40px 30px;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  background-color: white;
  border: 1px solid #eaeaea;
}

.tabs {
  display: flex;
  margin-bottom: 30px;
  border-bottom: 1px solid #ddd;
}

.tabs button {
  flex: 1;
  background: none;
  border: none;
  padding: 12px;
  font-size: 16px;
  font-weight: 600;
  color: #888;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
}

.tabs button.active {
  color: #111;
  border-bottom: 2px solid #111;
}

h3 {
  font-size: 18px;
  margin-bottom: 10px;
  color: #222;
}

.desc {
  font-size: 14px;
  color: #666;
  margin-bottom: 20px;
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

button[type="submit"] {
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
}

button[type="submit"]:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error-msg {
  color: #c62828;
  font-size: 13.5px;
  margin-top: -10px;
  margin-bottom: 15px;
}

.success-box {
  background-color: #e8f5e9;
  color: #2e7d32;
  padding: 15px;
  border-radius: 6px;
  font-size: 14px;
  margin-top: 10px;
  margin-bottom: 15px;
  white-space: pre-line;
  line-height: 1.5;
}

.login-link {
  text-align: center;
  margin-top: 25px;
  font-size: 14px;
}

.login-link a {
  color: #111;
  font-weight: 600;
  text-decoration: underline;
}
</style>
