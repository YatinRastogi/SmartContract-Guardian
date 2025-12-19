import os
import asyncio
import time
from dotenv import load_dotenv

# --- IMPORT AGENTS ---
from RunSlither import run_detective_agent
from VerificationAgent import run_verification_agent, get_groq_model as get_verifier_model
from HumanLogicAgent import run_logic_audit_agent, get_groq_model as get_logic_model
from RefactoringAgent import run_refactoring_agent
from ExploiterAgent import run_exploiter_agent, get_groq_model as get_exploiter_model
from ReportAgent import ReportAgent
from Reporter import generate_pdf_report
from Gatekeeper import Gatekeeper

load_dotenv()

# Wrapper to run blocking functions in threads
async def run_agent_in_thread(func, *args):
    return await asyncio.to_thread(func, *args)

async def run_pipeline_async(contract_path: str):
    if not os.path.exists(contract_path):
        print(f"FATAL ERROR: File not found at {contract_path}")
        return

    # --- DEFINE OUTPUT PATHS ---
    OUTPUT_BASE = os.path.join("SmartAudit", "outputs")
    EXPLOIT_DIR = os.path.join("SmartAudit", "red_team_manuals")
    
    SLITHER_OUT = os.path.join(OUTPUT_BASE, "agent_processed_output.json")
    VERIFIED_OUT = os.path.join(OUTPUT_BASE, "verified_slither_report.json")
    LOGIC_OUT = os.path.join(OUTPUT_BASE, "human_audit_report.json")
    PDF_REPORT = os.path.join("SmartAudit", "Final_Audit_Report.pdf")

    print(f"--- 🚀 STARTING 5-PHASE AUDIT PIPELINE for {os.path.basename(contract_path)} ---")
    start_time = time.time()

    # --- PHASE 1: SLITHER DETECTION (Sequential) ---
    print("\n[Phase 1] Running Detective Agent (Slither)...")
    try:
        slither_output = run_detective_agent(contract_path)
        if "error" in slither_output:
            print(f"❌ Slither Failed: {slither_output['error']}")
            return
        print(f"[Phase 1] SUCCESS. Found {len(slither_output.get('issues', []))} potential issues.")
    except Exception as e:
        print(f"[Phase 1] FAILED. Error in RunSlither.py: {e}")
        return

    # --- PHASE 2 & 3: PARALLEL AI AGENTS ---
    print("\n[Phase 2 & 3] Starting AI Agents in PARALLEL...")
    verifier_model = get_verifier_model()
    logic_model = get_logic_model()

    # Create async tasks
    task_verify = run_agent_in_thread(
        run_verification_agent,
        SLITHER_OUT,
        VERIFIED_OUT,
        contract_path,
        verifier_model
    )

    task_logic = run_agent_in_thread(
        run_logic_audit_agent,
        LOGIC_OUT,
        contract_path,
        logic_model
    )

    # Run simultaneously
    await asyncio.gather(task_verify, task_logic)
    
    # --- GATEKEEPER VALIDATION (BLOCKING STEP) ---
    print("\n[Quality Control] Running Gatekeeper Validation...")
    gatekeeper = Gatekeeper(contract_path)
    gatekeeper.validate_report(VERIFIED_OUT, is_logic=False)
    gatekeeper.validate_report(LOGIC_OUT, is_logic=True)
    print("[Phase 2 & 3] Analysis & QA Complete.")

    # --- PHASE 4 & 5: ACT (PARALLEL) ---
    # Now we run the Auto-Fixer AND the Red Teamer at the same time
    print("\n[Phase 4 & 5] Running Refactoring & Red Team (Parallel)...")
    
    # We reuse the Exploiter model (Text Mode) for Refactoring too
    shared_text_model = get_exploiter_model()

    task_refactor = run_agent_in_thread(
        run_refactoring_agent,
        contract_path, VERIFIED_OUT, LOGIC_OUT, shared_text_model
    )

    task_exploit = run_agent_in_thread(
        run_exploiter_agent,
        LOGIC_OUT, contract_path, EXPLOIT_DIR, shared_text_model
    )

    # Wait for both to finish
    await asyncio.gather(task_refactor, task_exploit)
    print("✅ Refactoring and Exploits Complete.")

    # --- PHASE 6: REPORTING ---
    print("\n[Phase 6] Generating Official Audit Reports...")
    try:
        # 1. Markdown Report
        reporter = ReportAgent(output_dir=OUTPUT_BASE)
        reporter.generate_report()
        
        # 2. PDF Report
        generate_pdf_report(contract_path, VERIFIED_OUT, LOGIC_OUT, PDF_REPORT)
    except Exception as e:
        print(f"⚠️ Phase 6 Warning: {e}")

    # --- FINAL SUMMARY ---
    end_time = time.time()
    print(f"\n✨ AUDIT PIPELINE FINISHED in {end_time - start_time:.2f} seconds.")
    print(f"📄 Official Report: SmartAudit/FINAL_AUDIT_REPORT.md")
    print(f"📕 PDF Report:      {PDF_REPORT}")
    
    fixed_path = os.path.join("SmartAudit", "fixed_contracts", f"Fixed_{os.path.basename(contract_path)}")
    if os.path.exists(fixed_path):
        print(f"🛠️  Fixed Contract:  {fixed_path}")
        
    print(f"⚔️  Red Team Manuals: {EXPLOIT_DIR}")

if __name__ == "__main__":
    # Update this path to your specific contract
    CONTRACT_TO_ANALYZE = r"C:\Users\yatin\OneDrive\Documents\College\pbl_project_major\smartbugs-curated\dataset\access_control\FibonacciBalance.sol"

    asyncio.run(run_pipeline_async(CONTRACT_TO_ANALYZE))