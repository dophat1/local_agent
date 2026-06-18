import pandas as pd 
import sys
from io import StringIO

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