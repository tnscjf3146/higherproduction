<template>
  <div :class="`stage-${currentStage}`">
    <!-- 인트로(스플래시) 스크린 -->
    <div class="intro-screen">
      
      <div class="intro-meta intro-meta--top">
        <span>left_top_meta</span>
        <span>right_top_meta</span>
      </div>
      
      <!-- 로고 영역 -->
      <div class="intro-logo">
        <img src="/logo_kr.png" alt="logo" class="intro-logo-img">
      </div>

      <div class="intro-meta intro-meta--bottom">
        <span>left_bottom_meta</span>
        <span>right_bottom_meta</span>
      </div>

    </div>

    <!-- 실제 앱(페이지) 화면 -->

    <div style="position: relative; min-height: 100vh;">
      <div class="grid"></div>

      <div class="meta">
        <div class="meta-l">
          <span>NOW REELING — 2026 EDITION</span>
        </div>
        <div class="meta-r">
          <span>{{ currentTime }} KST SEOUL · KR</span>
        </div>
      </div>

      <div class="stage">
        <div class="logo-wrap">
          <!-- 뷰파인더 내부 메타 텍스트 6구역 -->
          <span class="cam-meta cam-meta--tl">
            <span class="record-dot"></span> REC 00:00:24
          </span>
          <span class="cam-meta cam-meta--tc">FILM ✕ MOTION ✕ BRAND</span>
          <span class="cam-meta cam-meta--tr">2026 / EDITION</span>

          <span class="cam-meta cam-meta--bl">HIGHER / 01</span>
          <span class="cam-meta cam-meta--bc">SEOUL — 37.5665° N · 126.9780° E</span>
          <span class="cam-meta cam-meta--br">HIGHER PRODUCTION</span>

          <img src="/logo_kr.png" alt="" class="stage-logo-img">
        </div>
      </div>
      <div class="meta">
        <div class="meta-l">
          <span>A FILM & MOTION STUDIO — EST. 2026</span>
        </div>
      </div>
      <div>
        <div class="meta-title">
          <p>We make work</p>
          <p>that <span style="color: var(--primary-color);">raises</span> the bar.</p>
        </div>
        <div class="meta-context">
          <p>
            우리는 더 멀리 보이는 영상을 만듭니다.
          </p>
        </div>
      </div>
      <CommonTicker></CommonTicker>
      
      <!-- 새로 추가된 Service 섹션 -->
      <CommonServiceSection />

      <!-- 새로 추가된 Stats 섹션 -->
      <CommonStatsSection />

      <!-- 새로 추가된 About 섹션 -->
      <CommonAboutSection />
    </div>
    
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const currentStage = ref(0)

/* 실시간 시계 로직 */
const currentTime = ref('')
let timer = null

