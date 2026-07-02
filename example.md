# 혼자소누리

## 프로젝트 소개
코딩 없이 누구나 손쉽게 프리미엄 템플릿으로 나만의 온라인 쇼핑몰을 만들 수 있는 플랫폼입니다. 
다양한 쇼핑몰 커스텀 기능, 체계적인 관리자 백오피스, 멀티 테넌트 아키텍처, 그리고 **강력한 유튜브(YouTube) 연동 기능 및 AI 이미지 배경 합성 스튜디오**를 자랑합니다!

---

## 핵심 기능 (Key Features)

### 1. AI 스튜디오 (AI Image Studio)
- **자동 누끼 및 배경 합성**: 사용자가 업로드한 상품 이미지의 배경을 AI(Segment Anything)가 자동으로 제거하고, 프롬프트를 입력하면 원하는 컨셉의 배경 이미지를 Stable Diffusion으로 새롭게 그려 합성해 줍니다.
- **프롬프트 고도화 (Prompt Engineering)**: 한글로 대충 입력해도 백엔드의 GMS(OpenAI Proxy) 서버가 개입하여 전문 사진 촬영(Studio lighting, photorealistic 등) 스타일의 고품질 영문 프롬프트로 자동 고도화합니다.
- **AI 보관함 연동**: 생성된 5장의 결과물 중 마음에 드는 이미지를 저장하면 쇼핑몰별 `AIStudioImage` 보관함에 들어가, 상품 등록 시 설명란에 바로 첨부하거나 썸네일 이미지로 손쉽게 사용할 수 있습니다.

### 2. 강력한 유튜브 연동 기능 (Highlight!)
- **실시간 유튜브 검색 및 인라인 재생**: 유튜브 API를 통해 플랫폼 내에서 직접 원하는 영상을 검색하고 상세 페이지에서 iframe으로 즉시 재생할 수 있습니다.
- **영상 및 채널 저장 (Watch Later)**: 마음에 드는 유튜브 영상과 채널을 로컬 스토리지에 저장하여 언제든 `저장된 영상`, `저장된 채널` 전용 관리 페이지에서 모아볼 수 있습니다.
- **채널별 자동 최신 영상 모아보기**: 저장된 채널 리스트에서 채널명을 클릭하면, 즉시 검색 페이지로 이동하며 **해당 채널의 최신 영상들만** 자동으로 검색 및 정렬되어 나타납니다!
- **공지사항 유튜브 연동 모달**: 관리자가 전체 공지사항을 작성할 때, 자신이 **저장해둔 유튜브 영상 목록**을 모달 창으로 불러와 클릭 한 번으로 손쉽게 첨부할 수 있습니다.

### 3. 체계적인 관리자 전용 백오피스 (Admin Dashboard)
- **전체 공지사항 관리**: 상태별(발행됨, 비공개, 임시저장) 세분화 뱃지 및 드롭다운 필터, 최신 작성순/오래된 순 정렬, 즉시 키워드 검색 기능 제공.
- **전체 회원 권한 관리**: 유저명 및 이메일 기반 회원 검색 및 관리자 권한 즉각 부여/해제 기능.

### 4. 강력한 보안 및 전역 인증 관리
- **전역 Axios Interceptor**: 토큰 상태 불일치(401 Unauthorized) 발생 시 전역에서 감지하고 **자동으로 세션을 초기화 후 강제 로그아웃 처리**합니다.
- **완벽한 백엔드 세션 종료**: 로그아웃 시 장고 API 호출을 통해 JWT Refresh 토큰까지 완벽하게 블랙리스트 처리합니다.

### 5. 몰 커스텀 및 다차원 카테고리
- **디자인 테마 및 템플릿**: 레이아웃 구조 및 색상 테마 설정, 커스텀 로고/배너 업로드 지원.
- **다차원 카테고리 (Recursive)**: 부모-자식 관계를 가지는 N차원 카테고리 구성 가능.
- **카테고리별 필수 고시 정보 (CategoryRequirement)**: 각 카테고리마다 동적으로 필수 입력 필드를 정의하여 상품 등록 시 유효성 검증.

