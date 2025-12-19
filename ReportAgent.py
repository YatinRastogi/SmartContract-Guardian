import json
import os
from datetime import datetime

class ReportAgent:
    def __init__(self, output_dir="SmartAudit/outputs", final_report_path="SmartAudit/FINAL_AUDIT_REPORT.md"):
        self.slither_path = os.path.join(output_dir, "verified_slither_report.json")
        self.logic_path = os.path.join(output_dir, "human_audit_report.json")
        self.final_report_path = final_report_path

    def load_json(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def generate_report(self):
        print("\n[Phase 5] Generating Official Audit Report...")

        slither_data = self.load_json(self.slither_path)
        logic_data = self.load_json(self.logic_path)

        contract_name = slither_data.get("contract", "Unknown Contract")
        
        # Get findings (Gatekeeper has added 'confidence' fields)
        verified_bugs = [b for b in slither_data.get("verified_vulnerabilities", []) if b.get("is_vulnerability")]
        logic_bugs = logic_data.get("logic_vulnerabilities", [])
        all_findings = verified_bugs + logic_bugs

        confident_bugs = [b for b in all_findings if b.get("confidence") == "Confident"]
        review_bugs = [b for b in all_findings if b.get("confidence") != "Confident"]

        lines = []
        lines.append(f"# 🛡️ SmartAudit Security Report: {contract_name}")
        lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"**Total Findings:** {len(all_findings)} | **Confirmed:** {len(confident_bugs)} | **Pending Review:** {len(review_bugs)}\n")

        # Section 1: Confirmed
        lines.append("## ✅ Confirmed Threats (Verified by Gatekeeper)")
        if not confident_bugs:
            lines.append("_No high-confidence vulnerabilities found._\n")
        else:
            for i, bug in enumerate(confident_bugs, 1):
                title = bug.get('title') or bug.get('original_check')
                impact = bug.get('true_impact') or bug.get('verified_impact', 'Unknown')
                lines.append(f"### {i}. {title} ({impact})")
                lines.append(f"📍 **Line:** {bug.get('line_number', 'Unknown')}")
                lines.append(f"```solidity\n{bug.get('code_citation', 'N/A')}\n```")
                lines.append(f"**Fix:** {bug.get('remediation')}\n")

        # Section 2: Manual Review
        lines.append("## ⚠️ Items for Manual Review")
        if not review_bugs:
            lines.append("_No ambiguous findings._\n")
        else:
            for i, bug in enumerate(review_bugs, 1):
                title = bug.get('title') or bug.get('original_check')
                impact = bug.get('true_impact') or bug.get('verified_impact', 'Unknown')
                lines.append(f"### {i}. {title} ({impact})")
                lines.append(f"**Gatekeeper Note:** {bug.get('gatekeeper_note', 'Check manually.')}")
                lines.append(f"**Analysis:** {bug.get('explanation')}\n")

        with open(self.final_report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"✅ Official Report Generated: {self.final_report_path}")