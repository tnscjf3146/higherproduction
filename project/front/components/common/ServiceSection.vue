<template>
  <section class="service-section">
    <div class="service-container">
      
      <!-- 상단 헤더 영역 -->
      <div class="service-header-top">
        <div class="header-left">
          <span class="header-bracket">[ {{ sectionIndex }} / services ]</span>
          <h2 class="header-title">{{ title }}</h2>
        </div>
        <div class="header-right">
          <span class="header-desc">{{ desc }}</span>
        </div>
      </div>

      <!-- 메인 타이틀 영역 -->
      <div class="service-title-area">
        <h3 class="main-heading">
          처음부터 <span class="highlight-blue">제대로</span>, 꾸준히 <span class="highlight-blue">높게</span>.
        </h3>
        <p class="sub-heading">
          <strong>{{ plans.length }} 가지 운영 플랜</strong>으로 채널의 단계에 맞춰 시작합니다. 영상 마케팅이 처음인 기업부터 채널 성장과 브랜딩까지<br>
          플랜별로 같은 원칙, 다른 강도의 작업이 부과됩니다. 모든 플랜은 4주(한달) 기준이며, VAT별도입니다.
        </p>
      </div>

      <!-- 요금제 카드 영역 (슬라이더) -->
      <div class="slider-outer">
        <div class="plans-wrapper" ref="sliderRef" @scroll="onScroll">
          <div v-for="(plan, index) in plans" :key="plan.id" class="plan-card" :class="index % 2 === 0 ? 'plan-theme-light' : 'plan-theme-dark'">
            <div class="plan-header">
              <div class="plan-badge">
                <span class="badge-icon">{{ String.fromCharCode(65 + index) }}</span>
                <span class="badge-text">PLAN {{ String.fromCharCode(65 + index) }} - {{ plan.name }}</span>
              </div>
              <h4 class="plan-name">{{ plan.name }}</h4>
              <p class="plan-subname">{{ plan.subname }}</p>
              <div class="plan-price-wrap">
                <span class="price-number">{{ plan.price }}</span>
                <div class="price-meta">
                  <span class="price-unit">만원</span>
                  <span class="price-period">4주 / VAT 별도</span>
                </div>
              </div>
            </div>

            <div class="plan-details">
              <div class="detail-row">
                <div class="row-label">추천 대상</div>
                <div class="row-value">
                  <span v-for="(rec, idx) in plan.recommends" :key="rec.id">
                    {{ rec.name }}<br v-if="idx < plan.recommends.length - 1">
                  </span>
                </div>
              </div>
              <div class="detail-row">
                <div class="row-label">운영 목적</div>
                <div class="row-value">
                  <span v-for="(op, idx) in plan.operations" :key="op.id">
                    {{ op.name }}<br v-if="idx < plan.operations.length - 1">
                  </span>
                </div>
              </div>
              <div class="detail-row">
                <div class="row-label">촬영 / 편수</div>
                <div class="row-value">
                  <span v-for="(prod, idx) in plan.productions" :key="prod.id">
                    {{ prod.name }}<span v-if="idx < plan.productions.length - 1"> · </span>
                  </span>
                </div>
              </div>
              <div class="detail-row">
                <div class="row-label">제작 항목</div>
                <div class="row-value list-value">
                  <ul>
                    <li v-for="item in plan.items" :key="item.id">{{ item.name }}</li>
                  </ul>
                </div>
              </div>
            </div>
            <button class="plan-btn" :class="index % 2 === 0 ? 'btn-theme-light' : 'btn-theme-dark'"> 문의하기 <span>→</span></button>
          </div>
        </div>

        <!-- 네비게이션 닷 (보여지는 개수보다 플랜이 많을 때만 표시) -->
        <div class="slider-dots" v-if="plans.length > visibleCount">
          <span 
            v-for="i in Math.max(1, plans.length - visibleCount + 1)" 
            :key="'dot-'+i" 
            class="dot" 
            :class="{ active: currentIdx === i - 1 }" 
            @click="scrollTo(i - 1)"
          ></span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  sectionIndex: { type: String, default: '01' },
  title: { type: String, default: 'MONTHLY PLAN' },
  desc: { type: String, default: '영상 운영 가격 / 한달 기준' }
})

