"""
Handles low-level utilities for the PCAF system, including Azure OpenAI API 
communication, robust text extraction for math answers, and semantic verification logic.
"""

import json
import re
import ast
import math
from openai import OpenAI
from config import client, DEPLOYMENT_NAME

# --- Core Helper Functions ---

def get_llm_response(messages, temperature=0.0):
    """Sends a request to the Azure LLM."""
    # Configure the response format for JSON
    response_format = {"type": "text"}
    
    # Check for JSON requirement in the messages (robust check)
    if isinstance(messages, list) and len(messages) > 0:
        # Check first few messages for JSON instruction
        for m in messages[:2]:
            if "JSON" in str(m.get("content", "")):
                 response_format = {"type": "json_object"}
                 break
    
    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=messages,
            temperature=temperature,
            response_format=response_format
        )
        content = response.choices[0].message.content
        return content if content is not None else ""
    except Exception as e:
        return f"LLM API Error: {e}"

def extract_answer(text):
    """
    Robust extraction that handles nested \boxed{}, cleans up text artifacts,
    and prioritizes explicit answer markers.
    """
    if not isinstance(text, str): return None

    # --- Strategy 1: Boxed Content (Recursive for nested braces) ---
    start_idx = text.find(r'\boxed{')
    if start_idx != -1:
        content_start = start_idx + 7 
        brace_count = 1
        i = content_start
        while i < len(text) and brace_count > 0:
            if text[i] == '{':
                brace_count += 1
            elif text[i] == '}':
                brace_count -= 1
            i += 1
        
        if brace_count == 0:
            return text[content_start : i-1].strip()

    # --- Strategy 2: Explicit "Final Answer" text ---
    final_match = re.search(r'(?:Final Answer|answer is)[:\s]*([^\n]+)(?:\n|$)', text, re.IGNORECASE)
    if final_match:
        candidate = final_match.group(1).strip()
        candidate_norm = re.sub(r'\\(?:d)?frac\{([^{}]+)\}\{([^{}]+)\}', r'\1/\2', candidate)
        token_pattern = r'(?:-?\d+(?:,\d{3})*(?:\.\d+)?(?:/\d+)?|\\sqrt\{[^{}]+\}|\\pi)'
        tokens = re.findall(token_pattern, candidate_norm)
        
        if tokens:
            return tokens[-1].strip()
        return candidate.rstrip(".:,;!)]}")

    # --- Strategy 3: Last Math Token (Heuristic Fallback) ---
    text_norm = re.sub(r'\\(?:d)?frac\{([^{}]+)\}\{([^{}]+)\}', r'\1/\2', text)
    token_pattern = r'(?:-?\d+(?:,\d{3})*(?:\.\d+)?(?:/\d+)?|\\sqrt\{[^{}]+\}|\\pi)'
    candidates = re.findall(token_pattern, text_norm)

    if candidates:
        return candidates[-1].strip()

    return None

def check_correctness(prediction, ground_truth):
    """Semantically checks if the prediction matches the ground truth."""
    if prediction is None or ground_truth is None:
        return False
        
    pred_str = str(prediction).strip()
    gt_str = str(ground_truth).strip()

    def clean_string(s):
        s = s.replace(" ", "").replace(",", "")
        s = s.replace(r"\boxed", "").replace(r"\text", "")
        s = s.replace(r"\dfrac", r"\frac")
        s = s.replace(r"\(", "").replace(r"\)", "")
        return s
        
    p_clean = clean_string(pred_str)
    g_clean = clean_string(gt_str)

    if p_clean == g_clean:
        return True
        
    if g_clean in p_clean and len(p_clean) < len(g_clean) * 4:
        return True

    def safe_eval(s):
        try:
            s = s.replace(",", "").replace("^", "**").replace(r"\dfrac", r"\frac")
            s = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'(\1)/(\2)', s)
            s = s.replace(r"\sqrt", "sqrt").replace(r"\pi", "pi")
            s = s.replace("{", "(").replace("}", ")").replace("\\", "") 
            s = re.sub(r'(\d)\s*([a-zA-Z(])', r'\1*\2', s)
            safe_env = {"math": math, "sqrt": math.sqrt, "pi": math.pi, "abs": abs}
            return float(eval(s, {"__builtins__": {}}, safe_env))
        except Exception:
            return None

    val_pred = safe_eval(prediction)
    val_gt = safe_eval(ground_truth)

    if val_pred is not None and val_gt is not None:
        if abs(val_pred - val_gt) < 1e-3:
            return True

    return False

def extract_json_from_response(text):
    """Robustly extracts JSON from a string."""
    if text is None: return None

    def validate_and_default(data):
        if not isinstance(data, dict): return data
        if "error_category" in data and "error_type" not in data:
            data["error_type"] = data.pop("error_category")
        if "valid" not in data: data["valid"] = False
        if "error_type" not in data: data["error_type"] = "NONE"
        if "critique" not in data: 
            if "critique_summary" in data:
                data["critique"] = data.pop("critique_summary")
            else:
                data["critique"] = "The answer is incorrect but no specific critique was provided."
        return data

    text = re.sub(r"```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```python\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```\s*", "", text).strip()

    match = re.search(r"(\{.*\})", text, re.DOTALL)
    candidate = match.group(1) if match else text

    try:
        return validate_and_default(json.loads(candidate))
    except json.JSONDecodeError: pass

    candidate_clean = re.sub(r",\s*\}", "}", candidate)
    try:
        return validate_and_default(json.loads(candidate_clean, strict=False))
    except json.JSONDecodeError: pass

    try:
        candidate_python = candidate_clean.replace("true", "True").replace("false", "False").replace("null", "None")
        return validate_and_default(ast.literal_eval(candidate_python))
    except (ValueError, SyntaxError): pass

    return None