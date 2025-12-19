import os
import json
from langchain_core.output_parsers import StrOutputParser
from prompts import REFACTORING_PROMPT  # <--- Import the prompt

def load_json_file(file_path):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "verified_vulnerabilities" in data:
                return data["verified_vulnerabilities"]
            elif "logic_vulnerabilities" in data:
                return data["logic_vulnerabilities"]
            return []
    except:
        return []

def run_refactoring_agent(contract_path, slither_report_path, logic_report_path, model): # <--- Model passed in
    print(f"\n[Phase 4] Running Refactoring Agent (Auto-Fixer)...")
    
    try:
        with open(contract_path, "r", encoding="utf-8") as f:
            source_code = f.read()
    except Exception as e:
        print(f"   ❌ Could not read source code: {e}")
        return

    # Load findings
    slither_bugs = load_json_file(slither_report_path)
    logic_bugs = load_json_file(logic_report_path)

    # Filter only REAL bugs
    real_slither_bugs = [
        b for b in slither_bugs 
        if b.get("is_vulnerability") is True and b.get("verified_impact") != "Ignore"
    ]

    all_fixes = []
    for b in real_slither_bugs:
        all_fixes.append(f"- [Slither] {b.get('original_check')}: {b.get('remediation')}")
    
    for b in logic_bugs:
        all_fixes.append(f"- [Logic] {b.get('title')}: {b.get('remediation')}")

    if not all_fixes:
        print("   -> No bugs to fix! Skipping refactoring.")
        return

    print(f"   -> Applying {len(all_fixes)} fixes to the code...")

    # Run the Chain using the centralized prompt
    chain = REFACTORING_PROMPT | model | StrOutputParser()

    try:
        fixed_code = chain.invoke({
            "fixes_list": "\n".join(all_fixes),
            "source_code": source_code
        })

        # Cleanup
        fixed_code = fixed_code.replace("```solidity", "").replace("```", "").strip()

        # Save
        output_dir = os.path.join("SmartAudit", "fixed_contracts")
        os.makedirs(output_dir, exist_ok=True)
        
        filename = os.path.basename(contract_path)
        save_path = os.path.join(output_dir, f"Fixed_{filename}")

        with open(save_path, "w", encoding="utf-8") as f:
            f.write(fixed_code)
        
        print(f"   ✅ Fixed contract saved to: {save_path}")
        return save_path

    except Exception as e:
        print(f"   ❌ Refactoring failed: {e}")