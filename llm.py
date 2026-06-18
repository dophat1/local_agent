from ollama import chat
from ollama import ChatResponse


messages=[
  {
    'role': 'user',
    'content': 'this is a system prompt',
  },
]

def call_llm(messages):
    response: ChatResponse = chat(model='qwen2.5-coder:14b', messages=messages)
    return response['message']['content']
