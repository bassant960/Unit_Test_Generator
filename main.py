import argparse
import sys
import ast
import re
import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
key = os.getenv("LLM_API_KEY")
if not key: #check if llm api key is exist
    print("Error: API key not found.")
    sys.exit(1)
client = OpenAI(
    api_key=key,
    base_url="https://api.groq.com/openai/v1"
    ) 

def SanitizeCode(code: str)-> str:
    code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
    code = re.sub(r'"""(.*?)"""|\'\'\'(.*?)\'\'\'', '', code, flags=re.DOTALL | re.MULTILINE)
    lines = [line for line in code.splitlines() if line.strip()]
    return '\n'.join(lines)

parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()
testfile = args.file
if not os.path.exists(testfile): #check if file exist
    print("Error: File not found.")
    sys.exit(1)
try:  #check if able to read file and read the file
    with open(testfile, "r", encoding="utf-8") as f:
        source_code = f.read()
except Exception:
    print("Error: Unable to read file.")
    sys.exit(1)
try:  #check if there is at least a function 
    tree = ast.parse(source_code)
except SyntaxError:
    print("Error: Invalid Python syntax.")
    sys.exit(1)

function = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
if len(function) != 1:
    print("Error: This tool only generates unit tests for functions.")
    sys.exit(1)

function_name = function[0].name  
sanitized_code = SanitizeCode(source_code)
prompt = f"""
You are a professional pytest-only unit test generator.
Output **ONLY** the test code — nothing else in the world.

Strict rules — break any = invalid output:
- Start immediately with: import pytest
- Use plain assert (NOT unittest, NOT self.assert*)
- 4 to 8 test functions maximum
- Every test MUST have a complete body with at least one assert
- Unique test names: test_add_something_descriptive
- Cover: normal values, negatives, zero, boundaries, floats (use pytest.approx if needed)
- NEVER repeat the same test logic
- NEVER generate empty or incomplete functions
- NO comments, NO markdown, NO ```, NO explanations, NO if __name__
- The function name is: {function_name}

Code to test:
{sanitized_code}
"""
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": sanitized_code}
    ],
    temperature=0.0,
    max_tokens=1500
)

Unit_tests = response.choices[0].message.content.strip()
if Unit_tests.startswith("```"):
    Unit_tests = Unit_tests.split("```", 2)[1].strip() if len(Unit_tests.split("```")) > 2 else Unit_tests

Unit_tests = Unit_tests.split("if __name__")[0].strip()
print(Unit_tests)
                     