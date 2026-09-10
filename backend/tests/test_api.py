import os
os.environ["USE_MOCK_SERVICES"] = "true"
from fastapi.testclient import TestClient
from app.main import app, repository

client = TestClient(app)
def reset(): repository.data.clear(); repository.conversations.clear()
def test_health_crud_and_summary():
    reset(); assert client.get("/health").json()["mode"] == "mock"
    created = client.post("/api/data", json={"date":"2025-01-01","value":1,"memo":"a"}); assert created.status_code == 201
    item_id = created.json()["id"]
    assert client.put(f"/api/data/{item_id}", json={"date":"2025-01-02","value":2,"memo":"b"}).status_code == 200
    assert client.get("/api/data/summary").json()["average"] == 2
    assert client.delete(f"/api/data/{item_id}").json() == {"deleted": True}
    assert client.put("/api/data/missing", json={"date":"2025-01-01","value":1}).status_code == 404
def test_chat_context_and_conversation():
    reset()
    for day, value in [("2025-01-01", 1), ("2025-01-02", 3)]: assert client.post("/api/data", json={"date":day,"value":value}).status_code == 201
    chat = client.post("/api/chat", json={"message":"추세는?"}); assert chat.status_code == 200
    payload = chat.json(); assert payload["summary_used"] and "상승" in payload["answer"]
    assert len(client.get(f"/api/conversations/{payload['conversation_id']}").json()["messages"]) == 2
    assert client.delete(f"/api/conversations/{payload['conversation_id']}").status_code == 200