const plans = ref([])
const sliderRef = ref(null)
const currentIdx = ref(0)
const visibleCount = ref(3)

const updateVisibleCount = () => {
  if (window.innerWidth <= 768) visibleCount.value = 1
  else if (window.innerWidth <= 1024) visibleCount.value = 2
  else visibleCount.value = 3
}

const onScroll = () => {
  if (!sliderRef.value) return
  const scrollLeft = sliderRef.value.scrollLeft
  const cardWidth = sliderRef.value.children[0].offsetWidth
  currentIdx.value = Math.round(scrollLeft / cardWidth)
}

const scrollTo = (index) => {
  if (!sliderRef.value) return
  const cardWidth = sliderRef.value.children[0].offsetWidth
  sliderRef.value.scrollTo({
    left: cardWidth * index,
    behavior: 'smooth'
  })
}

onMounted(async () => {
  try {
    const data = await $fetch(useRuntimeConfig().public.apiBaseUrl + '/product/plans/')
    plans.value = data
  } catch (err) {
    console.error('Failed to load plans:', err)
  }
  
  updateVisibleCount()
  window.addEventListener('resize', updateVisibleCount)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateVisibleCount)
})
</script>

<style scoped>
.service-section {
  position: relative;
  z-index: 10;
  background-color: #fafafa; /* 밝은 배경 */
  padding: 60px 40px 40px; /* 하단 여백 적당히 조절 */
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', sans-serif;
}

.service-container {
  max-width: 1400px;
  margin: 0 auto;
}

/* 상단 헤더 */
.service-header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ddd;
  padding-bottom: 15px;
  margin-bottom: 50px; /* 여백 축소 */
  white-space: nowrap;
  word-break: keep-all;
}

.header-left {
  display: flex;
  align-items: center;
  gap: clamp(8px, 2vw, 15px);
}

.header-bracket {
  font-size: clamp(10px, 1.5vw + 6px, 14px);
  font-weight: 600;
  color: var(--primary-color);
  letter-spacing: 1px;
}

.header-title {
  font-size: clamp(14px, 2.5vw + 8px, 24px);
  font-weight: 800;
  color: #111;
  margin: 0;
  letter-spacing: 0.5px;
}

.header-right .header-desc {
  font-size: clamp(10px, 1.5vw + 6px, 14px);
  color: #666;
}

/* 메인 타이틀 영역 */
.service-title-area {
  text-align: center;
  margin-bottom: 40px; /* 여백 축소 */
}

.main-heading {
  font-size: 56px;
  font-weight: 800;
  color: #111;
  margin: 0 0 25px 0;
  letter-spacing: -2px;
}

.highlight-blue {
  color: var(--primary-deep-color);
}

.sub-heading {
  font-size: 16px;
  color: #666;
  line-height: 1.6;
  margin: 0;
}

.sub-heading strong {
  color: #333;
}

/* 슬라이더 래퍼 설정 */
.slider-outer {
  position: relative;
  width: 100%;
}

.plans-wrapper {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
  border-top: 2px solid #ccc;
  margin-top: 20px;
  margin-bottom: 10px;
}

.plans-wrapper::-webkit-scrollbar {
  display: none; /* Chrome/Safari/Opera */
}

.plan-card {
  flex: 1 0 calc(100% / 3); /* 아이템이 적을 경우 꽉 차게 분배됨, 넘칠 경우 3개 너비 유지 */
  scroll-snap-align: start;
  padding: 60px 40px 80px; /* 카드 안쪽 상하 여백을 크게 줘서 카드 영역 자체를 길게 넓힘 */
  display: flex;
  flex-direction: column;
}

/* 네비게이션 닷 */
.slider-dots {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.slider-dots .dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: #ddd;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-bottom: 30px;
}

.slider-dots .dot.active {
  background-color: var(--primary-color);
}

/* 라이트 테마 (기존 베이직 플랜) */
.plan-theme-light {
  background-color: #fff;
  color: #111;
}

