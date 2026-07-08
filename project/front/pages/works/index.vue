<template>
  <div class="works-layout">
    <div class="works-header">
      <h1 class="page-title">ALL WORKS</h1>
      <p class="page-desc">{{ totalCategories }} 개 장르 총 {{ totalWorks }}편의 작품</p>
    </div>

    <hr class="header-divider" />

    <!-- 카테고리 필터 버튼 캐러셀 (1차 탭) -->
    <div class="filter-carousel-wrapper main-filters">
      <button 
        v-if="showLeftArrow"
        class="filter-nav-arrow left" 
        @click="scrollFilters(-1)"
      >
        <svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M15.41 16.59L10.83 12l4.58-4.59L14 6l-6 6 6 6 1.41-1.41z"/></svg>
      </button>

      <div class="category-filters" ref="filtersContainer" @scroll="checkScroll">
        <button 
          class="filter-btn" 
          :class="{ active: selectedCategory === 'ALL' }" 
          @click="setCategory('ALL')"
        >
          <span class="filter-name">ALL</span>
        </button>
        <button 
          v-for="cat in categories" 
          :key="cat.id" 
          class="filter-btn"
          :class="{ active: selectedCategory === cat.id }"
          @click="setCategory(cat.id)"
        >
          <span class="filter-name">{{ cat.name }}</span>
          <span v-if="cat.subtitle" class="filter-subtitle">{{ cat.subtitle }}</span>
        </button>
      </div>

      <button 
        v-if="showRightArrow"
        class="filter-nav-arrow right" 
        @click="scrollFilters(1)"
      >
        <svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/></svg>
      </button>
    </div>

    <!-- 2차 탭 (중분류) -->
    <transition name="slide-fade">
      <div v-if="selectedCategory !== 'ALL' && activeSubCategories.length > 0" class="sub-category-filters">
        <button 
          class="sub-filter-btn" 
          :class="{ active: selectedSubCategory === 'ALL' }"
          @click="selectedSubCategory = 'ALL'"
        >
          전체
        </button>
        <button 
          v-for="sub in activeSubCategories" 
          :key="sub.id" 
          class="sub-filter-btn"
          :class="{ active: selectedSubCategory === sub.id }"
          @click="selectedSubCategory = sub.id"
        >
          {{ sub.name }}
        </button>
      </div>
    </transition>

    <div v-if="isLoading" class="loading-state">
      데이터를 불러오는 중입니다...
    </div>

    <div v-else class="categories-container">
      <div 
        v-for="category in filteredCategories" 
        :key="category.id" 
        class="category-section"
      >
        <div class="category-header">
          <div class="category-title-wrapper">
            <span class="category-index">[ {{ category.displayIndex }} ]</span>
            <h2 class="category-title">{{ category.name }}</h2>
            <span v-if="category.subtitle" class="category-subtitle">{{ category.subtitle }}</span>
          </div>
        </div>

        <div v-if="category.works && category.works.length > 0" class="carousel-container">
          <!-- 왼쪽 화살표 -->
          <button 
            class="nav-arrow left-arrow" 
            :disabled="(categoryPages[category.id] || 1) === 1" 
            @click="changePage(category.id, (categoryPages[category.id] || 1) - 1)"
          >
            <svg viewBox="0 0 24 24" class="nav-arrow-icon"><path fill="currentColor" d="M15.41 16.59L10.83 12l4.58-4.59L14 6l-6 6 6 6 1.41-1.41z"/></svg>
          </button>

          <!-- 뷰포트 (실제 그리드 컨테이너) -->
          <div class="carousel-viewport">
            <transition :name="slideDirection" mode="out-in" @after-enter="processInstagram">
                  <div 
                    :key="categoryPages[category.id] || 1"
                    class="works-grid" 
                    :class="{ 
                      'vertical-grid': category.is_vertical && !category.is_instagram,
                      'instagram-grid': category.is_instagram
                    }">
                
                <div 
                  v-for="work in getPaginatedWorks(category)" 
                  :key="work.id" 
                  class="work-card"
                >
                  <div class="thumbnail-wrapper" @click="!work.instagram_embed && openVideo(work.id, work.youtube_link)">
                    <template v-if="work.instagram_embed">
                      <div class="instagram-embed-container" v-html="work.instagram_embed"></div>
                    </template>
                    <template v-else>
                      <iframe v-if="playingWorkId === work.id"
                        :src="`https://www.youtube.com/embed/${getYoutubeVideoId(work.youtube_link)}?autoplay=1`"
                        frameborder="0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowfullscreen
                        class="work-iframe"
                      ></iframe>
                      <template v-else>
                        <img 
                          :src="getYoutubeThumbnail(work.youtube_link)" 
                          :alt="work.title" 
                          class="work-thumbnail"
                        />
                        <div class="play-overlay">
                          <svg class="play-icon" viewBox="0 0 24 24" width="48" height="48">
                            <path fill="currentColor" d="M8 5v14l11-7z"/>
                          </svg>
                        </div>
                      </template>
                    </template>
                  </div>
                  <div class="work-info">
                    <h3 class="work-title">{{ work.title }}</h3>
                  </div>
                </div>
              </div>
            </transition>
          </div>

          <!-- 오른쪽 화살표 -->
          <button 
            class="nav-arrow right-arrow" 
            :disabled="(categoryPages[category.id] || 1) >= getTotalPages(category)" 
            @click="changePage(category.id, (categoryPages[category.id] || 1) + 1)"
          >
            <svg viewBox="0 0 24 24" class="nav-arrow-icon"><path fill="currentColor" d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/></svg>
          </button>
        </div>
        <div v-else class="empty-works">
          등록된 작품이 없습니다.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

