const LOCAL_API_BASE_URL = "http://localhost:8000";
const PRODUCTION_API_BASE_URL = "https://m1-2-ai-data-assistant.onrender.com";
const isLocalhost = ["localhost", "127.0.0.1"].includes(window.location.hostname);

// Static frontend priority: runtime override, local backend, then the configured
// production target. The production target is configured but not locally verified.
const base = window.API_BASE_URL || (isLocalhost ? LOCAL_API_BASE_URL : PRODUCTION_API_BASE_URL);
let currentConversationId = null;
const byId = (id) => document.getElementById(id);

async function api(path, options = {}) {
  const response = await fetch(base + path, { headers: { "Content-Type": "application/json" }, ...options });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.detail || "요청을 처리하지 못했습니다.");
  return body;
}
function addMessage(text, role) {
  const node = document.createElement("div"); node.className = `message ${role}`; node.textContent = text; byId("messages").append(node);
}
function renderRows(rows) {
  const container = byId("rows"); container.replaceChildren();
  rows.forEach((row) => {
    const line = document.createElement("p"); line.textContent = `${row.date} / ${row.value} / ${row.memo || ""} `;
    const remove = document.createElement("button"); remove.type = "button"; remove.textContent = "삭제";
    remove.onclick = async () => { try { await api(`/api/data/${row.id}`, { method: "DELETE" }); await load(); } catch (error) { byId("summary").textContent = error.message; } };
    line.append(remove); container.append(line);
  });
}
function renderConversations(items) {
  const container = byId("conversations"); container.replaceChildren();
  items.forEach((item) => {
    const button = document.createElement("button"); button.type = "button"; button.textContent = item.title;
    button.onclick = () => openConversation(item.id); container.append(button);
  });
}
async function load() {
  const [summary, rows, conversations] = await Promise.all([api("/api/data/summary"), api("/api/data"), api("/api/conversations")]);
  byId("summary").textContent = `기간 ${summary.period_start || "-"} ~ ${summary.period_end || "-"} | ${summary.count}개 | 평균 ${summary.average ?? "-"} | ${summary.recent_trend}`;
  renderRows(rows); renderConversations(conversations);
}
async function openConversation(id) {
  try {
    const conversation = await api(`/api/conversations/${id}`); currentConversationId = conversation.id; byId("messages").replaceChildren();
    conversation.messages.forEach((message) => addMessage(message.content, message.role));
  } catch (error) { addMessage(error.message, "assistant"); }
}
byId("data").onsubmit = async (event) => {
  event.preventDefault();

  const form = event.target;
  const submitButton = form.querySelector('button[type="submit"]');

  if (submitButton?.disabled) return;

  if (submitButton) {
    submitButton.disabled = true;
    submitButton.textContent = "저장 중…";
  }

  try {
    await api("/api/data", {
      method: "POST",
      body: JSON.stringify(Object.fromEntries(new FormData(form))),
    });

    form.reset();
    await load();
  } catch (error) {
    byId("summary").textContent = error.message;
  } finally {
    if (submitButton) {
      submitButton.disabled = false;
      submitButton.textContent = "데이터 추가";
    }
  }
};
byId("chat").onsubmit = async (event) => {
  event.preventDefault(); const input = byId("question"), send = byId("send"), question = input.value.trim(); if (!question) return;
  addMessage(question, "user"); input.value = ""; send.disabled = true; send.textContent = "응답 생성 중…";
  try { const result = await api("/api/chat", { method: "POST", body: JSON.stringify({ message: question, conversation_id: currentConversationId }) }); currentConversationId = result.conversation_id; addMessage(result.answer, "assistant"); await load(); }
  catch (error) { addMessage(error.message, "assistant"); }
  finally { send.disabled = false; send.textContent = "전송"; }
};
load().catch((error) => { byId("summary").textContent = error.message; });