/* 다크 테마 (기존 그로스 플랜) */
.plan-theme-dark {
  background-color: var(--primary-color);
  color: #fff;
}

/* 뱃지 */
.plan-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 30px;
}

.badge-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  font-size: 12px;
  font-weight: 700;
}

.plan-theme-light .badge-icon {
  border: 1px solid var(--primary-color);
  color: var(--primary-color);
}
.plan-theme-dark .badge-icon {
  border: 1px solid #fff;
  color: #fff;
}

.badge-text {
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 1px;
}

.plan-theme-light .badge-text { color: var(--primary-color); }
.plan-theme-dark .badge-text { color: #fff; }

/* 플랜 제목 */
.plan-name {
  font-size: 32px;
  font-weight: 800;
  margin: 0 0 5px 0;
  letter-spacing: -1px;
}

.plan-subname {
  font-size: 14px;
  margin: 0 0 25px 0; /* 여백 축소 */
  opacity: 0.8;
}

/* 가격 영역 */
.plan-price-wrap {
  display: flex;
  align-items: baseline;
  gap: 15px;
  margin-bottom: 35px; /* 여백 축소 */
}

.price-number {
  font-size: 70px; /* 크기 축소 */
  font-weight: 800;
  line-height: 1;
  letter-spacing: -3px;
}

.price-meta {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.price-unit {
  font-size: 20px;
  font-weight: 800;
}

.plan-theme-dark .price-period {
  color: rgba(255, 255, 255, 0.7);
}

.price-period {
  font-size: 12px;
  opacity: 0.7;
}

/* 상세 내역 리스트 */
.plan-details {
  flex: 1;
  border-top: 1px solid;
  border-color: rgba(0,0,0,0.1);
  padding-top: 20px;
}

.plan-theme-dark .plan-details {
  border-color: rgba(255,255,255,0.2);
}

.detail-row {
  display: flex;
  padding: 20px 0;
  border-bottom: 1px solid;
}

.plan-theme-light .row-label { color: #666; border-right: 1px solid #eee; }
.plan-theme-dark .row-label { color: rgba(255,255,255,0.7); border-right: 1px solid rgba(255,255,255,0.2); }

.plan-theme-dark .detail-row {
  border-color: rgba(255,255,255,0.1);
}

.detail-row:last-child {
  border-bottom: none;
}

.row-label {
  width: 120px;
  font-size: 13px;
  font-weight: 600;
  opacity: 0.6;
}

.row-value {
  flex: 1;
  font-size: 14px;
  line-height: 1.5;
  font-weight: 500;
}

.list-value ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.list-value li {
  position: relative;
  padding-left: 12px;
  margin-bottom: 8px;
}

.list-value li::before {
  content: '·';
  position: absolute;
  left: 0;
  top: 0;
  font-weight: bold;
}

.plan-theme-light .list-value li::before {
  color: var(--primary-color);
}
.plan-theme-dark .list-value li::before {
  color: #fff;
}

/* 하단 버튼 */
.plan-btn {
  width: 100%;
  padding: 20px;
  font-size: 16px;
  font-weight: 700;
  border: none;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 40px;
  transition: all 0.3s ease;
}

.btn-theme-light {
  background-color: #111;
  color: #fff;
}
.btn-theme-light:hover {
  background-color: var(--primary-color);
}

.btn-theme-dark {
  background-color: #fff;
  color: var(--primary-color);
}
.btn-theme-dark:hover {
  background-color: #f0f0f0;
}

/* 반응형 */
@media (max-width: 1024px) {
  .plan-card {
    flex: 1 0 calc(100% / 2); /* 태블릿에서는 2개 보임 (적으면 분배) */
  }
  
  .price-number {
    font-size: 55px; /* 태블릿 폰트 크기 축소 */
  }
}

@media (max-width: 768px) {
  .service-section {
    padding: 60px 20px 0;
  }
  
  .main-heading {
    font-size: 36px;
  }
  
  .plan-card {
    padding: 40px 20px;
    flex: 1 0 100%; /* 모바일에서는 1개 보임 (적으면 분배) */
  }
  
  .row-label {
    width: 90px;
  }
}
</style>
