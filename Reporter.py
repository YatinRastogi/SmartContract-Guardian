import json
import os
from fpdf import FPDF
from datetime import datetime

class AuditReportPDF(FPDF):
    def header(self):
        # Logo or Title
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Smart Contract Security Audit Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, label):
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(230, 230, 230)  # Light gray background
        self.cell(0, 10, label, 0, 1, 'L', 1)
        self.ln(4)

    def add_finding(self, title, severity, description, remediation):
        # 1. Title
        self.set_font('Arial', 'B', 12)
        self.cell(0, 6, f"Issue: {title}", 0, 1)
        
        # 2. Severity (Color Coded)
        self.set_font('Arial', 'B', 10)
        if "Critical" in severity:
            self.set_text_color(255, 0, 0)      # Red
        elif "High" in severity:
            self.set_text_color(255, 128, 0)    # Orange
        elif "Medium" in severity:
            self.set_text_color(204, 204, 0)    # Dark Yellow
        else:
            self.set_text_color(0, 128, 0)      # Green
            
        self.cell(0, 6, f"Severity: {severity}", 0, 1)
        self.set_text_color(0, 0, 0)  # Reset to black

        # 3. Description
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, f"Description: {description}")
        self.ln(2)
        
        # 4. Remediation
        self.set_font('Arial', 'I', 10)
        self.multi_cell(0, 5, f"Remediation: {remediation}")
        self.ln(5)
        
        # Separator Line
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def generate_pdf_report(contract_path, slither_json_path, logic_json_path, output_pdf_path):
    print(f"\n[Phase 5] Generating PDF Report...")
    
    contract_name = os.path.basename(contract_path)
    slither_data = load_json(slither_json_path)
    logic_data = load_json(logic_json_path)
    
    # --- 1. Aggregate Findings ---
    all_findings = []
    
    # Process Slither (Verified Only)
    for issue in slither_data.get("verified_vulnerabilities", []):
        if issue.get("is_vulnerability") and issue.get("verified_impact") != "Ignore":
            all_findings.append({
                "title": f"[Automated] {issue.get('original_check')}",
                "severity": issue.get("verified_impact", "Low"),
                "desc": issue.get("explanation") or issue.get("analysis", "No description"),
                "fix": issue.get("remediation", "No fix provided")
            })

    # Process Logic Audit
    for issue in logic_data.get("logic_vulnerabilities", []):
        all_findings.append({
            "title": f"[Logic] {issue.get('title')}",
            "severity": issue.get("true_impact", "Low"),
            "desc": issue.get("explanation", "No description"),
            "fix": issue.get("remediation", "No fix provided")
        })

    # Sort by Severity (Critical First)
    severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Informational": 4, "Optimization": 5}
    all_findings.sort(key=lambda x: severity_order.get(x["severity"], 10))

    # --- 2. Build PDF ---
    pdf = AuditReportPDF()
    pdf.add_page()
    
    # Executive Summary Section
    pdf.chapter_title(f"Executive Summary: {contract_name}")
    pdf.set_font('Arial', '', 11)
    
    # Calculate Stats
    stats = {k: 0 for k in severity_order.keys()}
    for f in all_findings:
        s = f['severity']
        if s in stats: stats[s] += 1
            
    # --- FIX: Use Python datetime instead of os.popen ---
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    summary_text = (
        f"Audit Date: {current_date}\n"
        f"Total Issues Found: {len(all_findings)}\n\n"
        f"Breakdown:\n"
    )
    for k, v in stats.items():
        if v > 0: summary_text += f"- {k}: {v}\n"
        
    pdf.multi_cell(0, 6, summary_text)
    pdf.ln(10)
    
    # Detailed Findings Section
    pdf.add_page()
    pdf.chapter_title("Detailed Vulnerability Findings")
    
    if not all_findings:
        pdf.set_font('Arial', 'I', 12)
        pdf.cell(0, 10, "No vulnerabilities found. Good job!", 0, 1)
    else:
        for f in all_findings:
            pdf.add_finding(f['title'], f['severity'], f['desc'], f['fix'])

    # Save
    try:
        pdf.output(output_pdf_path)
        print(f"   ✅ PDF saved to: {output_pdf_path}")
    except Exception as e:
        print(f"   ❌ Failed to save PDF: {e}")
if __name__ == "__main__":
    # Test run
    generate_pdf_report("FibonacciBalance.sol", 
                        "SmartAudit/outputs/verified_slither_report.json",
                        "SmartAudit/outputs/human_audit_report.json", 
                        "SmartAudit/Final_Report.pdf")