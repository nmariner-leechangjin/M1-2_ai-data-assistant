# AI Data Assistant

시계열 데이터를 관리하고 요약 정보를 GPT 컨텍스트로 활용하는 FastAPI·Firestore·Vanilla JavaScript 서비스입니다.

## 기술 스택

Python 3.10+, FastAPI, Firestore, OpenAI GPT API, Vanilla HTML/CSS/JavaScript, Render, Vercel

## 로컬 실행

Python 3.10+ 환경에서 가상환경을 만든 뒤 `pip install -r requirements.txt`를 실행하고, `.env.example`을 `.env`로 복사해 설정합니다. 로컬 Mock 검증은 `USE_MOCK_SERVICES=true`로 설정한 뒤 `backend`에서 `uvicorn app.main:app --reload`를 실행합니다. Frontend는 정적 서버로 열고 `window.API_BASE_URL`(기본값 `http://localhost:8000`)이 Backend를 가리키게 합니다. 테스트는 `backend`에서 `pytest -q`로 실행합니다.

USE_MOCK_SERVICES=true는 개발용 API·UI 검증을 위한 Mock 모드이며 실제 Firestore/GPT 연동 검증은 아닙니다.

## 환경 변수

OPENAI_API_KEY, OPENAI_MODEL, FIREBASE_SERVICE_ACCOUNT_JSON, API_BASE_URL, ALLOWED_ORIGINS, USE_MOCK_SERVICES를 사용합니다. Secret 값은 Git에 기록하지 않습니다.

`FIREBASE_SERVICE_ACCOUNT_JSON`에는 서비스 계정 JSON 문자열 또는 해당 JSON 파일 경로를 지정합니다. `USE_MOCK_SERVICES=false`인 production 모드는 Firebase와 OpenAI 환경 변수가 모두 있어야 시작되며, 누락 시 의도적으로 시작을 거부합니다.

## 배포 및 증빙

Render Backend URL, Vercel Frontend URL, Swagger URL 및 제출 스크린샷은 승인 3 후 실제 값으로 기록합니다.
