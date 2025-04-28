import openai
from typing import List
from llm.base import BaseLLM
import asyncio

class ChatGPTLLM(BaseLLM):
    def __init__(self):
        # No arguments here
        pass

    def connect(self, connection_info):
        openai.api_key = connection_info.api_key
        openai.api_base = connection_info.base_url

    async def summarize(self, user_query: str, documents: List[str]) -> str:
        context = "\n\n".join(documents)
        prompt = (
            f"Given the following documents:\n\n{context}\n\n"
            f"Answer the following question in a clear and concise way:\n{user_query}"
        )

        response = await asyncio.to_thread(
            openai.ChatCompletion.create,
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant summarizing search results."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=500,
        )

        return response['choices'][0]['message']['content']