const categories = ref([])
const isLoading = ref(true)
const playingWorkId = ref(null)
const selectedCategory = ref('ALL') // 'ALL' 또는 category.id
const selectedSubCategory = ref('ALL')
const categoryPages = ref({}) // 각 카테고리별 현재 페이지 { categoryId: 1 }
const windowWidth = ref(1024)
const slideDirection = ref('slide-right') // 애니메이션 방향 상태

// 필터 스크롤 관련 상태
const filtersContainer = ref(null)
const showLeftArrow = ref(false)
const showRightArrow = ref(false)

const scrollFilters = (direction) => {
  if (filtersContainer.value) {
    const scrollAmount = 300 // 한 번에 이동할 픽셀 수
    filtersContainer.value.scrollBy({ left: direction * scrollAmount, behavior: 'smooth' })
  }
}

const checkScroll = () => {
  if (!filtersContainer.value) return
  const { scrollLeft, scrollWidth, clientWidth } = filtersContainer.value
  showLeftArrow.value = scrollLeft > 0
  // 1px 오차 방지 위해 -1 추가
  showRightArrow.value = Math.ceil(scrollLeft + clientWidth) < scrollWidth - 1
}

const handleResize = () => {
  windowWidth.value = window.innerWidth
  checkScroll()
}

const setCategory = (catId) => {
  selectedCategory.value = catId
  selectedSubCategory.value = 'ALL'
}

// 탭(카테고리 필터) 변경 시 각 페이지 1로 초기화
watch([selectedCategory, selectedSubCategory], () => {
  filteredCategories.value.forEach(cat => {
    categoryPages.value[cat.id] = 1
  })
  setTimeout(() => {
    processInstagram()
  }, 300)
})

const processInstagram = () => {
  if (window.instgrm) {
    window.instgrm.Embeds.process()
  }
}

const totalCategories = computed(() => {
  let count = 0
  categories.value.forEach(main => {
    if (main.sub_categories) count += main.sub_categories.length
  })
  return count
})
const totalWorks = computed(() => {
  let worksCount = 0
  categories.value.forEach(main => {
    if (main.sub_categories) {
      main.sub_categories.forEach(sub => {
        if (sub.works) worksCount += sub.works.length
      })
    }
  })
  return worksCount
})

