from app.clients.firestore_client import get_firestore_client
class FirestoreRepository:
    def __init__(self, credential): self.db = get_firestore_client(credential)
    def create_data(self, row):
        ref = self.db.collection("data").document(); ref.set(row); return {"id": ref.id, **row}
    def list_data(self): return [{"id": doc.id, **doc.to_dict()} for doc in self.db.collection("data").stream()]
    def update_data(self, item_id, row):
        ref = self.db.collection("data").document(item_id)
        if not ref.get().exists: return None
        ref.set(row); return {"id": item_id, **row}
    def delete_data(self, item_id):
        ref = self.db.collection("data").document(item_id)
        if not ref.get().exists: return False
        ref.delete(); return True
    def create_conversation(self, row):
        ref = self.db.collection("conversations").document(); ref.set(row); return {"id": ref.id, **row}
    def list_conversations(self): return [{"id": doc.id, **doc.to_dict()} for doc in self.db.collection("conversations").stream()]
    def get_conversation(self, cid):
        doc = self.db.collection("conversations").document(cid).get(); return {"id": doc.id, **doc.to_dict()} if doc.exists else None
    def replace_conversation(self, cid, row): self.db.collection("conversations").document(cid).set(row)
    def delete_conversation(self, cid):
        ref = self.db.collection("conversations").document(cid)
        if not ref.get().exists: return False
        ref.delete(); return True
