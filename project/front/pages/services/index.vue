<template>
  <div class="services-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          처음부터 <span class="text-gradient">제대로</span>,<br>
          꾸준히 <span class="text-gradient">높게</span>.
        </h1>
        <p class="hero-subtitle">
          단순한 영상 제작을 넘어, 브랜드의 성장을 위한 전략적 파트너가 됩니다.<br>
          {{ siteSetting.logo_kr }}의 체계적인 월간 운영 플랜을 만나보세요.
        </p>
      </div>
      <div class="hero-bg-glow"></div>
    </section>

    <!-- Plans Detailed Section -->
    <section class="plans-section">
      <div class="section-container">
        <div class="section-header">
          <h2 class="section-title">MONTHLY PLANS</h2>
          <p class="section-desc">채널의 단계에 맞춰 시작합니다. 모든 플랜은 4주(한달) 기준입니다.</p>
        </div>

        <div v-if="pending" class="loading-state">
          플랜 정보를 불러오는 중입니다...
        </div>
        
        <div v-else class="plans-grid">
          <div 
            v-for="(plan, index) in plans" 
            :key="plan.id" 
            class="plan-card"
            :class="[index % 2 === 0 ? 'plan-light' : 'plan-dark']"
          >
            <!-- Card Header -->
            <div class="plan-header">
              <div class="plan-badge">PLAN {{ String.fromCharCode(65 + index) }}</div>
              <h3 class="plan-name">{{ plan.name }}</h3>
              <p class="plan-subname">{{ plan.subname }}</p>
              
              <div class="plan-price-box">
                <span class="price-currency">₩</span>
                <span class="price-amount">{{ plan.price.toLocaleString() }}</span>
                <span class="price-unit">만원</span>
                <span class="price-period">/ 4주 (VAT 별도)</span>
              </div>
            </div>

            <!-- Card Body -->
            <div class="plan-body">
              <div class="feature-group">
                <h4 class="feature-title">추천 대상</h4>
                <ul class="feature-list">
                  <li v-for="rec in plan.recommends" :key="rec.id">{{ rec.name }}</li>
                </ul>
              </div>

              <div class="feature-group">
                <h4 class="feature-title">운영 목적</h4>
                <ul class="feature-list">
                  <li v-for="op in plan.operations" :key="op.id">{{ op.name }}</li>
                </ul>
              </div>

              <div class="feature-group">
                <h4 class="feature-title">촬영 / 편수</h4>
                <div class="tags-container">
                  <span class="tag" v-for="prod in plan.productions" :key="prod.id">{{ prod.name }}</span>
                </div>
              </div>

              <div class="feature-group">
                <h4 class="feature-title">상세 제작 항목</h4>
                <ul class="feature-list checklist">
                  <li v-for="item in plan.items" :key="item.id">
                    <span class="check-icon">✓</span>
                    {{ item.name }}
                  </li>
                </ul>
              </div>
            </div>

            <!-- Card Footer -->
            <div class="plan-footer">
              <NuxtLink to="/contact">
                <button class="cta-button" :class="index % 2 === 0 ? 'btn-dark' : 'btn-light'">
                  문의하기
                  <span class="arrow">→</span>
                </button>
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Process Section -->
    <section class="process-section">
      <div class="section-container">
        <div class="section-header center">
          <h2 class="section-title">WORK PROCESS</h2>
          <p class="section-desc">체계적이고 투명한 제작 과정을 통해 최상의 퀄리티를 보장합니다.</p>
        </div>

        <div class="process-timeline">
          <div class="process-step">
            <div class="step-number">01</div>
            <div class="step-content">
              <h3>기획 및 전략 수립</h3>
              <p>브랜드 분석, 타겟 고객층 설정, 채널 방향성 및 레퍼런스 기획</p>
            </div>
          </div>
          <div class="process-step">
            <div class="step-number">02</div>
            <div class="step-content">
              <h3>사전 준비 (Pre-production)</h3>
              <p>스토리보드 작성, 장소/모델/소품 섭외 및 촬영 스케줄링</p>
            </div>
          </div>
          <div class="process-step">
            <div class="step-number">03</div>
            <div class="step-content">
              <h3>프로덕션 (Shooting)</h3>
              <p>전문 장비와 인력을 투입한 고퀄리티 현장 촬영 진행</p>
            </div>
          </div>
          <div class="process-step">
            <div class="step-number">04</div>
            <div class="step-content">
              <h3>포스트 프로덕션 (Editing)</h3>
              <p>컷 편집, 색보정, 모션 그래픽, 사운드 믹싱 및 피드백 반영</p>
            </div>
          </div>
          <div class="process-step">
            <div class="step-number">05</div>
            <div class="step-content">
              <h3>최종 납품 및 운영</h3>
              <p>플랫폼별 최적화 규격 납품 및 채널 업로드, 성과 분석</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const plans = ref([])
