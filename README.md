
# 🛡️ Smart Contract Guardian

> **An Autonomous, Multi-Agent AI Pipeline for End-to-End Smart Contract Security Auditing.**

**Smart Contract Guardian** bridges the gap between automated static analysis and human expert review. By orchestrating a pipeline of **6 specialized AI agents**, it detects vulnerabilities, eliminates false positives, discovers deep business logic flaws, and generates runnable Proof-of-Concept (PoC) exploits—all validated by a deterministic "Gatekeeper" to prevent hallucinations.

---

## 🚀 Key Features

* **🕵️ Automated Detective:** Runs **Slither** static analysis and automatically manages Solidity compiler versions (`solc-select`) for hassle-free scanning.
* **🧠 AI Logic Auditor:** Uses **Llama 3.3 70B** (via Groq) to analyze code through "Four Lenses" (Storage, State, Access, Economics), finding complex bugs that tools miss.
* **🔒 The Gatekeeper (Hallucination Proof):** A deterministic validation layer that uses **Fuzzy Regex Matching** to mathematically verify every AI finding against the source code. If the code doesn't exist, the bug is rejected.
* **⚔️ Red Team Exploiter:** Automatically writes runnable **Foundry** test scripts (`.sol`) to prove high-severity vulnerabilities with mathematical assertions.
* **🛠️ Auto-Refactoring:** Generates secure code patches (`Fixed_Contract.sol`) that fix verified bugs while preserving business logic.
* **📄 Professional Reporting:** Delivers a stakeholder-ready **PDF Audit Report** and a real-time **Interactive Dashboard**.

---

## 🏗️ System Architecture

The system operates as a **Microservices-inspired pipeline**:

1.  **Frontend (React + Tailwind):** User uploads contracts and views real-time audit progress.
2.  **Backend (FastAPI):** Orchestrates the async Python pipeline.
3.  **Intelligence Layer (The 6 Agents):**
    * **Detective Agent:** `RunSlither.py` (Static Analysis)
    * **Verification Agent:** `VerificationAgent.py` (False Positive Filtering)
    * **Logic Audit Agent:** `HumanLogicAgent.py` (Deep Reasoning)
    * **Gatekeeper Agent:** `Gatekeeper.py` (Validation & Line Calculation)
    * **Exploiter Agent:** `ExploiterAgent.py` (PoC Generation)
    * **Refactoring & Reporting Agent:** `RefactoringAgent.py` & `Reporter.py`

---

## 🛠️ Tech Stack

* **Core:** Python 3.10+, FastAPI, AsyncIO
* **AI Inference:** Groq API (Llama 3.3 70B Versatile)
* **Static Analysis:** Slither, solc-select
* **Blockchain Testing:** Foundry (Forge)
* **Frontend:** React (Vite), Tailwind CSS, Lucide Icons, Axios
* **Reporting:** FPDF, LangChain

---

## ⚙️ Installation & Setup

### Prerequisites
* Python 3.10+
* Node.js & npm
* [Slither](https://github.com/crytic/slither) (`pip install slither-analyzer`)
* [Foundry](https://getfoundry.sh/) (for PoC generation)

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/smart-contract-guardian.git](https://github.com/yourusername/smart-contract-guardian.git)
cd smart-contract-guardian

```

### 2. Backend Setup

Create a virtual environment and install dependencies:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

```

**Environment Variables:**
Create a `.env` file in the `backend` folder:

```ini
GROQ_API_KEY=your_groq_api_key_here

```

### 3. Frontend Setup

Navigate to the frontend directory and install packages:

```bash
cd ../frontend
npm install

```

---

## 🏃‍♂️ Usage Guide

### Step 1: Start the Backend Server

In your backend terminal:

```bash
uvicorn server:app --reload

```

*Server will run on `http://localhost:8000*`

### Step 2: Launch the Dashboard

In your frontend terminal:

```bash
npm run dev

```

*UI will run on `http://localhost:5173*`

### Step 3: Run an Audit

1. Open the Dashboard in your browser.
2. Drag & drop a Solidity file (e.g., `Vulnerable.sol`).
3. Watch the **Live Stepper** as agents analyze, verify, and exploit the contract.
4. View the **Results Tabs**:
* **Vulnerabilities:** Confirmed bugs with line numbers.
* **Red Team:** Generated exploit code.
* **Refactored:** Fixed source code.


5. Download the **PDF Report**.

---

## 📂 Project Structure

```text
smart-contract-guardian/
├── backend/
│   ├── main.py                 # Orchestrator
│   ├── server.py               # FastAPI Gateway
│   ├── Gatekeeper.py           # Validation Logic
│   ├── HumanLogicAgent.py      # Logic Analysis
│   ├── VerificationAgent.py    # False Positive Filter
│   ├── RunSlither.py           # Static Analysis Wrapper
│   ├── ExploiterAgent.py       # PoC Generator
│   ├── Reporter.py             # PDF Generator
│   ├── prompts.py              # Centralized System Prompts
│   └── SmartAudit/             # Output Artifacts (JSON, PDF, Fixed Code)
├── frontend/
│   ├── src/
│   │   ├── components/         # Dashboard, Sidebar, VulnerabilityCard
│   │   ├── App.jsx             # Main UI Logic
│   │   └── index.css           # Tailwind Styles
└── README.md

```

---

## 🔮 Future Scope

* **Sandbox Execution:** Dockerized integration to automatically run generated Foundry tests.
* **AST-Based Gatekeeper:** Upgrading from Regex to Abstract Syntax Trees for deeper code validation.
* **Multi-File Support:** Analyzing complex repositories with cross-contract dependencies.

---

Working Project Video:
https://github.com/YatinRastogi/SmartContract-Guardian/issues/1

