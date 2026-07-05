<template>
  <footer class="global-footer">
    <div class="footer-container">
      
      <!-- 푸터 헤더 (About 섹션과 동일한 스타일) -->
      <div class="footer-header">
        <div class="header-left">
          <span class="header-bracket">[ 03 / contact ]</span>
          <h2 class="header-title">GET IN TOUCH</h2>
        </div>
        <div class="header-right">
          <span class="header-desc">하이어, 더 높은 곳으로</span>
        </div>
      </div>

      <!-- 상단 메인 텍스트 영역 -->
      <div class="footer-top">
        <div class="footer-top-text">
          <h2 class="main-heading">당신의 브랜드,<br>한 단계 더 위로</h2>
          <div class="sub-heading-wrap">
            <span class="arrow-icon">→</span>
            <h3 class="sub-heading">Let's go higher.</h3>
          </div>
        </div>
        
        <div class="cta-wrap">
          <button class="btn-contact" @click="showContactModal = true">
            문의하기 <span class="btn-arrow">→</span>
          </button>
        </div>
      </div>

      <!-- 연락처 정보 컬럼 영역 -->
      <div class="footer-info">
        <div class="info-col">
          <span class="info-label">EMAIL</span>
          <a href="mailto:higher3pd@gmail.com" class="info-value">higher3pd@gmail.com</a>
        </div>
        <div class="info-col">
          <span class="info-label">PHONE</span>
          <a href="tel:+821033130388" class="info-value">+82 10-3313-0388</a>
        </div>
        <div class="info-col">
          <span class="info-label">STUDIO</span>
          <span class="info-value">경기도 의정부시, KR</span>
        </div>
        <div class="info-col">
          <span class="info-label">INSTAGRAM</span>
          <a href="https://instagram.com/higher.production" target="_blank" rel="noopener noreferrer" class="info-value">@higher.production</a>
        </div>
      </div>

      <!-- 하단 카피라이트 영역 -->
      <div class="footer-bottom">
        <div class="copyright">
          © 2026 HIGHER PRODUCTION — ALL FRAMES RESERVED
        </div>
        <div class="designer-mark" @click="scrollToTop">
          DESIGNED IN KOREA — GO HIGHER ↑
        </div>
      </div>

    </div>

    <!-- 문의하기 팝업 모달 -->
    <ContactModal v-model="showContactModal" />
  </footer>
</template>

<script setup>
import { ref } from 'vue'
import ContactModal from '~/components/common/ContactModal.vue'

const showContactModal = ref(false)

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}
</script>

<style scoped>
.global-footer {
  background-color: #0b0c10; /* 다크 네이비/블랙 배경 */
  color: #ffffff;
  padding: 120px 0 40px;
  font-family: 'Pretendard', -apple-system, sans-serif;
}

.footer-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 40px;
}

/* 푸터 상단 헤더 (About 스타일) */
.footer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding-bottom: 20px;
  margin-bottom: 80px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.header-bracket {
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 1px;
}

.header-title {
  font-size: 24px;
  font-weight: 800;
  margin: 0;
  letter-spacing: 0.5px;
}

.header-right .header-desc {
  font-size: 14px;
  opacity: 0.8;
  letter-spacing: 1px;
}

/* 상단 메인 텍스트 */
.footer-top {
  text-align: center; /* 전체 블록은 중앙 정렬 */
  margin-bottom: 100px;
}

.footer-top-text {
  display: inline-block; /* 내용물 너비만큼 차지하게 하여 중앙에 배치되도록 함 */
  text-align: left; /* 텍스트 자체는 좌측 정렬 */
  margin-bottom: 50px;
}

.main-heading {
  font-size: clamp(48px, 6vw, 72px);
  font-weight: 800;
  line-height: 1.2;
  margin: 0 0 20px 0;
  letter-spacing: -2px;
}

.sub-heading-wrap {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 15px;
}

.arrow-icon {
  font-size: clamp(40px, 5vw, 60px);
  color: #1a3ae0;
  font-weight: 400;
}

.sub-heading {
  font-size: clamp(48px, 6vw, 72px);
  font-weight: 700;
  color: #1a3ae0;
  margin: 0;
  letter-spacing: -1px;
}

.cta-wrap {
  display: flex;
  justify-content: center; /* 다시 중앙 정렬로 변경 */
}

.btn-contact {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background-color: #1a3ae0;
  color: #ffffff;
  padding: 16px 36px;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 700;
  text-decoration: none;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.btn-contact:hover {
  background-color: #152bb5;
  transform: translateY(-2px);
}

.btn-arrow {
  font-weight: 400;
}

/* 연락처 정보 컬럼 */
.footer-info {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 40px 0;
  margin-bottom: 40px;
}

.info-col {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 0 20px;
  border-right: 1px solid rgba(255, 255, 255, 0.1);
}

.info-col:first-child {
  padding-left: 0;
}

.info-col:last-child {
  padding-right: 0;
  border-right: none;
}

.info-label {
  font-size: 11px;
  font-weight: 600;
  color: #666;
  letter-spacing: 1px;
}

.info-value {
  font-size: 15px;
  font-weight: 600;
  color: #fff;
  text-decoration: none;
  transition: color 0.2s ease;
}

a.info-value:hover {
  color: #1a3ae0;
}

/* 하단 카피라이트 */
.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 11px;
  font-weight: 500;
  color: #555;
  letter-spacing: 1px;
}

.designer-mark {
  cursor: pointer;
  transition: color 0.2s ease;
}

.designer-mark:hover {
  color: #fff;
}

/* 반응형 모바일 최적화 */
@media (max-width: 1024px) {
  .footer-info {
    grid-template-columns: repeat(2, 1fr);
    row-gap: 40px;
  }
  .info-col:nth-child(2) {
    border-right: none;
  }
  .info-col:nth-child(3) {
    padding-left: 0;
  }
}

@media (max-width: 600px) {
  .footer-info {
    grid-template-columns: 1fr;
    row-gap: 30px;
  }
  .info-col {
    padding: 0;
    border-right: none;
  }
  
  .footer-bottom {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
}
</style>
