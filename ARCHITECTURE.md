# ARCHITECTURE

## 1. 문서 목적과 설계 기준

이 문서는 ASSIGNMENT.md와 PRODUCT.md의 요구사항을 구현 구조로 연결한다. 확정된 과제 요구사항은 Fact로, 구현 구조와 상세 schema는 설계 결정 또는 미결정 사항으로 구분한다.

## 2. 전체 시스템 구조

Browser (Vanilla HTML/CSS/JavaScript) → FastAPI Backend (Render) → Firestore 및 OpenAI GPT API

FastAPI Backend는 routers(HTTP 요청·응답 경계), services(비즈니스 로직), schemas(Pydantic 요청·응답 검증), clients/repositories(외부 서비스 접근)로 구성한다.

### 관계

- Frontend는 FastAPI의 공개 API만 호출하며 Firestore 또는 OpenAI API를 직접 호출하지 않는다.
- Backend는 Firestore에서 데이터와 대화를 읽고 저장한다.
- Backend는 데이터 요약을 GPT 시스템 프롬프트에 주입한 뒤 OpenAI GPT API를 호출한다.
- Firestore와 OpenAI의 자격증명은 Backend 환경 변수로만 관리한다.

## 3. FastAPI 역할 분리

| 계층 | 역할 | 포함하지 않는 책임 |
| --- | --- | --- |
| main | 앱 생성, router 등록, CORS, 공통 예외 처리, 설정 초기화 | 도메인별 비즈니스 로직 |
| router | 경로 선언, 입력 수신, schema 검증 연결, HTTP 응답 반환 | Firestore 직접 조회, GPT 프롬프트 조립 |
| service | CRUD, 요약 계산, 대화 저장·조회, 채팅 컨텍스트 주입 | HTTP 프레임워크 초기화 |
| model/schema | Pydantic 요청·응답 모델과 도메인 데이터 구조 | 비즈니스 처리, 외부 호출 |
| repository/client | Firestore 및 OpenAI API 접근의 세부 구현 | 요청 검증과 UI 처리 |

main.py에는 앱 조립과 전역 설정만 둔다. Data CRUD, 요약 계산, 대화 처리, GPT 호출은 router와 service에 분리하며 main.py에 집중시키지 않는다.

## 4. 디렉터리 구조

### Backend

    backend/
    ├─ app/
    │  ├─ main.py
    │  ├─ core/ (config.py, exceptions.py)
    │  ├─ routers/ (data.py, conversations.py, chat.py)
    │  ├─ services/ (data_service.py, conversation_service.py, chat_service.py)
    │  ├─ schemas/ (data.py, conversation.py, chat.py)
    │  ├─ repositories/ (data_repository.py, conversation_repository.py)
    │  └─ clients/ (firestore_client.py, openai_client.py)
    ├─ scripts/seed_data.py
    └─ tests/test_api.py

### Frontend

    frontend/
    ├─ index.html
    ├─ css/styles.css
    └─ js/app.js

이는 설계 결정인 초기 구조안이다. 파일명 또는 보조 모듈은 구현 중 최소 범위에서 조정할 수 있으나, router/service/schema 역할 분리는 유지한다.

## 5. 데이터 모델과 Firestore 구조

### 5.1 Fact

- 필수 컬렉션은 data와 conversations이다.
- 시계열 데이터의 기본 필드는 date, value, memo이다.
- 데이터는 최소 100개 포인트가 필요하다.

### 5.2 설계 결정: data 문서 초안

| 필드 | 형식 | 설명 |
| --- | --- | --- |
| date | 날짜 또는 ISO 8601 문자열 | 시계열 기준일 |
| value | 숫자 | 분석 대상 수치 |
| memo | 문자열 | 데이터 메모 |

Firestore 문서 ID 생성 방식, timestamp 필드 추가 여부 및 date의 엄격한 저장 형식은 미결정 사항이다.

### 5.3 설계 결정: conversations 문서 및 messages schema 초안

