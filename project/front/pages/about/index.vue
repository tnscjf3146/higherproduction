<template>
  <div class="about-page">
    
    <!-- Floating Side Navigation -->
    <nav class="floating-nav">
      <ul>
        <li 
          v-for="(sec, index) in sectionData" 
          :key="sec.id"
          :class="{ active: activeSection === sec.id }"
          @click="scrollToSection(sec.id)"
        >
          <span class="nav-title">{{ sec.title }}</span>
          <span class="nav-dot"></span>
        </li>
        <li class="nav-divider"></li>
        <li class="contact-link" @click="goToContact">
          <span class="nav-title">문의하기</span>
          <span class="nav-dot"></span>
        </li>
      </ul>
    </nav>

    <!-- Content Sections -->
    <div class="content-wrapper">
      <div 
        v-for="sec in sectionData" 
        :key="sec.id" 
        :id="sec.id" 
        class="about-section"
        ref="sectionRefs"
      >
        <div class="simple-gallery">
          <div 
            v-for="(img, idx) in sec.images" 
            :key="idx" 
            class="gallery-item"
            :class="{ 'clickable-image': img === '34.gif' }"
          >
            <!-- 34.gif인 경우 works로 이동하는 링크 래핑 -->
            <NuxtLink v-if="img === '34.gif'" to="/works" style="width: 100%; display: flex; justify-content: center;">
              <img :src="`/jpg/${img}`" :alt="`${sec.title} image ${idx + 1}`" loading="lazy" style="cursor: pointer;" />
            </NuxtLink>
            <!-- 그 외 일반 이미지 -->
            <img v-else :src="`/jpg/${img}`" :alt="`${sec.title} image ${idx + 1}`" loading="lazy" />
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 사용자가 지정한 시작 기준점에 맞춰 이미지들을 분배
const sectionData = ref([
  { id: 'intro', title: '소개', images: ['01.gif', '02.gif', '03.gif'] },
  { id: 'team', title: '전문 팀', images: ['04.gif', '05.gif', '06.gif', '07.gif'] },
  { id: 'managing', title: '전문 매니징', images: ['08.gif', '09.gif', '10.gif', '11.gif', '12.gif', '13.gif', '14.gif'] },
  { id: 'topic', title: '주제 선정', images: ['15.jpg', '16.gif', '17.gif', '18.gif'] },
  { id: 'equipment', title: '장비 구성', images: ['19.jpg', '20_low.gif', '21_low.gif'] },
  { id: 'post-production', title: '후반 작업', images: ['22.gif', '23.gif'] },
  { id: 'retouching', title: '보정 서비스', images: ['24.jpg', '25.jpg', '26.gif', '260419_하이어-11.jpg', '260419_하이어-12.jpg', '260419_하이어-13.jpg', '27.gif', '28.gif', '29.gif', '30.gif'] },
  { id: 'pricing', title: '요금제', images: ['31.jpg', '32.gif', '33.gif'] },
  { id: 'portfolio', title: '포트폴리오', images: ['34.gif'] }
])

const activeSection = ref('intro')
const sectionRefs = ref([])
let observer = null

const scrollToSection = (id) => {
  const element = document.getElementById(id)
  if (element) {
    // 네비바 높이 등을 고려한 여백 추가 (약 80px)
    const y = element.getBoundingClientRect().top + window.scrollY - 80
    window.scrollTo({ top: y, behavior: 'smooth' })
  }
}

const goToContact = () => {
  router.push('/contact')
}

onMounted(() => {
  // IntersectionObserver를 이용한 스크롤 감지 로직
  const options = {
    root: null,
    rootMargin: '-20% 0px -60% 0px', // 화면 중앙 쯤 위치할 때 인식하도록 조정
    threshold: 0
  }

  observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        activeSection.value = entry.target.id
      }
    })
  }, options)

  sectionRefs.value.forEach(sec => {
    if (sec) observer.observe(sec)
  })
})

onUnmounted(() => {
  if (observer) {
    observer.disconnect()
  }
})
</script>

<style scoped>
.about-page {
  background-color: #fafafa;
  min-height: 100vh;
  padding-top: 80px; 
  position: relative;
}

/* =========================================
   Floating Navigation
   ========================================= */
.floating-nav {
  position: fixed;
  right: 40px;
  top: 50%;
  transform: translateY(-50%);
  background-color: #ffffff;
  border-radius: 16px;
  padding: 20px 24px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  z-index: 100;
  width: 150px;
}

.floating-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.floating-nav li {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-title {
  font-size: 14px;
  font-weight: 700;
  color: #888;
  transition: color 0.2s ease;
}

.nav-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #ccc;
  transition: background-color 0.2s ease, transform 0.2s ease;
}

/* 활성화(Active) 상태 및 호버 스타일 */
.floating-nav li:hover .nav-title {
  color: #1a3ae0;
}
.floating-nav li:hover .nav-dot {
  background-color: #1a3ae0;
  transform: scale(1.2);
}

.floating-nav li.active .nav-title {
  color: #1a3ae0;
}
.floating-nav li.active .nav-dot {
  background-color: #1a3ae0;
  transform: scale(1.2);
}

/* 구분선 */
.nav-divider {
  height: 1px;
  background-color: #eee;
  margin: 4px 0;
  cursor: default;
}
.nav-divider:hover .nav-title, 
.nav-divider:hover .nav-dot {
  /* 구분선 호버 무시 */
}

/* 문의하기 링크 스타일 (항상 파란색 유지) */
.contact-link .nav-title {
  color: #1a3ae0;
}
.contact-link .nav-dot {
  background-color: #1a3ae0;
}

/* =========================================
   Content / Gallery
   ========================================= */
.content-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-bottom: 100px;
}

.about-section {
  width: 100%;
}

.simple-gallery {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 700px; 
  margin: 0 auto;
  gap: 20px; 
}

.gallery-item {
  width: 100%;
  display: flex;
  justify-content: center;
}

.gallery-item img {
  width: 100%;
  height: auto;
  display: block; 
}

/* 랩탑 이하 작은 화면에서는 사이드바를 약간 작게 하거나, 모바일에선 숨김 처리 가능 */
@media (max-width: 1200px) {
  .floating-nav {
    right: 20px;
    padding: 16px 20px;
  }
}

@media (max-width: 900px) {
  /* 태블릿/모바일에서는 네비게이션 공간이 좁으므로 하단 고정형 혹은 숨김 추천 */
  .floating-nav {
    display: none; 
  }
}
</style>
