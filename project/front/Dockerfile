# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# 패키지 파일 복사 및 의존성 설치
COPY package*.json ./
RUN npm install

# 프로젝트 소스 복사 및 빌드
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine

WORKDIR /app

# 빌드 결과물 복사
COPY --from=builder /app/.output ./.output

# Nuxt 3 서버 설정
ENV HOST=0.0.0.0
ENV PORT=3000
ENV NODE_ENV=production

# 포트 노출
EXPOSE 3000

# 서버 실행
CMD ["node", ".output/server/index.mjs"]