const updateTime = () => {
  const now = new Date()
  // 24시간제 시:분:초 포맷으로 설정 (예: 14:05:32)
  currentTime.value = now.toLocaleTimeString('en-US', {
    hour12: false,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

onMounted(() => {
  // 컴포넌트가 로드되면 시계 작동 시작 (1초마다 업데이트)
  updateTime()
  timer = setInterval(updateTime, 1000)

  setTimeout(() => {
    currentStage.value = 1
  }, 100);

  setTimeout(() => {
    currentStage.value = 2
  }, 550);

  setTimeout(() => {
    currentStage.value = 3
  }, 3000);
})

onUnmounted(() => {
  // 다른 페이지로 이동할 때 타이머를 꺼서 메모리 누수 방지
  if (timer) clearInterval(timer)
})
</script>

<style scoped>
/* 인트로 화면 전체 영역 */
.intro-screen {
  justify-content: center;
  align-items: center;
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: var(--primary-color);
  color: #fff;
  display: flex;
  padding: 32px var(--gutter);
  opacity: 1;
  pointer-events: none;
  transition: opacity .9s cubic-bezier(.7,0,.2,1) .15s,
              transform 1.1s cubic-bezier(.7,0,.2,1);
}

.intro-screen::before{
  content: "";
  position: absolute; inset: 0;
  background-image:
    repeating-linear-gradient(45deg, rgba(255,255,255,.05) 0 1px, transparent 1px 14px);
  pointer-events: none;
}

.stage-2 .intro-screen,
.stage-3 .intro-screen{
  opacity: 0;
  transform: translateY(-100%);
}

.intro-logo{
  justify-content: center;
  align-items: center;
  width: clamp(350px, 50vw, 750px);
  height: auto;
  display: flex;
  flex-direction: column;
  filter: brightness(0) invert(1);
  transform: scale(0.85);
  opacity: 0;
  transition: opacity .8s cubic-bezier(.2,.7,.2,1) .15s,
              transform 1s cubic-bezier(.2,.8,.2,1) .15s;
  position: relative;
  z-index: 1;
}

/* 로고 텍스트 */
.intro-logo p{
  margin: 0;
  line-height: 0.9;
  text-align: center;
  font-size: clamp(32px,5vw,80px);
  font-family: var(--font-display);
  font-weight: 800;
}

.intro-logo-img{
  width: 100%;
  height: auto;
  display: block;
  object-fit: contain;
}

.stage-1 .intro-logo,
.stage-2 .intro-logo,
.stage-3 .intro-logo{
  opacity: 1;
  transform: scale(1);
}

.intro-meta{
  position: absolute;
  left: var(--gutter);
  right: var(--gutter);
  display: flex;
  justify-content: space-between;
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: rgba(255,255,255,.85);
  opacity: 0;
  transition: opacity .6s ease .35s;
}

.intro-meta--top{
  top: 32px;
}

.intro-meta--bottom{
  bottom: 32px;
}

.stage-1 .intro-meta,
.stage-2 .intro-meta,
.stage-3 .intro-meta{
  opacity: 1;
}

.grid{
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: .5;
  background-image: 
    linear-gradient(to right, var(--text-line) 1px, transparent 1px);
    background-size: calc(100% / 12) 100%;
}

.meta{
  pointer-events: none;
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: space-between;
  font-family: var(--font-mono);
  font-size: 14px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-mute);
  padding: 32px var(--gutter);
}

.meta-l,
.meta-r{
  display: inline-flex;
  gap: 16px;
  align-items: center;
}

/* 카메라 녹화중(REC) 빨간 점 깜빡임 효과 */
.record-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  background-color: #ff3b30; /* 쨍한 빨간색 */
  border-radius: 50%;
  
  /* 박스 그림자(box-shadow)를 이용해 바깥쪽에 연한 빨간색 테두리 원을 만듭니다 */
  box-shadow: 0 0 0 5px rgba(255, 59, 48, 0.3);
  
  animation: blink 2s infinite ease-in-out; /* 2초 간격으로 무한 반복 */
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.2; } /* 절반쯤 진행됐을 때 연해짐 */
}

.stage{
  position: relative;
  z-index: 1;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 24px 0;
  min-height: 60vh;
}

.stage-logo-img{
  width: clamp(800px, 65%, 1600px);
  height: auto;
  display: block;
  object-fit: contain;
  /* 6초 주기로 숨쉬듯 부드럽게 무한 반복 (로고 둥둥 효과) */
  animation: hire-logo-breath 6s infinite ease-in-out;
}

.logo-wrap{
  pointer-events: none;
  position: relative;
  width: 80%;
  display: flex;
  align-items: center;
  justify-content: center;
  filter: drop-shadow(0 30px 80px rgba(26,61,238,.18));
}

.logo-wrap::before{
  content: "";
  position: absolute;
  inset: 6% 8%;
  background: var(--primary-color);
  transform: scaleX(0);
  transition: transform 0.8s cubic-bezier(.7,0,.2,1);
  z-index: 0;
}

/* 카메라 구도(뷰파인더) 모서리 ┌ ┐ └ ┘ 프레임 효과 */
.logo-wrap::after {
  content: "";
  position: absolute;
  /* 로고보다 살짝 바깥으로 프레임을 씌우고 싶다면 -20px, 딱 맞추고 싶다면 0을 주세요 */
  inset: 0; 
  pointer-events: none;
  z-index: 2; /* 이미지보다 위로 오게 */

  /* 선 두께(t), 길이(l), 색상(c) 설정 */
  --t: 2px;
  --l: 30px;
  --c: var(--primary-color);

  /* 포커싱 애니메이션 준비 (크게 시작해서 투명한 상태) */
  transform: scale(1.15);
  opacity: 0;
  /* 0.8s 였던 시간을 1.8s로 늘려서 아주 천천히 고급스럽게 들어오도록 수정했습니다 */
  transition: transform 2.5s cubic-bezier(0.2, 0.8, 0.2, 1) 0.4s,
              opacity 1.8s ease 0.4s;

  /* 배경 그라디언트를 이용해 4개의 모서리에 선을 그려줍니다 (초고급 기술!) */
  background:
    linear-gradient(var(--c), var(--c)) 0 0 / var(--l) var(--t) no-repeat,
    linear-gradient(var(--c), var(--c)) 0 0 / var(--t) var(--l) no-repeat,
    linear-gradient(var(--c), var(--c)) 100% 0 / var(--l) var(--t) no-repeat,
    linear-gradient(var(--c), var(--c)) 100% 0 / var(--t) var(--l) no-repeat,
    linear-gradient(var(--c), var(--c)) 0 100% / var(--l) var(--t) no-repeat,
    linear-gradient(var(--c), var(--c)) 0 100% / var(--t) var(--l) no-repeat,
    linear-gradient(var(--c), var(--c)) 100% 100% / var(--l) var(--t) no-repeat,
    linear-gradient(var(--c), var(--c)) 100% 100% / var(--t) var(--l) no-repeat;
}

