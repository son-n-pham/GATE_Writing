# Add project root to path
import time
from pathlib import Path
import sys
import os
from datetime import datetime
import json
from src.grading_extraction import extract_grading_data_from_markdown_file
from test.grade_extraction.result import GRADING_FOR_TEST
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def evaluate_model_performance(model_name):
    """Compare extracted grades with reference results."""
    test_dir = "test/grade_extraction/md_data"
    results = []

    # Process each grading file
    for file_name in os.listdir(test_dir):
        if not (file_name.startswith('grading_') and file_name.endswith('.md')):
            continue

        student_name = file_name.replace('grading_', '').replace('.md', '')
        file_path = os.path.join(test_dir, file_name)

        try:
            # Get grades from model and reference
            extracted = extract_grading_data_from_markdown_file(
                file_path, model_name)
            reference = GRADING_FOR_TEST[student_name]

            # Compare categories
            comparison = {}
            for category in reference:
                matches = (
                    extracted[category]['marks'] == reference[category]['marks'] and
                    extracted[category]['total'] == reference[category]['total']
                )
                comparison[category] = {
                    'matches': matches,
                    'expected': reference[category],
                    'got': extracted[category]
                }

            results.append({
                'student': student_name,
                'categories': comparison
            })
        except Exception as e:
            print(f"Error processing {student_name}: {str(e)}")

    return results


def test_all_models(models_list):
    """Test multiple models and compare their grading accuracy."""
    model_results = {}

    for model in models_list:
        print(f"\nTesting model: {model}")
        try:
            results = []
            test_dir = "test/grade_extraction/md_data"
            model_start_time = time.time()

            for file_name in os.listdir(test_dir):
                if not (file_name.startswith('grading_') and file_name.endswith('.md')):
                    continue

                student_name = file_name.replace(
                    'grading_', '').replace('.md', '')
                file_path = os.path.join(test_dir, file_name)

                file_start_time = time.time()
                extracted = extract_grading_data_from_markdown_file(
                    file_path, model)
                file_execution_time = time.time() - file_start_time

                reference = GRADING_FOR_TEST[student_name]

                student_result = {
                    'student': student_name,
                    'matches': 0,
                    'total': 0,
                    'execution_time': file_execution_time,
                    'mismatches': []
                }

                for category in reference:
                    matches = (
                        extracted[category]['marks'] == reference[category]['marks'] and
                        extracted[category]['total'] == reference[category]['total']
                    )
                    student_result['total'] += 1
                    if matches:
                        student_result['matches'] += 1
                    else:
                        student_result['mismatches'].append({
                            'category': category,
                            'expected': reference[category],
                            'got': extracted[category]
                        })

                results.append(student_result)

            model_execution_time = time.time() - model_start_time
            total_comparisons = sum(r['total'] for r in results)
            total_matches = sum(r['matches'] for r in results)

            model_results[model] = {
                'accuracy': total_matches / total_comparisons if total_comparisons > 0 else 0,
                'total_comparisons': total_comparisons,
                'total_matches': total_matches,
                'execution_time': model_execution_time,
                'average_file_time': model_execution_time / len(results) if results else 0,
                'detailed_results': results
            }

        except Exception as e:
            print(f"Error testing model {model}: {str(e)}")
            model_results[model] = {'error': str(e)}

    return model_results


# Example usage:
models_to_test = [
    "phi3.5",
    "granite3.1-moe:1b",
    "granite3.1-dense:2b",
    "granite3.1-dense:latest",
    "llama3.2:latest",
    "minicpm-v:8b-2.6-q4_K_M",
    "vanilj/Phi-4:latest",
    "mistral",
    "phi3:3.8b-mini-4k-instruct-q8_0",
    "granite3.1-moe:3b-instruct-q8_0",
    "granite3.1-dense:8b-instruct-q5_K_M",
    "mistral-nemo:12b-instruct-2407-q4_K_M",
    "smallthinker:latest"
]

if __name__ == "__main__":
    results = test_all_models(models_to_test)

    # Save results to JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = os.path.join("test", "results")
    os.makedirs(results_dir, exist_ok=True)
    json_path = os.path.join(results_dir, f"model_comparison_{timestamp}.json")

    with open(json_path, 'w') as f:
        json.dump(results, f, indent=4)

    print(f"\nResults saved to: {json_path}")

    # Update results printing
    print("\nModel Comparison Results:")
    print("-" * 50)
    for model, data in results.items():
        print(f"\nModel: {model}")
        if 'error' in data:
            print(f"Error: {data['error']}")
        else:
            print(f"Accuracy: {data['accuracy']*100:.2f}%")
            print(
                f"Total matches: {data['total_matches']}/{data['total_comparisons']}")
            print(f"Total execution time: {data['execution_time']:.2f}s")
            print(f"Average time per file: {data['average_file_time']:.2f}s")
