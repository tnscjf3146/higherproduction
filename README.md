# 하이어 프로덕션

## 목차
|목차|세부사항|업데이트|비고|
|:---:|:---:|:---:|:---:|
|개요|프로젝트 개요|2026-06-29||
|환경/사용스택||2026-06-29||
|구조|back / front|2026-06-29||
|데이터테이블|세부설명|2026-06-30||
|기능목록||||

## 개요

### 프로젝트의 이유

>#### <br>반응성 이슈
>
>&emsp;해당 프로젝트는 창 줄이기 등 반응성이 원활하지 않음
>
>
>#### 메세지 전달력 부족
>
>&emsp;가시성 부족<br>
>&emsp;원인은 유저루트의 설계부족으로 보임<br>
>&emsp;성과에 대한 언급 없음
>
>#### 데이터 베이스 부재
>
>&emsp;기능 넣기 불가<br>
>&emsp;데이터 변경을 위해 코드 전체를 뜯어 고쳐야 함<br>
>
>#### 기능 부재
>
>&emsp;사이트의 유동성 상실
>
>#### 포트폴리오
>
>&emsp;무엇보다 나의 포트폴리오를 위함<br><br>

### 추가할 기능

>#### <br>어드민
>
>&emsp;유저 관리 기능 (사용자 권한 및 상태 관리)<br>
>&emsp;포트폴리오 관리 (유튜브 영상 링크를 활용한 게시글 형식의 작업물 저장)<br>
>&emsp;작업공간 관리 (프로젝트 및 진행 상황 파악)<br>
>&emsp;날짜 관리 시스템 (일정 관리)<br>
>&emsp;서비스 집중 모드 제어 (외부 유저 대상 프로덕트 노출 및 문의 차단)<br>
>
>#### 로그인
>
>&emsp;로그인 기능<br>
>&emsp;유저 프로필 기능<br>
>&emsp;카카오톡, 구글 로그인 기능<br><br>
>
>#### 사용자 인터페이스
>
>&emsp;작업물 목록 조회<br>
>&emsp;작업물 상세 보기<br>
>&emsp;구독 상품(플랜) 보기<br>
>&emsp;문의 기능 (일반 문의 및 시스템 문의)<br><br>
>
>#### 추천 추가 기능
>
>&emsp;통계 및 대시보드 (어드민 페이지 내 방문자 및 주요 지표 시각화)<br>
>&emsp;알림 시스템 (문의 답변 및 상태 변경 시 안내)<br>
>&emsp;SEO 최적화 (검색 엔진 노출 향상)<br><br>

## 환경/사용스택

### front

>#### <br>프레임워크
>
>&emsp;Nuxt.js<br>
>
>#### 의존성
>
>&emsp;VueUse &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp; UI/UX 편의 기능<br>
>&emsp;persistedstate &emsp;&emsp;&emsp;&nbsp; 전역 상태 관리 <br><br>

### back

>#### <br>프레임워크
>
>&emsp;Django<br>
>
>#### 의존성
>
>&emsp;djangorestframework &nbsp; json 통신을 위한 도구<br>
>&emsp;django-cors-headers &nbsp; CORS 제한 해제<br>
>&emsp;pillow &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;이미지 처리<br><br>

## 환경 변수 (.env) 설정

프로젝트를 실행하기 위해 `back`과 `front` 폴더 내에 `.env` 파일을 각각 생성해야 합니다.

### back/.env
```env
# 허용할 호스트 및 CORS 설정
DJANGO_ALLOWED_HOSTS=*
CORS_ALLOWED_ORIGINS=http://localhost:3000

# 이메일 발송 설정 (SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# 유튜브 API 키
YOUTUBE_API_KEY=your_youtube_api_key
```

### front/.env
```env
# Nuxt 서버에서 통신할 백엔드 API 주소
NUXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

## 구조

```
back/
  ├ .env
  ├ config
  │   └ api_urls.py
  ├ account                   로그인, 회원가입
  ├ schedule                  스케쥴 관리
  ├ notice                    관리자 개시글
  ├ space                     관리자 작업공간
  ├ work                      포트폴리오
  ├ product                   상품 등록, 조회 관리
  ├ community                 고객-관리자 간 상담 및 문의
  ├ inquiry                   관리자-개발자 간 시스템 문의
  └ system                    시스템 전역 설정 (집중 모드 등)

fornt/
  ├ .env
  ├ pages/
  │   ├ index.vue
  │   ├ account/
  │   ├ schedule/
  │   ├ notice/
  │   ├ space/
  │   ├ work/
  │   ├ product/
  │   ├ community/
  │   └ inquiry/
  │
  ├ stores/                     영구 상태 관리
  │   ├ auth.js
  │   ├ schedule.js             조작 시 여러 컴포넌트 실시간 공유
  │   └ system.js               다크모드, 전체 알림
  │
  └ components/
      ├ common/                 공통 레이아웃
      └ product/