const pending = ref(true)

const siteSetting = ref({
  logo_kr: '하이어 프로덕션'
})

const loadSiteSetting = async () => {
  try {
    const data = await $fetch('http://127.0.0.1:8000/system/settings/')
    if (data && data.logo_kr) {
      siteSetting.value.logo_kr = data.logo_kr
    }
  } catch (e) {
    console.error('Failed to load site setting:', e)
  }
}

onMounted(async () => {
  loadSiteSetting()
  try {
    const data = await $fetch('http://127.0.0.1:8000/product/plans/')
    plans.value = data
  } catch (error) {
    console.error('Failed to load plans:', error)
  } finally {
    pending.value = false
  }
})
</script>

<style scoped>
.services-page {
  font-family: 'Pretendard', -apple-system, sans-serif;
  background-color: #fafafa; /* 밝은 테마 */
  color: #111;
  min-height: 100vh;
  overflow-x: hidden;
}

/* =========================================
   Hero Section
   ========================================= */
.hero-section {
  position: relative;
  padding: 180px 20px 100px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  overflow: hidden;
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 800px;
}

.hero-title {
  font-size: clamp(48px, 8vw, 80px);
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 30px;
  letter-spacing: -2px;
}

.text-gradient {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: clamp(16px, 2vw, 20px);
  color: #555;
  line-height: 1.6;
  font-weight: 400;
}

.hero-bg-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(26,58,224,0.3) 0%, rgba(0,0,0,0) 70%);
  border-radius: 50%;
  z-index: 1;
  pointer-events: none;
}

/* =========================================
   Common Layouts
   ========================================= */
.section-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 40px;
}

.section-header {
  margin-bottom: 60px;
}

.section-header.center {
  text-align: center;
}

.section-title {
  font-size: 32px;
  font-weight: 800;
  color: #111;
  margin-bottom: 15px;
  letter-spacing: 1px;
}

.section-desc {
  font-size: 16px;
  color: #666;
}

/* =========================================
   Plans Section
   ========================================= */
.plans-section {
  padding: 80px 0 120px;
  position: relative;
  z-index: 2;
}

.plans-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 40px;
}

.plan-card {
  border-radius: 24px;
  padding: 50px 40px;
  display: flex;
  flex-direction: column;
  transition: transform 0.4s cubic-bezier(0.165, 0.84, 0.44, 1), box-shadow 0.4s ease;
  position: relative;
  overflow: hidden;
}

.plan-card:hover {
  transform: translateY(-10px);
}

.plan-light {
  background: #ffffff;
  border: 1px solid #e0e0e0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.plan-light:hover {
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1), 0 0 0 1px #e0e0e0;
}

.plan-dark {
  background: linear-gradient(145deg, #1a3ae0 0%, #0d1e70 100%);
  border: 1px solid rgba(26, 58, 224, 0.5);
  color: #fff;
}

.plan-dark:hover {
  box-shadow: 0 20px 40px rgba(26, 58, 224, 0.3), 0 0 0 1px rgba(26,58,224,0.5);
}

/* Plan Header */
.plan-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1px;
  margin-bottom: 20px;
}

