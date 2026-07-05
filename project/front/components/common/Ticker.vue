<template>
  <div class="ticker-wrap">
    <div class="ticker-track">
      <!-- 끊임없이 자연스럽게 이어지게 하기 위해 내용을 두 번 반복합니다 -->
      <div class="ticker-content">
        <span>FILM ✕ MOTION ✕ BRAND — HIGHER PRODUCTION</span>
        <span>FILM ✕ MOTION ✕ BRAND — HIGHER PRODUCTION</span>
        <span>FILM ✕ MOTION ✕ BRAND — HIGHER PRODUCTION</span>
      </div>
      <div class="ticker-content">
        <span>FILM ✕ MOTION ✕ BRAND — HIGHER PRODUCTION</span>
        <span>FILM ✕ MOTION ✕ BRAND — HIGHER PRODUCTION</span>
        <span>FILM ✕ MOTION ✕ BRAND — HIGHER PRODUCTION</span>
      </div>
    </div>
  </div>
</template>

<script setup>
// 나중에 프롭스(Props)로 외부에서 텍스트를 받아오게 만들 수도 있습니다.
// 현재는 기본 세팅만 둡니다.
</script>

<style scoped>
/* 가장 바깥쪽: 넘치는 텍스트를 숨겨주는 창문 역할 */
.ticker-wrap {
  position: relative;
  z-index: 10;
  width: 100%;
  overflow: hidden;
  background-color: var(--primary-color); /* 파란색 배경 */
  color: #fff;
  padding: 12px 0; /* 위아래 여백 */
  display: flex;
  white-space: nowrap;
}

/* 실제로 굴러가는 트랙 영역 */
.ticker-track {
  display: flex;
  /* 20초 동안 왼쪽으로 일정한 속도(linear)로 무한 반복 */
  animation: marquee 150s linear infinite;
}

/* (선택사항) 마우스 올리면 스크롤 멈춤 효과 */
.ticker-wrap:hover .ticker-track {
  animation-play-state: paused;
}

/* 텍스트 덩어리 디자인 */
.ticker-content {
  display: flex;
  gap: 100px; /* 문구 사이 간격 */
  padding-right: 100px; /* 두 덩어리 사이 간격 (gap과 동일하게 맞춰야 끊김이 없음) */
  font-family: var(--font-mono);
  /* 브라우저 너비에 따라 글자 크기가 물 흐르듯 자연스럽게 커지고 작아집니다 
     최소 28px ~ 최대 64px 사이에서 화면 크기(6vw)에 비례해서 변함 */
  font-size: clamp(28px, 6vw, 64px);
  font-weight: 600;
  letter-spacing: 0.1em;
}

/* 핵심! 부드러운 무한 롤링 키프레임 */
@keyframes marquee {
  0% {
    transform: translateX(0);
  }
  100% {
    /* 전체 길이의 절반(1개 덩어리)만큼 이동하면 다시 0%로 순간이동해서 무한반복됨 */
    transform: translateX(-50%);
  }
}
</style>
