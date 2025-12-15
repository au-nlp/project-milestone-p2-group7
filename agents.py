from utils import get_llm_response
import re

def run_solver_with_tools(system_prompt, user_problem, sandbox_instance, temperature=0.7, max_turns=3):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_problem}
    ]
    full_trace = ""
    
    for turn in range(max_turns):
        response = get_llm_response(messages, temperature=temperature)
        full_trace += f"\n\n--- Step {turn+1} ---\n{response}"
        
        # Find ALL code blocks
        code_blocks = re.findall(r"```python\n(.*?)```", response, re.DOTALL)
        
        if code_blocks:
            print(f"    [Tool Use] Detected {len(code_blocks)} code blocks.")
            
            combined_output = ""
            for i, code_str in enumerate(code_blocks):
                print(f"    [Block {i+1}] Executing...")
                out = sandbox_instance.run_code(code_str)
                # FORMATTING CHANGE HERE: Use a consistent tag for the trace
                combined_output += f"[Block {i+1} Output]:\n{out}\n\n"
            
            print(f"    [Tool Output] {combined_output.strip()[:100]}...")
            
            # Feed back to LLM (Model sees 'OBSERVATION' which is standard convention)
            messages.append({"role": "assistant", "content": response})
            messages.append({
                "role": "user", 
                "content": f"OBSERVATION (Code Output):\n{combined_output}\n\nContinue reasoning."
            })
            
            # Feed to Trace (We use [Tool Output] so the Verifier Regex can find it)
            # --- FIX IS HERE ---
            full_trace += f"\n\n[Tool Output]\n{combined_output}"
            # -------------------
            
        else:
            if "\\boxed" in response or "Final Answer" in response:
                return response, full_trace
            
            messages.append({"role": "assistant", "content": response})
            if turn == max_turns - 1:
                break
                
    return response, full_trace