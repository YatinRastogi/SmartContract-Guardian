from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
import shutil
import os
import json
import asyncio
import sys
import io
# Importing the pipeline function from main.py
# Make sure main.py is in the same directory
from main import run_pipeline_async

app = FastAPI()

# --- CORS CONFIGURATION ---
origins = ["http://localhost:5173"]  # Vite default port
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- STATE MANAGEMENT ---
class AuditManager:
    def __init__(self):
        self.status = "idle" # idle | scanning | completed | error
        self.current_contract = None

    def set_status(self, status):
        self.status = status

manager = AuditManager()

async def run_audit_task(file_path: str):
    manager.set_status("scanning")
    print(f"Server: Starting audit for {file_path}")
    
    # Debug: Check file existence
    if not os.path.exists(file_path):
        print(f"Error: File does not exist at {file_path}")
        manager.set_status("error")
        return

    # Clean previous outputs to avoid stale data
    output_dir = os.path.join("SmartAudit", "outputs")
    try:
        if os.path.exists(output_dir):
            for f in os.listdir(output_dir):
                if f.endswith(".json"):
                    os.remove(os.path.join(output_dir, f))
        print("Server: Cleared previous output files.")
    except Exception as e:
        print(f"Server Warning: Could not clear outputs: {e}")

    try:
        # Run the existing pipeline
        print("Server: Invoking run_pipeline_async...")
        await run_pipeline_async(file_path)
        print("Server: run_pipeline_async returned.")
        
        # Verify outputs
        slither_out = os.path.join(output_dir, "verified_slither_report.json")
        if os.path.exists(slither_out):
            print(f"Server: Report generated at {slither_out} (Size: {os.path.getsize(slither_out)} bytes)")
        else:
            print("Server ERROR: Report file was NOT generated.")
            
        manager.set_status("completed")
    except Exception as e:
        manager.set_status("error")
        print(f"Server CRITICAL ERROR in background task: {e}")
        import traceback
        traceback.print_exc()

# --- ENDPOINTS ---

@app.post("/upload")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Accepts a .sol file and starts the audit pipeline."""
    if not file.filename.endswith(".sol"):
        raise HTTPException(status_code=400, detail="Only .sol files are allowed")
    
    upload_dir = os.path.join("SmartAudit", "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = os.path.join(upload_dir, file.filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    manager.current_contract = file.filename
    manager.set_status("starting")
    
    # Start background task
    background_tasks.add_task(run_audit_task, file_path)
    
    return {"message": "Audit started", "filename": file.filename}

@app.get("/status")
def get_status():
    """Returns current status."""
    return {
        "status": manager.status
    }

@app.get("/report")
def get_report():
    """Combines JSON reports."""
    output_base = os.path.join("SmartAudit", "outputs")
    slither_path = os.path.join(output_base, "verified_slither_report.json")
    logic_path = os.path.join(output_base, "human_audit_report.json")
    
    slither_data = {}
    logic_data = {}

    if os.path.exists(slither_path):
        with open(slither_path, "r", encoding="utf-8") as f:
            try: slither_data = json.load(f)
            except: pass
            
    if os.path.exists(logic_path):
        with open(logic_path, "r", encoding="utf-8") as f:
            try: logic_data = json.load(f)
            except: pass
    
    return {
        "code_vulnerabilities": slither_data.get("verified_vulnerabilities", []),
        "logic_vulnerabilities": logic_data.get("logic_vulnerabilities", []),
        "contract": slither_data.get("contract", manager.current_contract or "Unknown"),
        "metrics": {
            "total_risks": len(slither_data.get("verified_vulnerabilities", [])) + len(logic_data.get("logic_vulnerabilities", [])),
        }
    }

@app.get("/manuals")
def get_manuals():
    """Returns Red Team Manuals."""
    manual_dir = os.path.join("SmartAudit", "red_team_manuals")
    manuals = []
    
    if os.path.exists(manual_dir):
        for f in os.listdir(manual_dir):
            if f.endswith(".md"):
                path = os.path.join(manual_dir, f)
                with open(path, "r", encoding="utf-8") as file:
                    manuals.append({
                        "id": f,
                        "title": f.replace(".md", "").replace("_", " "),
                        "content": file.read()
                    })
    return manuals

@app.get("/fixed-code")
def get_fixed_code():
    """Returns the content of the fixed contract."""
    if not manager.current_contract:
        return {"code": "// No contract uploaded yet."} 
        
    fixed_path = os.path.join("SmartAudit", "fixed_contracts", f"Fixed_{manager.current_contract}")
    if os.path.exists(fixed_path):
        with open(fixed_path, "r", encoding="utf-8") as f:
            return {"code": f.read()}
            
    return {"code": "// Fixed code not generated yet or refactoring failed."}

@app.get("/download-pdf")
def download_pdf():
    """Downloads the Final Audit PDF."""
    pdf_path = os.path.join("SmartAudit", "Final_Audit_Report.pdf")
    if os.path.exists(pdf_path):
        return FileResponse(pdf_path, media_type='application/pdf', filename="SmartAudit_Report.pdf")
    return JSONResponse(status_code=404, content={"message": "PDF Report not ready yet."})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
