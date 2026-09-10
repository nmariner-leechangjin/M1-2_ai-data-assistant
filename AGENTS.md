# AGENTS

## 1. 목적과 적용 범위

이 문서는 Codex가 이 프로젝트를 자율 개발할 때 따르는 작업 규칙이다. AI_DEVELOPMENT_PRINCIPLES.md를 최상위 원칙으로 하며, ASSIGNMENT.md, PRODUCT.md, ARCHITECTURE.md, CHECKLIST.md를 함께 따른다.

## 2. 자율 작업 루프

모든 개발 작업은 아래 순서로 수행한다.

PLAN
→ IMPLEMENT
→ VERIFY
→ 실패 시 ANALYZE
→ FIX
→ VERIFY 반복
→ DOCUMENT
→ FINAL VERIFY
→ USER APPROVAL

### 단계별 규칙

- PLAN: 요구사항, 완료 조건, 영향 범위, 미결정 사항을 확인하고 CHECKLIST 항목을 정한다.
- IMPLEMENT: 승인된 범위에서 최소 변경으로 구현한다.
- VERIFY: 실행, 테스트, API 요청, Swagger, UI 연결 등 가능한 검증을 수행한다.
- ANALYZE: 실패 원인을 Fact와 Hypothesis로 나누어 분석한다.
- FIX: 분석으로 뒷받침되는 최소 수정만 적용한다.
- DOCUMENT: README, CHECKLIST 상태, 테스트 결과, 제출 증빙 후보를 함께 갱신한다.
- FINAL VERIFY: 완료 주장 전 관련 항목을 실제로 재검증한다.
- USER APPROVAL: 정의된 승인 지점에서만 사용자에게 다음 권한을 요청한다.

사용자에게 매 단계마다 승인을 요청하지 않는다. 승인 1 이후 승인 2까지는 안전하고 과제 범위 안의 작업을 중간 승인 없이 자율적으로 계속한다.

## 3. 핵심 운영 규칙

- 요구사항과 완료 조건을 구현 전에 확인한다.
- 검증하지 않은 기능을 완료, 성공 또는 VERIFIED라고 표현하지 않는다.
- 오류가 발생하면 가능한 범위에서 원인을 분석하고 수정한 뒤 재검증한다.
- 기존 정상 기능을 수정하기 전 영향 범위를 확인하고, 회귀 검증을 수행한다.
- 요청과 무관한 대규모 리팩터링을 하지 않는다.
- FastAPI, Firestore, OpenAI GPT API, Vanilla HTML/CSS/JavaScript, Render, Vercel 기술 스택을 임의로 변경하지 않는다.
- API 키, Firebase 서비스 계정 키, 환경 변수 Secret을 코드, 문서, 로그, Git에 노출하지 않는다.
- 테스트 가능한 항목은 Codex가 직접 테스트한다.
- README, 테스트 결과, Git 기록, 제출 스크린샷 후보는 개발과 병행한다.
- 확인된 Fact와 추정 Hypothesis를 구분한다. 결정되지 않은 내용은 미결정 사항으로 기록한다.
- 외부 서비스 자격증명 제공, 실제 배포 승인, 제출 판단처럼 사람이 필요한 항목은 상태와 필요한 사용자 조치를 명확히 보고한다.

### 자율 설계 결정 범위

승인 1 이후 과제 요구사항을 변경하지 않는 기술적 세부사항은 사용자에게 불필요한 질문을 하지 않고 Codex가 합리적인 기본값으로 결정할 수 있다.

- Firestore document id 방식
- messages 상세 schema
- timestamp 방식
- API response schema와 오류 body 형식
- 최근 추세 계산 방식
- OpenAI 모델과 token 제한
- 파일 세부 구조
- 화면의 세부 배치

결정 시에는 가장 단순하고 과제 설명이 쉬운 방식, 무료 또는 저비용, 유지보수 용이성, 과제 요구사항 충실도를 우선한다. 결정한 내용은 ARCHITECTURE.md의 설계 결정에 기록한다.

다음 항목은 임의로 결정하지 않는다.

- 과제 필수 기능 삭제
- 지정 기술 스택 변경
- 보너스 과제 추가
- 비용이 크게 발생할 수 있는 선택
- 데이터 삭제
- Git commit/push
- production 배포

## 4. 문서와 구현의 연결

- ASSIGNMENT.md: 과제 원문의 기준
- PRODUCT.md: 제품 범위와 완료 조건
- ARCHITECTURE.md: 구현 구조, 데이터 흐름, 설계 결정
- CHECKLIST.md: 요구사항별 IMPLEMENTED/VERIFIED 상태
- README: 사용법, URL, 환경 변수, 제출 정보

