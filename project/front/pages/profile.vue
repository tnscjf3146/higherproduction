<template>
  <div class="profile-layout">
    <div v-if="isLoadingData" class="loading-box">
      정보를 불러오는 중입니다...
    </div>
    
    <div v-else class="profile-grid">
      <!-- 왼쪽: 대시보드 (구독 및 작업 현황) -->
      <aside class="dashboard-panel">
        <h2 class="panel-title">내 대시보드</h2>
        
        <!-- 구독 상품 영역 -->
        <div class="dashboard-card">
          <h3>구독 중인 상품</h3>
          <div v-if="form.userinfo.production" class="product-info">
            <h4 class="product-name">{{ form.userinfo.production.name }}</h4>
            <p class="product-desc">{{ form.userinfo.production.description }}</p>
          </div>
          <div v-else class="empty-state">
            구독 중인 상품이 없습니다.
          </div>
        </div>
        
        <!-- 내 작품 영역 -->
        <div class="dashboard-card">
          <h3>내 작품 진행 현황</h3>
          <div v-if="form.works && form.works.length > 0" class="works-list">
            <div v-for="work in form.works" :key="work.id" class="work-item">
              <div class="work-header">
                <span 
                  class="status-badge" 
                  :class="work.status === 'COMPLETED' ? 'completed' : 'in-progress'"
                >
                  {{ work.status === 'COMPLETED' ? '완료됨' : '작업중' }}
                </span>
                <span class="work-title">{{ work.title }}</span>
              </div>
              <a v-if="work.youtube_link" :href="work.youtube_link" target="_blank" class="youtube-link">
                영상 보기 ↗
              </a>
            </div>
          </div>
          <div v-else class="empty-state">
            아직 작업 내역이 없습니다.
          </div>
        </div>
      </aside>

      <!-- 오른쪽: 회원정보 수정 -->
      <main class="profile-panel">
        <h2 class="panel-title">회원정보 수정</h2>
        <form @submit.prevent="handleUpdateProfile" class="profile-form">
          <!-- 기본 정보 영역 -->
          <div class="section">
            <h3>기본 정보</h3>
            <div class="form-group">
              <label for="username">아이디 (변경 불가)</label>
              <input 
                id="username" 
                v-model="form.username" 
                type="text" 
                disabled 
                class="disabled-input"
              />
            </div>
            
            <div class="form-group">
              <label for="email">이메일</label>
              <input 
                id="email" 
                v-model="form.email" 
                type="email" 
              />
            </div>

            <div class="form-group">
              <label for="phone">전화번호</label>
              <input 
                id="phone" 
                v-model="form.phone_number" 
                type="text" 
              />
            </div>
          </div>
          
          <!-- 부가 정보 (UserInfo) 영역 -->
          <div class="section">
            <h3>부가 정보</h3>
            <div class="form-group">
              <label for="company_name">회사명 (Company Name)</label>
              <input 
                id="company_name" 
                v-model="form.userinfo.company_name" 
                type="text" 
                placeholder="회사명을 입력하세요"
              />
            </div>
            
            <div class="form-group">
              <label for="manager">담당자명 (Manager)</label>
              <input 
                id="manager" 
                v-model="form.userinfo.manager" 
                type="text" 
                placeholder="담당자명을 입력하세요"
              />
            </div>
            
            <div class="form-group">
              <label for="company_address">회사 주소 (Company Address)</label>
              <input 
                id="company_address" 
                v-model="form.userinfo.company_address" 
                type="text" 
                placeholder="주소를 입력하세요"
              />
            </div>
          </div>
          
          <div v-if="successMsg" class="success-msg">{{ successMsg }}</div>
          <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>
          
          <button type="submit" :disabled="isUpdating">
            {{ isUpdating ? '저장 중...' : '변경사항 저장하기' }}
          </button>
        </form>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '~/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const isLoadingData = ref(true)
const isUpdating = ref(false)
const successMsg = ref('')
const errorMsg = ref('')

const form = reactive({
  username: '',
  email: '',
  phone_number: '',
  userinfo: {
    company_name: '',
    manager: '',
    company_address: '',
    production: null // 구독 중인 상품 정보 추가
  },
  works: [] // 내 작품 리스트 추가
})

