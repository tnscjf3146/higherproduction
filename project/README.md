# 하이어 프로덕션

## 목차
|목차|세부사항|업데이트|비고|
|:---:|:---:|:---:|:---:|
|개요|프로젝트 개요|2026-06-29||
|환경/사용스택||2026-06-29||
|구조|back / front|2026-06-29||
|데이터테이블|세부설명|||
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
>&emsp;원인은 유저루트의 설계부족으로 보임
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
>&emsp;사용자 인터페이스 조정 기능<br>
>&emsp;문의 조정기능<br>
>&emsp;영상 추가기능<br>
>&emsp;커뮤니티 기능<br>
>&emsp;유저 관리기능<br>
>&emsp;일정 관리기능<br>
>
>#### 로그인
>
>&emsp;로그인 기능<br>
>&emsp;유저 프로필 기능<br>
>&emsp;카카오톡, 구글 로그인 기능<br><br>
>
>#### 사용자 인터페이스
>
>&emsp;소통 창구<br>
>&emsp;문의 기능<br>
>&emsp;시스템 문의 기능<br>
>&emsp;작업물 보기<br>
>&emsp;디테일 보기<br>
>&emsp;플랜 보기<br><br>

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
  ├ accounts                  로그인, 회원가입
  ├ schedule                  스케쥴 관리
  ├ notice                    관리자 개시글
  ├ space                     관리자 작업공간
  ├ works                     포트폴리오
  ├ products                  상품 등록, 조회 관리
  ├ community                 고객 상담,문의
  └ inquiry                   시스템 문의, 커뮤니티

fornt/
  ├ .env
  ├ pages/
  │   ├ index.vue
  │   ├ accounts/
  │   ├ schedule/
  │   ├ notice/
  │   ├ space/
  │   ├ works/
  │   ├ products/
  │   ├ comunity/
  │   └ inquiry/
  │
  ├ stores/                     영구 상태 관리
  │   ├ auth.js
  │   ├ schedule.js             조작 시 여러 컴포넌트 실시간 공유
  │   └ system.js               다크모드, 전체 알림
  │
  └ components/
      ├ common/                 공통 레이아웃
      └ products/
```

&emsp;

&emsp;4칸

&nbsp;1칸