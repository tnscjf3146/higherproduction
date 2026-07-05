<template>
  <div>
    <!-- 📱 모바일 메뉴 배경 (어둡게 깔리는 배경, 누르면 닫힘) -->
    <div class="menu-backdrop" :class="{ 'is-open': isMenuOpen }" @click="toggleMenu"></div>

    <!-- 📱 모바일 오른쪽 사이드바 메뉴 -->
    <div class="mobile-side-menu" :class="{ 'is-open': isMenuOpen }">
      <div class="mobile-menu-content">
        <!-- 🚀 v-for 반복문을 통해 데이터를 뿌려줍니다! -->
        <NuxtLink 
          v-for="(item, index) in menuItems" 
          :key="item.name" 
          :to="item.path" 
          @click="toggleMenu"
          :style="{ transitionDelay: `${0.1 + (index * 0.05)}s` }"
        >
          {{ item.name }}
        </NuxtLink>
      </div>
      
      <!-- 📱 사이드 메뉴 하단의 로그인/회원가입 영역 -->
      <div class="mobile-menu-footer">
        <template v-for="(item, index) in authItems" :key="item.name">
          <!-- 첫 번째 항목이 아닐 때만 구분선(|) 넣기 -->
          <span v-if="index > 0" class="divider"></span>
          <NuxtLink 
            :to="item.path !== '#logout' ? item.path : ''" 
            @click="handleAuthClick($event, item.path, true)"
          >
            {{ item.name }}
          </NuxtLink>
        </template>
      </div>
    </div>

    <!-- 상단 공통 네비게이션 자리 -->
    <div class="nav">
      <div class="nav-left">
        <NuxtLink to="/">
          <img src="/nav_logo_en.png" alt="logo" class="nav-logo-img">
        </NuxtLink>
      </div>
      
      <div class="nav-center">
        <!-- 🚀 모바일과 동일한 menuItems 배열 데이터를 재사용! -->
        <NuxtLink 
          v-for="item in menuItems" 
          :key="item.name" 
          :to="item.path"
        >
          <span>{{ item.name }}</span>
        </NuxtLink>
      </div>
      
      <div class="nav-right">
        <!-- 💻 PC용 우측 사용자 메뉴 (로그인/프로필) -->
        <div class="auth-links desktop-only">
          <template v-for="(item, index) in authItems" :key="item.name">
            <span v-if="index > 0" class="divider"></span>
            <NuxtLink 
              :to="item.path !== '#logout' ? item.path : ''" 
              @click="handleAuthClick($event, item.path, false)"
            >
              {{ item.name }}
            </NuxtLink>
          </template>
        </div>
        
        <button 
          class="hamburger mobile-only" 
          :class="{ 'is-active': isMenuOpen }"
          @click="toggleMenu"
        >
          <span class="line"></span>
          <span class="line"></span>
          <span class="line"></span>
        </button>
      </div>
    </div>

    <slot />

    <!-- 하단 공통 푸터 -->
    <Footer />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '~/stores/auth'
import Footer from '~/components/common/Footer.vue'

const authStore = useAuthStore()
const router = useRouter()
const isMenuOpen = ref(false)

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

// 스토어의 유저 정보 유무로 로그인 상태 자동 계산
const isLoggedIn = computed(() => !!authStore.user) 
// 백엔드에서 전달받은 is_admin 값을 바탕으로 관리자 권한 연동
const isAdmin = computed(() => authStore.user?.is_admin || false)    

// 🚀 인증(Auth) 관련 메뉴 (로그인/로그아웃/프로필) 배열 관리
const authItems = computed(() => {
  if (isLoggedIn.value) {
    return [
      { name: 'PROFILE', path: '/profile' },
      { name: 'LOGOUT', path: '#logout' } 
    ]
  }
  return [
    { name: 'LOGIN', path: '/account/login' },
    { name: 'SIGN UP', path: '/account/signup' }
  ]
})

