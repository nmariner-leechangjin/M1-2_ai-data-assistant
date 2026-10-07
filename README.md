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
├── evidence/             # 실제 검증 결과의 텍스트 증빙
├── ASSIGNMENT.md
├── PRODUCT.md
├── ARCHITECTURE.md
└── CHECKLIST.md
```

## Backend Layer Responsibilities

- **Router:** HTTP 요청·응답 경계를 담당하고 Pydantic 검증이 끝난 입력으로 Service를 호출합니다. Firestore 접근이나 비즈니스 규칙은 직접 구현하지 않습니다.
- **Service:** 데이터 요약, AI context 구성, 대화 저장 시점과 같은 비즈니스 규칙을 담당합니다.
- **Repository:** Firestore CRUD와 저장소 접근을 담당합니다. Service가 Firestore SDK에 직접 의존하지 않게 합니다.
- **Client:** OpenAI 및 Firebase 클라이언트 생성과 외부 서비스 접속 세부사항을 캡슐화합니다.

호출 흐름은 다음과 같습니다.

```text
Frontend → Router → Service → Repository / Client → Firestore / OpenAI
```

이 구조는 책임 분리, 단위 테스트 용이성, 외부 서비스 교체 가능성, 공통 로직 재사용성을 확보하기 위해 사용합니다.

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

### Firestore query와 validation 운영 기준

- 현재 목록은 repository에서 조회한 뒤 Service에서 `date` 기준으로 정렬합니다. 데이터 규모와 날짜 조건 조회가 늘어나면 Firestore single-field/composite index와 서버 측 정렬 쿼리를 검토합니다.
- 날짜 표현은 현재 `YYYY-MM-DD`로 통일합니다. 시간 단위 분석이 필요해지면 Firestore Timestamp로 일관되게 전환합니다.
- Pydantic이 `date`, `value` 타입과 `memo` 최대 500자, chat message 최대 4,000자를 검증합니다.
- 업무상 값의 범위가 정해지면 `Field(ge=..., le=...)` 또는 field validator로 `value` 범위를 추가 검증할 수 있습니다. 이는 현재 요구사항에 없는 향후 강화 항목입니다.

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

### Context Injection의 장단점

- 장점: 일반적인 답변이 아니라 사용자의 최신 데이터 통계를 근거로 답할 수 있습니다.
- 위험: context가 길어지거나 오래된 요약이 사용될 수 있고, 사용자 입력이 prompt를 오염시킬 수 있습니다.
- 완화: 원본 전체 대신 서버가 생성한 summary만 주입하고, 입력 길이를 제한하며, 매 요청마다 최신 데이터를 다시 요약합니다.

## Why Summary Logic Is Separated

- **책임 분리:** CRUD와 통계 계산을 분리해 저장 코드와 분석 코드가 섞이지 않게 합니다.
- **재사용성:** `/api/data/summary`와 `/api/chat`이 같은 `DataService.summary()` 결과를 사용합니다.
- **성능과 확장:** 향후 캐시, 집계 문서, 기간별 통계로 변경할 때 호출부를 유지하기 쉽습니다.
- **테스트:** 저장소를 Mock으로 교체해 통계 계산과 Chat context를 독립적으로 검증할 수 있습니다.

최근 추세는 날짜순 데이터의 최근 7개를 기본 window로 사용합니다. 데이터가 변경될 때 별도 캐시 없이 다시 계산합니다. 향후 요구가 생기면 `window_size` 파라미터나 집계 캐시를 도입할 수 있습니다.

### Conversation 저장 정책

새 chat 요청은 먼저 conversation을 준비하고, AI 응답이 성공한 뒤 user/assistant 메시지 2건을 함께 저장합니다. 현재 자동 재시도는 없으며, AI 호출이 실패하면 메시지는 저장되지 않지만 새로 만든 빈 conversation이 남을 수 있습니다. 재시도·부분 저장·빈 대화 정리는 향후 오류 정책으로 명시적으로 결정해야 합니다.

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

### Frontend 상태 흐름

데이터 저장과 AI 채팅은 `idle → loading → success/error → idle` 흐름을 따릅니다. 요청 중에는 버튼을 비활성화하고 로딩 문구를 표시하며, 성공 후 데이터를 다시 불러오고 오류 시 사용자 영역에 메시지를 표시합니다.

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

### 배포 환경변수 계획

- Render Backend: `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL`, `FIREBASE_SERVICE_ACCOUNT_JSON`, `ALLOWED_ORIGINS`, `USE_MOCK_SERVICES=false`
- Vercel/정적 Frontend: 배포 Backend를 가리키는 `API_BASE_URL` 또는 동등한 runtime config
- CORS: 실제 Vercel 도메인이 정해지면 정확한 origin을 Render의 `ALLOWED_ORIGINS`에 추가합니다.

## 실행 주의사항

- `OPENAI_BASE_URL` 값 뒤에 공백이 들어가면 올바르지 않은 URL로 처리되어 실제 AI 호출이 실패할 수 있습니다.
- 잘못된 `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`가 설정된 환경에서는 Firestore 연결이 실패할 수 있습니다. 필요한 경우 서버 프로세스 범위에서만 값을 제거하고 실행합니다.
- API 키와 Firebase 서비스 계정 값은 코드, 문서, 로그, Git에 기록하지 않습니다.

## Render Cold Start

무료 Render 환경에서는 일정 시간 미사용 후 첫 요청이 느릴 수 있습니다. 사용자에게 **“서버가 시작 중입니다. 첫 요청은 최대 수십 초 걸릴 수 있습니다.”**라고 안내할 수 있습니다.

대응 전략:

- Frontend의 loading 상태를 첫 응답까지 유지합니다.
- 첫 API 요청 timeout을 지나치게 짧게 설정하지 않습니다.
- 기존 `/health` endpoint를 배포 후 warm-up 후보로 사용할 수 있습니다.
- 운영 요구가 높아지면 always-on 유료 옵션을 검토합니다.

## Input Sanitization / XSS

- 현재 frontend는 message, memo, conversation title, summary와 오류를 모두 `textContent`로 표시합니다.
- `innerHTML` 기반 사용자 입력 렌더링을 사용하지 않습니다.
- Backend는 Pydantic으로 `date`/`value` 타입과 `memo`, `message`, `title` 길이를 제한합니다.
- 추가 강화 시 서버에서 memo/message 제어문자를 제거하고, HTML 허용 요구가 생길 때만 `bleach` 같은 allow-list sanitizer를 적용합니다.
- URL이나 사용자 제공 HTML을 직접 DOM에 삽입하지 않는 원칙을 유지합니다.

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

## Swagger / OpenAPI Evidence

로컬 production-mode Backend에서 확인한 결과입니다.

```text
GET http://127.0.0.1:8000/docs
→ HTTP 200

