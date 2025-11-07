# back

헬스장 회원 관리 시스템입니다. 키오스크를 통한 회원 입장 관리와 관리자용 웹 인터페이스를 제공합니다.

## 설치 및 실행

### 백엔드

1. Python 3.8 이상 설치
2. 의존성 설치:
```bash
cd backend
pip install -r requirements.txt
```

3. 환경 변수 설정:
`.env` 파일을 backend 폴더에 생성하고 다음 내용 추가:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=gym_admin
DB_PASSWORD=your_password
DB_NAME=gym_management
SECRET_KEY=your_secret_key
API_PREFIX=/api
```

4. 서버 실행:
```bash
cd backend
uvicorn app.main:app --reload
```

### 프론트엔드

1. Node.js 16 이상 설치
2. 의존성 설치:
```bash
cd frontend
npm install
```

3. 개발 서버 실행:
```bash
npm run dev
```

## 기술 스택

- Backend: FastAPI
- Database: MySQL with pymysql
- Frontend: React

### 디렉토리 구조
```
GYM_PROJECT_DB
├── backend/           # FastAPI 백엔드 서버
│   ├── app/
│   │   ├── routers/  # API 엔드포인트
│   │   ├── services/ # 비즈니스 로직
│   │   └── repositories/ # 데이터베이스 액세스
│   └── requirements.txt
└── frontend/          # React 프론트엔드
```

## API 문서

API 문서는 다음 URL에서 확인할 수 있습니다:
- Swagger UI: `/api/docs`
- ReDoc: `/api/redoc`

### 주요 API 엔드포인트

#### 키오스크 (사용자)
- `POST /api/kiosk/verify` - 전화번호로 회원 확인
- `POST /api/kiosk/checkin` - 회원 입장 처리

#### 관리자
- `POST /api/admin/login` - 관리자 로그인
- `PUT /api/admin/change-password` - 관리자 비밀번호 변경

#### 회원 관리
- `GET /api/members` - 회원 목록 조회
- `POST /api/members` - 새 회원 등록
- `PUT /api/members/{member_id}` - 회원 정보 수정
- `DELETE /api/members/{member_id}` - 회원 삭제

#### 체크인/출입 관리
- `GET /api/checkin/today` - 당일 입장 회원 목록
- `GET /api/checkin/stats` - 출입 통계

#### 대여 관리
- `GET /api/rentals/lockers` - 사물함 대여 현황
- `POST /api/rentals/lockers` - 사물함 대여
- `GET /api/rentals/uniforms` - 회원복 대여 현황
- `POST /api/rentals/uniforms` - 회원복 대여

### 기능정의

- 사용자 (키오스크)
첫화면에는 전화번호 키패드 12개가있고 숫자는0부터 9까지  있고 나머지 빈 두곳에는 확인버튼과 숫자를 잘못입력시 지울수있는 delete버튼 존재
전화번호 뒷 4자리 입력후 확인버튼 누르기
 if 전화번호 뒷 4자리 중복된 사람있을시  뒷4자리가 똑같은 사람들 목록창 뜸 그후 자신의 이름 선택후 입장
확인 누른후 상태창에는 회원정보인 이름 , 회원권 만료일자, 라커룸 만료일자, 회원복 만료일자, 입장확인입니다. 라고 총5개의 항목이 세로로 표시되어야해
입장확인표시

- 관리자(관리자 컴퓨터)
관리자 처음 웹 클릭시 지정해놓은 암호 4자리 입력 확인후 웹 접속 가능
관리자의 컴퓨터 안에는 회원 정보 조회 (회원번호,이름, 전화번호 11자리,  회원권등록일, 회원권만료일,라커룸대여 등록일, 라커룸대여 만료일, 회원복대여 등록일, 회원복대여 만료일 , 회원이 출석한 날짜와 시간 기록및 퇴장시간 기록) 
회원 추가기능 
회원권 연장 기능
당일 입장회원 표시 (이름,휴대폰 번호,회원권 종류, 입장시간 표시)
- 데이터베이스
Members에는 이름, 전화번호, 등록일 ,만료일, 회원권 종류등 표시
Members (1) : Locker_Rentals (1): 한 회원은 오직 하나의 락커 대여 정보를 가짐.
Members (1) : Uniform_Rentals (1): 한 회원은 오직 하나의 회원복 대여 정보를 가짐.
Members (1) : CheckIn_Log (N): 한 회원은 여러 번 출입할 수 있음.
Membership_Types (1) : Members (N): 하나의 상품에 여러 회원이 가입할 수 있음.
Uniforms (1) : Rental_Logs (N): 하나의 회원복은 여러 번 대여될 수 있음
UNIQUE 제약조건: Members 테이블의 phone_number 컬럼에 적용하여, 동일한 전화번호로 중복 가입하는 것을 원천적으로 방지함.
기본키 (Primary Key) 제약조건: CheckIn_Log 테이블에 자동으로 증가하는 고유 ID인 checkin_id를 기본 키(PK)로 설정했습니다. 이는 한 회원이 하루에 여러 번 출첵하더라도 각각의 출입 기록이 모두 고유하게 식별될 수 있도록 보장하는 핵심적인 설계입니다
