# CHECKLIST

## 상태 표기

- NOT_STARTED: 아직 시작하지 않음
- IMPLEMENTED: 코드 또는 문서가 작성되었으나 실제 동작 검증 전
- VERIFIED: 실제 실행 또는 요청으로 정상 동작 확인
- BLOCKED: 외부 자격증명, 승인 또는 해결되지 않은 문제로 진행 불가
- N/A: 과제 범위상 적용되지 않음

각 항목은 [AUTO] 또는 [HUMAN]으로 분류한다. 초기 상태는 모두 NOT_STARTED이며, 기준 문서 작성 완료 자체를 기능 VERIFIED로 간주하지 않는다.

## 현재 구현 상태

- [x] [AUTO] [VERIFIED] requirements.txt 설치 및 Python 가상환경 실행 확인
- [x] [AUTO] [VERIFIED] FastAPI 로컬 서버 실행 확인
- [x] [AUTO] [VERIFIED] Swagger `/docs` 정상 접속 확인
- [x] [AUTO] [VERIFIED] pytest 실행 결과 2 passed
- [x] [AUTO] [VERIFIED] Mock 기반 Data CRUD, Summary, Conversation, Chat 실제 API 요청 검증
- [x] [AUTO] [VERIFIED] Firestore 실제 데이터 저장·조회 확인
- [x] [AUTO] [VERIFIED] Firestore 실제 시계열 데이터 101건 저장 및 Summary 확인
- [x] [AUTO] [VERIFIED] Codyssey OpenAI 호환 API 실제 호출 확인
- [x] [AUTO] [VERIFIED] Firestore Summary를 AI 컨텍스트에 주입한 실제 답변 확인
- [x] [AUTO] [VERIFIED] Conversation 및 user/assistant 메시지 Firestore 자동 저장 확인
- [x] [AUTO] [VERIFIED] Frontend JavaScript 문법 검사 통과
- [x] [AUTO] [VERIFIED] Python 3.13 backend 문법 및 import 검증
- [x] [AUTO] [VERIFIED] Firebase/OpenAI Secret 파일 Git 추적 제외 확인
- [ ] [AUTO] [NOT_STARTED] Frontend 실제 브라우저 ↔ Backend 사용자 흐름 검증
- [ ] [HUMAN] [NOT_STARTED] Render/Vercel production 배포는 승인 3 전 미수행

## A. 요구사항

- [ ] [HUMAN] [NOT_STARTED] ASSIGNMENT.md 과제 원문과 최종 구현 범위 일치 최종 확인
- [x] [AUTO] [IMPLEMENTED] PRODUCT.md 필수 결과물 4개가 구현 구조와 연결됨
- [x] [HUMAN] [VERIFIED] 보너스 기능을 기본 필수 범위에 포함하지 않음
- [x] [AUTO] [IMPLEMENTED] 설계 결정과 구현 구조가 ARCHITECTURE.md에 반영됨

## B. 프로젝트 구조

- [x] [AUTO] [VERIFIED] Backend와 Frontend 디렉터리가 분리됨
- [x] [AUTO] [VERIFIED] FastAPI main, router, service, schema 역할이 분리됨
- [x] [AUTO] [VERIFIED] main.py에 도메인 비즈니스 로직이 집중되지 않음
- [x] [AUTO] [VERIFIED] 데이터·대화·채팅 모듈이 ARCHITECTURE.md 구조와 일치

## C. Backend

- [x] [AUTO] [VERIFIED] Python 3.13 환경에서 FastAPI import 성공
- [x] [AUTO] [VERIFIED] FastAPI 애플리케이션 로컬 실행
- [x] [AUTO] [VERIFIED] Data, Conversation, Chat router 실제 요청 확인
- [x] [AUTO] [VERIFIED] Pydantic 요청 검증 및 422 오류 확인
- [x] [AUTO] [VERIFIED] 존재하지 않는 resource의 404 응답 확인
- [x] [AUTO] [VERIFIED] `/docs` Swagger UI 정상 접속

## D. Firestore