GET http://127.0.0.1:8000/openapi.json
→ HTTP 200
```

OpenAPI에 확인된 주요 path:

```text
/health
/api/data
/api/data/summary
/api/data/{item_id}
/api/conversations
/api/conversations/{cid}
/api/chat
```

## Firestore Integration Evidence

REAL INTEGRATION VERIFY에서 실제 Firestore를 사용해 다음을 확인했습니다. document ID와 credential은 기록하지 않습니다.

```text
POST   /api/data       → 201
GET    /api/data       → 생성 문서 조회 확인
PUT    /api/data/{id}  → 값 변경 확인
DELETE /api/data/{id}  → 200, 삭제 확인
cleanup marker count   → 0
test memo              → REAL_INTEGRATION_TEST
```

## Conversation Integration Evidence

```text
POST   /api/conversations       → 201
GET    /api/conversations       → 200
GET    /api/conversations/{id}  → 200
DELETE /api/conversations/{id}  → 200
POST   /api/chat                → 200, summary_used=true
chat 이후 user/assistant 메시지 2건 자동 저장 확인
```

HUMAN VERIFY에서도 대화 목록 표시와 특정 대화 불러오기를 모두 PASS로 확인했습니다.

## URL

| 구분 | URL | 상태 |
| --- | --- | --- |
| Local Frontend | `http://127.0.0.1:5500` | VERIFIED |
| Local Backend | `http://127.0.0.1:8000` | VERIFIED |
| Local Swagger | `http://127.0.0.1:8000/docs` | VERIFIED |
| Render Backend | TBD | NOT VERIFIED |
| Render Swagger | TBD | NOT VERIFIED |
| Vercel Frontend | TBD | NOT VERIFIED |

Render/Vercel의 실제 배포 상태와 URL은 POST_DEPLOY VERIFY에서 확인한 뒤 갱신합니다.

## Deployment Evidence

- Backend Production URL: `TBD` — NOT VERIFIED
- Frontend Production URL: `TBD` — NOT VERIFIED
- Production Swagger URL: `TBD` — NOT VERIFIED
- Production `/health` screenshot: pending production deployment
- Production user-flow screenshot: pending production deployment

현재 확보된 것은 **로컬 production-mode Backend 실행 증거**와 **실제 Firestore/OpenAI 연동 증거**입니다. 이는 실제 Render/Vercel 배포 증거를 대체하지 않습니다. 배포 후 이 섹션에 실제 URL, 확인 일시, `/health`, Swagger, Frontend 사용자 흐름 캡처를 추가합니다.

## 제출 스크린샷

아래 이미지는 최종 배포 검증 후 추가합니다.

- [ ] 데이터 요약이 반영된 AI 채팅 질문·답변
- [ ] 데이터 추가·삭제 동작
- [ ] 이전 대화 목록과 대화 불러오기
- [ ] Swagger UI
- [ ] Render Backend 및 Vercel Frontend 실제 배포 URL