```

## 데이터 테이블

### accounts

#### User
|Column|Type|Foreign|Notice|
|:---:|:---:|:---:|:---:|
|pk|int|||
|username|CharField|||
|password|CharField|||
|email|EmailField|||
|phone_number|CharField|||

#### UserInfo
|Column|Type|Foreign|Notice|
|:---:|:---:|:---:|:---:|
|pk|int|||
|user_id|foreign|User||
|company_name|CharField||회사명|
|manager|CharField||담당자명|
|company_address|CharField||회사 주소|
|authority|Bool|||
|is_staff|Bool|||
|production|foreign|Products/Plan||

### Works

#### Category
|Column|Type|Foreign|Notice|
|:---:|:---:|:---:|:---:|
|pk|int|||
|name|CharField||카테고리명|
|subtitle|CharField||카테고리 부제목|
|order|int||노출 순서|
|is_vertical|Bool||세로형(쇼츠) 여부|

#### Work
|Column|Type|Foreign|Notice|
|:---:|:---:|:---:|:---:|
|pk|int|||
|category_id|foreign|Category|카테고리 분류|
|user_id|foreign|User|관련 고객|
|title|CharField||작품명|
|youtube_link|URLField||영상 링크|
|content|TextField||게시글 내용|
|status|CharField||진행 상태 (작업중/완료됨)|
|is_visible|Bool||공개 여부|
|created_at|DateTimeField||auto_now_add|
|updated_at|DateTimeField||auto_now|

#### BrandClient
|Column|Type|Foreign|Notice|
|:---:|:---:|:---:|:---:|
|pk|int|||
|name|CharField||브랜드명|
|subtitle|CharField||부가설명|
|created_at|DateTimeField||auto_now_add|

#### Project
|Column|Type|Foreign|Notice|
|:---:|:---:|:---:|:---:|
|pk|int|||
|title|CharField||프로젝트명|
|subtitle|CharField||부가설명|
|client_id|foreign|BrandClient|관련 브랜드 클라이언트|
|created_at|DateTimeField||auto_now_add|

#### Inquiry
|Column|Type|Foreign|Notice|
|:---:|:---:|:---:|:---:|
|pk|int|||
|title|CharField||문의 제목|
|name|CharField||고객 성함|
|company|CharField||회사명|
|phone|CharField||연락처|
|email|EmailField||이메일|
|category|CharField||문의 카테고리|
|budget|CharField||예산|
|details|TextField||상세 요청사항|
|created_at|DateTimeField||접수일자|
|is_read|Bool||관리자 읽음 여부|
|status|CharField||처리 상태 (미접수/처리 중/처리 완료)|

### Products

#### Plan (요금제)
|Column|Type|Foreign|Notice|
|:---:|:---:|:---:|:---:|
|pk|int|||
|plan_type|CharField||플랜 종류 (BASIC, GROWTH)|
|name|CharField||플랜명|
|subname|CharField||서브명|
|price|int||가격(만원)|
|recommends|ManyToMany|Recommend|추천 대상|
|operations|ManyToMany|Operation|운영 목적|
|productions|ManyToMany|Production|촬영/편수|
|items|ManyToMany|Item|제작 항목|
|created_at|DateTimeField||auto_now_add|
|updated_at|DateTimeField||auto_now|

#### Recommend / Operation / Production / Item
|Column|Type|Foreign|Notice|
|:---:|:---:|:---:|:---:|
|pk|int|||
|name|CharField||항목 이름|
### System

#### SiteSetting
|Column|Type|Foreign|Notice|
|:---:|:---:|:---:|:---:|
|pk|int|||
|logo_kr|CharField||국문 로고 텍스트/경로|
|logo_en|CharField||영문 로고 텍스트/경로|
|about_headings|JSONField||About 섹션 제목 리스트 (텍스트, 강조 여부)|
|email|EmailField||스튜디오 이메일|
|phone|CharField||스튜디오 전화번호|
|address|CharField||스튜디오 주소|
|instagram_handle|CharField||인스타그램 핸들 (예: @higher.production)|
|instagram_url|URLField||인스타그램 주소 (URL)|
|contact_title|CharField||Contact 페이지 타이틀|
|is_service_visible|BooleanField||Service 섹션 노출 여부|
|service_title|CharField||Service 섹션 메인 타이틀|
|service_desc|CharField||Service 섹션 서브 설명|
|is_about_visible|BooleanField||About 섹션 노출 여부|
|about_title|CharField||About 섹션 메인 타이틀|
|about_desc|CharField||About 섹션 서브 설명|
|is_contact_visible|BooleanField||Contact(Footer) 섹션 노출 여부|
|contact_header_title|CharField||Contact 섹션 메인 타이틀|
|contact_header_desc|CharField||Contact 섹션 서브 설명|
|footer_slogan_main|JSONField||푸터 메인 슬로건 (문장 리스트)|
|footer_slogan_sub|CharField||푸터 서브 슬로건|

&emsp;

&emsp;4칸

&nbsp;1칸