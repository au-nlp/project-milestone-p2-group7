import re

# ======================================================================
# FEW-SHOT EXAMPLES (clean dictionary)
# ======================================================================

FEW_SHOT_EXAMPLES = {
    "Algebra": """
## Few-Shot Example (Algebra)
Problem: Solve the equation $2x + 5 = 11$ for $x$.
Thought: This is a linear equation. First, I will isolate the term with $x$ by subtracting 5 from both sides:
$2x + 5 - 5 = 11 - 5$
$2x = 6$
Next, I will solve for $x$ by dividing both sides by 2:
$x = 6 / 2$
$x = 3$
Final Answer: \\boxed{3}
---
""",

    "Geometry": """
## Few-Shot Example (Geometry)
Problem: A right triangle has legs of length 3 and 4. Find the length of the hypotenuse.
Thought: I will use the Pythagorean theorem, $a^2 + b^2 = c^2$, where $a=3$ and $b=4$.
$3^2 + 4^2 = c^2$
$9 + 16 = c^2$
$25 = c^2$
Taking the square root of both sides, $c = \sqrt{25} = 5$.
Final Answer: \\boxed{5}
---
""",

    "Number Theory": """
## Few-Shot Example (Number Theory)
Problem: Find the remainder when $2^{10}$ is divided by 5.
Thought: I will find the pattern of powers of 2 modulo 5.
$2^1 \equiv 2 \pmod{5}$
$2^2 \equiv 4 \pmod{5}$
$2^3 \equiv 8 \equiv 3 \pmod{5}$
$2^4 \equiv 16 \equiv 1 \pmod{5}$
Since the cycle length is 4, I can simplify the exponent: $10 = 4 \times 2 + 2$.
Therefore, $2^{10} \equiv 2^{4 \times 2 + 2} \equiv (2^4)^2 \cdot 2^2 \equiv (1)^2 \cdot 4 \equiv 4 \pmod{5}$.
Final Answer: \\boxed{4}
---
""",

    "Combinatorics": """
## Few-Shot Example (Combinatorics)
Problem: In how many ways can 3 distinct books be arranged on a shelf?
Thought: This is a permutation problem for 3 distinct items. The number of arrangements is $3!$ (3 factorial).
$3! = 3 \times 2 \times 1$
$3! = 6$
Final Answer: \\boxed{6}
---
""",

    "DEFAULT": ""
}


# ======================================================================
# CLEAN, ROBUST NORMALIZER
# ======================================================================

def normalize_problem_type(ptype):
    """
    Converts the incoming problem_type (string or list) into a
    canonical form matching the FEW_SHOT_EXAMPLES dict keys.
    """
    # 1. If list, extract first element
    if isinstance(ptype, list) and ptype:
        ptype = ptype[0]

    # 2. If still not string → default
    if not isinstance(ptype, str):
        return "DEFAULT"

    # 3. Remove non-alphabetic characters (turn punctuation into spaces)
    cleaned = re.sub(r'[^a-zA-Z\s]', ' ', ptype)

    # 4. Normalize whitespace (collapse multiple spaces)
    cleaned = " ".join(cleaned.split())

    # 5. Title-case to match dictionary ("Number Theory", "Algebra", etc.)
    cleaned = cleaned.title()

    # 6. If unknown → DEFAULT
    return cleaned if cleaned in FEW_SHOT_EXAMPLES else "DEFAULT"


# ======================================================================
# MAIN ACCESSOR
# ======================================================================

def get_few_shot_content(problem_type_input):
    """Fetches the few-shot content, with debug prints to show the actual key."""
    if isinstance(problem_type_input, list) and problem_type_input:
        primary_type = problem_type_input[0]
    elif isinstance(problem_type_input, str):
        primary_type = problem_type_input
    else:
        print(f"[DEBUG] Input type invalid: {problem_type_input}")
        return FEW_SHOT_EXAMPLES['DEFAULT']

    # Show the raw key before cleaning
    print(f"[DEBUG] Raw primary_type: {repr(primary_type)}")

    # Cleaning (remove non-printable chars and normalize spaces)
    cleaned_type = ''.join(c for c in str(primary_type) if c.isprintable())
    cleaned_type = ' '.join(cleaned_type.split())

    # Show the cleaned key
    print(f"[DEBUG] Cleaned primary_type for lookup: {repr(cleaned_type)}")
    print(f"[DEBUG] Dictionary keys: {list(FEW_SHOT_EXAMPLES.keys())}")
    print(f"[DEBUG] Key exists? {cleaned_type in FEW_SHOT_EXAMPLES}")

    # Lookup
    return FEW_SHOT_EXAMPLES.get(cleaned_type, FEW_SHOT_EXAMPLES['DEFAULT'])