### 6. 장바구니 및 실시간 결제 통계 (Cart & Order Analytics)
- **프론트엔드 장바구니 (Pinia + LocalStorage)**: 상태 관리와 로컬 스토리지로 가볍게 유지하여 새로고침해도 보존되는 반응성 높은 장바구니 드로어 UI.
- **실제 DB 기반 결제 및 통계**: 프론트엔드 결제 완료 시 백엔드 DB에 주문(Order) 생성. 관리자 대시보드의 일/주/월 매출 및 판매량이 실시간으로 집계되어 시각화됩니다.

---

## AI 작동 아키텍처 및 원리 (AI Operation Architecture)

사용자가 단순히 상품 사진과 한국어 아이디어를 입력하면, 백엔드와 별도의 AI 특화 서버가 유기적으로 연동되어 최상급 퀄리티의 이미지를 생성해냅니다.

**[작동 흐름 및 원리]**
1. **Frontend (Vue)**
   - 사용자가 상품 이미지와 생성하고 싶은 배경 아이디어(예: "사막 한가운데")를 입력하여 Django API로 전송합니다.
2. **Backend (Django & GMS Proxy)**
   - Django 서버는 SSAFY GMS API (OpenAI GPT-5.5)로 프롬프트를 전송합니다. 
   - 이때 시스템 프롬프트(System Prompt)가 강력하게 개입하여, 사용자의 단순한 한글 입력을 `a futuristic city, cyberpunk style, neon lights, 8k resolution, photorealistic, masterpiece...` 와 같은 **SD 특화 고품질 영문 프롬프트**로 번역 및 확장(고도화)합니다.
3. **AI Server (FastAPI + GPU Container)**
   - **SAM (Segment Anything Model)**: 이미지 내의 상품(객체)을 분리(누끼)하기 위해 이미지 중앙부에 9개의 전경(Foreground) 점과 외곽 4개의 배경(Background) 힌트 점을 동적으로 찍어 마스크(Mask)를 완벽히 생성합니다.
   - **SD 1.5 Inpainting (Stable Diffusion)**: 원본 고해상도 이미지가 SD 1.5 모델의 한계로 깨지는 것을 막기 위해, 이미지와 마스크를 **512x512** 해상도로 최적화하여 렌더링합니다. (문자나 한자, 조잡한 패턴이 나오지 않도록 강력한 네거티브 프롬프트가 이 과정에서 주입됩니다.)
   - **Image Compositing**: AI가 그려낸 512x512의 배경 결과를 다시 원본 크기로 정교하게 늘린 후(Lanczos Resampling), SAM이 분리해둔 '원본 고화질 상품 이미지'를 최상단에 투명도(Alpha)를 사용해 깔끔하게 덮어씌웁니다(Composite).
4. **결과 반환**
   - 최종 합성된 5장의 결과물을 Base64 형태로 프론트엔드에 즉각 반환하여 화면에 보여줍니다.

---

## 데이터 테이블 구조 (최신화 적용)

### 1. accounts (회원 관리)
| Model | Fields | Description |
| :--- | :--- | :--- |
| **User** | username, password, email, first_name, last_name, bio, profile_image, is_active, is_staff, is_superuser, date_joined, last_login | 통합 회원 및 관리자 테이블 |

<br>

### 2. malls (쇼핑몰 통합 관리)
| Model | Fields | Description |
| :--- | :--- | :--- |
| **Mall** | is_domain, domain_name, domain_url, mall_call, mall_address, address_detail, latitude, longitude, mall_email, subscribe, template_type, theme_type, design_data, logo_image, main_banner, created_at | 생성된 개별 쇼핑몰 정보 보관 |
| **MallBanner** | mall, image, order, created_at | 쇼핑몰에 추가되는 다중 메인 배너 이미지 슬라이드 |
| **Staff** | user, mall, role, memo | 개별 쇼핑몰에 종속된 스태프 및 권한 관리 (1:N) |
| **Notice** | title, content, youtube_url, video_file, is_draft, is_public, created_at, updated_at | 서비스 전체 공지사항 |
| **Subscription** | user, mall, created_at | 일반 회원의 쇼핑몰 구독 정보 내역 |
| **MallDailyView** | mall, date, views | 특정 쇼핑몰의 일별 누적 조회수(방문자 수) 통계용 |
| **NoticeComment** | notice, author, content, parent, created_at, updated_at | 공지사항에 달리는 댓글 및 대댓글(Self 참조) |
| **MallLike** | user, mall, created_at | 회원의 쇼핑몰 '좋아요' 내역 |