// 인증 메뉴 클릭 핸들러
const handleAuthClick = (event, path, isMobile) => {
  if (path === '#logout') {
    event.preventDefault() // 기본 링크 이동 막기
    authStore.logout()     // Pinia Auth Store 로그아웃 실행
    alert('로그아웃 되었습니다.')
    router.push('/account/login') // 로그아웃 후 로그인 페이지로 리다이렉트
  }
  if (isMobile) {
    toggleMenu() // 모바일 메뉴면 클릭 시 닫기
  }
}

// 1. 일반 접속자 누구나 볼 수 있는 공용 메뉴
const publicMenuItems = [
  { name: 'WORKS', path: '/works' },
  { name: 'SERVICES', path: '/services' },
  { name: 'ABOUT', path: '/about' },
  { name: 'CONTACT', path: '/contact' }
]

// 2. 관리자 전용 메뉴
const adminMenuItems = [
  { name: 'EDIT', path: '/edit' }
]

// 3. 화면에 최종적으로 뿌려질 메뉴 리스트 (자동 계산)
const menuItems = computed(() => {
  if (isAdmin.value) {
    return [...publicMenuItems, ...adminMenuItems] // 관리자면 둘 다 합쳐서 보여줌
  }
  return publicMenuItems // 일반 유저면 공용 메뉴만 보여줌
})
</script>

<style scoped>
.nav {
    position: sticky;
    top: 0;
    z-index: 100;
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    /* 🚀 화면이 좁아지면 사이 공간도 16px까지 쫙 좁아지며 버티도록 clamp 적용 */
    column-gap: clamp(16px, 3vw, 80px); 
    padding: 16px var(--gutter);
    /* 투명도 40% 배경 + 뒤에 비치는 내용이 블러 처리되는 고급 유리창 효과 */
    background-color: rgba(255, 255, 255, 0.4);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    /* 딱딱한 선 대신 그림자로 아주 얇고 부드럽게 표현한 하단 구분선 */
    box-shadow: 0 1px 0 rgba(0, 0, 0, 0.04), 0 4px 16px rgba(0, 0, 0, 0.02);
}

.nav-logo-img{
  height: clamp(48px, 4vw, 64px);
  width: auto; 
  display: block;
  cursor: pointer; 
  transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1), filter 0.4s ease;
}

.nav-logo-img:hover {
  transform: scale(1.05) translateY(-2px);
  filter: drop-shadow(0 10px 20px rgba(255, 255, 255, 0.2)); 
}

.nav-center {
  display: flex;
  align-items: center;
  justify-content: center;
  /* 간격 하한선을 12px까지 낮춰서 최대한 오랫동안 버티게 함 */
  gap: clamp(12px, 2vw, 48px); 
}

.nav-center a {
  position: relative;
  font-family: var(--font-mono); 
  /* 폰트 하한선을 13px까지 낮춰서 좁은 창에서도 글씨가 작아지며 살아남게 함 */
  font-size: clamp(20px, 1.5vw, 32px);
  font-weight: 500;
  letter-spacing: 0.1em;
  color: var(--text-mute); 
  text-decoration: none;
  padding: 8px 0;
  cursor: pointer; 
  transition: color 0.3s ease;
}

.nav-center a:hover {
  color: var(--primary-color);
}

.nav-center a::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0%; 
  height: 2px;
  background-color: var(--primary-color);
  transition: width 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.nav-center a:hover::after {
  width: 100%; 
}

/* 오른쪽 네비게이션 정렬 */
.nav-right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

/* PC용 로그인/회원가입 텍스트 스타일 */
.auth-links {
  display: flex;
  align-items: center;
  gap: 12px;
}
.auth-links a {
  font-family: var(--font-mono);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.1em;
  color: var(--text-ink);
  text-decoration: none;
  cursor: pointer;
  transition: color 0.3s ease;
  white-space: nowrap; /* 글씨가 공간이 부족하다고 밑으로 떨어지는(줄바꿈) 현상 완벽 방지 */
}
.auth-links a:hover {
  color: var(--primary-color);
}
.auth-links .divider {
  width: 1px;
  height: 12px;
  background-color: var(--text-line-strong);
}