.plan-light .plan-badge { background: #f0f0f0; color: #111; }
.plan-dark .plan-badge { background: rgba(0,0,0,0.2); color: #fff; }

.plan-name {
  font-size: 36px;
  font-weight: 800;
  margin: 0 0 10px 0;
  letter-spacing: -1px;
}

.plan-subname {
  font-size: 15px;
  opacity: 0.7;
  margin: 0 0 40px 0;
}

.plan-price-box {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 40px;
  padding-bottom: 40px;
  border-bottom: 1px solid #ddd;
}
.plan-dark .plan-price-box {
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.price-currency {
  font-size: 24px;
  font-weight: 600;
}

.price-amount {
  font-size: 64px;
  font-weight: 800;
  letter-spacing: -2px;
  line-height: 1;
}

.price-unit {
  font-size: 20px;
  font-weight: 700;
}

.price-period {
  font-size: 14px;
  opacity: 0.6;
  margin-left: auto; /* 우측 정렬 */
}

/* Plan Body */
.plan-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.feature-title {
  font-size: 14px;
  font-weight: 700;
  opacity: 0.5;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin: 0 0 15px 0;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.feature-list li {
  font-size: 16px;
  font-weight: 500;
  line-height: 1.5;
}

.checklist li {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.check-icon {
  font-size: 14px;
  font-weight: bold;
}
.plan-light .check-icon { color: #4facfe; }
.plan-dark .check-icon { color: #fff; opacity: 0.8; }

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag {
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
}

.plan-light .tag { background: #f8f9fa; border: 1px solid #ddd; color: #333; }
.plan-dark .tag { background: rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,0.1); }

/* Plan Footer */
.plan-footer {
  margin-top: 50px;
}

.cta-button {
  width: 100%;
  padding: 20px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 700;
  border: none;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s;
}

.btn-light {
  background: #fff;
  color: #111;
}
.btn-light:hover {
  background: #f0f0f0;
  transform: scale(1.02);
}

.btn-dark {
  background: #1a3ae0;
  color: #fff;
}
.btn-dark:hover {
  background: #152bb5;
  transform: scale(1.02);
}

/* =========================================
   Process Section
   ========================================= */
.process-section {
  padding: 100px 0 150px;
  background: #ffffff;
}

.process-timeline {
  max-width: 800px;
  margin: 60px auto 0;
  position: relative;
}

.process-timeline::before {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  left: 30px;
  width: 2px;
  background: linear-gradient(to bottom, #1a3ae0, #00f2fe);
  opacity: 0.3;
}

.process-step {
  display: flex;
  gap: 40px;
  margin-bottom: 50px;
  position: relative;
}

.process-step:last-child {
  margin-bottom: 0;
}

.step-number {
  width: 62px;
  height: 62px;
  background: #fff;
  border: 2px solid #1a3ae0;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  font-weight: 800;
  color: #111;
  z-index: 2;
  flex-shrink: 0;
  box-shadow: 0 0 15px rgba(26, 58, 224, 0.15);
}

.step-content {
  padding-top: 15px;
}

.step-content h3 {
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 10px 0;
  color: #111;
}

.step-content p {
  font-size: 16px;
  color: #555;
  line-height: 1.6;
  margin: 0;
}

/* =========================================
   Responsive Design
   ========================================= */
@media (max-width: 1024px) {
  .plans-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 140px 20px 80px;
  }
  
  .section-container {
    padding: 0 20px;
  }
  
  .plan-card {
    padding: 40px 30px;
  }
  
  .price-amount {
    font-size: 48px;
  }
  
  .process-step {
    flex-direction: column;
    gap: 20px;
  }
  
  .process-timeline::before {
    left: 31px;
  }
  
  .step-content {
    padding-top: 0;
    padding-left: 80px;
    margin-top: -62px;
  }
}
</style>
