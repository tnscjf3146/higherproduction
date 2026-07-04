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
|authority|Bool|||
|is_staff|Bool|||
|production|foreign|Products/Product||

### Works

#### Work

|Column|Type|Foreign|Notice|
|:---:|:---:|:---:|:---:|
|pk|int|||
|title|CharField|||
|youtube_link|URLField||영상 링크|
|content|TextField||게시글 내용|
|is_visible|Bool||공개 여부|
|created_at|DateTimeField||auto_now_add|
|updated_at|DateTimeField||auto_now|

### Products

#### Product

|Column|Type|Foreign|Notice|
|:---:|:---:|:---:|:---:|
|pk|int|||
|name|CharField||구독 상품명|
|description|TextField||상품 설명|
|price|int||가격|
|is_active|Bool||개별 판매 여부 (True/False)|
|created_at|DateTimeField||auto_now_add|
|updated_at|DateTimeField||auto_now|

### Space

#### Workspace

|Column|Type|Foreign|Notice|
|:---:|:---:|:---:|:---:|
|pk|int|||
|title|CharField||작업공간 명|
|description|TextField||작업 내용|
|status|CharField||진행 상태|
|created_at|DateTimeField||auto_now_add|
|updated_at|DateTimeField||auto_now|

### Schedule

#### ScheduleEvent

|Column|Type|Foreign|Notice|
|:---:|:---:|:---:|:---:|
|pk|int|||
|title|CharField||일정 명|
|start_date|DateTimeField||시작일|
|end_date|DateTimeField||종료일|
|description|TextField||일정 설명|

### Community

#### CustomerInquiry

|Column|Type|Foreign|Notice|
|:---:|:---:|:---:|:---:|
|pk|int|||
|user_id|foreign|User||
|title|CharField||고객 문의 제목|
|content|TextField||고객 문의 내용|
|status|CharField||답변 상태 (대기/완료)|
|created_at|DateTimeField||auto_now_add|

### Inquiry

#### SystemIssue

|Column|Type|Foreign|Notice|
|:---:|:---:|:---:|:---:|
|pk|int|||
|admin_id|foreign|User||
|title|CharField||시스템 이슈 제목|
|content|TextField||이슈 및 버그 내용|
|status|CharField||해결 상태 (대기/진행/완료)|
|created_at|DateTimeField||auto_now_add|

### System

#### SystemSetting

|Column|Type|Foreign|Notice|
|:---:|:---:|:---:|:---:|
|pk|int|||
|focus_mode_active|Bool||서비스 집중기간 여부|
|hide_products|Bool||전체 프로덕트 강제 숨김 (전역 설정)|
|block_inquiries|Bool||전체 문의 강제 차단 (전역 설정)|


&emsp;

&emsp;4칸

&nbsp;1칸