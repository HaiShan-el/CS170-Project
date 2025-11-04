"""
Report Generation Script for 8-Puzzle Project
Generates tables and charts like the project report guidelines

This script:
1. Runs all test cases with all algorithms
2. Generates comparison tables
3. Creates visualizations (bar charts and line charts)
4. Saves results as images

Requirements: matplotlib, numpy (optional)
Install: pip install matplotlib
"""

import time
from eight_puzzle import Problem, Heuristic, graph_search

# Test cases from project requirements
test_cases = {
    "Trivial": [[1, 2, 3], [4, 5, 6], [7, 8, 0]],
    "Very Easy": [[1, 2, 3], [4, 5, 6], [7, 0, 8]],
    "Easy": [[1, 2, 0], [4, 5, 3], [7, 8, 6]],
    "Doable": [[0, 1, 2], [4, 5, 3], [7, 8, 6]],
    "Oh Boy": [[8, 7, 1], [6, 0, 2], [5, 4, 3]],
    "Impossible": [[1, 2, 3], [4, 5, 6], [8, 7, 0]],
}

# Algorithms to test
algorithms = {
    "Uniform Cost Search": Heuristic.uniform_cost,
    "Misplaced Tile": Heuristic.misplaced_tile,
    "Manhattan Distance": Heuristic.manhattan_distance,
}


def run_all_tests():
    """Run all test cases with all algorithms."""
    results = {}
    
    print("Running comprehensive tests...")
    print("="*80)
    
    for test_name, initial_state in test_cases.items():
        print(f"\nTesting: {test_name}")
        problem = Problem(initial_state)
        
        # Check solvability
        if not problem.is_solvable(initial_state):
            print(f"  {test_name}: IMPOSSIBLE")
            results[test_name] = None
            continue
        
        results[test_name] = {}
        
        for algo_name, heuristic_func in algorithms.items():
            start_time = time.time()
            goal_node, nodes_expanded, max_queue_size = graph_search(problem, heuristic_func)
            elapsed_time = time.time() - start_time
            
            if goal_node:
                results[test_name][algo_name] = {
                    'depth': goal_node.g,
                    'nodes': nodes_expanded,
                    'max_queue': max_queue_size,
                    'time': elapsed_time
                }
                print(f"  {algo_name:25s}: Depth={goal_node.g:2d}, Nodes={nodes_expanded:6d}, MaxQ={max_queue_size:6d}")
    
    return results


def print_tables(results):
    """Print comparison tables."""
    solvable_cases = {k: v for k, v in results.items() if v is not None}
    
    if not solvable_cases:
        print("No solvable cases to display!")
        return
    
    # Table 1: Number of Nodes Expanded
    print("\n" + "="*100)
    print("Number of Nodes Expanded")
    print("="*100)
    print(f"{'':15s} {'Uniform Cost Search':>22s} {'Misplaced Tile':>22s} {'Manhattan Distance':>22s}")
    print("-"*100)
    
    for test_name in solvable_cases.keys():
        row = f"{test_name:15s}"
        for algo_name in algorithms.keys():
            if algo_name in solvable_cases[test_name]:
                nodes = solvable_cases[test_name][algo_name]['nodes']
                row += f"{nodes:>22d}"
            else:
                row += f"{'N/A':>22s}"
        print(row)
    
    # Table 2: Maximum Queue Size
    print("\n" + "="*100)
    print("Maximum Queue Size")
    print("="*100)
    print(f"{'':15s} {'Uniform Cost Search':>22s} {'Misplaced Tile':>22s} {'Manhattan Distance':>22s}")
    print("-"*100)
    
    for test_name in solvable_cases.keys():
        row = f"{test_name:15s}"
        for algo_name in algorithms.keys():
            if algo_name in solvable_cases[test_name]:
                max_q = solvable_cases[test_name][algo_name]['max_queue']
                row += f"{max_q:>22d}"
            else:
                row += f"{'N/A':>22s}"
        print(row)


