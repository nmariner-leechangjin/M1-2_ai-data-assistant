# CHECKLIST

## 상태 표기

- NOT_STARTED: 아직 시작하지 않음
- IMPLEMENTED: 코드 또는 문서가 작성되었으나 실제 동작 검증 전
- VERIFIED: 실제 실행 또는 요청으로 정상 동작 확인
- BLOCKED: 외부 자격증명, 승인 또는 해결되지 않은 문제로 진행 불가
- N/A: 과제 범위상 적용되지 않음

각 항목은 [AUTO] 또는 [HUMAN]으로 분류한다. 초기 상태는 모두 NOT_STARTED이며, 기준 문서 작성 완료 자체를 기능 VERIFIED로 간주하지 않는다.

## 현재 구현 상태

- [x] [AUTO] [IMPLEMENTED] requirements.txt, .env.example, .gitignore, Backend·Frontend 기본 구조, README 초안 생성
- [x] [AUTO] [IMPLEMENTED] Mock 기반 Data CRUD, Summary, Conversation, Chat 컨텍스트 주입 및 import-safe 100개 데이터 seed 스크립트 작성
- [x] [AUTO] [VERIFIED] Frontend JavaScript 문법 검사 통과
- [x] [AUTO] [VERIFIED] Python 3.13으로 backend 전체 문법 컴파일 통과
- [ ] [AUTO] [BLOCKED] 의존성 다운로드 불가로 FastAPI import·실행, pytest, Swagger, API 실제 요청 검증 미수행
- [x] [AUTO] [IMPLEMENTED] Firebase 환경변수 기반 Firestore repository/client 구현
- [ ] [AUTO] [BLOCKED] Firebase 자격증명 부재로 실제 Firestore 저장·조회 미검증
- [ ] [AUTO] [BLOCKED] OpenAI 자격증명 부재로 실제 GPT 응답 미검증
- [ ] [HUMAN] [NOT_STARTED] Render/Vercel 계정·production 배포는 승인 3 전 미수행

## A. 요구사항

- [ ] [HUMAN] [NOT_STARTED] ASSIGNMENT.md 과제 원문과 최종 구현 범위 일치
- [ ] [AUTO] [NOT_STARTED] PRODUCT.md 필수 결과물 4개가 CHECKLIST에 연결됨
- [ ] [HUMAN] [NOT_STARTED] 보너스 기능이 기본 필수 범위에 포함되지 않음
- [ ] [HUMAN] [NOT_STARTED] 미결정 사항이 구현 전 설계 결정으로 명확히 처리됨

## B. 프로젝트 구조

- [x] [AUTO] [IMPLEMENTED] Backend와 Frontend 디렉터리가 분리됨
- [x] [AUTO] [IMPLEMENTED] FastAPI main, router, service, schema 역할이 분리됨
- [x] [AUTO] [IMPLEMENTED] main.py에 도메인 비즈니스 로직이 집중되지 않음
- [x] [AUTO] [IMPLEMENTED] 데이터·대화·채팅 모듈이 ARCHITECTURE.md 구조와 일치

## C. Backend

- [ ] [AUTO] [NOT_STARTED] Python 3.10+ 환경에서 FastAPI import 성공
- [ ] [AUTO] [NOT_STARTED] FastAPI 애플리케이션 로컬 실행
- [ ] [AUTO] [NOT_STARTED] Data, Conversation, Chat router 등록
- [ ] [AUTO] [NOT_STARTED] Pydantic 요청·응답 검증 적용
- [ ] [AUTO] [NOT_STARTED] 일관된 예외 처리와 오류 응답 적용
- [ ] [AUTO] [NOT_STARTED] /docs Swagger 응답 확인

## D. Firestore

- [ ] [AUTO] [NOT_STARTED] Firebase 인증 설정이 환경 변수에서만 로드됨
- [ ] [AUTO] [NOT_STARTED] data 컬렉션 읽기·쓰기 확인
- [ ] [AUTO] [NOT_STARTED] conversations 컬렉션 읽기·쓰기 확인
- [ ] [AUTO] [NOT_STARTED] Secret이 코드·로그·응답에 노출되지 않음
- [ ] [HUMAN] [NOT_STARTED] Firestore 프로젝트·권한·서비스 계정 설정 확인

## E. Data CRUD