- [x] [AUTO] [VERIFIED] Firebase 인증 설정이 환경 변수에서 로드됨
- [x] [AUTO] [VERIFIED] `data` 컬렉션 실제 쓰기·조회 확인
- [x] [AUTO] [VERIFIED] `conversations` 컬렉션 실제 쓰기·조회 확인
- [x] [AUTO] [VERIFIED] Firebase 서비스 계정 파일이 Git 추적 대상에서 제외됨
- [x] [HUMAN] [VERIFIED] Firebase 프로젝트·Firestore·서비스 계정 설정 완료
- [ ] [AUTO] [NOT_STARTED] Production Firestore에서 Data PUT/DELETE 실제 요청 최종 검증

## E. Data CRUD

- [x] [AUTO] [VERIFIED] POST `/api/data` 실제 요청으로 데이터 생성
- [x] [AUTO] [VERIFIED] GET `/api/data` 실제 요청으로 데이터 목록 조회
- [x] [AUTO] [VERIFIED] PUT `/api/data/{id}` Mock 실제 요청 검증
- [x] [AUTO] [VERIFIED] DELETE `/api/data/{id}` Mock 실제 요청 검증
- [x] [AUTO] [VERIFIED] 잘못된 입력 422 및 존재하지 않는 id 오류 확인
- [x] [AUTO] [VERIFIED] 실제 Firestore 시계열 데이터 101건으로 최소 100개 조건 확인
- [ ] [AUTO] [NOT_STARTED] Production Firestore PUT/DELETE 실제 요청 최종 확인

## F. Data Summary

- [x] [AUTO] [VERIFIED] GET `/api/data/summary` 실제 요청 확인
- [x] [AUTO] [VERIFIED] 기간 요약 반환 확인
- [x] [AUTO] [VERIFIED] 개수·평균·최대·최소 요약 반환 확인
- [x] [AUTO] [VERIFIED] 최근 추세 반환 확인
- [ ] [AUTO] [NOT_STARTED] 빈 데이터 경계 조건 최종 검증

실제 Firestore Summary 검증 예:
- count: 101
- average: 151.2
- minimum: 100
- maximum: 321.5
- recent_trend: 상승

## G. Conversation

- [x] [AUTO] [VERIFIED] POST `/api/conversations` 실제 요청 확인
- [x] [AUTO] [VERIFIED] GET `/api/conversations` 실제 요청 확인
- [x] [AUTO] [VERIFIED] GET `/api/conversations/{id}` 실제 요청 확인
- [x] [AUTO] [VERIFIED] DELETE `/api/conversations/{id}` Mock 실제 요청 확인
- [x] [AUTO] [VERIFIED] user/assistant messages schema 저장·조회 일관성 확인
- [ ] [AUTO] [NOT_STARTED] Production Firestore Conversation DELETE 실제 요청 최종 확인

## H. AI Chat

- [x] [AUTO] [VERIFIED] POST `/api/chat` 실제 요청 확인
- [x] [AUTO] [VERIFIED] 사용자 질문 Pydantic 처리 확인
- [x] [AUTO] [VERIFIED] Data Summary 조회 후 시스템 프롬프트 컨텍스트 주입
- [x] [AUTO] [VERIFIED] Codyssey OpenAI 호환 API 실제 호출 및 응답 확인
- [x] [AUTO] [VERIFIED] 사용자 질문과 AI 답변 Firestore 자동 저장
- [x] [AUTO] [VERIFIED] 101건 Summary를 반영한 실제 AI 답변 확인
- [ ] [AUTO] [NOT_STARTED] OpenAI/Codyssey API 오류의 사용자용 예외 처리 최종 검증
- [x] [HUMAN] [VERIFIED] 데이터 기반 답변이 실제 Summary 수치와 일치함을 확인

## I. Frontend

- [x] [AUTO] [VERIFIED] Vanilla HTML/CSS/JavaScript 구조 확인
- [x] [AUTO] [VERIFIED] 채팅 입력과 메시지 표시 실제 브라우저 확인
- [x] [AUTO] [VERIFIED] AI 응답 로딩 표시 실제 브라우저 확인
- [x] [AUTO] [VERIFIED] 데이터 추가와 데이터 목록 표시 실제 브라우저 확인
- [x] [AUTO] [VERIFIED] 데이터 삭제 UI 구현 확인
- [x] [AUTO] [VERIFIED] 이전 대화 목록 표시 실제 브라우저 확인
- [x] [AUTO] [VERIFIED] 특정 대화 불러오기 실제 브라우저 확인
- [x] [AUTO] [VERIFIED] 데이터 요약 표시 실제 브라우저 확인
- [x] [AUTO] [VERIFIED] Frontend ↔ Backend API 연결 확인
- [x] [AUTO] [VERIFIED] Frontend JavaScript 문법 검사 통과
- [x] [AUTO] [VERIFIED] 데이터 추가 버튼 중복 클릭 방지 확인
- [x] [HUMAN] [VERIFIED] 실제 브라우저 전체 사용자 흐름 확인
- [ ] [HUMAN] [NOT_STARTED] 화면 UX와 오류 안내 최종 점검