구현 중 설계 결정을 내려야 하면 ARCHITECTURE.md와 CHECKLIST.md를 먼저 갱신하고, PRODUCT.md의 필수 범위를 변경하지 않는다. 요구사항 자체의 변경은 사용자 확인 없이는 하지 않는다.

## 5. 검증 운영

- 자동 검증은 CHECKLIST.md의 [AUTO] 항목에 따라 실행한다.
- UX, 스크린샷 적절성, production 승인처럼 주관적 또는 권한이 필요한 검증은 [HUMAN]으로 남긴다.
- IMPLEMENTED는 코드가 작성된 상태이며 VERIFIED는 실제 동작이 확인된 상태다.
- 실패한 검증은 성공으로 표시하지 않고 BLOCKED 또는 현재 실패 상태와 원인을 기록한다.
- 외부 자격증명이 없어도 전체 개발을 중단하지 않는다. OPENAI_API_KEY, Firebase Service Account, Render/Vercel 계정 권한이 없으면 해당 실제 연동 검증만 BLOCKED로 기록한다.
- 자격증명이 없어도 mock, unit test, 구조 검증, 로컬에서 가능한 구현과 검증은 계속 수행한다.

### PRE_PUSH VERIFY

승인 2는 PRE_PUSH VERIFY 결과를 기준으로 한다. PRE_PUSH VERIFY는 production 배포 전 검증이며, 프로젝트 구조, Python 실행·문법·import, FastAPI 실행, API route, Swagger, CRUD·Summary·Conversation·Chat 컨텍스트 주입 로직, Frontend 구조와 Backend 연결 로직, 테스트, Secret 노출 여부, README 초안, 제출 증빙 준비 상태를 확인한다.

Render/Vercel 실제 URL은 PRE_PUSH VERIFY 또는 승인 2 조건에 포함하지 않는다.

### POST_DEPLOY VERIFY

승인 3 후에는 POST_DEPLOY VERIFY를 실행한다. Render 실제 URL, URL/docs Swagger, Vercel 실제 URL, Vercel과 Render 연결, 실제 Firestore, 실제 GPT 응답, production 사용자 흐름, 최종 README URL 및 제출 증빙을 확인한다.

최종 완료 판정은 POST_DEPLOY VERIFY 이후에만 한다.

## 6. 승인 지점

이 프로젝트의 승인 지점은 정확히 세 개다.

### 승인 1: 기준 문서 승인

다음 문서를 승인한다.

- AI_DEVELOPMENT_PRINCIPLES.md
- ASSIGNMENT.md
- PRODUCT.md
- ARCHITECTURE.md
- AGENTS.md
- CHECKLIST.md

승인 1 전에는 기준 문서 작성·수정 외 기능 구현, 패키지 설치, Git 초기화, commit, push, 배포를 하지 않는다.

### 승인 2: PRE_PUSH VERIFIED 후 Git commit/push 직전

승인 1 이후 승인 2까지 Codex는 과제 범위의 구현, 테스트, 문서화, 로컬 검증을 자율 수행한다. PRE_PUSH VERIFY가 완료되기 전과 승인 2 전에는 Git commit 또는 push를 하지 않는다.

승인 2에서 사용자는 자동 개발 및 검증 결과를 확인하고 Git commit/push 진행 여부를 승인한다.

### 승인 3: GitHub push 이후 production 배포 및 POST_DEPLOY VERIFY 직전

GitHub push 이후 Render/Vercel production 배포 전 사용자의 승인을 받는다. 승인 3 전에는 production Render/Vercel 배포를 실행하지 않는다. 승인 3 후 deployment를 진행하고 POST_DEPLOY VERIFY로 최종 완료를 판정한다.

## 7. 중단 및 보고 기준

다음 상황에서는 진행 상태와 필요한 정보를 명확히 보고한다.

- 요구사항이 서로 충돌하거나 새 요구사항이 기존 범위를 변경하는 경우
- OpenAI 또는 Firebase 자격증명이 필요한 경우
- 권한, 결제, 계정 접근 또는 production 배포 승인이 필요한 경우
- 세 번 이상의 자율 분석·수정 후에도 동일한 외부 의존성 문제로 검증할 수 없는 경우
- 삭제, 대규모 리팩터링, 의존성 변경의 필요성이 발생한 경우

이외의 안전한 구현·테스트·문서화 작업은 승인 1 후 자율적으로 수행한다.
