#!/usr/bin/env python3
"""
Prompt Evaluator - Simple Entry Point

Evaluate your AI prompts with ease. This script generates test cases, 
runs your prompt against them, grades the outputs, and produces a report.

Usage:
    python evaluate.py
"""

from prompt_evaluation_engine import PromptEvaluator, add_user_message, chat


def main():
    """Main entry point for prompt evaluation."""
    
    print("=" * 70)
    print("PROMPT EVALUATOR")
    print("=" * 70)
    print()

    # User defines their evaluation task
    print("Define your evaluation task:")
    print("-" * 70)
    
    task_description = input("Describe the task your prompt should accomplish:\n> ").strip()
    if not task_description:
        print("Error: Task description cannot be empty.")
        return
    
    print()
    print("Define the input parameters for your prompt:")
    print("(Enter input_name: description. Type 'done' when finished)")
    print("-" * 70)
    
    prompt_inputs_spec = {}
    while True:
        user_input = input("> ").strip()
        if user_input.lower() == "done":
            break
        if ":" not in user_input:
            print("Format: input_name: description")
            continue
        key, value = user_input.split(":", 1)
        prompt_inputs_spec[key.strip()] = value.strip()
    
    if not prompt_inputs_spec:
        print("Error: At least one input parameter is required.")
        return
    
    num_cases = input("\nHow many test cases should be generated? (default: 3): ").strip()
    try:
        num_cases = int(num_cases) if num_cases else 3
    except ValueError:
        print("Invalid number. Using default: 3")
        num_cases = 3
    
    extra_criteria = input("\nAny extra grading criteria? (press Enter to skip):\n> ").strip()
    if not extra_criteria:
        extra_criteria = None
    
    print()
    print("=" * 70)
    print("GENERATING DATASET")
    print("=" * 70)
    print()
    
    # Initialize evaluator
    evaluator = PromptEvaluator(max_concurrent_tasks=1)
    
    # Generate dataset
    print(f"Generating {num_cases} test cases for: '{task_description}'")
    print()
    
    try:
        dataset = evaluator.generate_dataset(
            task_description=task_description,
            prompt_inputs_spec=prompt_inputs_spec,
            num_cases=num_cases,
            output_file="dataset.json",
        )
        print(f"\n✓ Dataset generated successfully ({len(dataset)} test cases)")
    except Exception as e:
        print(f"✗ Error generating dataset: {e}")
        return
    
    # Define the prompt function
    print()
    print("=" * 70)
    print("DEFINING YOUR PROMPT")
    print("=" * 70)
    print()
    print("Paste your prompt template below.")
    print("Use {input_name} placeholders for your input parameters.")
    print("(End with 'END_PROMPT' on a new line)")
    print("-" * 70)
    
    prompt_lines = []
    while True:
        line = input()
        if line.strip() == "END_PROMPT":
            break
        prompt_lines.append(line)
    
    prompt_template = "\n".join(prompt_lines)
    if not prompt_template.strip():
        print("Error: Prompt template cannot be empty.")
        return
    
    def run_prompt(prompt_inputs):
        """Execute the user's prompt with the given inputs."""
        try:
            # Replace placeholders with input values
            prompt = prompt_template
            for key, value in prompt_inputs.items():
                prompt = prompt.replace(f"{{{key}}}", str(value))
            
            messages = []
            add_user_message(messages, prompt)
            return chat(messages)
        except Exception as e:
            return f"Error running prompt: {str(e)}"
    
    # Run evaluation
    print()
    print("=" * 70)
    print("RUNNING EVALUATION")
    print("=" * 70)
    print()
    
    try:
        results = evaluator.run_evaluation(
            run_prompt_function=run_prompt,
            dataset_file="dataset.json",
            extra_criteria=extra_criteria,
            json_output_file="evaluation_results.json",
            html_output_file="evaluation_report.html",
        )
    except Exception as e:
        print(f"✗ Error running evaluation: {e}")
        return
    
    # Display results
    print()
    print("=" * 70)
    print("EVALUATION RESULTS")
    print("=" * 70)
    print()
    
    scores = [result["score"] for result in results]
    if scores:
        average_score = sum(scores) / len(scores)
        min_score = min(scores)
        max_score = max(scores)
        pass_count = sum(1 for s in scores if s >= 7)
        
        print(f"Total Test Cases: {len(results)}")
        print(f"Average Score:   {average_score:.1f} / 10")
        print(f"Min Score:       {min_score} / 10")
        print(f"Max Score:       {max_score} / 10")
        print(f"Pass Rate (≥7):  {pass_count}/{len(results)} ({100*pass_count/len(results):.1f}%)")
        print()
        print("Detailed results saved:")
        print("  - evaluation_results.json (detailed JSON results)")
        print("  - evaluation_report.html (interactive HTML report)")
    
    print()
    print("=" * 70)
    print("✓ Evaluation complete!")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nEvaluation cancelled by user.")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