## J. Security / Environment

- [x] [AUTO] [VERIFIED] OPENAI_API_KEY 환경 변수 사용
- [x] [AUTO] [VERIFIED] OPENAI_BASE_URL 환경 변수 사용
- [x] [AUTO] [VERIFIED] OPENAI_MODEL 환경 변수 사용
- [x] [AUTO] [VERIFIED] FIREBASE_SERVICE_ACCOUNT_JSON 환경 변수 사용
- [x] [AUTO] [IMPLEMENTED] API_BASE_URL 설정 사용
- [x] [AUTO] [VERIFIED] ALLOWED_ORIGINS 기반 CORS 설정
- [x] [AUTO] [VERIFIED] `.env`가 Git 추적 대상에서 제외됨
- [x] [AUTO] [VERIFIED] `apikey.txt` Git 추적 제외 확인
- [x] [AUTO] [VERIFIED] Firebase Admin SDK JSON Git 추적 제외 확인
- [x] [AUTO] [VERIFIED] `git ls-files`에서 Secret 파일 미추적 확인

## K. Local Verification

- [x] [AUTO] [VERIFIED] Python 문법·import·pytest 통과
- [x] [AUTO] [VERIFIED] FastAPI 로컬 서버 실행
- [x] [AUTO] [VERIFIED] Swagger UI 정상 접속
- [x] [AUTO] [VERIFIED] Data CRUD 실제 요청 검증
- [x] [AUTO] [VERIFIED] Data Summary 실제 Firestore 요청 검증
- [x] [AUTO] [VERIFIED] Conversation API 실제 요청 검증
- [x] [AUTO] [VERIFIED] Chat API 실제 Codyssey AI 요청 검증
- [x] [AUTO] [VERIFIED] Firestore 실제 저장 결과 검증
- [x] [AUTO] [VERIFIED] pytest 결과 `2 passed`
- [x] [AUTO] [VERIFIED] Frontend ↔ Backend 실제 브라우저 연결 검증
- [x] [HUMAN] [VERIFIED] 데이터 추가 → 요약 갱신 → AI 채팅 → 이전 대화 불러오기 사용자 흐름 확인

## L. README

- [x] [AUTO] [IMPLEMENTED] 서비스 소개 작성
- [x] [AUTO] [IMPLEMENTED] 기술 스택 작성
- [x] [AUTO] [IMPLEMENTED] 로컬 실행법 작성
- [x] [AUTO] [IMPLEMENTED] 환경 변수 설명 및 Secret 값 미포함
- [ ] [AUTO] [NOT_STARTED] README에 최신 실제 검증 결과 반영
- [ ] [AUTO] [NOT_STARTED] Frontend/Backend/Swagger production URL 기록
- [ ] [HUMAN] [NOT_STARTED] 제출용 스크린샷 포함

## M. 제출 증빙

- [ ] [HUMAN] [NOT_STARTED] 데이터 요약이 반영된 채팅 질문·답변 화면 캡처
- [ ] [HUMAN] [NOT_STARTED] 데이터 관리 동작 화면 캡처
- [ ] [HUMAN] [NOT_STARTED] 대화 기록 불러오기 화면 캡처
- [ ] [HUMAN] [NOT_STARTED] Swagger UI 캡처
- [ ] [HUMAN] [NOT_STARTED] 실제 배포 URL 화면 및 접근 확인

## N. Git

- [x] [HUMAN] [VERIFIED] 최초 승인 2 후 commit/push 수행
- [x] [AUTO] [VERIFIED] 최초 commit `eef0c6060a4b179ab2e043a3721074f3d2cde866`
- [x] [AUTO] [VERIFIED] GitHub main과 최초 commit hash 일치 확인
- [ ] [HUMAN] [NOT_STARTED] 현재 추가 수정분 follow-up commit/push 승인
- [ ] [AUTO] [NOT_STARTED] 승인 후 현재 수정분 commit
- [ ] [AUTO] [NOT_STARTED] 승인 후 GitHub push

