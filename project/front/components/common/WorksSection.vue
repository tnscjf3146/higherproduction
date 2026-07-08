<template>
  <section class="works-section">
    <div class="works-container">
      <div class="section-header">
        <div class="header-left">
          <span class="header-bracket">[ {{ sectionIndex }} / works ]</span>
          <h2 class="header-title">OUR WORKS</h2>
        </div>
        <div class="header-right">
          <NuxtLink to="/works" class="view-all-btn">VIEW ALL WORKS →</NuxtLink>
        </div>
      </div>

      <div v-if="isLoading" class="loading-state">
        데이터를 불러오는 중입니다...
      </div>

      <div v-else>
        <!-- 카테고리 필터 영역 (1차 탭) -->
        <div class="category-filters main-filters">
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
          </button>
        </div>

        <!-- 서브 카테고리 필터 영역 (2차 탭) -->
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

        <div class="categories-container">
          <div 
            v-for="category in filteredCategories" 
            :key="category.id" 
            class="category-section"
          >
            <div class="category-header">
              <span class="category-index">[ {{ category.displayIndex }} ]</span>
              <h3 class="category-title">{{ category.name }}</h3>
              <span v-if="category.subtitle" class="category-subtitle">{{ category.subtitle }}</span>
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

              <!-- 뷰포트 -->
              <div class="carousel-viewport">
                <transition :name="slideDirection" mode="out-in">
                  <div 
                    :key="categoryPages[category.id] || 1"
                    class="works-grid" 
                    :class="{ 
                      'vertical-grid': category.is_vertical && !category.is_instagram,
                      'instagram-grid': category.is_instagram
                    }"
                  >
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
            
            <div v-if="!category.works || category.works.length === 0" class="empty-works">
              해당 카테고리에 등록된 작품이 없습니다.
            </div>
          </div>
        </div>
      </div>
    </div>

  </section>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRuntimeConfig } from '#app'

const props = defineProps({
  sectionIndex: {
    type: String,
    default: '01'
  }
})

const isLoading = ref(true)
const categories = ref([])
const selectedCategory = ref('ALL')
const selectedSubCategory = ref('ALL')
const playingWorkId = ref(null)

const categoryPages = ref({})
const slideDirection = ref('slide-right')

const setCategory = (catId) => {
  selectedCategory.value = catId
  selectedSubCategory.value = 'ALL'
}

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

watch([selectedCategory, selectedSubCategory], () => {
  filteredCategories.value.forEach(cat => {
    categoryPages.value[cat.id] = 1
  })
  setTimeout(() => {
    if (window.instgrm) window.instgrm.Embeds.process()
  }, 300)
})

const getPageSize = (isVertical) => {
  if (selectedCategory.value === 'ALL') {
    return isVertical ? 5 : 3
  }
  return isVertical ? 10 : 6
}

const getPaginatedWorks = (category) => {
  if (!category.works) return []
  const pageSize = getPageSize(category.is_vertical)
  const currentPage = categoryPages.value[category.id] || 1
  const start = (currentPage - 1) * pageSize
  return category.works.slice(start, start + pageSize)
}

const getTotalPages = (category) => {
  if (!category.works) return 1
  const pageSize = getPageSize(category.is_vertical)
  return Math.ceil(category.works.length / pageSize)
}

const changePage = (categoryId, newPage) => {
  const currentPage = categoryPages.value[categoryId] || 1
  if (newPage > currentPage) {
    slideDirection.value = 'slide-left'
  } else {
    slideDirection.value = 'slide-right'
  }
  categoryPages.value[categoryId] = newPage
  setTimeout(() => {
    if (window.instgrm) window.instgrm.Embeds.process()
  }, 300)
}

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

  try {
    const data = await $fetch(useRuntimeConfig().public.apiBaseUrl + '/work/categories/')
    categories.value = data
    filteredCategories.value.forEach(cat => {
      categoryPages.value[cat.id] = 1
    })
    setTimeout(() => {
      if (window.instgrm) window.instgrm.Embeds.process()
    }, 500)
  } catch (error) {
    console.error('Failed to load works:', error)
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
.works-section {
  position: relative;
  z-index: 10;
  width: 100%;
  background-color: #fafafa; /* 흰색 배경 */
  color: #111111; /* 배경이 흰색이므로 기본 텍스트를 어둡게 설정 */
  padding: 60px 40px 40px;
}

.works-container {
  max-width: 1400px;
  margin: 0 auto;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 50px;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.15);
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
  color: var(--text-mute);
  letter-spacing: 1px;
}

