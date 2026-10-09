# CHECKLIST

## 상태 표기

- `NOT_STARTED`: 아직 시작하지 않음
- `IMPLEMENTED`: 구현되었지만 실제 동작 검증 전
- `VERIFIED`: 자동 실행, 실제 요청 또는 사용자 확인으로 정상 동작 검증
- `BLOCKED`: 외부 권한이나 해결되지 않은 외부 의존성으로 검증 불가
- `N/A`: 과제 범위상 적용되지 않음

각 항목은 `[AUTO]` 또는 `[HUMAN]`으로 검증 주체를 표시한다. 로컬 실제 연동 검증과 Render/Vercel 배포 검증은 구분한다.

## 현재 상태

- [x] [AUTO] [VERIFIED] Python 3.13 가상환경과 의존성 실행
- [x] [AUTO] [VERIFIED] FastAPI production 모드 `/health` 및 Swagger `/docs`
- [x] [AUTO] [VERIFIED] pytest Mock API 테스트 `2 passed`
- [x] [AUTO] [VERIFIED] 실제 Firestore 저장·조회 및 100개 이상 데이터
- [x] [AUTO] [VERIFIED] 실제 Codyssey OpenAI 호환 API 응답
- [x] [AUTO] [VERIFIED] Firestore Summary의 AI Context Injection 및 대화 자동 저장
- [x] [HUMAN] [VERIFIED] 로컬 Frontend ↔ Backend 전체 사용자 흐름
- [x] [AUTO] [VERIFIED] Render/Vercel POST_DEPLOY VERIFY (읽기 흐름 및 실제 AI 응답)
- [ ] [HUMAN] [NOT_STARTED] 제출 스크린샷 준비

## A. 요구사항과 구조

- [x] [AUTO] [VERIFIED] ASSIGNMENT.md와 PRODUCT.md의 필수 기능이 구현 구조에 연결됨
- [x] [AUTO] [VERIFIED] FastAPI, Firestore, OpenAI 호환 API, Vanilla HTML/CSS/JavaScript 기술 스택 유지
- [x] [AUTO] [VERIFIED] Backend와 Frontend 디렉터리 분리
- [x] [AUTO] [VERIFIED] router, schema, service, repository/client 책임 분리
- [x] [HUMAN] [VERIFIED] 보너스 기능을 기본 과제 범위에 추가하지 않음

## B. Backend와 API

- [x] [AUTO] [VERIFIED] Python 문법·import 및 FastAPI 실행
- [x] [AUTO] [VERIFIED] `/health` production/mock 모드 응답
- [x] [AUTO] [VERIFIED] Swagger `/docs` 응답
- [x] [AUTO] [VERIFIED] Pydantic 요청 검증과 404/422 응답
- [x] [AUTO] [VERIFIED] `POST/GET/PUT/DELETE /api/data`
- [x] [AUTO] [VERIFIED] `GET /api/data/summary`
- [x] [AUTO] [VERIFIED] `POST/GET/DELETE /api/conversations`
- [x] [AUTO] [VERIFIED] `GET /api/conversations/{id}`
- [x] [AUTO] [VERIFIED] `POST /api/chat`

## C. Firestore와 데이터

- [x] [AUTO] [VERIFIED] Firebase 자격증명을 환경변수에서 로드
- [x] [AUTO] [VERIFIED] `data` 및 `conversations` 컬렉션 실제 읽기·쓰기
- [x] [AUTO] [VERIFIED] 실제 시계열 데이터 100개 이상 저장
- [x] [AUTO] [VERIFIED] 기간, 개수, 평균, 최소, 최대, 최근 추세 계산
- [x] [HUMAN] [VERIFIED] 로컬 production 모드에서 실제 데이터 추가·삭제
- [x] [HUMAN] [VERIFIED] 화면에 표시된 데이터 요약 확인
- [ ] [AUTO] [NOT_STARTED] 배포된 Render 서비스에서 실제 Firestore CRUD 확인

## D. AI Chat와 대화

- [x] [AUTO] [VERIFIED] Data Summary를 시스템 프롬프트에 주입
- [x] [AUTO] [VERIFIED] Codyssey OpenAI 호환 API 실제 호출과 응답
- [x] [AUTO] [VERIFIED] 질문과 AI 답변을 conversation에 자동 저장
- [x] [AUTO] [VERIFIED] 대화 목록·상세 조회 및 Mock 대화 삭제
- [x] [HUMAN] [VERIFIED] 실제 AI 답변 표시
- [x] [HUMAN] [VERIFIED] 대화 목록과 특정 대화 불러오기
- [x] [HUMAN] [VERIFIED] AI 답변의 기간·개수·평균·최소·최대·최근 추세가 현재 Firestore 데이터와 일치
- [ ] [AUTO] [NOT_STARTED] OpenAI/Codyssey API 실패의 사용자용 오류 응답 최종 검증

## E. Frontend와 HUMAN VERIFY

- [x] [AUTO] [VERIFIED] Vanilla HTML/CSS/JavaScript 구조와 JavaScript 문법
- [x] [AUTO] [VERIFIED] Backend API base URL 선택 로직
- [x] [AUTO] [VERIFIED] 데이터 추가 중복 클릭 방지
- [x] [HUMAN] [VERIFIED] 페이지/CSS
- [x] [HUMAN] [VERIFIED] 데이터 요약
- [x] [HUMAN] [VERIFIED] 데이터 추가
- [x] [HUMAN] [VERIFIED] 데이터 삭제
- [x] [HUMAN] [VERIFIED] 실제 AI 응답
- [x] [HUMAN] [VERIFIED] 대화 목록/불러오기

## F. 보안과 실행 환경

