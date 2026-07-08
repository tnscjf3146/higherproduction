<template>
  <div class="contact-page">
    <div class="contact-container">
      
      <!-- 헤더 섹션 -->
      <header class="contact-header">
        <h1 class="page-title">{{ siteSetting.contact_title }}</h1>
        <p class="page-subtitle">{{ siteSetting.logo_kr }}과 함께 당신의 브랜드를 한 단계 더 위로 끌어올려 보세요.</p>
      </header>

      <div class="contact-content">
        <!-- 좌측: 연락처 정보 -->
        <div class="contact-info">
          <div class="info-block">
            <span class="info-label">EMAIL</span>
            <a :href="'mailto:' + siteSetting.email" class="info-value">{{ siteSetting.email }}</a>
          </div>
          
          <div class="info-block">
            <span class="info-label">PHONE</span>
            <a :href="'tel:' + siteSetting.phone.replace(/[^0-9+]/g, '')" class="info-value">{{ siteSetting.phone }}</a>
          </div>
          
          <div class="info-block">
            <span class="info-label">STUDIO</span>
            <span class="info-value">{{ siteSetting.address }}</span>
          </div>
          
          <div class="info-block">
            <span class="info-label">INSTAGRAM</span>
            <a :href="siteSetting.instagram_url" target="_blank" rel="noopener noreferrer" class="info-value">{{ siteSetting.instagram_handle }}</a>
          </div>
          
          <div class="business-info">
            <p>상담은 365일 24시간 언제든 열려있습니다.</p>
            <p>프로젝트 기획부터 예산까지 편하게 문의 남겨주세요.</p>
          </div>
        </div>

        <!-- 우측: 문의하기 폼 -->
        <div class="contact-form-wrapper">
          <div class="form-header">
            <h2>견적·문의하기</h2>
            <p>아래 내용을 작성해주시면 빠르게 검토 후 연락드리겠습니다.</p>
          </div>

          <form @submit.prevent="submitForm" class="contact-form">
            <div class="form-group">
              <label>제목 <span class="required">*</span></label>
              <input type="text" v-model="form.title" placeholder="예) 브랜드 영상 제작 문의" required />
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>성함 <span class="required">*</span></label>
                <input type="text" v-model="form.name" placeholder="홍길동" required />
              </div>
              <div class="form-group">
                <label>회사명</label>
                <input type="text" v-model="form.company" :placeholder="siteSetting.logo_kr" />
              </div>
            </div>

            <div class="form-group">
              <label>연락처 <span class="required">*</span></label>
              <div class="phone-inputs">
                <input type="text" v-model="form.phone1" maxlength="3" placeholder="010" required />
                <span class="dash">-</span>
                <input type="text" v-model="form.phone2" maxlength="4" placeholder="0000" required />
                <span class="dash">-</span>
                <input type="text" v-model="form.phone3" maxlength="4" placeholder="0000" required />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>이메일</label>
                <input type="email" v-model="form.email" placeholder="example@email.com" />
              </div>
              <div class="form-group">
                <label>카테고리</label>
                <select v-model="form.category">
                  <option value="">선택</option>
                  <option value="브랜드 필름">브랜드 필름</option>
                  <option value="유튜브 기획/운영">유튜브 기획/운영</option>
                  <option value="숏폼 영상">숏폼 영상</option>
                  <option value="기타">기타</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <div class="budget-header">
                <label>예산</label>
                <NuxtLink to="/services" class="plan-link">플랜 보기 &rarr;</NuxtLink>
              </div>
              <div class="budget-options">
                <label v-for="(plan, index) in plans" :key="plan.id" class="budget-radio" :class="{ active: form.selectedBudgetOptions.includes(plan.id) }">
                  <input type="checkbox" v-model="form.selectedBudgetOptions" :value="plan.id" /> PLAN {{ String.fromCharCode(65 + index) }}
                </label>
                <label class="budget-radio" :class="{ active: form.selectedBudgetOptions.includes('상담 후 협의') }">
                  <input type="checkbox" v-model="form.selectedBudgetOptions" value="상담 후 협의" /> 상담 후 협의
                </label>
                <label class="budget-radio" :class="{ active: form.selectedBudgetOptions.includes('기타') }">
                  <input type="checkbox" v-model="form.selectedBudgetOptions" value="기타" /> 기타
                </label>
              </div>
            </div>

            <div class="form-group">
              <label>상세 요청사항</label>
              <textarea v-model="form.details" rows="5" placeholder="레퍼런스, 촬영 일정, 특이사항 등 자유롭게 작성해주세요."></textarea>
            </div>

            <button type="submit" class="submit-btn" :disabled="isSubmitting">
              {{ isSubmitting ? '전송 중...' : '견적 받아보기 &rarr;' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

const siteSetting = ref({
  logo_kr: '하이어 프로덕션',
  contact_title: "LET'S GO HIGHER",
  email: 'higher3pd@gmail.com',
  phone: '+82 10-3313-0388',
  address: '경기도 의정부시, KR',
  instagram_handle: '@higher.production',
  instagram_url: 'https://instagram.com/higher.production'
})

const loadSiteSetting = async () => {
  try {
    const data = await $fetch(useRuntimeConfig().public.apiBaseUrl + '/system/settings/')
    if (data) {
      siteSetting.value = {
        logo_kr: data.logo_kr || '하이어 프로덕션',
        contact_title: data.contact_title || "LET'S GO HIGHER",
        email: data.email || 'higher3pd@gmail.com',
        phone: data.phone || '+82 10-3313-0388',
        address: data.address || '경기도 의정부시, KR',
        instagram_handle: data.instagram_handle || '@higher.production',
        instagram_url: data.instagram_url || 'https://instagram.com/higher.production'
      }
    }
  } catch (e) {
    console.error('Failed to load site setting:', e)
  }
}

const plans = ref([])
const loadPlans = async () => {
  try {
    const data = await $fetch(useRuntimeConfig().public.apiBaseUrl + '/product/plans/')
    if (data) {
      plans.value = data
    }
  } catch (e) {
    console.error('Failed to load plans:', e)
  }
}

onMounted(() => {
  loadSiteSetting()
  loadPlans()
})

const form = reactive({
  title: '',
  name: '',
  company: '',
  phone1: '',
  phone2: '',
  phone3: '',
  email: '',
  category: '',
  selectedBudgetOptions: ['상담 후 협의'],
  details: ''
})

const isSubmitting = ref(false)

const submitForm = async () => {
  if (isSubmitting.value) return
  isSubmitting.value = true

  try {
    const selectedPlanIds = form.selectedBudgetOptions.filter(opt => typeof opt === 'number')
    const selectedStrings = form.selectedBudgetOptions.filter(opt => typeof opt === 'string')

    const payload = {
      title: form.title,
      name: form.name,
      company: form.company,
      phone: `${form.phone1}-${form.phone2}-${form.phone3}`,
      email: form.email,
      category: form.category,
      plans: selectedPlanIds,
      budget: selectedStrings.join(', '),
      details: form.details
    }

    const res = await fetch(useRuntimeConfig().public.apiBaseUrl + '/work/inquiries/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (!res.ok) {
      throw new Error('전송 실패')
    }

    alert('문의가 성공적으로 접수되었습니다. 빠르게 확인 후 연락드리겠습니다.')
    
    // 폼 초기화
    Object.assign(form, {
      title: '', name: '', company: '', phone1: '', phone2: '', phone3: '',
      email: '', category: '', selectedBudgetOptions: ['상담 후 협의'], details: ''
    })
  } catch (error) {
    console.error(error)
    alert('문의 접수 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.contact-page {
  background-color: #fafafa;
  min-height: 100vh;
  padding: 120px 20px 80px;
  font-family: 'Pretendard', -apple-system, sans-serif;
}

.contact-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Header */
.contact-header {
  text-align: center;
  margin-bottom: 80px;
}

.page-title {
  font-size: clamp(40px, 6vw, 72px);
  font-weight: 900;
  color: #111;
  margin: 0 0 20px;
  letter-spacing: -2px;
}

.page-subtitle {
  font-size: clamp(16px, 2vw, 20px);
  color: #555;
  margin: 0;
  font-weight: 500;
}

/* Content Grid */
.contact-content {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 60px;
  align-items: start;
}

@media (max-width: 900px) {
  .contact-content {
    grid-template-columns: 1fr;
    gap: 40px;
  }
  .contact-info {
    display: none;
  }
}

/* Left: Info */
.contact-info {
  background-color: #111;
  color: #fff;
  padding: 60px 40px;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  position: sticky;
  top: 100px;
}

.info-block {
  margin-bottom: 40px;
}

.info-label {
  display: block;
  font-size: 13px;
  font-weight: 700;
  color: #666;
  letter-spacing: 2px;
  margin-bottom: 10px;
}

.info-value {
  display: inline-block;
  font-size: 20px;
  font-weight: 600;
  color: #fff;
  text-decoration: none;
  transition: color 0.3s ease;
}

a.info-value:hover {
  color: #1a3ae0;
}

.business-info {
  margin-top: 60px;
  padding-top: 40px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 14px;
  color: #999;
  line-height: 1.6;
}
.business-info p { margin: 0 0 5px; }

/* Right: Form */
.contact-form-wrapper {
  background-color: #fff;
  padding: 60px 50px;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.05);
}

.form-header {
  margin-bottom: 40px;
}

.form-header h2 {
  font-size: 28px;
  font-weight: 800;
  margin: 0 0 10px;
  color: #111;
}

.form-header p {
  font-size: 15px;
  color: #666;
  margin: 0;
}

.contact-form {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.form-row {
  display: flex;
  gap: 20px;
}
.form-row .form-group {
  flex: 1;
}

@media (max-width: 600px) {
  .form-row {
    flex-direction: column;
  }
  .contact-form-wrapper {
    padding: 40px 30px;
  }
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}

.required {
  color: #1a3ae0;
}

input[type="text"],
input[type="email"],
select,
textarea {
  width: 100%;
  padding: 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 15px;
  background-color: #fcfcfc;
  transition: all 0.3s;
  box-sizing: border-box;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: #1a3ae0;
  background-color: #fff;
  box-shadow: 0 0 0 4px rgba(26, 58, 224, 0.1);
}

textarea {
  resize: vertical;
}

/* Phone */
.phone-inputs {
  display: flex;
  align-items: center;
  gap: 10px;
}
.phone-inputs input {
  text-align: center;
}
.dash {
  color: #999;
}

/* Budget */
.budget-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.budget-header label { margin: 0; }

.plan-link {
  font-size: 12px;
  font-weight: 600;
  color: #1a3ae0;
  text-decoration: none;
  background-color: rgba(26, 58, 224, 0.1);
  padding: 6px 12px;
  border-radius: 12px;
  transition: all 0.3s;
}
.plan-link:hover {
  background-color: #1a3ae0;
  color: #fff;
}

.budget-options {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.budget-radio {
  flex: 1;
  display: inline-block;
  padding: 14px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  color: #555;
  cursor: pointer;
  background: #fcfcfc;
  transition: all 0.3s;
  text-align: center;
  margin: 0;
  white-space: nowrap;
}

.budget-radio input {
  display: none;
}

.budget-radio.active {
  border-color: #1a3ae0;
  color: #1a3ae0;
  font-weight: 700;
  background-color: rgba(26, 58, 224, 0.05);
}

/* Submit */
.submit-btn {
  background-color: #1a3ae0;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 20px;
  font-size: 16px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 10px;
  letter-spacing: 1px;
}

.submit-btn:hover {
  background-color: #152bb5;
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(26, 58, 224, 0.3);
}

.submit-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}
</style>
