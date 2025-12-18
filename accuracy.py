import pandas as pd
import glob
import ast
import os

def calculate_competition_metrics(file_pattern="PCAF_*.csv"):
    files = glob.glob(file_pattern)
    results = []

    for file in files:
        df = pd.read_csv(file)
        
        # 1. Calculate Accuracy (Mean of final_score)
        accuracy = df['final_score'].mean()
        
        # 2. Parse lists for advanced metrics (Recovery Rate & Avg Turns)
        def safe_eval(val):
            try: return ast.literal_eval(val)
            except: return []

        scores_list = df['pcaf_scores'].apply(safe_eval)
        turns_list = df['pcaf_turns'].apply(safe_eval)
        
        initial_fails = 0
        recovered_runs = 0
        all_turns = []
        
        for row_scores, row_turns in zip(scores_list, turns_list):
            for score, turn in zip(row_scores, row_turns):
                all_turns.append(turn)
                # A "Recovery" is a successful attempt (score=1) that failed on Turn 1 (turn > 1)
                if turn > 1:
                    initial_fails += 1
                    if score == 1:
                        recovered_runs += 1
        
        recovery_rate = recovered_runs / initial_fails if initial_fails > 0 else 0
        avg_turns = sum(all_turns) / len(all_turns) if all_turns else 0
        
        # Extract name and clean up
        comp_name = os.path.basename(file).replace("PCAF_Final_Result_", "").replace(".csv", "").upper()
        
        results.append({
            "Competition": comp_name,
            "Accuracy": f"{accuracy:.2%}",
            "Avg Turns": round(avg_turns, 2),
            "Recovery Rate": f"{recovery_rate:.1%}"
        })

    return pd.DataFrame(results).sort_values("Competition")

# Run and display
results_df = calculate_competition_metrics()
print(results_df.to_string(index=False))