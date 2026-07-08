# AWS EC2 배포 가이드라인

현재 프로젝트는 `docker-compose`를 사용하여 백엔드와 프론트엔드가 컨테이너화되어 있으므로, EC2에 배포하는 과정이 비교적 간단합니다. 아래의 순서대로 진행해 주세요.

## 1. AWS EC2 인스턴스 생성 및 설정

1. **EC2 인스턴스 생성**: AWS 콘솔에 접속하여 **Ubuntu Server** (최신 LTS 버전)로 인스턴스를 생성합니다.
2. **보안 그룹(인바운드 규칙) 설정**: 다음 포트들을 열어주어야 외부에서 접근이 가능합니다.
   - `SSH` (22): 내 IP 혹은 위치에서 접속하기 위해
   - `HTTP` (80): Nginx 등을 통해 웹 서비스 시 필요
   - `HTTPS` (443): SSL(HTTPS) 적용 시 필요
   - `사용자 지정 TCP` (3000): 프론트엔드 직접 접근 시 (Nginx를 쓴다면 안 열어도 됨)
   - `사용자 지정 TCP` (8000): 백엔드 직접 접근 시 (Nginx를 쓴다면 안 열어도 됨)
3. **키 페어(Pem 키)**: 발급받은 키 페어를 안전한 곳에 저장합니다.

## 2. EC2 인스턴스 접속

터미널(또는 PuTTY 등)을 열고 발급받은 키 페어를 이용해 EC2에 SSH로 접속합니다.

```bash
# 키 파일 권한 설정 (Mac/Linux의 경우)
chmod 400 your-key.pem

# EC2 접속
ssh -i "your-key.pem" ubuntu@<EC2-퍼블릭-IP>
```

## 3. 필수 프로그램 설치 (Docker & Git)

EC2에 접속한 후, 프로젝트를 실행하기 위한 환경을 구성합니다.

```bash
# 패키지 업데이트
sudo apt-get update
sudo apt-get upgrade -y

# Git 설치 (보통 기본 설치되어 있음)
sudo apt-get install git -y

# Docker 설치
sudo apt-get install docker.io -y

# Docker Compose 설치
sudo apt-get install docker-compose -y

# (선택) sudo 없이 docker 명령어를 쓰기 위한 권한 설정 (적용 후 재접속 필요)
sudo usermod -aG docker ubuntu
```

## 4. 프로젝트 가져오기 및 환경변수 설정

서버로 프로젝트 파일을 가져오는 방법은 **A) Git Clone 방식**과 **B) 로컬에서 직접 업로드 방식**이 있습니다. 원하시는 방법을 하나 선택해 진행해 주세요.

### 방법 A: Git Clone 방식 (추천)
GitHub에서 프로젝트를 클론하고, 앞서 만든 `.env` 파일을 서버에서 다시 생성합니다.

```bash
# 1. 깃허브에서 프로젝트 클론
git clone https://github.com/tnscjf3146/higherproduction.git

# 2. 프로젝트 폴더로 이동
cd higherproduction/project

# 3. back 폴더에 .env 파일 생성
nano back/.env
# (복사한 백엔드 .env 내용을 붙여넣고 Ctrl+O -> Enter -> Ctrl+X 로 저장)

# 4. front 폴더에 .env 파일 생성
nano front/.env
# (복사한 프론트엔드 .env 내용을 붙여넣고 Ctrl+O -> Enter -> Ctrl+X 로 저장)
```

### 방법 B: 로컬에서 직접 업로드 방식 (`scp` 명령어 활용)
Git을 거치지 않고, 현재 작업 중인 Windows 로컬 컴퓨터에서 EC2 서버로 폴더를 통째로 전송하는 방법입니다. `.env` 파일까지 모두 한 번에 전송되므로 서버에서 다시 만들 필요가 없습니다.

새로운 Windows 터미널(PowerShell)을 열고, 현재 접속 중이신 환경에 맞춰 아래 명령어를 실행해 주세요. (EC2에 접속된 터미널이 아닌, **내 컴퓨터 터미널**에서 실행해야 합니다)

```powershell
# 현재 위치: c:\Users\tnscj\Desktop\first
# higherproduction 폴더 전체를 EC2의 /home/ubuntu 경로로 전송합니다.
scp -i "ec2/homekey.pem" -r ./higherproduction ubuntu@15.164.221.172:/home/ubuntu/
```

