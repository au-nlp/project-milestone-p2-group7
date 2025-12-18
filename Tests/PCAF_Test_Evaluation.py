"""
PCAF Evaluation Kernel (PCAF_TEST Script):

This final script is the Execution Orchestrator for the full PCAF experiment. It helped us to debug our prompt and make them better. It does not contain agent logic; its sole purpose is to run the iterative run_pcaf_on_problem loop on a test batch and manage the results.
Core Action: The script iterates over a defined test set (30 problems) and, for each, calls the primary control function: run_pcaf_on_problemn(problem_text, max_retries=3.
Data Capture (Analysis Focus): 
- It extracts and logs key metrics from the final attempt: is_correct: The boolean result of the final check_correctness score.
- text_attempts_used: The total turns the PCAF required (1 to 4).
- text_full_history_json: The entire interaction log (Solver traces, Verifier critiques, Planner instructions) is serialized and stored, providing the complete debugging record for analysis.

Final Metric: Calculates and prints the PCAF Accuracy, which is the primary measure of the framework's effectiveness."""

# --- START PCAF EVALUATION ---

# 1. Select the first 30 problems from the loaded DataFrame 'df'
test_subset = df.iloc[30:60].copy()
pcaf_results = []

print("=======================================================")
print(f"STARTING PCAF TEST ON Batch 1 {len(test_subset)} PROBLEMS (N=3 ITERATIONS MAX)")
print("=======================================================")

# 2. Loop over the test subset
for index, row in test_subset.iterrows():
    problem_id = row['problem_idx']
    problem_text = row['problem']
    problem_type = row['problem_type']
    problem_competition = row['competition']
    ground_truth = str(row['answer']) 

    print(f"\n--- RUNNING PCAF FOR PROBLEM {index + 1-30}/{len(test_subset)} (ID: {problem_id}) ---")
    print(f"--- [COMPETITION: {problem_competition}] ---")  # <--- PRINT COMPETITION NAME HERE
    
    # 3. Call the main PCAF loop function
    final_output, history = run_pcaf_on_problem(problem_text, max_retries=3)
    
    # 4. Analyze the results from the final attempt
    final_attempt = history[-1]
    final_solver_output = final_attempt['solution_text']
    
    final_extracted_answer = extract_answer(final_solver_output) 
    is_correct = check_correctness(final_extracted_answer, ground_truth)
    
    # 5. Summarize and store
    result_summary = {
        'problem_idx': problem_id,
        'problem_competition': problem_competition,
        'problem_type': problem_type,
        'ground_truth': ground_truth,
        'pcaf_answer': final_extracted_answer,
        'is_correct': is_correct,
        'attempts_used': len(history),
        'final_status': 'Verified' if is_correct else 'Failed',
        'final_verifier_valid': final_attempt['verifier_json'].get('valid', False) if final_attempt['verifier_json'] else 'N/A',
        # --- NEW LOGGING FIELD ---
        'full_history_json': json.dumps(history, indent=2) # Convert the history list to a readable JSON string
        # -------------------------
    }
    pcaf_results.append(result_summary)
    
    # Log summary for quick review during the run
    print(f"\nRESULTS: Correct? {'YES' if is_correct else 'NO'} | Attempts: {len(history)}")

print("\n=======================================================")
print("PCAF Test Complete. Generating Results DataFrame.")

# 6. Convert results to DataFrame and display summary
pcaf_results_df = pd.DataFrame(pcaf_results)

accuracy = pcaf_results_df['is_correct'].mean() * 100
print(f"\n--- Baseline Complete ---")
print(f"Accuracy: {accuracy:.2f}% ({pcaf_results_df['is_correct'].sum()}/{30})")

print("\nNEXT 30 PCAF Results Summary (including full history):")
print(pcaf_results_df[['problem_idx', 'problem_competition' ,'is_correct', 'attempts_used', 'pcaf_answer']])

# Save the results to a CSV file for documentation
pcaf_results_df.to_csv('andras_pcaf_test_results_hmmt_few_shot.csv', index=False) 
print("\nDetailed results saved to andras_pcaf_test_results_aime_more_corr2.csv")