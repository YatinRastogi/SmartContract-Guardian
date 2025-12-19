import json
import os
import pathlib
from dotenv import load_dotenv
from langchain_core.runnables import Runnable
from langchain_groq import ChatGroq

# --- IMPORT CENTRALIZED PROMPT ---
from prompts import LOGIC_AUDIT_PROMPT

load_dotenv()

def get_groq_model() -> ChatGroq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError("GROQ_API_KEY not found.")
    
    print("Using Model: Groq Llama 3.3 70B (Versatile)")
    return ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.0,
        model_kwargs={"response_format": {"type": "json_object"}}
    )

def read_file_content(file_path: str) -> str:
    try:
        return pathlib.Path(file_path).read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""

def clean_and_parse_json(raw_output: str) -> dict:
    try:
        start = raw_output.find('{')
        end = raw_output.rfind('}')
        if start == -1 or end == -1: return {}
        return json.loads(raw_output[start: end + 1])
    except:
        return {}

def run_logic_audit_agent(output_json_path: str, source_code_path: str, model: Runnable):
    print(f"Reading source code from: {source_code_path}")
    source_code = read_file_content(source_code_path)
    if not source_code: return

    print("\nStarting deep logic analysis (Four Lenses)...")

    # Define Schema here to pass as a variable
    schema_example = """
    {
      "logic_vulnerabilities": [
        {
          "true_impact": "string (e.g., 'Critical', 'High', 'Medium', 'Low', or 'Informational')",
          "title": "string (A short, descriptive title)",
          "explanation": "string (Your concise explanation of the *actual* risk)",
          "remediation": "string (The specific code fix or recommendation)",
          "code_citation": "string (Copy the code snippet exactly)"
        }
      ]
    }
    """

    try:
        # Use imported prompt
        chain = LOGIC_AUDIT_PROMPT | model
        
        response = chain.invoke({
            "source_code": source_code, 
            "schema": schema_example
        })
        
        analysis = clean_and_parse_json(response.content)
        print(f"\n✅ Logic audit complete. Found {len(analysis.get('logic_vulnerabilities', []))} issues.")

    except Exception as e:
        print(f"    -> ERROR: API call failed. Reason: {e}.")
        analysis = {"logic_vulnerabilities": []}

    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2)