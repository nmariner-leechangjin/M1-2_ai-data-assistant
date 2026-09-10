from fastapi import APIRouter, Depends
from app.schemas.chat import ChatIn, ChatOut
router = APIRouter(prefix="/api/chat", tags=["chat"])
def service(): from app.main import chat_service; return chat_service
@router.post("", response_model=ChatOut)
def chat(item: ChatIn, svc=Depends(service)): return svc.chat(item)
