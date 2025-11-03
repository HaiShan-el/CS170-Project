"""
Test script for 8-puzzle solver
Tests all the sample cases from the project requirements

Usage:
    python run_tests.py              # Run all tests with summary
    python run_tests.py --trace      # Run required trace for submission
    python run_tests.py --verbose    # Run all tests with detailed output
    python run_tests.py --quick      # Quick test with Manhattan Distance only
"""

import sys
import io
import time

from eight_puzzle import Problem, Heuristic, graph_search, print_state

# Test cases from project document
test_cases = {
    "Trivial": [[1, 2, 3], [4, 5, 6], [7, 8, 0]],
    "Very Easy": [[1, 2, 3], [4, 5, 6], [7, 0, 8]],
    "Easy": [[1, 2, 0], [4, 5, 3], [7, 8, 6]],
    "Doable": [[0, 1, 2], [4, 5, 3], [7, 8, 6]],
    "Oh Boy": [[8, 7, 1], [6, 0, 2], [5, 4, 3]],
    "Impossible": [[1, 2, 3], [4, 5, 6], [8, 7, 0]],
}

# Additional challenging test cases
extra_test_cases = {
    "Medium": [[1, 3, 0], [4, 2, 6], [7, 5, 8]],
    "Hard": [[2, 8, 1], [0, 4, 3], [7, 6, 5]],
    "Very Hard": [[5, 6, 7], [4, 0, 8], [3, 2, 1]],
}

# Required trace puzzle
required_trace = {
    "Required Trace": [[1, 0, 3], [4, 2, 6], [7, 5, 8]]
}

# All available algorithms
algorithms = {
    "Uniform Cost Search": Heuristic.uniform_cost,
    "Misplaced Tile": Heuristic.misplaced_tile,
    "Euclidean Distance": Heuristic.euclidean_distance,
    "Manhattan Distance": Heuristic.manhattan_distance,
}


def format_time(seconds):
    """Format time in human-readable format."""
    if seconds < 0.001:
        return f"{seconds*1000000:.0f}µs"
    elif seconds < 1:
        return f"{seconds*1000:.1f}ms"
    else:
        return f"{seconds:.2f}s"


def run_test(name, initial_state, heuristic_name, heuristic_func, verbose=False):
    """Run a single test case and return performance metrics."""
    problem = Problem(initial_state)
    
    # Check if solvable
    if not problem.is_solvable(initial_state):
        if verbose:
            print(f"  {heuristic_name}: IMPOSSIBLE (not solvable)")
        return None
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"Testing: {name} with {heuristic_name}")
        print(f"{'='*60}")
        print_state("Initial State:", initial_state)
        print()
    
    # Run the search and measure time
    start_time = time.time()
    goal_node, nodes_expanded, max_queue_size = graph_search(problem, heuristic_func)
    elapsed_time = time.time() - start_time
    
    if goal_node:
        depth = goal_node.g
        if verbose:
            print(f"\nGoal reached!")
            print(f"Solution depth: {depth}")
            print(f"Nodes expanded: {nodes_expanded}")
            print(f"Max queue size: {max_queue_size}")
            print(f"Time: {format_time(elapsed_time)}")
        return {
            'nodes_expanded': nodes_expanded,
            'max_queue_size': max_queue_size,
            'depth': depth,
            'time': elapsed_time,
            'solved': True
        }
    else:
        if verbose:
            print(f"\nNo solution found!")
        return {
            'nodes_expanded': nodes_expanded,
            'max_queue_size': max_queue_size,
            'depth': -1,
            'time': elapsed_time,
            'solved': False
        }


def run_all_tests(verbose=False, include_extra=False):
    """Run all test cases with all algorithms."""
    print("\n" + "="*80)
    print("COMPREHENSIVE TEST RESULTS")
    print("="*80)
    
    results = {}
    all_cases = dict(test_cases)
    if include_extra:
        all_cases.update(extra_test_cases)
    
    for test_name, initial_state in all_cases.items():
        print(f"\n{test_name}:")
        print_state("", initial_state)
        
        # Check solvability first
        problem = Problem(initial_state)
        if not problem.is_solvable(initial_state):
            print("  STATUS: ❌ IMPOSSIBLE (This puzzle cannot be solved)")
            continue
        
        print("  STATUS: ✓ Solvable")
        results[test_name] = {}
        
        for algo_name, heuristic_func in algorithms.items():
            result = run_test(test_name, initial_state, algo_name, heuristic_func, verbose=verbose)
            if result:
                results[test_name][algo_name] = result
                time_str = format_time(result['time'])
                print(f"  {algo_name:25s}: Depth={result['depth']:2d}, "
                      f"Nodes={result['nodes_expanded']:6d}, "
                      f"MaxQ={result['max_queue_size']:6d}, "
                      f"Time={time_str:>8s}")
    
    return results