<br>

### 3. categories (카테고리 시스템)
| Model | Fields | Description |
| :--- | :--- | :--- |
| **Category** | name, parent, category_notice | 부모-자식 계층 구조를 가지는 N차원 다중 카테고리 |
| **CategoryRequirement** | category, field_name, field_type, is_required | 특정 카테고리의 상품 등록 시 요구되는 필수 고시 정보(동적 폼) 정의 |

<br>

### 4. products (상품 및 주문 관리)
| Model | Fields | Description |
| :--- | :--- | :--- |
| **Product** | mall, category, title, content, price, delivery, requirement_values, created_at, updated_at | 판매할 상품의 본체 정보 (JSONField로 동적 고시정보 보관) |
| **DetailImage** | product, image | 특정 상품 종속 다중 상세/썸네일 이미지 |
| **Order** | mall, total_price, created_at | 실제 결제 및 장바구니 구매 발생 시 생성되는 주문서 내역 |
| **OrderItem** | order, product, quantity, price | 해당 주문서(Order) 안에 담긴 실제 개별 구매 상품 목록 |
| **ProductDailyView** | product, date, views | 특정 상품의 일별 상세 페이지 조회수 통계 데이터 |
| **AIStudioImage** | mall, image, created_at | AI 스튜디오에서 배경 합성 후 저장된 결과물 보관함 |
| **DescriptionImage** | mall, image, created_at | 상품 상세 설명 텍스트 에디터 내부 삽입용 이미지 전용 버킷 |

<br>

### 5. community (판매자/유저 커뮤니티)
| Model | Fields | Description |
| :--- | :--- | :--- |
| **SellerPost** | author, title, content, is_notice, youtube_video_id, external_url, attached_file, like_users, wish_users, created_at, updated_at | 커뮤니티 피드 / 게시글 테이블 |
| **SellerComment** | post, author, content, parent, like_users, created_at, updated_at | 커뮤니티 게시글 댓글 및 대댓글 |

<br>

### 6. support (고객 지원 센터)
| Model | Fields | Description |
| :--- | :--- | :--- |
| **SupportTicket** | author, title, content, is_resolved, created_at, updated_at | 유저가 남긴 1:1 고객 문의(Ticket) 내역 |
| **SupportComment** | ticket, author, content, parent, created_at, updated_at | 문의 내역에 대한 관리자/유저의 피드백 댓글 |

<br>

### 7. 유튜브 연동 데이터 (LocalStorage)
> 백엔드 부하 감소 및 쾌적한 속도를 위해 Client-Side(Pinia) 기반 로컬 스토리지에 유지되는 상태 데이터입니다.

| Name | Key/Type | Description |
| :--- | :--- | :--- |
| **savedYoutubeVideos** | videoId (Key) | 유튜브 비디오 고유 ID, 영상 제목, 채널명, 썸네일 이미지 저장 목록 |
| **savedYoutubeChannels** | channelId (Key) | 유튜브 채널 고유 ID, 채널명 저장 목록 (클릭 시 전용 채널 최신 영상 렌더링) |

<br>
<br>

---

## 프로젝트 구조 (Project Directory Tree)

