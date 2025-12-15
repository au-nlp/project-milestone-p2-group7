"""
Defines a secure, persistent Python execution environment (sandbox) for the Solver.
It manages state across multiple execution turns and enforces time limits to prevent infinite loops.
"""

import sys
import io
import contextlib
import textwrap
# Make sure you have run: !pip install func_timeout
from func_timeout import func_timeout, FunctionTimedOut

class PersistentSolverSandbox:
    def __init__(self):
        self.globals = {
            "__builtins__": __builtins__,
            "print": print
        }
        self._exec_setup()
        
    def _exec_setup(self):
        setup_code = """
import math
import sympy
import numpy as np
import itertools
import sys

# 1. Safe Math Imports
from math import sqrt, sin, cos, tan, log, exp, pi, e, factorial, acos, asin, atan, radians, degrees

# 2. Robust SymPy Imports
from sympy import symbols, solve, nsolve, Eq, simplify, expand, factor, Rational, isprime, N
from sympy import Reals, S 

# 3. Config
sys.set_int_max_str_digits(0)
"""
        try:
            exec(setup_code, self.globals)
        except Exception as e:
            print(f"Sandbox Setup Error: {e}")

    def run_code(self, code_str, timeout_seconds=20):
        # 1. Auto-Fix Indentation
        try:
            code_str = textwrap.dedent(code_str)
        except:
            pass

        # 2. Auto-Clean Non-ASCII Characters (Fixes the '≈' crash)
        code_str = code_str.replace("≈", "=").replace("≠", "!=").replace("≤", "<=").replace("≥", ">=")

        output_buffer = io.StringIO()
        error_buffer = io.StringIO()
        
        def _run_captured():
            with contextlib.redirect_stdout(output_buffer), contextlib.redirect_stderr(error_buffer):
                exec(code_str, self.globals)
        
        try:
            func_timeout(timeout_seconds, _run_captured)
            
            stdout_val = output_buffer.getvalue()
            stderr_val = error_buffer.getvalue()
            
            # 3. Combine output
            full_output = stdout_val
            if stderr_val:
                full_output += f"\n[WARNINGS/ERRORS]:\n{stderr_val}"
            
            # 4. Check for "Empty" success (The Silent Killer)
            if not full_output.strip():
                return "[SYSTEM]: Code executed but produced NO OUTPUT. Did you forget to print(result)? Variables are NOT returned automatically."
            
            # 5. Check for Empty Lists specifically
            if full_output.strip() == "[]":
                return "[]\n[SYSTEM]: Your code returned an empty list. Check your variable ranges or equations."

            if len(full_output) > 2500: 
                return full_output[:2500] + f"\n... [OUTPUT TRUNCATED. Total: {len(full_output)} chars]"
            
            return full_output
            
        except FunctionTimedOut:
            return "RUNTIME ERROR: Code execution exceeded time limit (20s). Loop likely infinite."
        except IndentationError:
            return "RUNTIME ERROR: IndentationError. Ensure code is properly formatted."
        except Exception as e:
            return f"RUNTIME ERROR: {str(e)}"

# --- Unit Tests (Only run if file is executed directly) ---
if __name__ == "__main__":
    test_code = """
import sympy
x = sympy.symbols('x')
sol = sympy.solve(x**2 - 4, x)
print(sol)
"""
    env = PersistentSolverSandbox()
    print(f"Sandbox Test Output: {env.run_code(test_code)}")

    persist_test_code = """
print(sol)
"""
    print(f"Persistency test output: {env.run_code(persist_test_code)}")

    empty_test_code = """
print([])
"""
    print(f"Empty list test output: {env.run_code(empty_test_code)}")