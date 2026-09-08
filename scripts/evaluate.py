import json
from ask import ask

test_questions = "eval/test_questions.json"

def run_eval(test_file):
    with open(test_file, "r") as file:
        test_cases = json.load(file)


    results = []
    for case in test_cases:
        res = ask(case["question"])

        results.append({
            "question": case["question"],
            "expected": case["expected_answer"],
            "actual": res
        })

    return results

def print_results(results):
    print(f"\nEval Results:\n")
    for r in results:
        print(f"Question: {r["question"]}\n")
        print(f"Expected Response: {r["expected"]}\n")
        print(f"Actual Response: {r["actual"]}\n")
        print("\n")

if __name__ == "__main__":
    results = run_eval(test_questions)
    print_results(results)
