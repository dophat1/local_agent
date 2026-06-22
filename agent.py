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

user_file_path = input("Provide me the file path of your data.")

message = {
    'role':'user', 
    'content': user_prompt
}
messages.append(message)

file_path = {
    'role':'user', 
    'content': user_file_path
}


# Only check if user's input is non empty, read_csv do the rest.
if user_file_path:
    messages.append(file_path)


# A helper function to check json file
def extract_json(text):
    # finds first '{', tracks depth, returns the balanced substring
    depth = 0
    start = -1
    
    for index, letter in enumerate(text):
        if letter == '{':
            depth += 1
            if start == -1:
                start = index
            
        elif letter == '}':
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
            
    
attempts = 0
max_attempts = 5

while True:
    if attempts >= max_attempts:
        print("Max attempts reached, the program will stop")
        break


    llm_output = call_llm(messages)
    messages.append(
        {
            'role':'assistant',
            'content':llm_output
        }
    )

    # Clean the llm output before feed in
    cleaned_output = llm_output.replace('```json', '').replace('```', '').strip()

    json_match = extract_json(cleaned_output)

    if not json_match:
        # No JSON found at all -> this is a genuine final plain-text answer.
        print(cleaned_output)
        break

    try:
        parsed = json.loads(json_match)
    except json.JSONDecodeError:
        # Looked like JSON but wasn't parseable -> treat as final answer.
        print(cleaned_output)
        break

    if not isinstance(parsed, dict) or 'tool' not in parsed:
        # Not actually a tool-call structure -> treat as final answer.
        print(cleaned_output)
        break

    tool_name = parsed['tool']

    if tool_name not in tools:
        messages.append(
            {
                'role': 'user',
                'content': f"You have called the wrong tool '{tool_name}', there are only the following tools that you can call: {list(tools.keys())}"
            }
        )
        attempts += 1
        continue

    tool_function = tools[tool_name]
    result, is_progress = tool_function(parsed['input'])
    messages.append(
        {
            'role': 'user',
            'content': result
        }
    )
    if is_progress:
        attempts = 0
    else:
        attempts += 1 