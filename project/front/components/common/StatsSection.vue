<script setup>
import { useFetch } from '#app'

// 백엔드 API에서 통계 정보 가져오기 (만약 실패하거나 로딩 중이면 기본 0으로 표시)
const { data: stats } = await useFetch(useRuntimeConfig().public.apiBaseUrl + '/work/stats/', {
  default: () => ({
    projects_count: 0,
    final_cuts_count: 0,
    clients_count: 0,
    categories_count: 0
  })
})

// 범주 숫자(카테고리)가 10 미만일 경우 앞에 0을 붙여주는 헬퍼 함수
const padZero = (num) => num < 10 ? `0${num}` : num
</script>

<template>
  <section class="stats-section">
    <div class="stats-container">
      <div class="stat-item">
        <h3 class="stat-number">{{ stats.projects_count }}+</h3>
        <p class="stat-en">PROJECTS / 2024-26</p>
        <p class="stat-ko">납품 프로젝트</p>
      </div>
      
      <div class="stat-divider"></div>
      
      <div class="stat-item">
        <h3 class="stat-number">{{ stats.final_cuts_count }}</h3>
        <p class="stat-en">FINAL CUTS</p>
        <p class="stat-ko">최종 영상</p>
      </div>
      
      <div class="stat-divider"></div>
      
      <div class="stat-item">
        <h3 class="stat-number">{{ stats.clients_count }}+</h3>
        <p class="stat-en">BRAND CLIENTS</p>
        <p class="stat-ko">브랜드 클라이언트</p>
      </div>
      
      <div class="stat-divider"></div>
      
      <div class="stat-item">
        <h3 class="stat-number">{{ padZero(stats.categories_count) }}</h3>
        <p class="stat-en">CATEGORIES</p>
        <p class="stat-ko">전문 분야</p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.stats-section {
  position: relative;
  z-index: 10;
  background-color: #fafafa;
  padding: 80px 40px;
  border-top: 1px solid #eaeaea;
  border-bottom: 1px solid #eaeaea;
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', sans-serif;
}

.stats-container {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.stat-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 0 40px;
}

/* 첫 번째 요소는 왼쪽 여백 제거 */
.stat-item:first-child {
  padding-left: 0;
}

/* 마지막 요소는 오른쪽 여백 제거 */
.stat-item:last-child {
  padding-right: 0;
}

.stat-divider {
  width: 1px;
  height: 80px;
  background-color: #ddd;
}

.stat-number {
  font-size: 80px;
  font-weight: 800;
  color: var(--primary-color); /* 메인 블루 컬러 */
  margin: 0 0 20px 0;
  line-height: 1;
  letter-spacing: -2px;
}

.stat-en {
  font-size: 12px;
  font-weight: 700;
  color: #666;
  margin: 0 0 5px 0;
  letter-spacing: 2px;
}

.stat-ko {
  font-size: 14px;
  font-weight: 500;
  color: #888;
  margin: 0;
}

/* 반응형 디자인 */
@media (max-width: 1024px) {
  .stat-number {
    font-size: 60px;
  }
  
  .stat-item {
    padding: 0 20px;
  }
  
  .stat-divider {
    height: 60px;
  }
}

@media (max-width: 768px) {
  .stats-section {
    padding: 40px 10px;
  }
  
  .stats-container {
    flex-direction: row; /* 무조건 가로 유지 */
    justify-content: space-between;
    gap: 0;
  }
  
  .stat-item {
    padding: 0 5px;
    align-items: center;
    text-align: center;
  }

  .stat-number {
    font-size: clamp(24px, 6vw, 40px); /* 폰트 크기를 화면에 맞게 자동 축소 */
    margin-bottom: 8px;
    letter-spacing: -1px;
  }

  .stat-en {
    font-size: clamp(8px, 1.8vw, 10px);
    letter-spacing: 0;
    white-space: nowrap; /* 줄바꿈 방지 */
  }

  .stat-ko {
    font-size: clamp(9px, 2.2vw, 12px);
    white-space: nowrap; /* 줄바꿈 방지 */
  }
  
  .stat-divider {
    width: 1px;
    height: 40px; /* 구분선은 세로로 유지하되 길이 축소 */
  }
}
</style>