| 필드 | 형식 | 설명 |
| --- | --- | --- |
| title | 문자열 | 대화 목록 표시에 사용할 제목 |
| messages | 배열 | 사용자와 AI의 메시지 목록 |
| created_at | 시간 | 생성 시각 |
| updated_at | 시간 | 마지막 변경 시각 |

메시지 항목 초안은 role, content, created_at으로 구성한다. role의 허용값, 제목 생성 방식, timestamp 생성 주체, 메시지 크기 제한 및 목록 정렬 방식은 ARCHITECTURE 구현 전 확정할 미결정 사항이다.

## 6. API와 데이터 흐름

### 6.1 /api/data CRUD 흐름

1. Frontend가 POST, GET, PUT, DELETE 요청을 보낸다.
2. data router가 Pydantic schema로 입력을 검증한다.
3. data service가 CRUD 규칙을 수행한다.
4. data repository가 Firestore data 컬렉션을 읽거나 변경한다.
5. router가 검증된 응답 schema를 반환한다.

### 6.2 /api/data/summary 흐름

1. Frontend 또는 chat service가 summary endpoint 또는 data service를 호출한다.
2. data service가 data 컬렉션의 시계열 데이터를 조회한다.
3. 기간, 개수, 평균, 최대, 최소, 최근 추세를 계산한다.
4. summary schema에 맞춰 결과를 반환한다.

최근 추세의 계산 방식, 빈 데이터 처리, 반올림 규칙 및 date 정렬 규칙은 미결정 사항이다.

### 6.3 /api/conversations 흐름

1. Frontend는 대화를 생성하고 목록을 조회하며 삭제한다.
2. 특정 대화 불러오기는 GET /api/conversations/{id}로 조회한다.
3. conversation router가 요청을 service로 전달한다.
4. conversation service가 conversation repository를 통해 Firestore conversations 컬렉션을 처리한다.
5. 대화 목록과 단일 대화는 각각 용도에 맞는 응답 schema로 반환한다.

### 6.4 /api/chat 컨텍스트 주입 흐름

1. Frontend가 사용자 질문과 대화 식별에 필요한 정보를 POST /api/chat으로 전송한다.
2. chat router가 chat 요청 schema를 검증한다.
3. chat service가 data service를 통해 최신 데이터 요약을 확보한다.
4. chat service가 데이터 요약을 시스템 프롬프트에 삽입한다.
5. OpenAI client가 GPT API를 호출한다.
6. chat service가 사용자 질문과 AI 답변을 conversations에 자동 저장한다.
7. router가 AI 답변과 필요한 대화 식별 정보를 반환한다.

프롬프트의 정확한 문구, 모델명, 토큰 제한, 대화 컨텍스트의 포함 범위 및 신규 대화 생성 규칙은 미결정 사항이다.

## 7. Pydantic 검증

설계 결정:

- 모든 쓰기 요청은 Pydantic request schema로 검증한다.
- date, value, memo의 필수 여부·형식·범위는 schema에 정의한다.
- path parameter의 id, query parameter, chat 질문과 대화 식별자도 schema 또는 FastAPI 타입으로 검증한다.
- 응답은 response schema로 직렬화하여 내부 저장 구조를 그대로 노출하지 않는다.

value의 허용 범위, memo 최대 길이, 날짜 허용 형식, 빈 문자열 정책과 필수·선택 필드는 미결정 사항이다.

## 8. CORS와 환경 변수

### 8.1 CORS

FastAPI에서 ALLOWED_ORIGINS 환경 변수에 지정된 Frontend origin만 허용하는 CORS 미들웨어를 설정한다. 로컬 개발 origin과 Vercel production origin의 정확한 값은 환경별 설정으로 관리한다.

### 8.2 환경 변수

