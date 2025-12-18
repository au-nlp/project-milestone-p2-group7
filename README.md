
# PCAF: Prompt-Based Collaborative Agent Framework

**Course:** NLP Group 7 Project (Milestone P3)  
**Paper:** [Read the Full Report (PDF)](./report.pdf)

## 📄 Abstract
The inherent unreliability of Large Language Models (LLMs) in complex, multi step calculations necessitates architectural 
  interventions to achieve trustworthy accuracy in mathematical reasoning. This paper introduces 
  the Prompt Based Collaborative Agent Framework (PCAF), a novel, architecture driven approach 
  aimed at significantly improving final answer accuracy on the MathArena benchmark suite, including AIME 2025, HMMT (Feb/Nov) 2025, BRUMO 2025, SMT 2025, and CMIMC 2025.
  The method utilizes a single LLM instance (DeepSeek-V3-03-24) and employs sequential, 
  role specific prompting to simulate a sophisticated, three agent collaborative system (Solver, Verifier, and Planner).
  This architecture transforms the LLM's linear reasoning into a persistent self correction mechanism. 
  Through systematic evaluation across six distinct competition formats, we demonstrate that PCAF yields a significant accuracy uplift over the MathArena Zero-Shot CoT baseline, specifically improving scores from 50.0\% to 56.67\% on AIME 2025 and from 29.0\% to 45.83\% on HMMT Feb 2025. A global recovery rate of 38.9\% across all benchmarks confirms the efficacy of deterministic, architecture-driven reflection in transforming initial logical failures into verified successes.
  
## 📂 Repository Structure

This repository is organized to separate the orchestration logic from the agent definitions and tools, adhering to the Milestone P3 requirements.

```text
├── main.ipynb          # PRIMARY ENTRY POINT. Contains the main loop, evaluation logic, and data loading.
├── report.pdf          # Final project report (NeurIPS style).
├── README.md           # Project documentation.
├── src/                # HELPER MODULES & AGENT LOGIC
│   ├── agents.py       # Defines the interaction loop between Solver, Verifier, and Planner.
│   ├── sandbox.py      # Implements the PersistentSolverSandbox for stateful execution.
│   ├── utils.py        # Low-level utilities (API wrappers, answer extraction).
│   ├── prompts.py      # System prompts, role definitions, and few-shot examples.
│   └── config.py       # Configuration settings (API keys, deployment names).
├── final_results/            # EXPERIMENTAL DATA
│   └── *.csv           # Detailed CSV logs of the PCAF runs on MathArena competitions.
└── report-src/      # DOCUMENTATION SOURCE
    └── main.tex        # LaTeX source code for the final report.
```

## 🚀 Installation & Requirements

1. **Clone the repository:**
```bash
git clone [https://github.com/au-nlp/project-milestone-p2-group7.git](https://github.com/au-nlp/project-milestone-p2-group7.git)
cd project-milestone-p2-group7

```


2. **Install dependencies:**
The project requires Python 3.10+ and the following packages:
```bash
pip install openai pandas datasets func-timeout python-dotenv jupyter

```


3. **Environment Setup:**
Create a `.env` file in the root directory to store your Azure/OpenAI credentials, and make sure to use DeepSeek-V3-03-24 LLM model:
```env
API_KEY=your_azure_openai_api_key_here

```



## ⚙️ Methodology: The PCAF Architecture

The framework operates on a deterministic, closed-loop system designed to enforce self-correction through three distinct agents:

### 1. The Solver (Generator)

* **Role:** Generates solutions using a **Dual-Verification Protocol**.


* **Mandate:** Must use two strictly different methods:
    1. *Analytical Method:* Symbolic math using `sympy`.


    2. *Naive Brute-Force:* Simple simulation/loops.




* **Tooling:** Operates within a `PersistentSolverSandbox` that maintains variable state across turns.



### 2. The Verifier (Auditor)

* **Role:** Audits the execution trace against a structured checklist.


* **Output:** Returns a JSON object flagging specific error types:


* `METHOD_CONFLICT`: Analytical result \neq Brute-force result.


* `VALUE_MISMATCH`: Text conclusion \neq Code output.


* `LOGIC_FLAW`: Edge cases, hardcoding suspicion, or conceptual errors.





### 3. The Planner (Router)

* **Role:** Deterministic function that translates Verifier errors into mandatory instructions.


* **Strategy:** Breaks reasoning inertia by issuing specific commands (e.g., "Protocol Reset" for value mismatches or "Syntax Repair" for runtime errors).



## 📊 Usage

All experiments and logic are contained within `main.ipynb`.

### Running the Benchmark

To replicate the results from the report:

1. Open `main.ipynb`.
2. Run the cells to load the datasets (`aime_2025`, `hmmt_feb_2025`, etc.).
3. Execute the `run_matharena_pcaf_benchmark` function.
* *Note:* The system defaults to `attempts_per_problem=4` to account for stochasticity.





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
| **AIME 2025** | **50.0%** | **56.67%** | 29.5% |
| **BRUMO 2025** | N/A | 65.83% | 48.2% |
| **CMIMC 2025** | N/A | 51.25% | 41,6% |
| **HMMT Feb 2025** | **29.0%** | **45.83%** | 35.0% |
| **HMMT Nov 2025** | N/A | 46.67% | 25.4% |
| **SMT 2025** | N/A | 55.66% | 36.7% |
| **Global Average** | N/A| **53.65%** | **38.9%** |

*Recovery Rate indicates the percentage of correct answers achieved via self-correction after an initial failure.*

## 👥 Team Contributions

| Team Member | Contributions |
| --- | --- |
| **[Member Name 1]** | Developed the `PersistentSolverSandbox` (`sandbox.py`) and safety wrappers; implemented the `agents.py` orchestration logic; ran experiments for AIME 2025. |
| **[Member Name 2]** | Designed the Solver and Verifier system prompts (`prompts.py`); managed dataset ingestion and cleaning in `main.ipynb`; wrote the Methodology and Abstract sections of the report. |
| **András Szabolcs Gyüre** | Implemented the iterative room, FEW_SHOT_CORRECTION_EXAMPLES in utils.py, ran tests for AIME 2025, wrote the logic of the code in markdowns/comments, contributed in part of the report, e.g. Abstarct, Introduction, Related Work, Methodology, Experiments, Conclusion. |

## 🔗 Artifacts

* **Final Report:** [report.pdf](./report.pdf)