```text
project/
  ├─ back/                                    // Django 백엔드
  │    ├─ config/                             // 설정 파일 및 최상위 urls
  │    ├─ accounts/                           // 회원 관리 및 인증 (JWT, dj-rest-auth)
  │    ├─ malls/                              // 쇼핑몰 생성, 관리, 스태프, 공지사항 API
  │    ├─ products/                           // 상품 CRUD 및 동적 이미지 관리, 주문서 결제
  │    ├─ categories/                         // 계층형 카테고리 및 고시 정보 로직
  │    ├─ community/                          // 사용자 커뮤니티 기능 로직
  │    ├─ support/                            // 1:1 문의 등 지원 기능 로직
  │    ├─ media/                              // 동적 업로드 정적 파일 (로고, 배너, 상품 등)
  │    └─ requirements.txt                    // 파이썬 의존성
  │
  ├─ front/                                   // Vue 3 프론트엔드 (Composition API)
  │    ├─ src/
  │    │   ├─ assets/                         // 글로벌 CSS (main.css)
  │    │   ├─ components/                     // 재사용 가능한 UI 컴포넌트
  │    │   ├─ router/                         // Vue-Router 라우팅 설정
  │    │   ├─ stores/                         // Pinia 상태 관리 (accounts, malls, youtube, categories, products)
  │    │   └─ views/
  │    │       ├─ accounts/                   // 로그인, 회원가입 뷰
  │    │       ├─ shops/                      // 쇼핑몰 렌더링, 공지사항 관리, 회원 권한 관리 등 백오피스 뷰
  │    │       ├─ youtube/                    // 유튜브 검색, 영상 상세, 저장된 영상/채널 뷰
  │    │       └─ pages/                      // 메인 홈 화면 뷰
  │    ├─ package.json                        // npm 의존성
  │    └─ vite.config.js                      // Vite 설정
  │
  └─ assets/
       └─ ai/                                 // 🌟 별도 GPU AI 연산 컨테이너 서버 (FastAPI)
            ├─ server.py                      // AI 인페인팅 및 합성 처리를 담당하는 메인 API
            ├─ pipeline.py                    // Segment Anything & Stable Diffusion 처리 파이프라인
            ├─ Dockerfile & docker-compose    // CUDA 지원 격리된 GPU 컨테이너 환경
            └─ weights/                       // AI 기반 모델 가중치 데이터베이스
```

---

## 실행 방법

### Django 백엔드 서버 구동
```bash
cd back
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Vue 프론트엔드 서버 구동
```bash
cd front
npm install
npm run dev
```

### AI 전용 GPU 컨테이너 서버 구동 (선택)
```bash
cd assets/ai
docker-compose up --build -d
```
> 초기 빌드 시 PyTorch CUDA 컨테이너 다운로드로 인해 시간이 소요됩니다.

---

## 주요 사용 라이브러리 (Stack)
- **Frontend**: Vue 3, Vue-Router, Pinia, Axios, pinia-plugin-persistedstate
- **Backend**: Django, Django REST Framework (DRF), dj-rest-auth, djangorestframework-simplejwt, django-cors-headers, Pillow
- **AI Server**: FastAPI, PyTorch(CUDA), diffusers(Stable Diffusion), Segment Anything, OpenCV
- **External API**: YouTube Data API v3, OpenAI API (SSAFY GMS Proxy)

---

## ***느낀점***

### 황순철
프로젝트의 기반부터 직접 설계하고 구현하려는 목표를 가졌기에 초기 개발 속도는 다소 지연되었습니다. 하지만 이 과정을 통해 기술적 이해도를 깊이 있게 다질 수 있었습니다. 특히 유튜브 API를 활용한 영상 검색 및 저장 기능을 성공적으로 구현해 내면서, 구상한 아이디어가 실제 동작하는 서비스로 실체화되는 과정에서 큰 성취감과 보람을 느꼈습니다.

### 조가을
기획부터 디자인, 개발까지 쉴 새 없이 달려왔던 시간이었습니다. 특히 AI 스튜디오의 누끼/합성 기능을 Docker 컨테이너 위에서 구현하며, 모델 배포와 GPU 리소스 활용이라는 새로운 영역에 도전해볼 수 있어 뜻깊었습니다. 프론트엔드와 백엔드가 복잡하게 데이터를 주고받는 과정을 디버깅하며 전역적인 에러 핸들링과 아키텍처의 중요성을 뼈저리게 느낀 소중한 경험이었습니다.