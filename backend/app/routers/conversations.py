from fastapi import APIRouter, Depends
from app.schemas.conversation import ConversationCreate, ConversationListItem, ConversationOut
router = APIRouter(prefix="/api/conversations", tags=["conversations"])
def service(): from app.main import conversation_service; return conversation_service
@router.post("", response_model=ConversationOut, status_code=201)
def create(item: ConversationCreate, svc=Depends(service)): return svc.create(item.title)
@router.get("", response_model=list[ConversationListItem])
def list_all(svc=Depends(service)): return svc.list()
@router.get("/{cid}", response_model=ConversationOut)
def read(cid: str, svc=Depends(service)): return svc.get(cid)
@router.delete("/{cid}")
def delete(cid: str, svc=Depends(service)): svc.delete(cid); return {"deleted":True}
