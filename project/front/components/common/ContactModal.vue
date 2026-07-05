<template>
  <div v-if="modelValue" class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <button class="close-btn" @click="close">&times;</button>
      
      <div class="modal-header">
        <span class="brand-label">HIGHER PRODUCTION</span>
        <h2 class="modal-title">견적·문의하기</h2>
        <p class="modal-subtitle">아래 내용을 작성해주시면 빠르게 검토 후 연락드리겠습니다.</p>
      </div>

      <form @submit.prevent="submitForm" class="contact-form">
        <!-- 제목 -->
        <div class="form-group">
          <label>제목 <span class="required">*</span></label>
          <input type="text" v-model="form.title" placeholder="예) 브랜드 영상 제작 문의" required />
        </div>

        <!-- 성함 / 회사명 -->
        <div class="form-row">
          <div class="form-group">
            <label>성함 <span class="required">*</span></label>
            <input type="text" v-model="form.name" placeholder="홍길동" required />
          </div>
          <div class="form-group">
            <label>회사명</label>
            <input type="text" v-model="form.company" placeholder="하이어 프로덕션" />
          </div>
        </div>

        <!-- 연락처 -->
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

        <!-- 이메일 / 카테고리 -->
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

        <!-- 예산 -->
        <div class="form-group">
          <div class="budget-header">
            <label>예산</label>
            <NuxtLink to="/services" class="plan-link" @click="close">플랜 보기 &rarr;</NuxtLink>
          </div>
          <div class="budget-options">
            <label class="budget-radio" :class="{ active: form.budget === '플랜 A' }">
              <input type="radio" v-model="form.budget" value="플랜 A" /> 플랜 A
            </label>
            <label class="budget-radio" :class="{ active: form.budget === '플랜 B' }">
              <input type="radio" v-model="form.budget" value="플랜 B" /> 플랜 B
            </label>
            <label class="budget-radio" :class="{ active: form.budget === '상담 후 협의' }">
              <input type="radio" v-model="form.budget" value="상담 후 협의" /> 상담 후 협의
            </label>
            <label class="budget-radio" :class="{ active: form.budget === '기타' }">
              <input type="radio" v-model="form.budget" value="기타" /> 기타
            </label>
          </div>
        </div>

        <!-- 상세 요청사항 -->
        <div class="form-group">
          <label>상세 요청사항</label>
          <textarea v-model="form.details" rows="3" placeholder="레퍼런스, 촬영 일정, 특이사항 등 자유롭게 작성해주세요."></textarea>
        </div>

        <!-- 버튼 -->
        <button type="submit" class="submit-btn" :disabled="isSubmitting">
          {{ isSubmitting ? '전송 중...' : '견적 받아보기 &rarr;' }}
        </button>
      </form>

      <div class="modal-footer">
        higher3pd@gmail.com - +82 10-3313-0388
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

const close = () => {
  emit('update:modelValue', false)
}

const form = reactive({
  title: '',
  name: '',
  company: '',
  phone1: '',
  phone2: '',
  phone3: '',
  email: '',
  category: '',
  budget: '상담 후 협의',
  details: ''
})

const isSubmitting = ref(false)

const submitForm = async () => {
  if (isSubmitting.value) return
  isSubmitting.value = true

  try {
    const payload = {
      title: form.title,
      name: form.name,
      company: form.company,
      phone: `${form.phone1}-${form.phone2}-${form.phone3}`,
      email: form.email,
      category: form.category,
      budget: form.budget,
      details: form.details
    }

    const res = await fetch('http://127.0.0.1:8000/work/inquiries/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (!res.ok) {
      throw new Error('전송 실패')
    }

    alert('문의가 성공적으로 접수되었습니다. 빠르게 확인 후 연락드리겠습니다.')
    close()
    
    // 폼 초기화
    Object.assign(form, {
      title: '', name: '', company: '', phone1: '', phone2: '', phone3: '',
      email: '', category: '', budget: '상담 후 협의', details: ''
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
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  padding: 20px;
}

.modal-content {
  background-color: #fcfcfc;
  width: 100%;
  max-width: 650px;
  border-radius: 12px;
  padding: 30px;
  position: relative;
  max-height: 95vh;
  overflow-y: auto;
  font-family: 'Pretendard', -apple-system, sans-serif;
  box-shadow: 0 20px 40px rgba(0,0,0,0.2);
}

/* 스크롤바 숨기기 (선택) */
.modal-content::-webkit-scrollbar {
  display: none;
}
.modal-content {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.close-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  background: none;
  border: none;
  font-size: 24px;
  color: #999;
  cursor: pointer;
  padding: 5px;
  line-height: 1;
}

.close-btn:hover {
  color: #333;
}

/* Header */
.modal-header {
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
}

.brand-label {
  display: block;
  font-size: 11px;
  font-weight: 700;
  color: #1a3ae0;
  margin-bottom: 8px;
  letter-spacing: 1px;
}

.modal-title {
  font-size: 20px;
  font-weight: 800;
  margin: 0 0 5px 0;
  color: #111;
}

.modal-subtitle {
  font-size: 12px;
  color: #666;
  margin: 0;
}

/* Form */
.contact-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.form-row {
  display: flex;
  gap: 15px;
}
.form-row .form-group {
  flex: 1;
}

.form-group label {
  display: block;
  font-size: 11px;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}

.required {
  color: #1a3ae0;
}

input[type="text"],
input[type="email"],
select,
textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 13px;
  background-color: #fff;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: #1a3ae0;
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
  margin-bottom: 8px;
}
.budget-header label { margin: 0; }

.plan-link {
  font-size: 11px;
  font-weight: 600;
  color: #1a3ae0;
  text-decoration: none;
  border: 1px solid #1a3ae0;
  padding: 4px 10px;
  border-radius: 12px;
  transition: all 0.2s;
}
.plan-link:hover {
  background-color: #1a3ae0;
  color: #fff;
}

.budget-options {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.budget-radio {
  display: inline-block;
  padding: 10px 14px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 13px;
  color: #555;
  cursor: pointer;
  background: #fff;
  transition: all 0.2s;
  margin: 0;
  flex: 1;
  text-align: center;
  white-space: nowrap;
}

.budget-radio input {
  display: none;
}

.budget-radio.active {
  border-color: #1a3ae0;
  color: #1a3ae0;
  font-weight: 600;
  background-color: rgba(26, 58, 224, 0.03);
}

/* Submit */
.submit-btn {
  background-color: #111;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 12px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-top: 5px;
}

.submit-btn:hover {
  background-color: #333;
}

.submit-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

/* Footer */
.modal-footer {
  text-align: center;
  font-size: 10px;
  color: #999;
  margin-top: 20px;
}
</style>
