FROM python:3.11-slim

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 시스템 의존성 설치 (필요한 경우)
# RUN apt-get update && apt-get install -y ...

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 소스 복사
COPY . .

# 포트 노출
EXPOSE 8000

# 서버 실행 명령어 (AWS 배포를 위한 gunicorn 사용)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
