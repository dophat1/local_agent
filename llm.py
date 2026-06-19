from ollama import chat
from ollama import ChatResponse


messages=[
  {
    'role': 'system',
    'content': 'Hey, I am your data science assistant. How can I help you ?'
  },
  {
    'role': 'user',
    'content': 'analyze my csv file'
  }
]

def call_llm(messages):
    response: ChatResponse = chat(model='qwen2.5-coder:14b', messages=messages)
    return response['message']['content']