def print_comparison_table(results):
    """Print a detailed comparison table of all results."""
    if not results:
        print("\nNo results to display!")
        return
    
    # Nodes Expanded Table
    print("\n" + "="*100)
    print("COMPARISON TABLE: Number of Nodes Expanded")
    print("="*100)
    
    header = f"{'Puzzle':<15s}"
    for algo_name in algorithms.keys():
        short_name = algo_name.replace(" Search", "").replace(" Distance", "")
        header += f"{short_name:>20s}"
    print(header)
    print("-"*100)
    
    for test_name in results.keys():
        row = f"{test_name:<15s}"
        for algo_name in algorithms.keys():
            if algo_name in results[test_name]:
                nodes = results[test_name][algo_name]['nodes_expanded']
                row += f"{nodes:>20d}"
            else:
                row += f"{'N/A':>20s}"
        print(row)
    
    # Maximum Queue Size Table
    print("\n" + "="*100)
    print("COMPARISON TABLE: Maximum Queue Size")
    print("="*100)
    print(header)
    print("-"*100)
    
    for test_name in results.keys():
        row = f"{test_name:<15s}"
        for algo_name in algorithms.keys():
            if algo_name in results[test_name]:
                queue = results[test_name][algo_name]['max_queue_size']
                row += f"{queue:>20d}"
            else:
                row += f"{'N/A':>20s}"
        print(row)
    
    # Execution Time Table
    print("\n" + "="*100)
    print("COMPARISON TABLE: Execution Time")
    print("="*100)
    print(header)
    print("-"*100)
    
    for test_name in results.keys():
        row = f"{test_name:<15s}"
        for algo_name in algorithms.keys():
            if algo_name in results[test_name]:
                time_val = results[test_name][algo_name]['time']
                row += f"{format_time(time_val):>20s}"
            else:
                row += f"{'N/A':>20s}"
        print(row)
    
    # Performance Summary
    print("\n" + "="*100)
    print("PERFORMANCE SUMMARY (Average across all solvable puzzles)")
    print("="*100)
    print(f"{'Algorithm':<25s} {'Avg Nodes':>12s} {'Avg MaxQ':>12s} {'Avg Time':>12s}")
    print("-"*100)
    
    for algo_name in algorithms.keys():
        total_nodes = 0
        total_queue = 0
        total_time = 0.0
        count = 0
        
        for test_name in results.keys():
            if algo_name in results[test_name]:
                total_nodes += results[test_name][algo_name]['nodes_expanded']
                total_queue += results[test_name][algo_name]['max_queue_size']
                total_time += results[test_name][algo_name]['time']
                count += 1
        
        if count > 0:
            avg_nodes = total_nodes / count
            avg_queue = total_queue / count
            avg_time = total_time / count
            print(f"{algo_name:<25s} {avg_nodes:>12.1f} {avg_queue:>12.1f} {format_time(avg_time):>12s}")


def test_required_trace():
    """Run the required trace for submission with detailed output."""
    print("\n" + "="*80)
    print("REQUIRED TRACE FOR SUBMISSION")
    print("Using Euclidean Distance Heuristic")
    print("="*80)
    
    name, initial_state = list(required_trace.items())[0]
    print_state("\nInitial State:", initial_state)
    print("\nTarget Goal State:")
    goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    print_state("", goal)
    
    # Check solvability
    problem = Problem(initial_state)
    if not problem.is_solvable(initial_state):
        print("\n❌ This puzzle is not solvable!")
        return
    
    print("\n✓ Puzzle is solvable")
    print("\n" + "-"*80)
    print("RUNNING SEARCH...")
    print("-"*80 + "\n")
    
    start_time = time.time()
    goal_node, nodes_expanded, max_queue_size = graph_search(
        problem, Heuristic.euclidean_distance
    )
    elapsed_time = time.time() - start_time
    
    if goal_node:
        print("\n" + "="*80)
        print("✓ SOLUTION FOUND!")
        print("="*80)
        print(f"\nSolution depth:      {goal_node.g}")
        print(f"Nodes expanded:      {nodes_expanded}")
        print(f"Maximum queue size:  {max_queue_size}")
        print(f"Execution time:      {format_time(elapsed_time)}")
        
        # Print solution path
        print("\n" + "-"*80)
        print("Solution path (sequence of moves):")
        print("-"*80)
        current = goal_node
        actions = []
        while current.parent:
            actions.append(current.action)
            current = current.parent
        actions.reverse()
        print(" → ".join(actions))
        
        # Print step-by-step solution
        print("\n" + "-"*80)
        print("Step-by-step solution:")
        print("-"*80)
        states = []
        current = goal_node
        while current:
            states.append((current.action, current.state))
            current = current.parent
        states.reverse()
        
        for i, (action, state) in enumerate(states):
            if action is None:
                print(f"\nStep 0: Initial State")
            else:
                print(f"\nStep {i}: Move blank {action}")
            print_state("", state)
    else:
        print("\n❌ No solution found!")


