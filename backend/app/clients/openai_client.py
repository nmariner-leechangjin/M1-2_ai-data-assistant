from openai import OpenAI
class OpenAIChatClient:
    def __init__(self, api_key, model): self.client, self.model = OpenAI(api_key=api_key), model
    def answer(self, system_prompt, question):
        response = self.client.chat.completions.create(model=self.model, temperature=0.2, max_tokens=500, messages=[{"role":"system", "content":system_prompt}, {"role":"user", "content":question}])
        return response.choices[0].message.content or "응답을 생성하지 못했습니다."