- [ ] [AUTO] [NOT_STARTED] POST /api/data로 date, value, memo 데이터 생성
- [ ] [AUTO] [NOT_STARTED] GET /api/data로 데이터 목록 조회
- [ ] [AUTO] [NOT_STARTED] PUT /api/data/{id}로 데이터 수정
- [ ] [AUTO] [NOT_STARTED] DELETE /api/data/{id}로 데이터 삭제
- [ ] [AUTO] [NOT_STARTED] 잘못된 입력과 존재하지 않는 id의 오류 응답 확인
- [ ] [AUTO] [NOT_STARTED] 시계열 데이터 포인트 최소 100개 조건 확인

## F. Data Summary

- [ ] [AUTO] [NOT_STARTED] GET /api/data/summary endpoint 존재
- [ ] [AUTO] [NOT_STARTED] 기간 요약 반환
- [ ] [AUTO] [NOT_STARTED] 개수, 평균, 최대, 최소 요약 반환
- [ ] [AUTO] [NOT_STARTED] 최근 추세 요약 반환
- [ ] [AUTO] [NOT_STARTED] 빈 데이터 및 정렬 경계 조건 검증

## G. Conversation

- [ ] [AUTO] [NOT_STARTED] POST /api/conversations로 대화 생성
- [ ] [AUTO] [NOT_STARTED] GET /api/conversations로 이전 대화 목록 조회
- [ ] [AUTO] [NOT_STARTED] GET /api/conversations/{id}로 특정 대화 불러오기
- [ ] [AUTO] [NOT_STARTED] DELETE /api/conversations/{id}로 대화 삭제
- [ ] [AUTO] [NOT_STARTED] messages schema 저장·조회 일관성 확인

## H. AI Chat

- [ ] [AUTO] [NOT_STARTED] POST /api/chat endpoint 존재
- [ ] [AUTO] [NOT_STARTED] 사용자 질문 Pydantic 검증
- [ ] [AUTO] [NOT_STARTED] Data Summary 조회 후 시스템 프롬프트에 컨텍스트 주입
- [x] [AUTO] [IMPLEMENTED] OpenAI GPT API 호출과 응답 반환
- [x] [AUTO] [IMPLEMENTED] 사용자 질문과 AI 답변 자동 저장
- [ ] [AUTO] [NOT_STARTED] OpenAI 오류 시 Secret 미노출 오류 처리
- [ ] [HUMAN] [NOT_STARTED] 데이터 기반 답변의 유용성과 맥락 적절성 확인

## I. Frontend

- [ ] [AUTO] [NOT_STARTED] Vanilla HTML/CSS/JavaScript로 구성
- [ ] [AUTO] [NOT_STARTED] 채팅 입력과 메시지 표시
- [ ] [AUTO] [NOT_STARTED] AI 응답 로딩 표시
- [ ] [AUTO] [NOT_STARTED] 데이터 추가와 데이터 목록 표시
- [x] [AUTO] [IMPLEMENTED] 데이터 삭제 UI와 채팅 로딩 표시 구현
- [ ] [AUTO] [NOT_STARTED] 이전 대화 목록 표시
- [ ] [AUTO] [NOT_STARTED] 특정 대화 불러오기
- [ ] [AUTO] [NOT_STARTED] 데이터 요약 표시
- [ ] [AUTO] [NOT_STARTED] Frontend에서 Backend API URL 연결
- [ ] [HUMAN] [NOT_STARTED] 화면 UX와 오류 안내의 적절성 확인

## J. Security / Environment

- [ ] [AUTO] [NOT_STARTED] OPENAI_API_KEY 환경 변수 사용
- [ ] [AUTO] [NOT_STARTED] FIREBASE_SERVICE_ACCOUNT_JSON 또는 서비스 계정 키 경로 사용
- [ ] [AUTO] [NOT_STARTED] API_BASE_URL 설정 사용
- [ ] [AUTO] [NOT_STARTED] ALLOWED_ORIGINS 기반 CORS 설정
- [ ] [AUTO] [NOT_STARTED] .env가 Git 추적 대상에서 제외됨
- [ ] [AUTO] [NOT_STARTED] API 키와 Firebase 키의 하드코딩 부재 확인

## K. Local Verification

