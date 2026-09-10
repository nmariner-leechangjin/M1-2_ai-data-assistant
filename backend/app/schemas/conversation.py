from pydantic import BaseModel, Field
class MessageOut(BaseModel): role: str; content: str; created_at: str
class ConversationCreate(BaseModel): title: str = Field(default="새 대화", min_length=1, max_length=80)
class ConversationOut(BaseModel): id: str; title: str; messages: list[MessageOut]; created_at: str; updated_at: str
class ConversationListItem(BaseModel): id: str; title: str; created_at: str; updated_at: str