> **참고**: 터미널 명령어가 익숙하지 않으시다면 **FileZilla(파일질라)** 나 **WinSCP** 같은 무료 프로그램을 설치하여, 마치 폴더에 파일 복사하듯 드래그 앤 드롭으로 업로드하실 수도 있습니다. (접속 시 프로토콜은 SFTP를 선택하고, 호스트에 IP 주소, 사용자에 `ubuntu`, 키 파일에 `.pem` 파일을 등록하시면 됩니다.)

파일 전송이 완료되었다면 EC2 터미널에서 폴더로 이동합니다.
```bash
cd higherproduction/project
```

> [!CAUTION]
> **중요**: 프론트엔드의 `NUXT_PUBLIC_API_BASE_URL`은 로컬 배포 시 `http://127.0.0.1:8000`이었지만, 실제 배포 환경에서는 백엔드의 **실제 도메인 또는 EC2의 퍼블릭 IP 주소**로 변경해야 합니다. (예: `http://<EC2-퍼블릭-IP>:8000`)
> 마찬가지로 백엔드의 `CORS_ALLOWED_ORIGINS`에도 프론트엔드의 퍼블릭 주소를 추가해야 합니다.

## 5. 프로젝트 실행

프로젝트 실행은 상황에 따라 명령어가 다릅니다. `docker-compose.yml` 파일이 있는 `project` 디렉토리에서 실행해 주세요.

### 1) 최초 실행 시 (데이터베이스 생성 포함)
처음 서버를 켤 때는 컨테이너를 실행한 뒤, 백엔드 데이터베이스 테이블을 생성해야 합니다.

```bash
# 1. 이미지 빌드 및 백그라운드에서 컨테이너 실행
sudo docker-compose up -d --build

# 2. 데이터베이스 테이블 생성 (최초 1회 필수)
sudo docker-compose exec back python manage.py migrate

# 3. 관리자 계정 생성 (선택 사항)
sudo docker-compose exec back python manage.py createsuperuser --username admin
```

### 2) 코드 수정 후 업데이트 시
이후 프론트엔드나 백엔드의 코드를 수정하여 서버에 반영할 때는 데이터베이스 명령 없이 이미지만 다시 빌드하여 재시작합니다.

```bash
# 수정된 코드를 바탕으로 이미지를 다시 빌드하고 띄우기
sudo docker-compose up -d --build
```

명령어가 완료되면 아래 주소로 접속하여 정상적으로 켜졌는지 확인합니다.
- 프론트엔드: `http://<EC2-퍼블릭-IP>:3000`
- 백엔드(API): `http://<EC2-퍼블릭-IP>:8000`

## 6. 서버 중지 및 초기화 (Docker Compose 명령어)

프로젝트 폴더(`project`) 내에서 아래 명령어들을 사용하여 서버를 관리할 수 있습니다.

### 서버(컨테이너) 안전하게 닫기/중지하기
현재 실행 중인 컨테이너들을 중지하고 네트워크를 제거합니다. (데이터베이스 볼륨 등은 유지됨)
```bash
sudo docker-compose down
```

### 서버(컨테이너) 및 데이터 완전히 삭제하기
컨테이너뿐만 아니라 저장된 데이터(볼륨)와 이미지까지 모두 초기화하고 싶을 때 사용합니다.
```bash
# -v: 볼륨(데이터베이스 저장소 등)까지 모두 삭제
# --rmi all: 빌드된 이미지까지 모두 삭제
sudo docker-compose down -v --rmi all
```
(이 명령어를 실행하면 데이터베이스가 초기화되어 기존 데이터가 사라지므로 주의하세요!)

---

> [!TIP]
> **추가 권장 사항 (Nginx + HTTPS 적용)**
> 위와 같이 포트번호(3000)를 붙여서 서비스하는 것보다, 도메인을 연결하고 **Nginx**를 리버스 프록시로 사용하여 80 포트로 접속 시 3000 포트로 연결되게 하는 것이 좋습니다. 추가로 **Certbot(Let's Encrypt)**을 사용해 무료로 HTTPS 통신을 적용할 것을 강력히 권장합니다.

---

## 7. 리눅스 파일 및 폴더 삭제 방법 (기본 명령어)

터미널에서 파일을 잘못 올렸거나 폴더를 삭제해야 할 때는 아래 명령어를 사용합니다.

### 개별 파일 삭제
```bash
rm 파일이름
```
*(예: `rm test.txt`)*

### 폴더 전체 삭제 (내부 파일 포함)
```bash
rm -rf 폴더이름
```
*(예: `rm -rf higherproduction`)*
> **주의**: `-rf` 옵션을 사용하면 묻지 않고 폴더와 그 안의 모든 내용이 즉시 삭제되므로 절대 경로를 헷갈리지 않도록 주의하세요!

