import json
from llm import call_llm
from tools import tools

SYSTEM_PROMPT = """
You are an expert Data Scientist. Your goal is to analyze data and answer the user's questions accurately using your available tools.

### AVAILABLE TOOLS
1. `csv_reader`: Use this tool when the user uploads a CSV file to inspect its structure and content.
2. `python_runner`: Use this tool to execute Python code for data manipulation, statistical analysis, or visualization.
3. `sql_query`: Use this tool to execute database queries to retrieve or aggregate structured data.

### INTERACTION PROTOCOL

#### Phase 1: Tool Execution (Structured JSON)
Whenever you need to invoke a tool, you MUST respond strictly with a JSON object. Do not include any conversational filler, markdown formatting outside the JSON, or thoughts. Use the following exact schema:
{
    "tool": "tool_name",
    "input": "exact input arguments or queries required for the tool"
}

#### Phase 2: Final Answer (Plain Text)
Once you have collected enough information from the tool outputs to comprehensively answer the user's question, you must transition out of JSON mode. Respond in clear, professional plain text with your final analysis and answer. Do not use the JSON format for your final response.
"""

messages = []

messages.append(
    {
        'role': 'system',
        'content': SYSTEM_PROMPT
    }
)

user_prompt = input("How can I help you ?")
message = {
    'role':'user', 
    'content': user_prompt
}
messages.append(message)

while True:
    llm_output = call_llm(messages)
    messages.append(
        {
            'role':'assistant',
            'content':llm_output
        }
    )
    try:
        parsed = json.loads(llm_output)
        tool_name = parsed['tool']
        tool_function = tools[tool_name]
        result = tool_function(parsed['input'])
        messages.append(
            {
                'role':'user',
                'content': result
            }
        )
    except json.JSONDecodeError:
        print(llm_output)
        break
    except KeyError:
        messages.append(
            {
                'role':'user',
                'content':f"You have called the wrong in {tool_name}, there are only the following tools that you can call {tools.keys()}"

            }
        )