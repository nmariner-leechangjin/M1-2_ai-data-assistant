from copy import deepcopy
from uuid import uuid4
class MockRepository:
    def __init__(self): self.data, self.conversations = {}, {}
    def create_data(self, row):
        row = {"id": uuid4().hex, **row}; self.data[row["id"]] = row; return deepcopy(row)
    def list_data(self): return deepcopy(list(self.data.values()))
    def update_data(self, item_id, row):
        if item_id not in self.data: return None
        self.data[item_id] = {"id": item_id, **row}; return deepcopy(self.data[item_id])
    def delete_data(self, item_id): return self.data.pop(item_id, None) is not None
    def create_conversation(self, row):
        row = {"id": uuid4().hex, **row}; self.conversations[row["id"]] = row; return deepcopy(row)
    def list_conversations(self): return deepcopy(list(self.conversations.values()))
    def get_conversation(self, cid): return deepcopy(self.conversations.get(cid))
    def replace_conversation(self, cid, row): self.conversations[cid] = {"id": cid, **row}
    def delete_conversation(self, cid): return self.conversations.pop(cid, None) is not None
