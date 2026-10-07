# AI Data Assistant

시계열 데이터를 Firestore에 저장·관리하고, 현재 데이터 요약을 AI 컨텍스트로 주입해 데이터 기반 답변을 제공하는 웹 애플리케이션입니다.

## 해결하려는 문제

원시 시계열 데이터만으로는 기간, 평균, 범위, 최근 변화 방향을 빠르게 파악하기 어렵습니다. AI Data Assistant는 데이터를 한곳에서 관리하고 핵심 통계를 자동 계산한 뒤, 그 결과를 AI가 참고하도록 하여 사용자가 자연어로 현재 데이터 상태를 확인할 수 있게 합니다.

## 주요 기능

- `date`, `value`, `memo` 기반 시계열 데이터 추가·조회·수정·삭제 API
- 기간, 개수, 평균, 최솟값, 최댓값, 최근 추세 자동 요약
- Firestore 데이터 요약을 시스템 프롬프트에 주입하는 AI 채팅
- 사용자 질문과 AI 답변의 Firestore 자동 저장
- 이전 대화 목록 조회 및 특정 대화 불러오기
- 데이터 추가·삭제, 요약, 채팅, 대화 기록을 제공하는 단일 페이지 UI
- FastAPI Swagger 문서

## 기술 스택

- Backend: Python 3.10+, FastAPI, Uvicorn, Pydantic
- Database: Firebase Firestore
- AI: Codyssey OpenAI 호환 API, OpenAI Python SDK
- Frontend: Vanilla HTML, CSS, JavaScript
- Test: pytest, FastAPI TestClient, HTTPX
- Deployment target: Render, Vercel

## 프로젝트 구조

```text
.
├── backend/
│   ├── app/
│   │   ├── clients/       # Firestore/OpenAI 클라이언트
│   │   ├── core/          # 환경 설정
│   │   ├── repositories/  # Mock/Firestore 데이터 접근
│   │   ├── routers/       # FastAPI 엔드포인트
│   │   ├── schemas/       # Pydantic 요청·응답 모델
│   │   └── services/      # 데이터·대화·채팅 비즈니스 로직
│   ├── scripts/           # 시계열 데이터 seed 스크립트
│   └── tests/             # API 자동 테스트
├── frontend/
│   ├── css/
│   ├── js/
│   └── index.html
├── ASSIGNMENT.md
├── PRODUCT.md
├── ARCHITECTURE.md
└── CHECKLIST.md
```

## 데이터 구조

### `data` 컬렉션

| 필드 | 형식 | 설명 |
| --- | --- | --- |
| `id` | string | Firestore document ID, API 응답에 포함 |
| `date` | `YYYY-MM-DD` | 시계열 기준 날짜 |
| `value` | number | 분석 대상 값 |
| `memo` | string | 선택 메모, 최대 500자 |

### `conversations` 컬렉션

| 필드 | 형식 | 설명 |
| --- | --- | --- |
| `id` | string | Firestore document ID |
| `title` | string | 대화 제목 |
| `messages` | array | `role`, `content`, `created_at`을 가진 메시지 목록 |
| `created_at` | ISO 8601 string | 생성 시각 |
| `updated_at` | ISO 8601 string | 최근 변경 시각 |

## API 목록

| Method | Path | 설명 |
| --- | --- | --- |
| GET | `/health` | 서버 상태와 mock/production 모드 확인 |
| POST | `/api/data` | 데이터 생성 |
| GET | `/api/data` | 데이터 목록 조회 |
| GET | `/api/data/summary` | 기간·개수·평균·최소·최대·최근 추세 조회 |
| PUT | `/api/data/{id}` | 데이터 수정 |
| DELETE | `/api/data/{id}` | 데이터 삭제 |
| POST | `/api/conversations` | 대화 생성 |
| GET | `/api/conversations` | 대화 목록 조회 |
| GET | `/api/conversations/{id}` | 특정 대화와 메시지 조회 |
| DELETE | `/api/conversations/{id}` | 대화 삭제 |
| POST | `/api/chat` | 데이터 요약 기반 AI 답변 생성 및 대화 자동 저장 |

## AI Context Injection

`POST /api/chat` 요청을 받으면 ChatService가 Firestore의 최신 데이터를 요약합니다. 기간, 데이터 개수, 평균, 최솟값, 최댓값, 최근 추세를 시스템 프롬프트에 넣은 뒤 사용자 질문과 함께 AI API로 전송합니다. 생성된 답변은 질문과 함께 해당 conversation에 자동 저장됩니다.

HUMAN VERIFY에서는 실제 AI 답변에 표시된 기간, 개수, 평균, 최솟값, 최댓값, 최근 추세가 당시 Firestore 요약과 일치함을 확인했습니다.

