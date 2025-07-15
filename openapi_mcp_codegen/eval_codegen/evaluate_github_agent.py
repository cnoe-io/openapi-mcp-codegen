"""
Standalone GitHub Agent Evaluation Script

This script evaluates the GitHub agent in isolation using:
- Custom YAML dataset with realistic test cases
- Mini LangGraph with only GitHub agent
- Trajectory matching, correctness, and hallucination evaluation
- Test categorization by type (basic_functionality, tool_trajectory, completeness, hallucination)
"""

import yaml
import asyncio
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional

# Add parent directories to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from agentevals.trajectory.match import create_trajectory_match_evaluator
from openevals.llm import create_llm_as_judge
from openevals.prompts import CORRECTNESS_PROMPT, HALLUCINATION_PROMPT

from jarvis_agent.llm_factory import JarvisLLMFactory
from jarvis_agent.github_agent.eval.github_mini_graph import generate_github_trajectory

# Set up evaluators
hallucination_evaluator = create_llm_as_judge(
    prompt=HALLUCINATION_PROMPT,
    feedback_key="hallucination",
    judge=JarvisLLMFactory("gpt-4o-mini").get_llm_connection(),
    continuous=True  # Return float score 0.0-1.0 instead of boolean
)

correctness_evaluator = create_llm_as_judge(
    prompt=CORRECTNESS_PROMPT,
    feedback_key="correctness",
    judge=JarvisLLMFactory("gpt-4o-mini").get_llm_connection(),
    continuous=True  # Return float score 0.0-1.0 instead of boolean
)

trajectory_match_evaluator_unordered = create_trajectory_match_evaluator(
    trajectory_match_mode="unordered",
)

trajectory_match_evaluator_strict = create_trajectory_match_evaluator(
    trajectory_match_mode="strict",
)


def convert_simple_trajectory_to_detailed(simple_trajectory):
    """
    Convert simple semicolon-separated trajectory to detailed format expected by evaluators.

    Args:
        simple_trajectory (list): List of node names like ['__start__', 'github_agent', 'github_tools', 'github_agent', '__end__']

    Returns:
        list: List of detailed trajectory dictionaries
    """
    detailed_trajectory = []

    for node in simple_trajectory:
        detailed_trajectory.append({
            'role': "system",
            'agent': node,
            'content': "",
        })

    return detailed_trajectory


