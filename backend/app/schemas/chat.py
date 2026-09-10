from pydantic import BaseModel, Field
class ChatIn(BaseModel): message: str = Field(min_length=1, max_length=4000); conversation_id: str | None = None
class ChatOut(BaseModel): conversation_id: str; answer: str; summary_used: bool