const activeSubCategories = computed(() => {
  if (selectedCategory.value === 'ALL') return []
  const main = categories.value.find(c => c.id === selectedCategory.value)
  return main && main.sub_categories ? main.sub_categories : []
})

const filteredCategories = computed(() => {
  let result = []
  if (selectedCategory.value === 'ALL') {
    categories.value.forEach(main => {
      let mergedWorks = []
      if (main.sub_categories) {
        main.sub_categories.forEach(sub => {
          if (sub.works) mergedWorks.push(...sub.works)
        })
      }
      mergedWorks.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
      const isVertical = main.sub_categories && main.sub_categories.some(sub => sub.is_vertical)
      const isInstagram = main.sub_categories && main.sub_categories.some(sub => sub.is_instagram)
      
      if (mergedWorks.length > 0 || categories.value.length === 1) {
        result.push({
          id: `main-${main.id}`,
          name: main.name,
          is_vertical: isVertical,
          is_instagram: isInstagram,
          works: mergedWorks
        })
      }
    })
  } else {
    const main = categories.value.find(c => c.id === selectedCategory.value)
    if (main && main.sub_categories) {
      if (selectedSubCategory.value === 'ALL') {
        // 개별 중분류 섹션들만 표시
        main.sub_categories.forEach(sub => {
          if (sub.works && sub.works.length > 0) {
            result.push(sub)
          }
        })
      } else {
        // 특정 중분류 선택 시 해당 중분류만 표시
        const sub = main.sub_categories.find(s => s.id === selectedSubCategory.value)
        if (sub && sub.works && sub.works.length > 0) result.push(sub)
      }
    }
  }
  result.forEach((cat, index) => {
    cat.displayIndex = String(index + 1).padStart(2, '0')
  })
  return result
})

// --- 페이지네이션 로직 ---
const getPageSize = (category) => {
  const isSmallScreen = windowWidth.value <= 768
  const isVertical = category.is_vertical
  const isInstagram = category.is_instagram
  
  if (selectedCategory.value === 'ALL') {
    if (isInstagram) return 3 // 인스타그램은 ALL탭에서 3개(1줄)
    if (isSmallScreen) {
      return isVertical ? 6 : 4 // 모바일: 가로형 4개(2줄), 세로형 6개(2줄)
    }
    return isVertical ? 5 : 6 // PC: 가로형 6개(2줄), 세로형 5개(1줄)
  }
  
  // 개별 카테고리 선택 시
  if (isInstagram) return 9 // 인스타그램은 상세에서 9개(3줄)
  return isSmallScreen ? (isVertical ? 12 : 10) : 15 
}

const getPaginatedWorks = (category) => {
  if (!category.works) return []
  const pageSize = getPageSize(category)
  const currentPage = categoryPages.value[category.id] || 1
  const start = (currentPage - 1) * pageSize
  return category.works.slice(start, start + pageSize)
}

const getTotalPages = (category) => {
  if (!category.works) return 1
  const pageSize = getPageSize(category)
  return Math.ceil(category.works.length / pageSize)
}

const changePage = (categoryId, newPage) => {
  const currentPage = categoryPages.value[categoryId] || 1
  if (newPage > currentPage) {
    slideDirection.value = 'slide-left' // 다음 페이지: 왼쪽으로 밀려남
  } else {
    slideDirection.value = 'slide-right' // 이전 페이지: 오른쪽으로 밀려남
  }
  categoryPages.value[categoryId] = newPage
  // 뷰 트랜지션 @after-enter 훅에서 processInstagram() 이 호출됩니다.
}
// ----------------------

// 유튜브 ID 추출기
const getYoutubeVideoId = (url) => {
  if (!url) return ''
  let videoId = ''
  if (url.includes('youtu.be/')) {
    videoId = url.split('youtu.be/')[1]?.split('?')[0]
  } else if (url.includes('youtube.com/watch')) {
    const urlParams = new URLSearchParams(url.split('?')[1])
    videoId = urlParams.get('v')
  } else if (url.includes('youtube.com/shorts/')) {
    videoId = url.split('youtube.com/shorts/')[1]?.split('?')[0]
  }
  return videoId
}

