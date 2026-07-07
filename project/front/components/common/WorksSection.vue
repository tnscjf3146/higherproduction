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

      <div v-else class="works-grid">
        <div 
          v-for="work in recentWorks" 
          :key="work.id" 
          class="work-card"
        >
          <div class="thumbnail-wrapper" @click="openVideo(work.youtube_link)">
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
          </div>
          <div class="work-info">
            <h3 class="work-title">{{ work.title }}</h3>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRuntimeConfig } from '#app'

const props = defineProps({
  sectionIndex: {
    type: String,
    default: '01'
  }
})

const isLoading = ref(true)
const recentWorks = ref([])

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

const openVideo = (url) => {
  window.open(url, '_blank')
}

onMounted(async () => {
  try {
    const data = await $fetch(useRuntimeConfig().public.apiBaseUrl + '/work/categories/')
    let allWorks = []
    data.forEach(cat => {
      if (cat.works) {
        allWorks = [...allWorks, ...cat.works]
      }
    })
    // 전체 작품 중 최신(또는 앞에서부터) 6개 표시
    recentWorks.value = allWorks.slice(0, 6)
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

.works-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

@media (max-width: 1024px) {
  .works-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .works-section {
    padding: 60px 20px;
  }
  .works-grid {
    grid-template-columns: 1fr;
  }
  .header-title {
    font-size: 14px;
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
  background-color: #222;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 15px;
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
</style>