- [ ] [AUTO] [NOT_STARTED] Python 문법·import·테스트 통과
- [ ] [AUTO] [NOT_STARTED] FastAPI 로컬 서버 실행
- [ ] [AUTO] [NOT_STARTED] Swagger UI 정상 접속
- [ ] [AUTO] [NOT_STARTED] Data CRUD API 실제 요청 검증
- [ ] [AUTO] [NOT_STARTED] Data Summary 실제 요청 검증
- [ ] [AUTO] [NOT_STARTED] Conversation API 실제 요청 검증
- [ ] [AUTO] [NOT_STARTED] Chat API 실제 요청 검증
- [ ] [AUTO] [NOT_STARTED] Firestore 저장 결과 검증
- [ ] [AUTO] [NOT_STARTED] Frontend ↔ Backend 연결 검증

## L. README

- [ ] [AUTO] [NOT_STARTED] 서비스 소개 작성
- [ ] [AUTO] [NOT_STARTED] 기술 스택 작성
- [ ] [AUTO] [NOT_STARTED] 로컬 실행법 작성
- [ ] [AUTO] [NOT_STARTED] 환경 변수 설명 작성, Secret 값 미포함
- [ ] [AUTO] [NOT_STARTED] 프론트 배포 URL, 백엔드 API URL, Swagger URL 기록
- [ ] [AUTO] [NOT_STARTED] 제출용 스크린샷 포함

## M. 제출 증빙

- [ ] [HUMAN] [NOT_STARTED] 데이터 요약이 반영된 채팅 질문·답변 화면 캡처
- [ ] [HUMAN] [NOT_STARTED] 데이터 관리 동작 화면 캡처
- [ ] [HUMAN] [NOT_STARTED] 대화 기록 불러오기 화면 캡처
- [ ] [HUMAN] [NOT_STARTED] Swagger UI 캡처
- [ ] [HUMAN] [NOT_STARTED] 실제 배포 URL 화면 및 접근 확인

## N. Git

- [ ] [AUTO] [NOT_STARTED] 승인 2 전 Git commit/push 미수행
- [ ] [HUMAN] [NOT_STARTED] 승인 2에서 commit/push 진행 승인
- [ ] [AUTO] [NOT_STARTED] 승인된 경우에만 Git commit 수행
- [ ] [AUTO] [NOT_STARTED] 승인된 경우에만 GitHub push 수행

## O. PRE_PUSH VERIFY

- [x] [AUTO] [VERIFIED] 프로젝트 구조가 ARCHITECTURE.md와 일치
- [x] [AUTO] [VERIFIED] Python 문법 컴파일 및 Frontend JavaScript 문법 확인
- [ ] [AUTO] [BLOCKED] FastAPI 의존성 미설치로 import·로컬 실행, API route, Swagger 확인 불가
- [x] [AUTO] [IMPLEMENTED] CRUD, Summary, Conversation 로직 확인용 pytest 작성
- [x] [AUTO] [IMPLEMENTED] Chat 시스템 프롬프트 context injection 및 pytest 작성
- [x] [AUTO] [IMPLEMENTED] Frontend 구조와 Backend 연결 로직 확인
- [ ] [AUTO] [BLOCKED] pytest 의존성 미설치로 테스트 실행 결과 확인 불가
- [x] [AUTO] [VERIFIED] Secret 패턴 탐지 및 .gitignore 설정 확인
- [x] [AUTO] [VERIFIED] README 초안 준비
- [ ] [HUMAN] [NOT_STARTED] 제출 증빙 후보 준비 상태 확인
- [ ] [HUMAN] [NOT_STARTED] 승인 2: PRE_PUSH VERIFIED 결과를 기준으로 commit/push 승인

Render/Vercel 실제 URL은 이 단계의 조건이 아니다.

### PRE_PUSH 판정: CONDITIONAL PASS

2026-09-11 기준, 구현·문서·Python 컴파일·JavaScript 문법·Secret 탐지는 완료했다. `pip install -r requirements.txt`가 현재 패키지 인덱스에서 FastAPI를 찾지 못해 FastAPI import/실행, Swagger, pytest 및 실제 Mock API 요청만 BLOCKED다. Firebase/OpenAI 실제 연동은 자격증명 부재로 BLOCKED이며 production 배포는 승인 3 전이므로 수행하지 않았다.

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