## O. PRE_PUSH VERIFY

- [x] [AUTO] [VERIFIED] 프로젝트 구조 확인
- [x] [AUTO] [VERIFIED] Python 실행 및 pytest `2 passed`
- [x] [AUTO] [VERIFIED] FastAPI 로컬 실행
- [x] [AUTO] [VERIFIED] Swagger `/docs` 확인
- [x] [AUTO] [VERIFIED] 실제 Firestore 연결 및 101건 데이터 확인
- [x] [AUTO] [VERIFIED] 실제 Codyssey OpenAI 호환 API 응답 확인
- [x] [AUTO] [VERIFIED] 실제 Conversation Firestore 저장 확인
- [x] [AUTO] [VERIFIED] Secret 파일 `.gitignore` 및 `git ls-files` 검증
- [x] [AUTO] [VERIFIED] Seed 스크립트가 실제 API를 통해 100건 저장함을 확인
- [x] [AUTO] [VERIFIED] Frontend 실제 브라우저 ↔ Backend 연결 검증
- [ ] [AUTO] [NOT_STARTED] README/CHECKLIST 최신 상태 반영 완료 확인
- [ ] [HUMAN] [NOT_STARTED] follow-up commit/push 승인

### PRE_PUSH 판정: LOCAL FUNCTIONAL PASS

Backend 핵심 기능, 실제 Firestore 연동, Codyssey OpenAI 호환 API, Conversation 저장, Frontend ↔ Backend 브라우저 사용자 흐름까지 로컬에서 검증했다.

현재 남은 작업은 README/CHECKLIST 최종 동기화, 최종 pytest/git 상태 확인, follow-up commit/push 승인, production Render/Vercel 배포 검증이다.

## P. POST_DEPLOY VERIFY

- [ ] [HUMAN] [NOT_STARTED] 승인 3에서 Render production 배포 승인
- [ ] [AUTO] [NOT_STARTED] Render Backend 환경 변수 설정 확인
- [ ] [AUTO] [NOT_STARTED] Render Backend 배포 URL 응답 확인
- [ ] [AUTO] [NOT_STARTED] Render URL/docs Swagger 정상 접속
- [ ] [HUMAN] [NOT_STARTED] 승인 3에서 Vercel production 배포 승인
- [ ] [AUTO] [NOT_STARTED] Vercel Frontend API_BASE_URL 설정 확인
- [ ] [AUTO] [NOT_STARTED] Vercel Frontend 배포 URL 응답 확인
- [ ] [AUTO] [NOT_STARTED] Vercel Frontend와 Render Backend 연결 확인
- [ ] [AUTO] [NOT_STARTED] 실제 Firestore 저장·조회 확인
- [ ] [AUTO] [NOT_STARTED] 실제 GPT 응답 확인
- [ ] [HUMAN] [NOT_STARTED] 실제 production 사용자 흐름 확인
- [ ] [AUTO] [NOT_STARTED] 최종 README에 실제 URL 반영
- [ ] [HUMAN] [NOT_STARTED] 최종 제출 증빙 확인

외부 자격증명 또는 계정 권한이 없으면 실제 연동 항목만 BLOCKED로 표시하고, mock·unit test·구조 검증·로컬 작업은 계속한다.

## Q. Final Verification

- [ ] [AUTO] [NOT_STARTED] 필수 Backend API와 Firestore 저장이 VERIFIED
- [ ] [AUTO] [NOT_STARTED] GPT Context Injection과 Chat API가 VERIFIED
- [ ] [AUTO] [NOT_STARTED] Frontend ↔ Backend 연결과 대화 불러오기가 VERIFIED
- [ ] [AUTO] [NOT_STARTED] POST_DEPLOY VERIFY의 Render와 Vercel 실제 배포 URL이 VERIFIED
- [ ] [HUMAN] [NOT_STARTED] README와 제출 증빙의 완결성 확인
- [ ] [HUMAN] [NOT_STARTED] 과제 요구사항 충족 최종 확인
