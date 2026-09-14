from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.clients.openai_client import OpenAIChatClient
from app.core.config import get_settings
from app.repositories.firestore import FirestoreRepository
from app.repositories.mock import MockRepository
from app.services.chat_service import ChatService
from app.services.conversation_service import ConversationService
from app.services.data_service import DataService

settings = get_settings()
if settings.use_mock_services:
    repository = MockRepository()
else:
    if not settings.firebase_service_account_json or not settings.openai_api_key:
        raise RuntimeError("Production mode requires Firebase and OpenAI environment variables.")
    repository = FirestoreRepository(settings.firebase_service_account_json)
data_service = DataService(repository)
conversation_service = ConversationService(repository)
chat_client = None if settings.use_mock_services else OpenAIChatClient(
    settings.openai_api_key,
    settings.openai_model,
    settings.openai_base_url,
)
chat_service = ChatService(data_service, conversation_service, chat_client, settings.use_mock_services)
app = FastAPI(title="AI Data Assistant")
app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health(): return {"status": "ok", "mode": "mock" if settings.use_mock_services else "production"}

from app.routers import chat, conversations, data
app.include_router(data.router)
app.include_router(conversations.router)
app.include_router(chat.router)