// 유튜브 링크에서 썸네일 고화질 이미지 URL 추출기
const getYoutubeThumbnail = (url) => {
  const videoId = getYoutubeVideoId(url)
  if (videoId) {
    return `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`
  }
  return '/placeholder-image.jpg'
}

const openVideo = (workId, url) => {
  if (getYoutubeVideoId(url)) {
    playingWorkId.value = workId
  } else if (url) {
    window.open(url, '_blank')
  }
}

onMounted(async () => {
  if (!document.getElementById('instagram-embed-script')) {
    const script = document.createElement('script')
    script.id = 'instagram-embed-script'
    script.src = '//www.instagram.com/embed.js'
    script.async = true
    document.head.appendChild(script)
  }

  windowWidth.value = window.innerWidth
  window.addEventListener('resize', handleResize)

  try {
    const data = await $fetch(useRuntimeConfig().public.apiBaseUrl + '/work/categories/')
    categories.value = data
    filteredCategories.value.forEach(cat => {
      categoryPages.value[cat.id] = 1
    })
    // 렌더링 이후 스크롤 체크 및 인스타그램 임베드 처리
    setTimeout(() => {
      checkScroll()
      if (window.instgrm) window.instgrm.Embeds.process()
    }, 100)
  } catch (error) {
    console.error('Failed to load works:', error)
  } finally {
    isLoading.value = false
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.works-layout {
  max-width: 1600px; /* 좌우 여백 축소를 위해 최대 넓이 확장 */
  margin: 0 auto;
  padding: 80px 40px;
}

.works-header {
  text-align: left;
  margin-bottom: 60px;
  display: flex;
  align-items: baseline;
  gap: 15px;
}

.page-title {
  font-size: 32px;
  font-weight: 800;
  letter-spacing: 2px;
  margin: 0;
}

.page-desc {
  color: #666;
  font-size: 16px;
  margin: 0;
}

.header-divider {
  border: 0;
  height: 1px;
  background-color: #ddd;
  margin-bottom: 30px;
}

.sub-category-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 40px;
  padding-left: 10px;
}

/* 2차 탭 애니메이션 (Slide down + Fade in) */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  transform-origin: top center;
  max-height: 100px;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
  max-height: 0;
  margin-bottom: 0;
  overflow: hidden;
}

.sub-filter-btn {
  background: transparent;
  border: none;
  padding: 8px 18px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: #777;
  transition: all 0.2s ease;
}

.sub-filter-btn:hover {
  color: #111;
  background: rgba(0,0,0,0.05);
}

.sub-filter-btn.active {
  background: #111;
  color: #fff;
  font-weight: 600;
}

/* 필터 버튼 캐러셀 영역 */
.filter-carousel-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  margin-bottom: 50px;
}

.category-filters {
  display: flex;
  flex-wrap: nowrap;
  gap: 10px;
  overflow-x: auto;
  scroll-behavior: smooth;
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
  flex: 1;
}

.category-filters::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

.filter-nav-arrow {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #333;
  z-index: 10;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transition: all 0.2s;
  flex-shrink: 0;
}

.filter-nav-arrow:hover {
  background: #f5f5f5;
  transform: scale(1.05);
}

.filter-nav-arrow.left {
  margin-right: 15px;
}

.filter-nav-arrow.right {
  margin-left: 15px;
}

.filter-btn {
  background: transparent;
  border: 1px solid #ddd;
  padding: 10px 22px;
  border-radius: 30px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  color: #555;
  transition: all 0.2s ease;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 6px;
}

.filter-btn:hover {
  background: #f5f5f5;
}

.filter-btn.active {
  background: #111;
  color: #fff;
  border-color: #111;
}

.filter-subtitle {
  font-size: 13px;
  color: #999;
  font-weight: 500;
}

.filter-btn.active .filter-subtitle {
  color: #ccc;
}

.loading-state {
  text-align: center;
  padding: 100px;
  color: #888;
}

.category-section {
  margin-bottom: 70px;
}

.category-header {
  margin-bottom: 25px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eaeaea;
}

