import json
import os
import pathlib
import time
from typing import Dict, Any, List
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq
from prompts import VERIFICATION_PROMPT 
load_dotenv()

# --- CONFIGURATION ---
BATCH_SIZE = 5 

def get_groq_model() -> ChatGroq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError("GROQ_API_KEY not found.")
    
    # Using Llama 3.3 70B for high-quality reasoning
    return ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.0,
        model_kwargs={"response_format": {"type": "json_object"}}
    )

# --- DATA MODELS ---
class VerifiedIssue(BaseModel):
    original_check: str = Field(description="The original check name from the tool.")
    is_vulnerability: bool = Field(description="Is this a real issue (true) or a false positive (false)?")
    true_impact: str = Field(description="Strict severity: 'Critical', 'High', 'Medium', 'Low', 'Informational'.")
    explanation: str = Field(description="Concise explanation of the risk.")
    code_citation: str = Field(description="Exact code snippet/lines proving the bug. Write 'N/A' if false positive.")
    remediation: str = Field(description="Specific fix.")

class BatchAnalysisResult(BaseModel):
    verified_issues: List[VerifiedIssue] = Field(description="List of verified results.")

def create_verification_chain(model: Runnable) -> Runnable:
    parser = JsonOutputParser(pydantic_object=BatchAnalysisResult)
    
    # Use the imported prompt, just inject partial variables
    prompt = VERIFICATION_PROMPT.partial(
        format_instructions=parser.get_format_instructions()
    )
    
    return prompt | model | parser

def read_file_content(file_path: str) -> str:
    try:
        return pathlib.Path(file_path).read_text(encoding="utf-8")
    except Exception:
        return ""

def load_json_file(file_path: str) -> Dict[str, Any]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def run_verification_agent(input_json_path: str, output_json_path: str, source_code_path: str, model: Runnable):
    print(f"Reading source code from: {source_code_path}")
    source_code = read_file_content(source_code_path)
    if not source_code: return

    report_data = load_json_file(input_json_path)
    all_issues = report_data.get("issues", [])
    if not all_issues: return

    verification_chain = create_verification_chain(model)
    final_verified_list = []
    
    print(f"\nStarting BATCH verification of {len(all_issues)} issues...")

    for i in range(0, len(all_issues), BATCH_SIZE):
        batch = all_issues[i : i + BATCH_SIZE]
        try:
            # Minify input to save tokens
            min_batch = [{"check": x.get("check"), "description": x.get("description")} for x in batch]
            
            result = verification_chain.invoke({
                "source_code": source_code,
                "issues_json": json.dumps(min_batch)
            })
            
            results = result.get("verified_issues", [])
            final_verified_list.extend(results)
            print(f"     ✅ Batch {i//BATCH_SIZE + 1} complete.")

        except Exception as e:
            print(f"     ❌ Batch {i//BATCH_SIZE + 1} Failed: {e}")
            # Fallback
            for issue in batch:
                final_verified_list.append({
                    "original_check": issue.get("check"),
                    "is_vulnerability": False,
                    "true_impact": "Error",
                    "explanation": "Batch verification failed.",
                    "code_citation": "N/A",
                    "remediation": "Manual review."
                })

    # Save
    final_report = {
        "contract": os.path.basename(source_code_path),
        "verified_vulnerabilities": final_verified_list
    }
    
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(final_report, f, indent=2)