.header-title {
  font-size: clamp(14px, 2.5vw + 8px, 24px);
  font-weight: 800;
  color: #111;
  margin: 0;
  letter-spacing: 0.5px;
}

.view-all-btn {
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  color: #111111; /* 버튼 글자색 어둡게 */
  border: 1px solid rgba(0, 0, 0, 0.3); /* 버튼 테두리 어둡게 */
  padding: 10px 20px;
  border-radius: 30px;
  transition: all 0.3s ease;
}

.view-all-btn:hover {
  background: #111111;
  color: #ffffff; /* 호버 시 반전 */
}

/* 카테고리 필터 CSS */
.category-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.sub-category-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 30px;
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
  padding: 6px 15px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 13px;
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

.filter-btn {
  background: transparent;
  border: 1px solid #ddd;
  padding: 8px 20px;
  border-radius: 30px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  color: #555;
  transition: all 0.2s ease;
}

.filter-btn:hover {
  background: #f5f5f5;
}

.filter-btn.active {
  background: #111;
  color: #fff;
  border-color: #111;
}

.categories-container {
  display: flex;
  flex-direction: column;
  gap: 60px;
}

.category-section {
  display: flex;
  flex-direction: column;
}

.category-header {
  margin-bottom: 25px;
  display: flex;
  align-items: baseline;
  gap: 12px;
  border-bottom: 1px solid #eaeaea;
  padding-bottom: 12px;
}

.category-title {
  font-size: 22px;
  font-weight: 800;
  margin: 0;
  color: #111;
  letter-spacing: -0.5px;
}

.category-index {
  color: var(--text-mute);
  font-family: monospace;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 1px;
}

.category-subtitle {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.works-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

/* 세로형(쇼츠) 그리드 (숏 플랫폼 - 5열) */
.vertical-grid {
  grid-template-columns: repeat(5, 1fr);
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

@media (max-width: 768px) {
  .works-section {
    padding: 60px 20px;
  }
  .works-grid {
    gap: 10px; /* 모바일에서는 간격을 줄여서 한 줄에 다 들어가게 함 */
  }
  .categories-container {
    gap: 30px;
  }
  .header-title {
    font-size: 16px;
  }
  .header-bracket {
    font-size: 10px;
  }
  .category-title {
    font-size: 18px;
  }
  .category-index {
    font-size: 12px;
  }
  .work-title {
    font-size: 11px;
    font-weight: 600;
    line-height: 1.3;
  }
}

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
  padding-top: 56.25%;
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

.play-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
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
  transform: scale(0.8);
  transition: transform 0.3s ease;
}

.work-card:hover .play-icon {
  transform: scale(1);
}

.work-info {
  padding: 0 5px;
}

.work-title {
  font-size: 18px;
  font-weight: 700;
  margin: 0;
  color: #111111; /* 작품 제목 어둡게 */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.loading-state {
  text-align: center;
  padding: 50px;
  color: #888;
}

.empty-works {
  grid-column: 1 / -1;
  text-align: center;
  padding: 40px 0;
  color: #888;
  font-size: 14px;
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

.left-arrow {
  margin-right: 15px;
}

.right-arrow {
  margin-left: 15px;
}

/* 슬라이딩 모션 트랜지션 (out-in) */
.slide-left-enter-active,
.slide-left-leave-active,
.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.35s cubic-bezier(0.25, 1, 0.5, 1);
}

.slide-left-enter-from {
  opacity: 0;
  transform: translateX(40px);
}
.slide-left-leave-to {
  opacity: 0;
  transform: translateX(-40px);
}

.slide-right-enter-from {
  opacity: 0;
  transform: translateX(-40px);
}
.slide-right-leave-to {
  opacity: 0;
  transform: translateX(40px);
}

@media (max-width: 768px) {
  .close-btn {
    top: -35px;
    right: 0px;
    font-size: 32px;
  }
  .left-arrow { margin-right: 5px; }
  .right-arrow { margin-left: 5px; }
}
</style>
