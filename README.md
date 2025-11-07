[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/hgNAtOO3)



## Project Proposal: Prompt-Based Collaborative Agent Framework (PCAF) for Enhanced LLM Mathematical Reasoning

### Abstract
This project aims to enhance the final-answer acccuracy of a selected Large Language Model (LLM), specifically one **underperforming or untested** on specific sub-sections of the **Matharena** benchmark. We will implement a **Prompt-Based Collaborative Agent Framework (PCAF)**, which simulates a multi-agent system using only sequential, specialized zero/few-shot prompts within the context of a single LLM instance hosted on Azure. The framework employs three virtual agents, a **Solver**, a **Verifier**, and a **Planner**, who communicate via structured **JSON** output. The core goal is to demonstrate that this reflective, architecturally structured prompting approach provides a clear performance gain over the model's standard Zero-Shot Chain-of-Thought (CoT) baseline, proving the value of structured collaboration in complex mathematical reasoning.

Also inspired by these papers: - https://arxiv.org/abs/2503.03205
                                - https://arxiv.org/abs/2509.22819
---

### Contributions and Novelty

1. **Targeted Performance Gain:** We provide a strong counter-measure to known LLM weaknesses (e.g., calculation errors, stubbornness in self-correction) by applying the PCAF to a model with a clear performance ceiling on Matharena's final-answer sub-sections (like AIME, HMMT, or CMIMC)
2. **Architecture-Driven Reasoning:** The novelty lies entirely in the **PCAF's algorithmic structure**, which uses sequential, role-specific prompts to forche the single LLM to adopt the roles of **Generation (Solver)**, **Critique (Verifier)** and **Coordinator (Planner)** This simulates a high-quality, iterative self-refinement loop.
3. **Generalizability of Prompting:** By proving that this collaborative prompting architecture yields significant gains on a robust, uncontaminated benchmark like MathArena, we demonstrate the power of **structured context management** as a high-value technique independent of the model's size or specific training data.

---

### Model Selection Criteria 

We have selected the DeepSeek-V3-03-24 model, which hasn't been fully tested on the final-answer MathArena benchmark. It achieved a score of 50% on AIME and 29% on HMMT, and still needs to be tested on BRUMO, SMT, and CMIMC. The model runs on Azure's AI Foundry. First we were thinking to use DeepSeek-V3 which has similar attributes but we couldn't make the model work with Azure since it's a "retired model".


---

### Proposed Data and Their Role

Since we are relying on **prompting**, these datasets serve as sources for **few-shot examples and prompt design**.

| Dataset | Role in Project | Usage for Prompt Design/Evaluation |
| :--- | :--- | :--- |
| **MathArena** | **Evaluation & Baseline** | Used only for testing (the primary metric). |
| **MathInstruct** | **Few-Shot Example Source** | Manually transform a few complex problems into full, multi-turn PCAF traces (showing an error and correction) to embed directly in the system prompt. |
| **NaturalProofs** | **Verifier Prompt Guidance** | Inform the design of the **Verifier Agent's system prompt** and the definitive **Error Categories** for structured JSON output. |


---

### Methods: Prompt-Based Collaborative Agent Framework (PCAF)

The entire system runs on the **single selected LLM** hosted on Azure, through iterative prompting.

#### Agent Roles and Communication (Sequential Prompting)
The PCAF relies on a sequence of API calls to the single LLM, dynamically switching its role via prompts. The loop runs for a maximum of $N$ iterations ($N=?$ max).

1.  **Initial Attempt (Solver):** The LLM receives the problem and few-shot examples and generates solution $\mathbf{S}_i$.
2.  **Critique (Verifier):** A new prompt is sent, instructing the LLM to adopt the Verifier role. It analyzes $\mathbf{S}_i$ and must output a **structured JSON** object:
    * **JSON Schema:** $`\{\text{"valid": bool, "error\_category": str, "critique\_summary": str}\}`$
    * **Error Categories:** The Verifier is guided to classify errors into: `CALCULATION_ERROR`, `CONCEPTUAL_FLAW`, or `LOGIC_OMISSION`.
3.  **Correction (Planner/Solver):** If the Verifier outputs `valid: false`, the system parses the JSON. A final prompt is constructed, instructing the LLM to **incorporate the specific error category and critique summary** to generate a corrected solution $\mathbf{S}_{i+1}$.

#### Evaluation
* **Baseline:** Zero-shot Chain-of-Thought (CoT) performance of the chosen LLM on the MathArena test set.
* **PCAF Metric:** Final answer correctness score of the PCAF on the same MathArena test set.
* **Analysis:** Compare the scores and analyze the **average number of correction steps** required by the PCAF to reach a correct final answer.

---

### Proposed Timeline

| Week | Internal Milestone (Team Focus) | Requirement Focus |
| :--- | :--- | :--- |
| **Week 1** | Select LLM, establish **Zero-Shot CoT Baseline** on MathArena subset. Draft few-shot traces. | **main.ipynb (Data/Baseline), Feasibility check.** |
| **Week 2** | Finalize S/V/P role prompts and **JSON schema**. Implement the iterative loop logic and JSON parsing code. | **Code Quality, System Logic.** |
| **Week 3** | Full PCAF integration. Run controlled tests on small dev set. Debug prompt logic and JSON stability. | **System integration, Prompt stability.** |
| **Week 4** | **Evaluation Run 1.** Run PCAF on larger subset of MathArena. Compare performance uplift against the baseline. | **Initial results, Uplift analysis.** |
| **Week 5-6** | Final Evaluation. Complete final comparison and documentation. | **Final Deliverable.** |


---


### Reaching Project Goal
Each component of this project—from dataset selection to architectural design and evaluation strategy—has been deliberately structured to achieve our central objective: improving final-answer accuracy on the MathArena benchmark.

**The PCAF’s multi-agent structure (Solver, Verifier, Planner)** enables systematic self-reflection and correction within a single LLM instance, directly addressing the known issues of arithmetic and logical consistency that often reduce MathArena scores.

*https://arxiv.org/pdf/2502.08680

**The use of specialized datasets (MathInstruct and NaturalProofs)** supports role-specific prompt engineering, ensuring that each agent’s reasoning, critique, and planning processes are grounded in examples of mathematically sound reasoning and structured verification.

**Iterative prompting and JSON-based** feedback loops transform what is typically a linear reasoning process into a collaborative refinement cycle, helping the model converge more reliably on correct final answers.

**The evaluation framework**, which compares PCAF’s performance to the baseline Zero-Shot CoT results, provides a clear, quantitative measure of improvement, allowing us to attribute accuracy gains directly to the proposed collaborative prompting structure.

Through this integrated design, the PCAF serves as a targeted mechanism to elevate the reasoning reliability and final-answer accuracy of LLMs on MathArena’s final-answer sub-sections—achieving the core goal established at the outset of this project.


