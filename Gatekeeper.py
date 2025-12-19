import json
import re
import os

class Gatekeeper:
    def __init__(self, source_code_path):
        self.source_code = self._read_file(source_code_path)
        # Patterns that MUST exist for "High Confidence" (Case-Insensitive)
        self.patterns = {
            "reentrancy": [r"\.call", r"\.transfer", r"\.send", r"external"],
            "access-control": [r"onlyOwner", r"require", r"msg\.sender", r"modifier"],
            "tx-origin": [r"tx\.origin"],
            "arithmetic": [r"\+", r"\-", r"\*", r"\/", r"SafeMath"],
            "timestamp": [r"block\.timestamp", r"now"],
            "suicide": [r"selfdestruct", r"suicide"]
        }

    def _read_file(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except:
            return ""

    def _fuzzy_search(self, snippet):
        """Finds code even if AI added/removed spaces or newlines."""
        if not snippet or snippet == "N/A": return None
        # Escape special characters and convert spaces to 'match any whitespace'
        clean = re.escape(snippet.strip())
        pattern = re.sub(r'(\\ )+', r'\\s*', clean)
        try:
            return re.search(pattern, self.source_code, re.IGNORECASE | re.DOTALL)
        except:
            return None

    def _calculate_line(self, match):
        """Math: Count newlines before the match start."""
        return self.source_code[:match.start()].count('\n') + 1

    def validate_report(self, json_path, is_logic=False):
        if not os.path.exists(json_path): return
        print(f"🔒 Gatekeeper: Validating {'Logic' if is_logic else 'Code'} Findings...")

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            return

        key = "logic_vulnerabilities" if is_logic else "verified_vulnerabilities"
        original_issues = data.get(key, [])
        validated_issues = []

        for issue in original_issues:
            snippet = issue.get("code_citation", "N/A")
            check_name = issue.get("original_check" if not is_logic else "title", "").lower()

            match = self._fuzzy_search(snippet)

            if not match:
                if is_logic:
                    # Logic bugs are abstract, so we keep them but mark for review
                    issue["confidence"] = "Manual Review"
                    issue["gatekeeper_note"] = "Logic finding: Verbatim code snippet match failed. Verify logic manually."
                    issue["line_number"] = "Global/Logic"
                    validated_issues.append(issue)
                    continue
                else:
                    # Static findings MUST match code or they are hallucinations.
                    print(f"   -> ❌ Rejected Hallucination: {check_name[:30]}...")
                    continue

            # Match found
            line_no = self._calculate_line(match)
            issue["line_number"] = line_no
            issue["confidence"] = "Confident"
            issue["gatekeeper_note"] = "Code match confirmed."
            validated_issues.append(issue)

        data[key] = validated_issues
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)