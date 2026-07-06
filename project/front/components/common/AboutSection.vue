<template>
  <section class="about-section">
    <div class="about-container">
      <div class="about-header">
        <div class="header-left">
          <span class="header-bracket">[ {{ sectionIndex }} / about ]</span>
          <h2 class="header-title">{{ title }}</h2>
        </div>
        <div class="header-right">
          <span class="header-desc">{{ desc }}</span>
        </div>
      </div>

      <div class="about-content">
        <div class="content-left">
          <h3 class="main-heading">
            <template v-for="(line, idx) in aboutHeadings" :key="idx">
              <span :class="{ 'highlight-text': line.is_highlighted }" style="white-space: nowrap; word-break: keep-all;">{{ line.text }}</span><br />
            </template>
            <span class="logo-text">
              <img src="/nav_logo_en.png" alt="HIGHER PRODUCTION" class="logo-img" />
            </span>
          </h3>
        </div>
        
        <div class="content-right">
          <div class="feature-item">
            <div class="feature-number">01</div>
            <div class="feature-text">
              <p class="feature-subtitle">SPECIALTY BY INDUSTRY</p>
              <h4 class="feature-title">업종별 전문성을 그대로</h4>
              <p class="feature-desc">
                브랜드 업종의 전문성을 머금을 수 있는 채널&콘텐츠 기획하며<br/>
                영상의 단순한 콘텐츠성을 넘어 <strong>브랜드의 신뢰와 가치</strong>를 높입니다.
              </p>
            </div>
          </div>
          
          <div class="feature-item">
            <div class="feature-number">02</div>
            <div class="feature-text">
              <p class="feature-subtitle">BRAND STAYS FOCUSED</p>
              <h4 class="feature-title">브랜드는 오직 본업에 집중</h4>
              <p class="feature-desc">
                브랜드는 오직 전문적인 정보와 팩트 체크에 집중,<br/>
                해당 정보를 토대로 신뢰가 쌓이고 트래픽이 모이는<br/>
                <strong>콘텐츠 기획은 하이어프로덕션</strong>에서 진행하겠습니다.
              </p>
            </div>
          </div>
          
          <div class="feature-item">
            <div class="feature-number">03</div>
            <div class="feature-text">
              <p class="feature-subtitle">UPWARD WITH THE CHANNEL</p>
              <h4 class="feature-title">채널과 함께 우상향하는 브랜드</h4>
              <p class="feature-desc">
                시즌별·업종별·고객 관심별 기획 등을 통해 채널 우상향 전략을 수립하고<br/>
                <strong>고품질 콘텐츠</strong>를 통해 채널의 성장과 브랜드의 우상향을 만들어냅니다.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  sectionIndex: { type: String, default: '02' },
  title: { type: String, default: 'ABOUT THE STUDIO' },
  desc: { type: String, default: '하이어, 더 높은 곳으로' }
})

const aboutHeadings = ref([
  { text: '브랜드의 고도를 높이는', is_highlighted: false },
  { text: '우상향 프로덕션', is_highlighted: false }
])

const loadSiteSetting = async () => {
  try {
    const data = await $fetch('http://127.0.0.1:8000/system/settings/')
    if (data && data.about_headings && data.about_headings.length > 0) {
      aboutHeadings.value = data.about_headings
    }
  } catch (e) {
    console.error('Failed to load site setting:', e)
  }
}

onMounted(() => {
  loadSiteSetting()
})
</script>

<style scoped>
.about-section {
  position: relative;
  z-index: 10;
  background-color: var(--primary-color); /* 메인 블루 컬러 */
  color: #ffffff;
  padding: 80px 40px 120px;
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', sans-serif;
}

.about-container {
  max-width: 1400px;
  margin: 0 auto;
}

/* 상단 헤더 영역 */
.about-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding-bottom: 20px;
  margin-bottom: 60px;
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
  font-weight: 500;
  letter-spacing: 1px;
}

.header-title {
  font-size: clamp(14px, 2.5vw + 8px, 24px);
  font-weight: 800;
  margin: 0;
  letter-spacing: 0.5px;
}

.header-desc {
  font-size: clamp(10px, 1.5vw + 6px, 14px);
  opacity: 0.8;
  letter-spacing: 1px;
}

/* 메인 컨텐츠 영역 */
.about-content {
  display: flex;
  justify-content: space-between;
  gap: 60px;
}

/* 왼쪽 타이틀 영역 */
.content-left {
  flex: 1;
  align-self: center; /* 수직 중앙 정렬 추가 */
}

.main-heading {
  font-size: 52px;
  font-weight: 700;
  line-height: 1.3;
  margin: 0;
  letter-spacing: -1px;
}

.highlight-text {
  color: var(--primary-deep-color); /* 강조 텍스트 색상 (노란색) */
  font-weight: 800;
}

.logo-text {
  display: inline-flex;
  align-items: center;
  font-size: 64px;
  font-weight: 900;
  line-height: 1.1;
  margin-top: 20px;
  letter-spacing: -2px;
}

.logo-img {
  margin: auto;
  height: 80px; 
  width: auto;
  /* 파란색 로고를 완전히 흰색으로 만들기 위한 필터 */
  filter: brightness(0) invert(1); 
}

/* 오른쪽 특징 리스트 영역 */
.content-right {
  flex: 1;
  display: flex;
  flex-direction: column;
  /* 화면이 좁아질 때 반응하는 동적 왼쪽 마진 추가 (화면 너비의 5% 정도) */
  margin-left: 5vw; 
}

.feature-item {
  display: flex;
  gap: 30px;
  padding: 35px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
}

.feature-item:first-child {
  padding-top: 0;
}

.feature-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.feature-number {
  font-size: 48px;
  font-weight: 800;
  line-height: 1;
  min-width: 60px;
}

.feature-text {
  flex: 1;
}

.feature-subtitle {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 2px;
  margin: 0 0 10px 0;
  opacity: 0.7;
}

.feature-title {
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 15px 0;
  letter-spacing: -0.5px;
}

.feature-desc {
  font-size: 15px;
  line-height: 1.6;
  margin: 0;
  opacity: 0.9;
  word-break: keep-all;
}

.feature-desc strong {
  background-color: rgba(255, 255, 255, 0.2);
  padding: 2px 6px;
  border-radius: 2px;
  font-weight: 600;
}

/* 반응형 디자인 */
@media (max-width: 1024px) {
  .about-content {
    flex-direction: column;
    gap: 50px;
  }
  
  .main-heading {
    font-size: 42px;
  }
  
  .logo-text {
    font-size: 52px;
  }
}

@media (max-width: 768px) {
  .about-section {
    padding: 60px 20px 80px;
  }
  
  .main-heading {
    font-size: 32px;
  }
  
  .logo-text {
    font-size: 40px;
  }
  
  .feature-item {
    flex-direction: column;
    gap: 15px;
  }
  
  .feature-number {
    font-size: 36px;
  }
  
  .feature-title {
    font-size: 20px;
  }
}
</style>