- [x] [AUTO] [VERIFIED] OpenAI/Firebase 자격증명을 환경변수로 주입
- [x] [AUTO] [VERIFIED] `.env`, `apikey.txt`, Firebase 서비스 계정 JSON이 Git 추적 대상에서 제외됨
- [x] [AUTO] [VERIFIED] `.browser_verify_profile/`, `.tmp/`, pytest 캐시가 Git 제외 대상임
- [x] [AUTO] [VERIFIED] `ALLOWED_ORIGINS`에 로컬 frontend origin 허용
- [x] [AUTO] [VERIFIED] `OPENAI_BASE_URL` 끝 공백이 실제 AI 호출을 실패시킬 수 있음을 README에 기록
- [x] [AUTO] [VERIFIED] 잘못된 proxy 환경이 Firestore 연결을 실패시킬 수 있음을 README에 기록

## G. README와 제출 자료

- [x] [AUTO] [VERIFIED] 소개, 문제, 기능, 기술 스택, 구조, 데이터 구조, API 목록 작성
- [x] [AUTO] [VERIFIED] AI Context Injection, 로컬 실행, 환경변수, 검증 결과 작성
- [x] [AUTO] [VERIFIED] 로컬 Frontend/Backend/Swagger URL을 VERIFIED로 기록
- [x] [AUTO] [VERIFIED] Render 후보 URL은 NOT VERIFIED, Vercel URL은 TBD로 기록
- [ ] [HUMAN] [NOT_STARTED] 제출 스크린샷 추가

## H. PRE_PUSH VERIFY

- [x] [AUTO] [VERIFIED] `git status`와 `git diff` 검토
- [x] [AUTO] [VERIFIED] Secret 파일 미추적 확인
- [x] [AUTO] [VERIFIED] Python 18개 파일 AST syntax 확인
- [x] [AUTO] [VERIFIED] pytest `2 passed`
- [x] [AUTO] [VERIFIED] FastAPI `/health` production 응답과 `/docs` HTTP 200
- [x] [AUTO] [VERIFIED] Mock Data CRUD와 Summary
- [x] [AUTO] [VERIFIED] Mock Conversation CRUD
- [x] [AUTO] [VERIFIED] Mock Chat, Context Injection, 자동 저장
- [x] [AUTO] [VERIFIED] frontend JavaScript syntax
- [x] [HUMAN] [VERIFIED] 이번 follow-up commit/push 승인

실제 Firestore와 Codyssey OpenAI 호출은 REAL INTEGRATION VERIFY 및 HUMAN VERIFY에서 통과했으므로 PRE_PUSH에서 반복하지 않는다.

### PRE_PUSH 판정: PASS

로컬 기능, Mock 회귀 테스트, 실제 연동 및 HUMAN VERIFY, 문서와 Secret 제외 상태가 확인되었다.

## H-1. 사전평가 FAIL 최소 보완

- [x] [AUTO] [VERIFIED] #1 실제 Render/Vercel 배포 URL과 Backend/Frontend 읽기 흐름
- [x] [AUTO] [VERIFIED] #2 Swagger `/docs` 및 `/openapi.json` HTTP 200 증거와 path 목록 문서화
- [x] [AUTO] [VERIFIED] #3 실제 Firestore CRUD 및 test marker cleanup 증거 문서화
- [x] [AUTO] [VERIFIED] #5 Conversation CRUD, chat 자동 저장, HUMAN VERIFY 증거 문서화
- [x] [AUTO] [VERIFIED] #7 Router/Service/Repository/Client 책임과 호출 흐름 문서화
- [x] [AUTO] [VERIFIED] #12 Summary 로직 분리 이유와 최근 7개 window 정책 문서화
- [x] [AUTO] [VERIFIED] #15 Render cold start 안내와 `/health` warm-up 후보 문서화
- [x] [AUTO] [VERIFIED] #17 `textContent`, Pydantic 검증, 향후 sanitizer 정책 문서화
- [x] [AUTO] [VERIFIED] Firestore index, validator, frontend 상태, context 장단점, conversation 저장 정책, 배포 환경변수와 CORS 권고 반영
- [x] [AUTO] [VERIFIED] `evidence/pre_push_verify.txt`, `real_integration_verify.txt`, `human_verify.txt` 작성

#1은 실제 Render/Vercel 배포와 production screenshot 없이는 완전 PASS로 처리하지 않는다.

## I. GitHub

- [x] [HUMAN] [VERIFIED] 이번 변경의 commit/push 승인
- [x] [AUTO] [VERIFIED] 필요한 파일만 stage
- [x] [AUTO] [VERIFIED] commit 생성
- [x] [AUTO] [VERIFIED] `origin/main` push
- [x] [AUTO] [VERIFIED] local HEAD와 `origin/main` 일치 확인

## J. POST_DEPLOY VERIFY

- [x] [HUMAN] [VERIFIED] Render/Vercel 신규 배포 승인
- [x] [AUTO] [VERIFIED] Render Backend URL과 `/docs`
- [x] [AUTO] [VERIFIED] Vercel Frontend URL
- [x] [AUTO] [VERIFIED] Vercel Frontend ↔ Render Backend 연결
- [x] [AUTO] [VERIFIED] 배포 환경의 Firestore 읽기 및 실제 AI 응답
- [ ] [HUMAN] [NOT_STARTED] production 사용자 흐름
- [x] [AUTO] [VERIFIED] README 실제 배포 URL 반영
- [ ] [HUMAN] [NOT_STARTED] 제출 스크린샷과 최종 제출 적합성

Render/Vercel 관련 항목은 실제 배포 상태를 확인하기 전까지 VERIFIED로 처리하지 않는다.
