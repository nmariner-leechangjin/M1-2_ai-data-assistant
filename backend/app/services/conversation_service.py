from datetime import datetime, timezone
from fastapi import HTTPException
def now(): return datetime.now(timezone.utc).isoformat()
class ConversationService:
    def __init__(self, repository): self.repository = repository
    def create(self, title="새 대화"):
        timestamp = now(); return self.repository.create_conversation({"title":title,"messages":[],"created_at":timestamp,"updated_at":timestamp})
    def list(self): return sorted(self.repository.list_conversations(), key=lambda row:row["updated_at"], reverse=True)
    def get(self, cid):
        row = self.repository.get_conversation(cid)
        if not row: raise HTTPException(404, "대화를 찾을 수 없습니다.")
        return row
    def delete(self, cid):
        if not self.repository.delete_conversation(cid): raise HTTPException(404, "대화를 찾을 수 없습니다.")
    def append_messages(self, cid, question, answer):
        row, timestamp = self.get(cid), now()
        row["messages"] += [{"role":"user","content":question,"created_at":timestamp},{"role":"assistant","content":answer,"created_at":timestamp}]
        row["updated_at"] = timestamp; row.pop("id", None); self.repository.replace_conversation(cid, row)
