# AI Data Assistant

시계열 데이터를 저장·관리하고, 저장된 데이터의 요약 정보를 AI 컨텍스트로 활용하여 질문에 답하는 웹 서비스입니다.

## 주요 기능

- 시계열 데이터 CRUD
  - date
  - value
  - memo
- 데이터 자동 요약
  - 기간
  - 개수
  - 평균
  - 최솟값
  - 최댓값
  - 최근 추세
- 저장된 데이터 요약을 활용한 AI 채팅
- 대화 기록 저장 및 조회
- Firestore 영구 저장
- FastAPI Swagger 문서 제공
- 데이터 추가 중복 클릭 방지

## 기술 스택

- Backend: Python 3.10+, FastAPI
- Database: Firebase Firestore
- AI: Codyssey OpenAI 호환 API
- Frontend: Vanilla HTML / CSS / JavaScript
- Backend 배포 예정: Render
- Frontend 배포 예정: Vercel

## 프로젝트 구조

```text
backend/
  app/
    clients/
    core/
    repositories/
    routers/
    schemas/
    services/
  scripts/
  tests/

frontend/
  css/
  js/
  index.html