## 로컬 실행 방법

### 1. 가상환경과 의존성

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 2. Backend 환경변수

`backend/.env.example`을 참고해 현재 터미널 또는 별도의 `.env`에 값을 설정합니다. `.env`와 실제 자격증명 파일은 Git에 추가하지 않습니다. `.env` 파일을 사용한다면 Backend 실행 명령에 `--env-file .env`를 추가합니다.

Production 연동에 필요한 주요 값:

```text
OPENAI_API_KEY=<secret>
OPENAI_BASE_URL=https://copa.codyssey.kr/v1
OPENAI_MODEL=gpt-5.4-mini
FIREBASE_SERVICE_ACCOUNT_JSON=<JSON 문자열 또는 로컬 JSON 파일 경로>
ALLOWED_ORIGINS=http://localhost:5500,http://127.0.0.1:5500
USE_MOCK_SERVICES=false
```

외부 자격증명 없이 로컬 자동 테스트를 실행할 때는 `USE_MOCK_SERVICES=true`를 사용합니다.

### 3. Backend 실행

```powershell
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 4. Frontend 실행

새 터미널에서 다음을 실행합니다.

```powershell
cd frontend
python -m http.server 5500 --bind 127.0.0.1
```

브라우저에서 `http://127.0.0.1:5500`으로 접속합니다.

## 환경변수 목록

| 변수 | 필수 조건 | 설명 |
| --- | --- | --- |
| `OPENAI_API_KEY` | production | AI API 인증 키 |
| `OPENAI_BASE_URL` | Codyssey API 사용 시 | OpenAI 호환 API base URL |
| `OPENAI_MODEL` | 선택 | 사용할 모델명 |
| `FIREBASE_SERVICE_ACCOUNT_JSON` | production | 서비스 계정 JSON 문자열 또는 파일 경로 |
| `ALLOWED_ORIGINS` | 권장 | 쉼표로 구분한 CORS 허용 origin |
| `USE_MOCK_SERVICES` | 선택 | `true`이면 Mock repository와 Mock chat 사용 |
| `API_BASE_URL` | seed/runtime 설정 | seed 스크립트 또는 frontend runtime override용 Backend URL |

## 실행 주의사항

- `OPENAI_BASE_URL` 값 뒤에 공백이 들어가면 올바르지 않은 URL로 처리되어 실제 AI 호출이 실패할 수 있습니다.
- 잘못된 `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`가 설정된 환경에서는 Firestore 연결이 실패할 수 있습니다. 필요한 경우 서버 프로세스 범위에서만 값을 제거하고 실행합니다.
- API 키와 Firebase 서비스 계정 값은 코드, 문서, 로그, Git에 기록하지 않습니다.

## 검증 결과

### 자동 및 실제 연동 검증

- Python 문법/import 및 frontend JavaScript 문법: PASS
- pytest Mock API 테스트: PASS
- FastAPI `/health`와 `/docs`: PASS
- Data CRUD와 Summary: PASS
- Conversation CRUD와 메시지 자동 저장: PASS
- 실제 Firestore 저장·조회: PASS
- 실제 Codyssey OpenAI 호환 API 응답: PASS
- Firestore Summary의 AI Context Injection: PASS

### HUMAN VERIFY

- 페이지/CSS: PASS
- 데이터 요약: PASS
- 데이터 추가: PASS
- 데이터 삭제: PASS
- 실제 AI 응답: PASS
- 대화 목록/불러오기: PASS
- AI 답변과 현재 Firestore 요약 수치 일치: PASS

## URL

| 구분 | URL | 상태 |
| --- | --- | --- |
| Local Frontend | `http://127.0.0.1:5500` | VERIFIED |
| Local Backend | `http://127.0.0.1:8000` | VERIFIED |
| Local Swagger | `http://127.0.0.1:8000/docs` | VERIFIED |
| Render Backend candidate | `https://m1-2-ai-data-assistant.onrender.com` | NOT VERIFIED |
| Render Swagger candidate | `https://m1-2-ai-data-assistant.onrender.com/docs` | NOT VERIFIED |
| Vercel Frontend | TBD | NOT VERIFIED |

Render/Vercel의 실제 배포 상태와 URL은 POST_DEPLOY VERIFY에서 확인한 뒤 갱신합니다.

## 제출 스크린샷

아래 이미지는 최종 배포 검증 후 추가합니다.

- [ ] 데이터 요약이 반영된 AI 채팅 질문·답변
- [ ] 데이터 추가·삭제 동작
- [ ] 이전 대화 목록과 대화 불러오기
- [ ] Swagger UI
- [ ] Render Backend 및 Vercel Frontend 실제 배포 URL
