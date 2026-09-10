# PRODUCT

## 1. 프로젝트 개요

- **프로젝트명:** AI Data Assistant
- **프로젝트 유형:** AI Agent 개발 과제
- **핵심 목표:** 시계열 데이터를 분석·저장하고, 해당 데이터를 컨텍스트로 활용해 맞춤형 답변을 제공하는 AI 웹 서비스

본 문서는 ASSIGNMENT.md와 AI_DEVELOPMENT_PRINCIPLES.md를 기준으로 작성한 과제용 제품 요구사항 문서다.

## 2. 최종 결과물

다음 네 가지를 필수 결과물로 정의한다.

1. 데이터 기반 AI 채팅
2. 데이터 CRUD
3. 대화 기록 저장·조회·불러오기
4. Render/Vercel 배포 및 README 문서화

## 3. 필수 기술 제약

- Python 3.10+
- FastAPI
- Firestore
- OpenAI GPT API
- Vanilla HTML/CSS/JavaScript
- Render
- Vercel

과제에서 지정한 기술을 임의로 변경하지 않는다.

## 4. 데이터 요구사항

- 시계열 데이터를 사용한다.
- 최소 100개 데이터 포인트를 제공한다.
- 각 데이터의 기본 구조는 date, value, memo이다.
- 데이터로부터 기간, 개수, 평균, 최대, 최소, 최근 추세를 포함한 요약 정보를 생성한다.

## 5. 필수 Backend API

### 5.1 Data

- POST /api/data
- GET /api/data
- PUT /api/data/{id}
- DELETE /api/data/{id}
- GET /api/data/summary

### 5.2 Conversation

- POST /api/conversations
- GET /api/conversations
- DELETE /api/conversations/{id}
- 특정 대화 불러오기는 GET /api/conversations/{id} 방식으로 정의한다.

### 5.3 Chat

- POST /api/chat

각 API의 요청·응답 모델, 오류 처리, 저장 흐름은 ARCHITECTURE.md에서 확정한다.

## 6. AI Chat 동작 흐름

1. 사용자가 질문을 입력한다.
2. 시스템이 데이터 요약을 조회한다.
3. 요약 정보를 시스템 프롬프트에 삽입한다.
4. OpenAI GPT API를 호출한다.
5. AI 답변을 사용자에게 반환한다.
6. 대화를 자동 저장한다.

## 7. Firestore 구조

필수 컬렉션:

- data
- conversations

상세 필드, 문서 식별자, conversations 내부 메시지 schema, 인덱스 및 조회 전략은 이 문서에서 확정하지 않는다. 해당 항목은 ARCHITECTURE.md에서 확정해야 한다.

## 8. Frontend 필수 기능

- 채팅 입력
- 메시지 표시
- AI 응답 로딩 표시
- 데이터 추가
- 데이터 목록 표시
- 수정 또는 삭제 중 최소 하나가 UI에서 실제 동작
- 이전 대화 목록
- 대화 불러오기
- 데이터 요약 표시

## 9. 배포 요구사항

### Backend

- Render에 배포한다.
- 배포 URL을 제공한다.
- /docs Swagger에 정상 접속할 수 있어야 한다.

### Frontend

- Vercel에 배포한다.
- 배포 URL을 제공한다.
- Backend API URL을 연결한다.

## 10. README 제출 요구사항

- 서비스 소개
- 기술 스택
- 프론트 배포 URL
- 백엔드 API URL
- Swagger URL
- 로컬 실행법
- 환경 변수
- 제출용 스크린샷

## 11. 제출 증빙

최소 다음 화면 증빙이 필요하다.

- 데이터 요약이 반영된 채팅 질문·답변 화면
- 데이터 관리 동작 화면
- 대화 기록 불러오기 화면
- Swagger UI
- 실제 배포 URL

## 12. 환경 변수

- OPENAI_API_KEY
- FIREBASE_SERVICE_ACCOUNT_JSON 또는 서비스 계정 키 경로
- API_BASE_URL
- ALLOWED_ORIGINS

실제 Secret 값은 문서, 코드, Git 기록에 포함하지 않는다. .env 파일은 Git에 올리지 않는다.

## 13. 완료 조건

IMPLEMENTED와 VERIFIED를 반드시 구분한다.

- **IMPLEMENTED:** 코드가 작성된 상태
- **VERIFIED:** 실제 실행 또는 요청을 통해 정상 동작을 확인한 상태

최종 완료는 최소 다음 항목이 VERIFIED 상태여야 한다.

- FastAPI 로컬 실행
- Swagger
- Data CRUD
- Data Summary
- Conversation API
- Chat API
- Firestore 저장
- GPT Context Injection
- Frontend ↔ Backend 연결
- 대화 불러오기
- Render 배포
- Vercel 배포
- 실제 배포 URL
- README 및 제출 증빙

## 14. Fact / 미결정 사항

### Fact

다음은 과제 원문에서 확인된 요구사항이다.

- 최종 결과물 네 가지
- 지정 기술 스택
- 시계열 데이터 및 최소 100개 데이터 포인트
- 기본 데이터 필드 date, value, memo
- 필수 Data, Conversation, Chat API
- 데이터 요약 기반 GPT 컨텍스트 주입과 자동 대화 저장
- 필수 Firestore 컬렉션 data, conversations
- 필수 프론트엔드 기능, 배포, README, 제출 증빙 및 검증 기준

### 미결정 사항

다음은 Hypothesis로 간주하지 않으며, 이후 명시적으로 결정해야 한다.

- 사용할 시계열 데이터의 주제
- Firestore document 상세 구조
- conversations messages 상세 schema
- OpenAI 모델
- 화면 디자인
- 보너스 과제 수행 여부
- API의 상세 요청·응답 형식과 오류 정책

## 15. 범위 외 기능

보너스 과제는 기본 필수 범위에 포함하지 않는다.

다음 기능은 사용자가 승인하기 전까지 구현하지 않는다.

- Function Calling
- MCP Server
- GPT Actions
- 추가 통계 API
- 그래프
- CSV/JSON Export
- Dark Mode

위 기능은 향후 확장 후보로 기록할 수 있으나, 기본 요구사항 구현 범위에는 포함하지 않는다.