| 변수 | 용도 | 노출 위치 |
| --- | --- | --- |
| OPENAI_API_KEY | OpenAI GPT API 인증 | Backend 환경 |
| FIREBASE_SERVICE_ACCOUNT_JSON 또는 서비스 계정 키 경로 | Firestore 인증 | Backend 환경 |
| API_BASE_URL | Frontend가 호출할 Backend API 기준 URL | Frontend 빌드/런타임 설정 |
| ALLOWED_ORIGINS | Backend CORS 허용 origin | Backend 환경 |

Secret 값은 코드, 문서, Git에 기록하지 않는다. .env는 로컬 환경용이며 Git에 올리지 않는다.

## 9. 예외 처리 전략

설계 결정:

- 입력 검증 오류는 일관된 4xx 응답으로 반환한다.
- 존재하지 않는 data 또는 conversation은 명확한 not-found 응답으로 반환한다.
- Firestore 및 OpenAI 호출 실패는 내부 상세 Secret을 노출하지 않는 일관된 5xx 또는 외부 의존성 오류 응답으로 처리한다.
- 서버 로그에는 원인 추적에 필요한 안전한 정보를 기록하고, 사용자 응답에는 이해 가능한 오류 메시지를 제공한다.

정확한 상태 코드 표준, 오류 응답 body schema, 재시도 정책과 timeout 값은 미결정 사항이다.

## 10. 배포 구조

### Render Backend

- Render는 FastAPI Backend를 실행한다.
- Render 환경 변수에 OpenAI와 Firebase 자격증명, ALLOWED_ORIGINS를 설정한다.
- 배포 후 Backend URL과 URL/docs의 Swagger 접근을 검증한다.

### Vercel Frontend

- Vercel은 Vanilla HTML/CSS/JavaScript Frontend를 배포한다.
- Frontend의 API_BASE_URL은 Render Backend URL을 가리킨다.
- Backend의 ALLOWED_ORIGINS에는 Vercel Frontend origin을 반영한다.

배포 명령, 서비스 설정 화면의 정확한 값, production URL은 배포 승인 후 결정한다.

## 11. 검증 전략

### IMPLEMENTED / VERIFIED

- IMPLEMENTED: 코드가 작성되고 정적 확인 또는 테스트 준비가 된 상태다.
- VERIFIED: 실제 실행, API 요청, UI 연결 또는 배포 URL 확인으로 정상 동작이 확인된 상태다.

### PRE_PUSH VERIFY

PRE_PUSH VERIFIED는 승인 2 직전의 로컬·구조·자동 검증 완료 상태다. production 배포 전 단계이므로 Render/Vercel 실제 URL은 포함하지 않는다.

다음 항목을 확인한다.

- 프로젝트 구조
- Python 실행, 문법, import
- FastAPI 실행
- API route와 Swagger
- Data CRUD, Summary, Conversation 로직
- Chat 컨텍스트 주입 로직
- Frontend 구조와 Backend 연결 로직
- 테스트
- Secret 노출 여부
- README 초안
- 제출 증빙 준비 상태

외부 자격증명이 없으면 실제 Firestore 또는 GPT 연동 검증만 BLOCKED로 기록한다. mock, unit test, 구조 검증, 로컬에서 가능한 구현과 검증은 계속 수행한다.

### POST_DEPLOY VERIFY

POST_DEPLOY VERIFY는 승인 3 후 production 배포를 대상으로 수행하는 최종 검증이다. 최종 완료 판정은 이 단계 이후에만 한다.

다음 항목을 확인한다.

- Render 실제 URL과 URL/docs Swagger
- Vercel 실제 URL
- Vercel과 Render의 실제 연결
- 실제 Firestore 저장·조회
- 실제 GPT 응답
- 실제 production 사용자 흐름
- 최종 README URL
- 제출 증빙

### 자동 검증과 사람 확인

구조, 문법, route, API 요청, 로컬 서버, 테스트, Secret 탐지는 가능한 범위에서 자동 검증한다. 화면 UX, 실제 답변의 유용성, 스크린샷 적절성, production 배포 승인과 최종 제출 적합성은 사람이 확인한다. 검증 항목의 상태 관리는 CHECKLIST.md에서 수행한다.

