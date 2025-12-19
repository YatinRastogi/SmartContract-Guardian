import json
import re
import os
import subprocess
import shutil

def get_pragma_version(contract_path: str) -> str:
    """Extracts the solidity version from the pragma string."""
    try:
        with open(contract_path, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(r'pragma solidity\s+([^;]+);', content)
        if match:
            version_str = match.group(1).strip()
            version_match = re.search(r'(\d+\.\d+\.\d+)', version_str)
            if version_match:
                return version_match.group(1)
    except Exception as e:
        print(f"⚠️ Error reading pragma: {e}")
    return None

def manage_solc_version(target_version: str):
    """Uses 'solc-select' to install and set the correct compiler version."""
    if not target_version:
        print("⚠️ No pragma version found. Using system default.")
        return

    print(f"🔧 Detected Solidity version: {target_version}")
    try:
        subprocess.run(["solc-select", "install", target_version], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        subprocess.run(["solc-select", "use", target_version], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"   ✅ Successfully switched to solc {target_version}")
    except subprocess.CalledProcessError as e:
        print(f"   ⚠️ Failed to set solc version {target_version}. Slither might fail.")
    except FileNotFoundError:
        print("   ⚠️ 'solc-select' tool not found. Please ensure it is installed.")

def clean_and_parse_json(raw_output: str) -> dict:
    if not raw_output: return {}
    try:
        start, end = raw_output.find('{'), raw_output.rfind('}')
        if start == -1 or end == -1: return {}
        return json.loads(raw_output[start: end + 1])
    except json.JSONDecodeError:
        return {}

def run_detective_agent(contract_path: str, output_json_path: str = None) -> dict:
    """
    Analyzes a Solidity contract using Slither.
    ARGS:
      output_json_path: Optional custom path to save the JSON output. 
                        If None, defaults to 'agent_processed_output.json'.
    """
    manage_solc_version(get_pragma_version(contract_path))
    
    command = ['slither', contract_path, '--json', '-']
    print(f"Running command: {' '.join(command)}")

    try:
        env = os.environ.copy()
        env["NO_COLOR"] = "1"
        result = subprocess.run(command, capture_output=True, text=True, check=True, env=env)
        slither_output = clean_and_parse_json(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Slither finished with exit code (findings likely detected).")
        slither_output = clean_and_parse_json(e.stdout or "")
        if "results" not in slither_output:
            return {"contract": os.path.basename(contract_path), "error": e.stderr or e.stdout or "Unknown error"}
    except Exception as e:
        return {"contract": os.path.basename(contract_path), "error": str(e)}

    # Format Results
    issues = [
        {
            "check": f.get("check"),
            "description": f.get("description", "").strip(),
            "impact": f.get("impact"),
            "confidence": f.get("confidence")
        } 
        for f in slither_output.get("results", {}).get("detectors", [])
    ]

    agent_output = {"contract": os.path.basename(contract_path), "issues": issues}

    # --- DYNAMIC SAVE PATH LOGIC ---
    if output_json_path:
        final_path = output_json_path
    else:
        # Default fallback
        output_dir = os.path.join("SmartAudit", "outputs")
        final_path = os.path.join(output_dir, "agent_processed_output.json")

    os.makedirs(os.path.dirname(final_path), exist_ok=True)
    with open(final_path, "w", encoding="utf-8") as f:
        json.dump(agent_output, f, indent=2)
        print(f"Slither JSON saved to: {final_path}")

    return agent_output