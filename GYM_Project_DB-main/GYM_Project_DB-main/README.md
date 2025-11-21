# 🏋️ 헬스장 관리 시스템 (GYM Management System)

FastAPI + React 기반 헬스장 회원 관리 및 키오스크 출입 시스템

---

## 📁 프로젝트 구조

```
GYM_PROJECT_DB/
├── Back/                    # FastAPI 백엔드
│   ├── app/
│   │   ├── main.py         # FastAPI 앱 진입점
│   │   ├── config.py       # 환경설정
│   │   ├── database.py     # DB 연결 및 세션 관리
│   │   ├── models/         # SQLAlchemy ORM 모델
│   │   ├── schemas/        # Pydantic 스키마
│   │   ├── repositories/   # DB CRUD 로직
│   │   ├── services/       # 비즈니스 로직
│   │   ├── routers/        # API 라우터
│   │   └── utils/          # 유틸리티 함수
│   ├── .venv/              # 가상환경
│   ├── requirements.txt    # Python 패키지 목록
│   └── .env                # 백엔드 환경변수
│
└── Front/                   # React 프론트엔드
    ├── src/
    │   ├── pages/          # 페이지 컴포넌트
    │   │   ├── KioskPage.tsx    # 키오스크 화면
    │   │   └── AdminApp.tsx     # 관리자 화면
    │   ├── services/       # API 서비스
    │   └── components/     # 재사용 컴포넌트
    ├── package.json
    └── .env                # 프론트엔드 환경변수
```

---

## 🎯 주요 기능

### 1. 키오스크 (사용자 입장)

#### 기능
- **전화번호 키패드 입력**: 숫자 0~9, 확인, 삭제 버튼 (총 12개)
- **전화번호 뒷 4자리 입력**: 회원 검색
- **중복 처리**:
  - 뒷 4자리가 중복되면 → 이름 목록 표시 → 사용자가 선택
  - 단일 회원이면 → 자동 입장

#### 입장 확인 화면 (5개 항목 세로 배치)
1. 이름
2. 회원권 만료일자
3. 락커룸 만료일자
4. 회원복 만료일자
5. **"입장확인입니다."** 메시지

#### 특징
- 10초 후 자동으로 화면 초기화

---

### 2. 관리자 웹

#### 기능
- **로그인**: 4자리 비밀번호 인증
- **회원 정보 조회**:
  - 회원번호
  - 이름
  - 전화번호 (11자리)
  - 회원권 등록일 / 만료일
  - 락커룸대여 등록일 / 만료일
  - 회원복대여 등록일 / 만료일
  - 출석 날짜/시간 기록
  - 퇴장 시간 기록
- **회원 추가**: 신규 회원 등록
- **회원권 연장**: 기존 회원 회원권 연장
- **당일 입장 회원 표시**:
  - 이름
  - 휴대폰 번호
  - 회원권 종류
  - 입장 시간

---

## 🗄️ 데이터베이스 구조

### 테이블 관계
- **Members (1) : Locker_Rentals (1)**: 한 회원당 하나의 락커 대여
- **Members (1) : Uniform_Rentals (1)**: 한 회원당 하나의 회원복 대여
- **Members (1) : CheckIn_Log (N)**: 한 회원이 여러 번 출입
- **Membership_Types (1) : Members (N)**: 하나의 회원권에 여러 회원

### 주요 제약조건
- **UNIQUE**: `phone_number` (전화번호 중복 방지)
- **Primary Key**: `checkin_id` (출입 기록 고유 ID, 자동 증가)

---

## 🚀 설치 및 실행

### 1️⃣ 백엔드 (FastAPI)

```bash
# 백엔드 폴더로 이동
cd Back

# 가상환경 활성화 (Windows)
.\.venv\Scripts\Activate.ps1

# 패키지 설치
pip install -r requirements.txt

# 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**백엔드 실행 확인:**
```
http://localhost:8000
```

---

### 2️⃣ 프론트엔드 (React + Vite)

```bash
# 프론트엔드 폴더로 이동
cd Front

# 패키지 설치
npm install

# 개발 서버 실행
npm run dev
```

**프론트엔드 실행 확인:**
```
http://localhost:5173
```

---

## 🔧 환경 설정

### 백엔드 `.env` (Back/.env)

```env
# 데이터베이스 연결
DATABASE_URL=sqlite:///./gym.db

# 관리자 비밀번호 (4자리)
ADMIN_PASSWORD=1234

# JWT 시크릿 키
SECRET_KEY=your-secret-key-here
```

---

### 프론트엔드 `.env` (Front/.env)

```env
# 백엔드 API URL
VITE_API_URL=http://10.1.3.149:8000/api
```

**⚠️ IP 주소는 본인의 PC IP로 변경하세요!**

---

## 📱 접속 방법

### PC에서
- **키오스크**: `http://localhost:5173/kiosk`
- **관리자**: `http://localhost:5173/admin`

### 핸드폰에서 (같은 Wi-Fi)
- **키오스크**: `http://[PC_IP]:5173/kiosk`
- **관리자**: `http://[PC_IP]:5173/admin`

---

## 🔄 실행 흐름

### 회원 입장 흐름

```
1. 핸드폰에서 /kiosk 접속
   ↓
2. 전화번호 뒷 4자리 입력 (키패드)
   ↓
3. 확인 버튼 클릭
   ↓
4. checkinService.checkin({ last4 }) 호출
   ↓
5. FastAPI → POST /api/checkin
   ↓
6. 회원 검색 결과:
   - 중복 → 이름 목록 표시 → 선택
   - 단일 → 자동 입장
   ↓
7. 입장 확인 화면 (5개 항목 표시)
   ↓
8. 10초 후 자동으로 화면 초기화
```

---

## 🛠️ 기술 스택

### 백엔드
- **FastAPI**: Python 웹 프레임워크
- **SQLAlchemy**: ORM
- **Uvicorn**: ASGI 서버
- **Pydantic**: 데이터 검증

### 프론트엔드
- **React**: UI 라이브러리
- **TypeScript**: 타입 안전성
- **Vite**: 빌드 툴
- **Tailwind CSS**: 스타일링
- **Axios**: HTTP 클라이언트

### 데이터베이스
- **SQLite** (개발용)
- **PostgreSQL/MySQL** (프로덕션용)

---

## 📝 API 엔드포인트

### 키오스크 API

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/api/checkin` | 전화번호 뒷 4자리로 체크인 |
| GET | `/api/member/{member_id}` | 회원 정보 조회 |

### 관리자 API

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/api/admin/login` | 관리자 로그인 |
| GET | `/api/admin/members` | 회원 목록 조회 |
| POST | `/api/admin/members` | 회원 추가 |
| PUT | `/api/admin/members/{id}` | 회원 정보 수정 |
| POST | `/api/admin/extend` | 회원권 연장 |
| GET | `/api/admin/today-checkins` | 당일 입장 회원 |

---

## 🐛 트러블슈팅

### 1. 백엔드 연결 실패

**문제**: `ERR_CONNECTION_TIMED_OUT`

**해결:**
```bash
# 1. PC IP 주소 확인
ipconfig

# 2. Front/.env 파일 수정
VITE_API_URL=http://[새IP주소]:8000/api

# 3. 프론트엔드 재시작
npm run dev
```

---

### 2. 백엔드 포트 이미 사용 중

```bash
# 포트 사용 중인 프로세스 확인
netstat -ano | findstr :8000

# 프로세스 종료 (PID 확인 후)
taskkill /F /PID [PID번호]
```

---
  