## 12. 미결정 사항

- 시계열 데이터 주제
- Firestore document 상세 필드와 인덱스
- conversation 제목, 메시지 schema 및 목록 정렬 정책
- OpenAI 모델, 프롬프트 문구, 토큰·재시도 정책
- 데이터 요약의 최근 추세 계산 방식
- API 상세 요청·응답 및 오류 body
- 화면 디자인

이 항목들은 Fact가 아니며, 구현 전에 필요한 범위만 설계 결정으로 확정한다.

## 13. 구현을 위한 설계 결정

다음은 승인 1 이후 과제 범위를 바꾸지 않는 세부사항으로 확정한다.

### 13.1 데이터와 요약

- 데이터 주제는 특정 산업에 종속되지 않는 일별 시계열 수치 데이터로 한다.
- date는 YYYY-MM-DD 형식의 문자열, value는 실수, memo는 선택 문자열로 검증한다.
- 최소 100개 조건은 Backend seed endpoint가 아니라 개발용 seed 스크립트로 준비한다. 운영 API에 과제 범위 밖의 데이터를 임의 생성하는 기능을 추가하지 않는다.
- 기간은 가장 이른 date와 가장 늦은 date로 표시한다.
- 최근 추세는 date 오름차순 마지막 7개 데이터의 첫 value와 마지막 value를 비교해 상승, 하락, 보합으로 계산한다. 7개 미만이면 전체 데이터를 사용한다.

### 13.2 Firestore와 대화

- data와 conversations의 document id는 Firestore 자동 ID를 사용한다.
- conversation 메시지는 role(user 또는 assistant), content, created_at 필드를 가진다.
- created_at과 updated_at은 서버의 UTC ISO 8601 문자열로 기록한다.
- 대화 제목은 첫 사용자 질문의 앞 40자를 사용하며, 신규 대화에서 질문이 없으면 기본 제목은 새 대화로 한다.
- 목록은 updated_at 내림차순으로 반환한다.

### 13.3 API 형식과 오류

- 생성 성공은 201, 조회·수정·삭제 성공은 200을 사용한다.
- 오류 body는 detail 필드를 가진 JSON으로 통일한다.
- Chat은 선택 conversation_id가 없으면 새 대화를 생성하고, 있으면 해당 대화에 메시지를 추가한다.

### 13.4 외부 서비스와 화면

- OpenAI 모델은 환경 변수 OPENAI_MODEL로 지정하며, 기본값은 gpt-4o-mini로 한다.
- Chat 요청은 temperature 0.2, 최대 출력 토큰 500을 기본값으로 한다.
- OpenAI 또는 Firestore 자격증명이 없는 로컬 개발에서는 명시적 mock mode를 제공한다. mock mode는 실제 연동을 대체하는 개발용 검증 수단이며 실제 연동 VERIFIED를 의미하지 않는다.
- 화면은 하나의 페이지에서 요약, 데이터 관리, 대화 목록, 채팅 영역을 제공하는 단순한 반응형 배치로 한다.

### 13.5 구현 동기화

- `main.py`는 설정·repository/service 조립, CORS와 router 등록만 담당한다.
- `USE_MOCK_SERVICES=true`이면 in-memory MockRepository를 사용한다. false이면 `FIREBASE_SERVICE_ACCOUNT_JSON`의 JSON 문자열 또는 파일 경로로 FirestoreRepository를 초기화하며, Firebase와 OpenAI 키가 모두 없으면 의도적으로 시작을 거부한다.
- OpenAI client는 system/user 메시지를 분리해 요청한다. system prompt에는 최신 summary(기간, 개수, 평균, 최대, 최소, 최근 추세)를 주입한다.
- `seed_data.py`는 import 시 실행되지 않으며, 명시 실행 때에만 100개 이상 데이터를 생성한다.
