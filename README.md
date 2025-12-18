
# PCAF: Prompt-Based Collaborative Agent Framework

**Course:** NLP Group 7 Project (Milestone P3)  
**Paper:** [Read the Full Report (PDF)](./report.pdf)

## 📄 Abstract
[cite_start]The inherent unreliability of Large Language Models (LLMs) in complex, multi-step calculations necessitates architectural interventions to achieve trustworthy accuracy[cite: 5]. [cite_start]This project introduces the **Prompt-Based Collaborative Agent Framework (PCAF)**, a novel architecture utilizing a single LLM instance (DeepSeek-V3-0324) to simulate a sophisticated, three-agent collaborative system (Solver, Verifier, and Planner)[cite: 6].

[cite_start]Instead of relying on fine-tuning, PCAF employs sequential, role-specific prompting to enforce a "Code-First" mandate[cite: 14, 22]. [cite_start]Through systematic evaluation on the MathArena benchmark (AIME, HMMT, BRUMO, SMT, CMIMC), the framework achieved a global accuracy of **53.65%** (compared to a 39.5% baseline) and demonstrated a **38.9% recovery rate**, validating the efficacy of deterministic self-correction[cite: 8].

## 📂 Repository Structure

This repository is organized to separate the orchestration logic from the agent definitions and tools, adhering to the Milestone P3 requirements.

```text
├── main.ipynb          # PRIMARY ENTRY POINT. Contains the main loop, evaluation logic, and data loading.
├── agents.py           # Defines the interaction loop between Solver, Verifier, and Planner.
├── sandbox.py          # Implements the PersistentSolverSandbox for stateful, secure Python execution.
├── utils.py            # Low-level utilities (API wrappers, robust answer extraction, JSON parsing).
├── prompts.py          # Contains system prompts, role definitions, and few-shot correction examples.
├── config.py           # Configuration settings (API keys, model deployment names).
├── report.pdf          # Final project report (NeurIPS style).
└── README.md           # Project documentation.

```

## 🚀 Installation & Requirements

1. **Clone the repository:**
```bash
git clone [https://github.com/au-nlp/project-milestone-p2-group7.git](https://github.com/au-nlp/project-milestone-p2-group7.git)
cd nlp-group-7-p3

```


2. **Install dependencies:**
The project requires Python 3.10+ and the following packages:
```bash
pip install openai pandas datasets func-timeout python-dotenv jupyter

```


3. **Environment Setup:**
Create a `.env` file in the root directory to store your Azure/OpenAI credentials:
```env
API_KEY=your_azure_openai_api_key_here

```



## ⚙️ Methodology: The PCAF Architecture

The framework operates on a deterministic, closed-loop system designed to enforce self-correction through three distinct agents:

### 1. The Solver (Generator)

* 
**Role:** Generates solutions using a **Dual-Verification Protocol**.


* **Mandate:** Must use two strictly different methods:
1. 
*Analytical Method:* Symbolic math using `sympy`.


2. 
*Naive Brute-Force:* Simple simulation/loops.




* 
**Tooling:** Operates within a `PersistentSolverSandbox` that maintains variable state across turns.



### 2. The Verifier (Auditor)

* 
**Role:** Audits the execution trace against a structured checklist.


* 
**Output:** Returns a JSON object flagging specific error types:


* 
`METHOD_CONFLICT`: Analytical result \neq Brute-force result.


* 
`VALUE_MISMATCH`: Text conclusion \neq Code output.


* 
`LOGIC_FLAW`: Edge cases, hardcoding suspicion, or conceptual errors.





### 3. The Planner (Router)

* 
**Role:** Deterministic function that translates Verifier errors into mandatory instructions.


* 
**Strategy:** Breaks reasoning inertia by issuing specific commands (e.g., "Protocol Reset" for value mismatches or "Syntax Repair" for runtime errors).



## 📊 Usage

All experiments and logic are contained within `main.ipynb`.

### Running the Benchmark

To replicate the results from the report:

1. Open `main.ipynb`.
2. Run the cells to load the datasets (`aime_2025`, `hmmt_feb_2025`, etc.).
3. Execute the `run_matharena_pcaf_benchmark` function.
* 
*Note:* The system defaults to `attempts_per_problem=4` to account for stochasticity.





### Single Problem Execution

You can run the PCAF loop on a specific text input using the helper in `main.ipynb` (imported from `agents.py`):

```python
from agents import run_pcaf_on_problem

# Example problem
problem_text = "Find the number of integers between 1 and 50 divisible by 2 or 3."
solution, trace_history = run_pcaf_on_problem(problem_text, max_retries=3)

print(solution)

```

## 📈 Key Results

The PCAF architecture consistently outperforms the Zero-Shot CoT baseline across all tested competitions.

| Competition Subset | Baseline Accuracy | PCAF Accuracy | Recovery Rate |
| --- | --- | --- | --- |
| **AIME 2025** | 50.0% | **56.67%** | 29.5% |
| **HMMT Feb 2025** | 29.0% | **45.83%** | 35.0% |
| **BRUMO 2025** | N/A | **65.83%** | 48.2% |
| **SMT 2025** | N/A | **55.66%** | 36.7% |
| **Global Average** | **39.5%** | **53.65%** | **38.9%** |

*Recovery Rate indicates the percentage of correct answers achieved via self-correction after an initial failure.*

## 👥 Team Contributions

| Team Member | Contributions |
| --- | --- |
| **[Member Name 1]** | Developed the `PersistentSolverSandbox` (`sandbox.py`) and safety wrappers; implemented the `agents.py` orchestration logic; ran experiments for AIME 2025. |
| **[Member Name 2]** | Designed the Solver and Verifier system prompts (`prompts.py`); managed dataset ingestion and cleaning in `main.ipynb`; wrote the Methodology and Abstract sections of the report. |
| **[Member Name 3]** | Implemented the evaluation pipeline and answer extraction logic (`utils.py`); analyzed failure cases (Geometry); compiled the final `report.pdf` and managed repository organization. |

## 🔗 Artifacts

* **Final Report:** [report.pdf](./report.pdf)