/* 인트로가 걷히는 스테이지 2에서 카메라가 '착!' 하고 포커스를 맞춥니다 */
.stage-2 .logo-wrap::after,
.stage-3 .logo-wrap::after {
  transform: scale(1); /* 원래 크기로 착! 줄어듦 */
  opacity: 1;          /* 선명하게 나타남 */
}

/* 뷰파인더 내부 메타 텍스트 설정 */
.cam-meta {
  position: absolute;
  z-index: 3; /* 프레임 위로 오게 */
  font-family: var(--font-mono);
  font-size: 14px;
  font-weight: bold;
  letter-spacing: 0.1em;
  color: var(--primary-color);
  opacity: 0; /* 처음엔 투명하게 숨김 */
  pointer-events: none;
}

/* 상하좌우 및 중앙 모서리 배치 */
.cam-meta--tl { top: 20px; left: 24px; display: inline-flex; align-items: center; gap: 8px; }
.cam-meta--tc { top: 20px; left: 50%; transform: translateX(-50%); }
.cam-meta--tr { top: 20px; right: 24px; }
.cam-meta--bl { bottom: 20px; left: 24px; }
.cam-meta--bc { bottom: 20px; left: 50%; transform: translateX(-50%); }
.cam-meta--br { bottom: 20px; right: 24px; }

/* 스테이지 2가 되면 프레임 포커스와 함께 서서히 나타남 */
.stage-2 .cam-meta,
.stage-3 .cam-meta {
  opacity: 1;
  transition: opacity 1.8s ease 0.8s; /* 프레임이 어느 정도 들어온 뒤에 텍스트가 뜸 */
}

.stage-1 .logo-wrap::before{
  transform: scaleX(1);
  transform-origin: left center;
}
.stage-2 .logo-wrap::before,
.stage-3 .logo-wrap::before{
  transform: scaleX(0);
  transform-origin: right center;
  /* 사라질 때(나갈 때)만 적용되는 트랜지션 (들어올 때 0.8s보다 느린 1.5s) */
  transition: transform 1s cubic-bezier(.7,0,.2,1);
}

.stage-logo-img,
.logo-wrap,
.meta {
  user-select: none;
  -webkit-user-select: none;
  -webkit-user-drag: none;
  pointer-events: none;
}

@keyframes hire-logo-breath {
  /* 로고가 둥둥 떠다니는 애니메이션 키프레임 */
  0%, 100% { transform: scale(1) translateY(0); }
  50%      { transform: scale(1.08) translateY(-10px); }
}

/* 반응형(모바일) 디자인: 창이 작아졌을 때 */
@media (max-width: 768px) {
  /* 불필요한 메타 텍스트 숨기기 (tc, bl, br, meta-l 만 남기고 숨김) */
  .cam-meta--tl,
  .cam-meta--tr,
  .cam-meta--bc,
  .meta-r {
    display: none !important;
  }

  /* 텍스트 크기 축소 */
  .cam-meta {
    font-size: 9px;
  }
  
  .meta {
    font-size: 10px;
    padding: 12px var(--gutter); /* 여백도 폰트 크기에 맞게 살짝 축소 */
  }
}

.meta-title {
  margin: 0 var(--gutter);
  font-family: var(--font-display);
  font-size: clamp(32px,5vw,48px);
  font-weight: 480;
  line-height: 1.2;
}

.meta-context {
  margin: 16px var(--gutter);
  font-family: var(--font-display);
  font-size: clamp(18px,5vw,22px);
  color: var(--text-mute);
  line-height: 1.2;
}


</style>