.category-title-wrapper {
  display: flex;
  align-items: baseline;
  gap: 15px;
}

.category-index {
  color: #3b5bdb;
  font-family: monospace;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 1px;
}

.category-title {
  font-size: 22px;
  font-weight: 800;
  margin: 0;
  color: #111;
  letter-spacing: -0.5px;
}

.category-subtitle {
  font-size: 14px;
  color: #666;
  font-weight: 500;
  margin-left: 5px;
}

/* 일반 가로형 그리드 (롱 플랫폼 - 3열) */
.works-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

/* 세로형(쇼츠) 그리드 (숏 플랫폼 - 5열) */
.vertical-grid {
  grid-template-columns: repeat(5, 1fr);
}

@media (max-width: 1024px) {
  .works-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  .vertical-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 768px) {
  .works-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .vertical-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 480px) {
  .works-grid {
    grid-template-columns: 1fr;
  }
  .vertical-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* 인스타그램 그리드 (3열) */
.instagram-grid {
  grid-template-columns: repeat(3, 1fr);
}

.instagram-grid .thumbnail-wrapper {
  padding-top: 0;
  background-color: transparent;
  min-height: 400px;
}

.instagram-embed-container {
  width: 100%;
  display: flex;
  justify-content: center;
}

/* 작품 카드 UI */
.work-card {
  cursor: pointer;
  transition: transform 0.3s ease;
}

.work-card:hover {
  transform: translateY(-5px);
}

.thumbnail-wrapper {
  position: relative;
  width: 100%;
  padding-top: 56.25%; /* 16:9 비율 */
  background-color: #f0f0f0;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 12px;
}

.vertical-grid .thumbnail-wrapper {
  padding-top: 177.77%; /* 9:16 비율 (쇼츠) */
}

.work-thumbnail {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.work-card:hover .work-thumbnail {
  transform: scale(1.05);
}

.work-iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: none;
  z-index: 10;
}

.play-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.work-card:hover .play-overlay {
  opacity: 1;
}

.play-icon {
  color: white;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
  transform: scale(0.8);
  transition: transform 0.3s ease;
}

.work-card:hover .play-icon {
  transform: scale(1);
}

.work-info {
  padding: 0 4px;
}

.work-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: #111;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 캐러셀 레이아웃 및 화살표 UI */
.carousel-container {
  display: flex;
  align-items: center;
  position: relative;
  width: 100%;
}

.carousel-viewport {
  flex: 1;
  overflow: hidden;
  position: relative;
  padding: 10px 0;
}

.nav-arrow {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 10px;
  color: #999;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.nav-arrow:hover:not(:disabled) {
  color: #111;
  transform: scale(1.1);
}

.nav-arrow:disabled {
  opacity: 0.2;
  pointer-events: none;
}

.nav-arrow-icon {
  width: clamp(32px, 4vw, 64px);
  height: clamp(32px, 4vw, 64px);
  transition: all 0.3s ease;
}

/* 스크롤바 미세조정 */
.left-arrow {
  margin-right: 15px;
}

.right-arrow {
  margin-left: 15px;
}

@media (max-width: 768px) {
  .left-arrow { margin-right: 5px; }
  .right-arrow { margin-left: 5px; }
}

/* 슬라이딩 모션 트랜지션 (out-in) */
.slide-left-enter-active,
.slide-left-leave-active,
.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.35s cubic-bezier(0.25, 1, 0.5, 1);
}

/* 다음 버튼 누를 때 (오른쪽에서 나타남) */
.slide-left-enter-from {
  opacity: 0;
  transform: translateX(40px);
}
.slide-left-leave-to {
  opacity: 0;
  transform: translateX(-40px);
}

/* 이전 버튼 누를 때 (왼쪽에서 나타남) */
.slide-right-enter-from {
  opacity: 0;
  transform: translateX(-40px);
}
.slide-right-leave-to {
  opacity: 0;
  transform: translateX(40px);
}

.empty-works {
  color: #888;
  font-size: 14px;
  padding: 20px 0;
}
</style>
