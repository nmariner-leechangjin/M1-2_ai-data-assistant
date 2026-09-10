class ChatService:
    def __init__(self, data_service, conversation_service, chat_client, mock_mode): self.data_service, self.conversation_service, self.chat_client, self.mock_mode = data_service, conversation_service, chat_client, mock_mode
    def chat(self, request):
        cid = request.conversation_id or self.conversation_service.create(request.message[:40])["id"]
        self.conversation_service.get(cid)
        summary = self.data_service.summary()
        prompt = "당신은 시계열 데이터 분석 도우미입니다. 다음 최신 데이터 요약만 근거로 답하세요.\n데이터 요약: " + str(summary)
        answer = "[개발용 Mock 응답] " + prompt + "\n질문: " + request.message if self.mock_mode else self.chat_client.answer(prompt, request.message)
        self.conversation_service.append_messages(cid, request.message, answer)
        return {"conversation_id":cid,"answer":answer,"summary_used":True}