/* --- 🍔 모바일 햄버거 버튼 디자인 --- */
.mobile-only { display: none !important; }

.hamburger {
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 6px; 
  padding: 8px;
  z-index: 9999; 
  position: relative;
}
.hamburger .line {
  width: 28px;
  height: 2px;
  background-color: var(--text-ink); 
  transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1), opacity 0.3s;
  transform-origin: left center;
}

.hamburger.is-active .line:nth-child(1) { transform: translateY(8px) rotate(45deg); }
.hamburger.is-active .line:nth-child(2) { opacity: 0; }
.hamburger.is-active .line:nth-child(3) { transform: translateY(-8px) rotate(-45deg); }


/* --- 📱 오른쪽 사이드바 메뉴 (Side Drawer) --- */
.menu-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 8000;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.4s ease;
}
.menu-backdrop.is-open {
  opacity: 1;
  pointer-events: auto;
}

.mobile-side-menu {
  position: fixed;
  top: 0;
  right: 0; 
  bottom: 0;
  width: 360px; 
  max-width: 100vw;
  background-color: var(--primary-paper-color);
  z-index: 9000;
  display: flex;
  flex-direction: column;
  padding: 120px 40px 60px; 
  box-shadow: -10px 0 30px rgba(0,0,0,0.1); 
  
  transform: translateX(100%);
  transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.mobile-side-menu.is-open {
  transform: translateX(0);
}

/* 모바일 메뉴 리스트 */
.mobile-menu-content {
  display: flex;
  flex-direction: column;
  text-align: center;
  width: 100%;
}
.mobile-menu-content a {
  font-family: var(--font-display);
  font-size: 32px;
  font-weight: 800;
  color: var(--text-ink);
  text-decoration: none;
  letter-spacing: 0.05em;
  cursor: pointer;
  
  opacity: 0;
  transform: translateY(20px);
}
.mobile-menu-content a:hover {
  color: var(--primary-color);
}

.mobile-menu-content a::after {
  content: "";
  display: block;
  width: 24px;
  height: 2px;
  background-color: var(--text-line);
  margin: 24px auto; 
}
.mobile-menu-content a:last-child::after {
  display: none; 
}

/* 모바일 사이드바 하단 (로그인, 회원가입) */
.mobile-menu-footer {
  margin-top: auto; 
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  
  opacity: 0;
  transform: translateY(20px);
}
.mobile-menu-footer a {
  font-family: var(--font-mono);
  font-size: 14px;
  font-weight: 600;
  color: var(--text-mute);
  text-decoration: none;
  cursor: pointer;
  letter-spacing: 0.05em;
  transition: color 0.3s;
}
.mobile-menu-footer a:hover {
  color: var(--primary-color);
}
.mobile-menu-footer .divider {
  width: 1px;
  height: 12px;
  background-color: var(--text-line-strong);
}

/* 🎨 폭포수 애니메이션 */
.mobile-side-menu.is-open .mobile-menu-content a,
.mobile-side-menu.is-open .mobile-menu-footer {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 0.5s ease, transform 0.5s cubic-bezier(0.2, 0.8, 0.2, 1), color 0.3s ease;
}

/* 푸터(로그인) 애니메이션 딜레이 (메뉴 개수에 상관없이 메뉴 다음으로 나오도록 여유 부여) */
.mobile-side-menu .mobile-menu-footer { transition-delay: 0.4s; }


/* 📱 임계점 도달 (1024px 이하: 최대한 버티다가 태블릿 사이즈가 되면 햄버거로 체인지!) */
@media (max-width: 1024px) {
  .nav {
    grid-template-columns: 1fr auto; 
  }
  .nav-center { display: none !important; }
  .desktop-only { display: none !important; } 
  .mobile-only { display: flex !important; } 
}
</style>