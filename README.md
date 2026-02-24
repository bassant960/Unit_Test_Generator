# Unit Test Generator
CLI tool that automatically generates high-quality unit tests for a single Python function using an LLM API (Groq + Llama model).
The tool:
- accepts Python source code
- validates that the file contains **exactly one** top-level function
- sanitizes input to prevent prompt injection
- uses a strict system prompt to force clean pytest output only
- refuses any input that does not match the required scope
## Features 
- Only generates unit tests for exactly one function
- Refuses invalid input with message:  
  `Error: This tool only generates unit tests for functions.`
- Uses LLM API with strict output constraints (no explanation, no markdown, no comments, no extra text)
- Input sanitization (removes comments)
## Requirements
- Python 3.8+
- `openai` library (or compatible LLM API client)
- `python-dotenv` for loading API keys
- Internet connection (to call LLM API)
## Installation
## 1. Clone the repository
git clone https://github.com/bassant960/Unit_Test_Generator.git
cd Unit_Test_Generator

## 2. Create virtual environment 
python -m venv venv
source venv/bin/activate    # Linux / macOS
 or on Windows: venv\Scripts\activate

## 3. Install dependencies
pip install -r requirements.txt

## Setup
1. Create a `.env` file in the project root:

```env
LLM_API_KEY=your_api_key_here
2. Make sure your Python file with the function is ready
Create a .env file in the project root:

LLM_API_KEY=your_api_key_here

Make sure your Python file with the function is ready.

Usage

Generate tests from a Python file:

python main.py test_input.py

Example

Given a file math_funcs.py with:

def add(a, b):
    return a + b

Run:

python main.py math_funcs.py

Output:

import pytest

def test_add_positive_numbers():
    assert add(1, 2) == 3

def test_add_negative_numbers():
    assert add(-1, -2) == -3

def test_add_zero():
    assert add(0, 0) == 0
Notes

Requires an LLM API key.

The file must contain exactly one function, otherwise the tool exits with an error.

Designed to be deterministic: same input produces same output (temperature=0).