def generate_charts(results):
    """Generate charts using matplotlib."""
    try:
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend
    except ImportError:
        print("\nWarning: error")
        return
    
    solvable_cases = {k: v for k, v in results.items() if v is not None}
    
    if not solvable_cases:
        print("No solvable cases to visualize!")
        return
    
    # Prepare data
    test_names = list(solvable_cases.keys())
    algo_names = list(algorithms.keys())
    
    # Data for nodes expanded
    nodes_data = {algo: [] for algo in algo_names}
    queue_data = {algo: [] for algo in algo_names}
    
    for test_name in test_names:
        for algo_name in algo_names:
            if algo_name in solvable_cases[test_name]:
                nodes_data[algo_name].append(solvable_cases[test_name][algo_name]['nodes'])
                queue_data[algo_name].append(solvable_cases[test_name][algo_name]['max_queue'])
            else:
                nodes_data[algo_name].append(0)
                queue_data[algo_name].append(0)
    
    # Chart 1: Line chart for Number of Nodes Expanded
    plt.figure(figsize=(12, 6))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    markers = ['o', 's', '^']
    
    for idx, algo_name in enumerate(algo_names):
        plt.plot(test_names, nodes_data[algo_name], 
                marker=markers[idx], 
                color=colors[idx], 
                label=algo_name,
                linewidth=2,
                markersize=8)
    
    plt.xlabel('Puzzle (Difficulty)', fontsize=12)
    plt.ylabel('Number of Nodes Expanded', fontsize=12)
    plt.title('Number of Nodes Expanded Per Puzzle', fontsize=14, fontweight='bold')
    plt.legend(loc='upper left', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('nodes_expanded_chart.png', dpi=150, bbox_inches='tight')
    print("\n[OK] Saved: nodes_expanded_chart.png")
    plt.close()
    
    # Chart 2: Line chart for Maximum Queue Size
    plt.figure(figsize=(12, 6))
    
    for idx, algo_name in enumerate(algo_names):
        plt.plot(test_names, queue_data[algo_name], 
                marker=markers[idx], 
                color=colors[idx], 
                label=algo_name,
                linewidth=2,
                markersize=8)
    
    plt.xlabel('Puzzle (Difficulty)', fontsize=12)
    plt.ylabel('Maximum Queue Size', fontsize=12)
    plt.title('Maximum Queue Size Per Puzzle', fontsize=14, fontweight='bold')
    plt.legend(loc='upper left', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('max_queue_chart.png', dpi=150, bbox_inches='tight')
    print("[OK] Saved: max_queue_chart.png")
    plt.close()
    
    # Chart 3: Stacked bar chart for Number of Nodes Expanded
    plt.figure(figsize=(12, 7))
    
    x_pos = range(len(test_names))
    bar_width = 0.25
    
    for idx, algo_name in enumerate(algo_names):
        offset = (idx - 1) * bar_width
        plt.bar([p + offset for p in x_pos], 
               nodes_data[algo_name], 
               bar_width,
               label=algo_name,
               color=colors[idx],
               alpha=0.8)
    
    plt.xlabel('Puzzle', fontsize=12)
    plt.ylabel('Number of Nodes Expanded', fontsize=12)
    plt.title('Number of Nodes Expanded', fontsize=14, fontweight='bold')
    plt.xticks(x_pos, test_names, rotation=0)
    plt.legend(loc='upper left', fontsize=10)
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('nodes_expanded_bar.png', dpi=150, bbox_inches='tight')
    print("[OK] Saved: nodes_expanded_bar.png")
    plt.close()
    
    # Chart 4: Comparison table as image
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis('tight')
    ax.axis('off')
    
    # Prepare table data
    table_data = [['Puzzle'] + algo_names]
    for test_name in test_names:
        row = [test_name]
        for algo_name in algo_names:
            if algo_name in solvable_cases[test_name]:
                row.append(str(solvable_cases[test_name][algo_name]['nodes']))
            else:
                row.append('N/A')
        table_data.append(row)
    
    table = ax.table(cellText=table_data, 
                    cellLoc='center',
                    loc='center',
                    colWidths=[0.15] * 4)
    
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2)
    
    # Style header row
    for i in range(len(table_data[0])):
        table[(0, i)].set_facecolor('#4472C4')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Style data rows
    for i in range(1, len(table_data)):
        for j in range(len(table_data[0])):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#E7E6E6')
    
    plt.title('Number of Nodes Expanded - Comparison Table', 
             fontsize=14, fontweight='bold', pad=20)
    plt.savefig('comparison_table.png', dpi=150, bbox_inches='tight')
    print("[OK] Saved: comparison_table.png")
    plt.close()
    
    print("\n" + "="*80)
    print("All charts generated successfully!")
    print("="*80)


def main():
    """Main function."""
    print("\n" + "="*80)
    print("8-PUZZLE PROJECT - REPORT GENERATION")
    print("="*80)
    
    # Run tests
    results = run_all_tests()
    
    # Print tables
    print_tables(results)
    
    # Generate charts
    print("\n" + "="*80)
    print("Generating charts...")
    print("="*80)
    generate_charts(results)
    
    print("\nReport generation complete!")
    print("Files generated:")
    print("  - nodes_expanded_chart.png")
    print("  - max_queue_chart.png")
    print("  - nodes_expanded_bar.png")
    print("  - comparison_table.png")


if __name__ == "__main__":
    main()