def load_github_dataset(test_type_filter: Optional[str] = None):
    """Load the GitHub agent test dataset from YAML with optional filtering by test type."""
    dataset_path = Path(__file__).parent / "github_agent_dataset.yaml"

    with open(dataset_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    test_cases = []
    for test_id, test_data in data['tests'].items():
        # Skip if test type filter is specified and doesn't match
        test_type = test_data.get('test_type', 'basic_functionality')
        if test_type_filter and test_type != test_type_filter:
            continue

        # Convert semicolon-separated trajectory to list
        simple_trajectory = test_data['reference_trajectory']['solution_1'].split(';')
        # Convert to detailed format expected by evaluators
        detailed_trajectory = convert_simple_trajectory_to_detailed(simple_trajectory)

        test_cases.append({
            'test_id': test_id,
            'input': test_data['input'],
            'test_type': test_type,
            'reference_trajectory': detailed_trajectory,
            'reference_output': test_data['reference_output'].strip(),
            'metadata': test_data.get('metadata', {}),
            'focus': test_data.get('metadata', {}).get('focus', '')
        })

    return test_cases


class GitHubAgentEvaluationResult:
    """Container for evaluation results."""

    def __init__(self, test_id: str, test_type: str):
        self.test_id = test_id
        self.test_type = test_type
        self.trajectory_match_unordered_score = None
        self.trajectory_match_strict_score = None
        self.correctness_score = None
        self.hallucination_score = None
        self.actual_trajectory = None
        self.actual_output = None
        self.error = None
        self.warnings = []
        self.focus_area_passed = None  # Specific to the test's focus area


def evaluate_test_type_specific_criteria(result: GitHubAgentEvaluationResult, test_case: Dict) -> List[str]:
    """Evaluate criteria and return warnings for scores below 0.5."""
    warnings = []

    # Check if any score is below 0.5 threshold
    if result.trajectory_match_strict_score < 0.5:
        warnings.append(f"🎯 Trajectory score below threshold: {result.trajectory_match_strict_score:.2f} < 0.5")

    if result.correctness_score < 0.5:
        warnings.append(f"✅ Correctness score below threshold: {result.correctness_score:.2f} < 0.5")

    if result.hallucination_score < 0.5:
        warnings.append(f"🚫 Hallucination score below threshold: {result.hallucination_score:.2f} < 0.5")

    # Test passes if all scores are >= 0.5
    result.focus_area_passed = (result.trajectory_match_strict_score >= 0.5 and
                              result.correctness_score >= 0.5 and
                              result.hallucination_score >= 0.5)

    return warnings


async def evaluate_single_test(test_case):
    """Evaluate a single test case with test-type-specific criteria."""
    test_type = test_case['test_type']
    print(f"🧪 {test_case['test_id']} [{test_type.upper()}]")

    result = GitHubAgentEvaluationResult(test_case['test_id'], test_type)

    try:
        # Set dry run mode for testing
        os.environ["JARVIS_DRYRUN"] = "true"

        # Generate trajectory and output
        trajectory, output = await generate_github_trajectory(test_case['input'])

        result.actual_trajectory = trajectory
        result.actual_output = output

        # Evaluate trajectory matching - convert to numeric scores
        try:
            trajectory_result = trajectory_match_evaluator_unordered(
                outputs=trajectory,
                reference_outputs=test_case['reference_trajectory'],
            )
            result.trajectory_match_unordered_score = 1.0 if trajectory_result['score'] else 0.0
        except Exception:
            result.trajectory_match_unordered_score = 0.0

        try:
            trajectory_result = trajectory_match_evaluator_strict(
                outputs=trajectory,
                reference_outputs=test_case['reference_trajectory'],
            )
            result.trajectory_match_strict_score = 1.0 if trajectory_result['score'] else 0.0
        except Exception:
            result.trajectory_match_strict_score = 0.0

        # Evaluate correctness
        correctness_result = correctness_evaluator(
            inputs=test_case['input'],
            outputs=output,
            reference_outputs=test_case['reference_output'],
        )
        result.correctness_score = correctness_result['score']

        # Evaluate hallucination
        hallucination_result = hallucination_evaluator(
            inputs=test_case['input'],
            outputs=output,
            context=test_case['reference_trajectory'],
            reference_outputs=test_case['reference_output'],
        )
        result.hallucination_score = hallucination_result['score']

        # Generate test-type-specific warnings
        warnings = evaluate_test_type_specific_criteria(result, test_case)
        result.warnings = warnings

        # Print warnings only if test failed
        if warnings and not result.focus_area_passed:
            for warning in warnings:
                print(f"   {warning}")

    except Exception as e:
        result.error = str(e)
        print(f"❌ ERROR: {e}")

    return result


async def run_github_agent_evaluation(test_id: str = None, test_type: str = None):
    """Run the complete GitHub agent evaluation with optional filtering."""
    print("🚀 GitHub Agent Evaluation")
    print("=" * 50)

    # Load test cases with optional filtering
    test_cases = load_github_dataset(test_type_filter=test_type)

    # Filter by test_id if specified
    if test_id:
        test_cases = [tc for tc in test_cases if tc['test_id'] == test_id]
        if not test_cases:
            print(f"❌ Test '{test_id}' not found!")
            return []
        print(f"📊 Running: {test_id}")
    else:
        if test_type:
            print(f"📊 Running {len(test_cases)} {test_type} tests")
        else:
            print(f"📊 Running {len(test_cases)} tests")

    print()  # Empty line before tests

    # Run evaluations
    results = []
    for test_case in test_cases:
        result = await evaluate_single_test(test_case)
        results.append(result)

    # Calculate overall scores
    print("\n" + "=" * 50)
    print("📈 RESULTS")
    print("=" * 50)

    valid_results = [r for r in results if not r.error]

    if valid_results:
        # Calculate overall average score (0-1)
        total_trajectory = sum(r.trajectory_match_strict_score for r in valid_results) / len(valid_results)
        total_correctness = sum(r.correctness_score for r in valid_results) / len(valid_results)
        total_hallucination = sum(r.hallucination_score for r in valid_results) / len(valid_results)

        # Overall score is average of all metrics
        overall_score = (total_trajectory + total_correctness + total_hallucination) / 3

        # Focus area pass rate
        focus_pass_rate = sum(1 for r in valid_results if r.focus_area_passed) / len(valid_results)

        print(f"🏆 Overall Score: {overall_score:.3f}/1.000")
        print(f"🎯 Focus Area Pass Rate: {focus_pass_rate:.3f} ({sum(1 for r in valid_results if r.focus_area_passed)}/{len(valid_results)})")
        print()
        print("📊 Component Scores:")
        print(f"   Trajectory: {total_trajectory:.3f}")
        print(f"   Correctness: {total_correctness:.3f}")
        print(f"   Hallucination: {total_hallucination:.3f}")

        # Show tests with errors
        error_tests = [r for r in results if r.error]
        if error_tests:
            print(f"\n💥 Error Tests ({len(error_tests)}):")
            for result in error_tests:
                print(f"   💥 {result.test_id}: {result.error}")
    else:
        print("❌ No valid results")
        overall_score = 0.0

    print(f"\n🎯 FINAL SCORE: {overall_score:.3f}")
    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="GitHub Agent Evaluation")
    parser.add_argument("--test-id", help="Run specific test case")
    parser.add_argument("--test-type", help="Filter by test type",
                       choices=["basic_functionality", "tool_trajectory", "completeness", "hallucination"])

    args = parser.parse_args()

    # Run standalone evaluation with optional filtering
    asyncio.run(run_github_agent_evaluation(args.test_id, args.test_type))