// 페이지 렌더링 시 기존 데이터 불러오기
onMounted(async () => {
  if (!authStore.accessToken) {
    alert('로그인이 필요합니다.')
    router.push('/account/login')
    return
  }
  
  try {
    const response = await $fetch(useRuntimeConfig().public.apiBaseUrl + '/account/profile/', {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${authStore.accessToken}`
      }
    })
    
    // 불러온 데이터를 form 객체에 매핑
    form.username = response.username
    form.email = response.email || ''
    form.phone_number = response.phone_number || ''
    form.works = response.works || []
    
    if (response.userinfo) {
      form.userinfo.company_name = response.userinfo.company_name || ''
      form.userinfo.manager = response.userinfo.manager || ''
      form.userinfo.company_address = response.userinfo.company_address || ''
      form.userinfo.production = response.userinfo.production || null
    }
  } catch (error) {
    if (error.response?.status === 401) {
      alert('로그인이 만료되었습니다. 다시 로그인해 주세요.')
      authStore.logout()
      router.push('/account/login')
    } else {
      console.error('Failed to load profile:', error)
      alert('프로필 정보를 불러오는데 실패했습니다.')
    }
  } finally {
    isLoadingData.value = false
  }
})

// 폼 제출 시 데이터 수정 요청 (PUT)
const handleUpdateProfile = async () => {
  errorMsg.value = ''
  successMsg.value = ''
  isUpdating.value = true
  
  try {
    const response = await $fetch(useRuntimeConfig().public.apiBaseUrl + '/account/profile/', {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${authStore.accessToken}`
      },
      body: {
        email: form.email || null,
        phone_number: form.phone_number || null,
        userinfo: {
          company_name: form.userinfo.company_name || null,
          manager: form.userinfo.manager || null,
          company_address: form.userinfo.company_address || null
          // production 정보는 읽기 전용이므로 PUT에 포함하지 않음
        }
      }
    })
    
    successMsg.value = '회원정보가 성공적으로 수정되었습니다.'
  } catch (error) {
    if (error.response?.status === 401) {
      alert('로그인이 만료되었습니다. 다시 로그인해 주세요.')
      authStore.logout()
      router.push('/account/login')
    } else {
      console.error('Failed to update profile:', error)
      errorMsg.value = error.response?._data?.error || '회원정보 수정 중 오류가 발생했습니다.'
    }
  } finally {
    isUpdating.value = false
  }
}
</script>

<style scoped>
.profile-layout {
  max-width: 1000px;
  margin: 60px auto;
  padding: 0 20px;
}

.loading-box {
  text-align: center;
  padding: 80px;
  color: #666;
  font-size: 16px;
}

.profile-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

@media (max-width: 768px) {
  .profile-grid {
    grid-template-columns: 1fr;
  }
}

/* 패널 공통 */
.dashboard-panel, .profile-panel {
  background-color: white;
  border-radius: 8px;
  padding: 40px 30px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  border: 1px solid #eaeaea;
}

.panel-title {
  text-align: center;
  margin-bottom: 30px;
  font-weight: 700;
  color: #222;
  font-size: 20px;
}

/* 대시보드 쪽 */
.dashboard-card {
  background-color: #fafafa;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 25px;
  margin-bottom: 20px;
}

.dashboard-card h3 {
  font-size: 16px;
  font-weight: 700;
  color: #111;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 2px solid #ddd;
}

.empty-state {
  color: #888;
  font-size: 14px;
  text-align: center;
  padding: 20px 0;
}

.product-name {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin-bottom: 6px;
}

.product-desc {
  font-size: 13.5px;
  color: #666;
  line-height: 1.5;
}

/* 작품 리스트 */
.work-item {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 15px;
  margin-bottom: 12px;
}
.work-item:last-child {
  margin-bottom: 0;
}

.work-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.status-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 4px;
  margin-right: 10px;
}
.status-badge.in-progress {
  background-color: #fff3e0;
  color: #e65100;
}
.status-badge.completed {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.work-title {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.youtube-link {
  display: inline-block;
  font-size: 12.5px;
  color: #1976d2;
  text-decoration: none;
  font-weight: 600;
}
.youtube-link:hover {
  text-decoration: underline;
}

/* 회원정보 수정 폼 (오른쪽) */
.section {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}
.section:last-of-type {
  border-bottom: none;
}

.section h3 {
  font-size: 15px;
  color: #555;
  margin-bottom: 20px;
  padding-left: 5px;
  border-left: 4px solid #111;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-size: 13px;
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

.disabled-input {
  background-color: #f5f5f5;
  color: #888;
  cursor: not-allowed;
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
  transition: background-color 0.2s;
}

button:hover:not(:disabled) {
  background-color: #333;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.success-msg {
  background-color: #e8f5e9;
  color: #2e7d32;
  padding: 12px;
  border-radius: 6px;
  font-size: 14px;
  margin-bottom: 20px;
  text-align: center;
}

.error-msg {
  background-color: #ffebee;
  color: #c62828;
  padding: 12px;
  border-radius: 6px;
  font-size: 14px;
  margin-bottom: 20px;
  text-align: center;
}
</style>
