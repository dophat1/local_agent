import pandas as pd 
import sys
from io import StringIO
import duckdb

def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df.to_string()

"""
1. Save real terminal → old_out
2. Replace terminal with fake one → sys.stdout = StringIO()
3. Run code → output goes into fake terminal
4. Restore real terminal → sys.stdout = old_out
5. Read fake terminal contents → output.getvalue()
"""

def python_runner(code):
    old_out = sys.stdout
    output = sys.stdout = StringIO()
    exec(code)
    sys.stdout = old_out
    return output.getvalue()


def sql_query(query):
    result = duckdb.sql(query)
    return str(result)

"""
The agent loop receives this JSON from the LLM:
json
{
    "tool": "csv_reader",
    "input": "data.csv"
}

We need the dictionary to map the input to the tool so the program know which function to call.
"""

tools = {
    "csv_reader": read_csv,
    "python_runner": python_runner,
    "sql_query": sql_query
}