def quick_test():
    """Quick test with Manhattan Distance only (fastest heuristic)."""
    print("\n" + "="*80)
    print("QUICK TEST - Manhattan Distance Heuristic Only")
    print("="*80)
    
    results = {}
    
    for test_name, initial_state in test_cases.items():
        print(f"\n{test_name}:")
        print_state("", initial_state)
        
        problem = Problem(initial_state)
        if not problem.is_solvable(initial_state):
            print("  ❌ IMPOSSIBLE")
            continue
        
        start_time = time.time()
        goal_node, nodes_expanded, max_queue_size = graph_search(
            problem, Heuristic.manhattan_distance
        )
        elapsed_time = time.time() - start_time
        
        if goal_node:
            print(f"  ✓ Depth={goal_node.g}, Nodes={nodes_expanded}, "
                  f"MaxQ={max_queue_size}, Time={format_time(elapsed_time)}")
            results[test_name] = {
                'depth': goal_node.g,
                'nodes': nodes_expanded,
                'max_q': max_queue_size,
                'time': elapsed_time
            }
        else:
            print(f"  ❌ No solution found")
    
    return results


def test_solvability():
    """Test the solvability checker with known solvable and unsolvable puzzles."""
    print("\n" + "="*80)
    print("SOLVABILITY TEST")
    print("="*80)
    
    solvable_puzzles = [
        ("Trivial", [[1, 2, 3], [4, 5, 6], [7, 8, 0]]),
        ("Easy", [[1, 2, 0], [4, 5, 3], [7, 8, 6]]),
        ("Very Easy", [[1, 2, 3], [4, 5, 6], [7, 0, 8]]),
    ]
    
    unsolvable_puzzles = [
        ("Impossible", [[1, 2, 3], [4, 5, 6], [8, 7, 0]]),
        ("Swapped", [[1, 2, 3], [4, 5, 6], [8, 0, 7]]),
    ]
    
    print("\nTesting solvable puzzles (should all return True):")
    print("-" * 80)
    all_correct = True
    for name, state in solvable_puzzles:
        problem = Problem(state)
        is_solvable = problem.is_solvable(state)
        status = "✓ PASS" if is_solvable else "❌ FAIL"
        print(f"{name:15s}: {status} (is_solvable={is_solvable})")
        if not is_solvable:
            all_correct = False
    
    print("\nTesting unsolvable puzzles (should all return False):")
    print("-" * 80)
    for name, state in unsolvable_puzzles:
        problem = Problem(state)
        is_solvable = problem.is_solvable(state)
        status = "✓ PASS" if not is_solvable else "❌ FAIL"
        print(f"{name:15s}: {status} (is_solvable={is_solvable})")
        if is_solvable:
            all_correct = False
    
    print("\n" + "="*80)
    if all_correct:
        print("✓ All solvability tests passed!")
    else:
        print("❌ Some solvability tests failed!")
    print("="*80)


def main():
    """Main entry point for the test suite."""
    import sys
    
    # Set UTF-8 encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg == "--trace":
            # Run required trace for submission
            test_required_trace()
        
        elif arg == "--verbose":
            # Run all tests with detailed output
            results = run_all_tests(verbose=True)
            print_comparison_table(results)
        
        elif arg == "--quick":
            # Quick test with Manhattan Distance only
            quick_test()
        
        elif arg == "--solvability":
            # Test solvability checker
            test_solvability()
        
        elif arg == "--extra":
            # Run all tests including extra challenging cases
            results = run_all_tests(verbose=False, include_extra=True)
            print_comparison_table(results)
        
        elif arg == "--help" or arg == "-h":
            print("\n" + "="*80)
            print("8-Puzzle Test Suite - Usage")
            print("="*80)
            print("\nUsage: python run_tests.py [option]")
            print("\nOptions:")
            print("  (none)          Run all standard tests with summary and comparison tables")
            print("  --trace         Run required trace for submission (Euclidean Distance)")
            print("  --verbose       Run all tests with detailed output")
            print("  --quick         Quick test with Manhattan Distance only (fastest)")
            print("  --extra         Include extra challenging test cases")
            print("  --solvability   Test the solvability checker")
            print("  --help, -h      Show this help message")
            print("\nExamples:")
            print("  python run_tests.py")
            print("  python run_tests.py --trace")
            print("  python run_tests.py --quick")
            print("="*80 + "\n")
        
        else:
            print(f"\nUnknown option: {sys.argv[1]}")
            print("Use --help or -h to see available options.\n")
    
    else:
        # Default: Run all tests with summary and comparison tables
        print("\n" + "="*80)
        print("8-PUZZLE SOLVER - COMPREHENSIVE TEST SUITE")
        print("="*80)
        print("\nRunning all standard test cases with all algorithms...")
        print("(Use --help to see more options)")
        
        results = run_all_tests(verbose=False)
        print_comparison_table(results)
        
        print("\n" + "="*80)
        print("Test suite completed!")
        print("="*80)
        print("\nTip: Use 'python run_tests.py --trace' to generate the required trace.")


if __name__ == "__main__":
    main()




