"""
8-Puzzle Solver 
CS 170 Project 1

This version implements:
- Node and Problem classes
- Multiple search algorithms (Uniform Cost Search, A* with various heuristics)
- Heuristic functions (Misplaced Tile, Manhattan Distance, Euclidean Distance)
- Solvability checking
"""

import heapq
import math
from copy import deepcopy


class Node:
    """Represents a node in the search tree."""
    
    def __init__(self, state, parent=None, operator=None, depth=0, path_cost=0, heuristic_cost=0):
        self.state = state
        self.parent = parent
        self.operator = operator
        self.action = operator  # Alias for compatibility
        self.depth = depth
        self.path_cost = path_cost
        self.heuristic_cost = heuristic_cost
    
    def __lt__(self, other):
        """Compare nodes based on f value for priority queue."""
        return self.f < other.f
    
    @property
    def g(self):
        """Return the cost from start to this node."""
        return self.depth
    
    @property
    def h(self):
        """Return the heuristic cost."""
        return self.heuristic_cost
    
    @property
    def f(self):
        """Return the evaluation function f(n) = g(n) + h(n)."""
        return self.g + self.h


class Problem:
    """Defines the 8-Puzzle problem."""
    
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    
    def operators(self, state):
        """Return list of valid operators for the current state."""
        ops = []
        blank_row, blank_col = self._find_blank(state)
        
        if blank_row > 0:
            ops.append("up")
        if blank_row < 2:
            ops.append("down")
        if blank_col > 0:
            ops.append("left")
        if blank_col < 2:
            ops.append("right")
        
        return ops
    
    def result(self, state, operator):
        """Return the state that results from applying the operator."""
        new_state = deepcopy(state)
        blank_row, blank_col = self._find_blank(state)
        
        # Determine new position of blank
        if operator == "up":
            new_row, new_col = blank_row - 1, blank_col
        elif operator == "down":
            new_row, new_col = blank_row + 1, blank_col
        elif operator == "left":
            new_row, new_col = blank_row, blank_col - 1
        elif operator == "right":
            new_row, new_col = blank_row, blank_col + 1
        else:
            return new_state
        
        # Swap blank with tile
        new_state[blank_row][blank_col] = new_state[new_row][new_col]
        new_state[new_row][new_col] = 0
        
        return new_state
    
    def goal_test(self, state):
        """Check if the state is the goal state."""
        return state == self.goal_state
    
    def is_solvable(self, state):
        """
        Check if the puzzle is solvable.
        A puzzle is solvable if the number of inversions is even.
        """
        # Flatten the state, ignoring the blank
        tiles = []
        for row in state:
            for tile in row:
                if tile != 0:
                    tiles.append(tile)
        
        # Count inversions
        inversions = 0
        for i in range(len(tiles)):
            for j in range(i + 1, len(tiles)):
                if tiles[i] > tiles[j]:
                    inversions += 1
        
        return inversions % 2 == 0
    
    def _find_blank(self, state):
        """Find the position of the blank (0) in the state."""
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return i, j
        return None, None


class Heuristic:
    """Collection of heuristic functions for A* search."""
    
    @staticmethod
    def uniform_cost(state):
        """Uniform cost heuristic (always returns 0) - equivalent to Dijkstra's algorithm."""
        return 0
    
    @staticmethod
    def misplaced_tile(state):
        """
        Count the number of misplaced tiles (excluding the blank).
        This is an admissible heuristic because each misplaced tile must be moved at least once.
        """
        goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        count = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != 0 and state[i][j] != goal[i][j]:
                    count += 1
        return count
    
    @staticmethod
    def manhattan_distance(state):
        """
        Calculate Manhattan distance for all tiles (excluding the blank).
        Manhattan distance is the sum of horizontal and vertical distances.
        This is an admissible and consistent heuristic.
        """
        distance = 0
        for i in range(3):
            for j in range(3):
                value = state[i][j]
                if value != 0:
                    # Calculate goal position for this value
                    goal_i = (value - 1) // 3
                    goal_j = (value - 1) % 3
                    distance += abs(i - goal_i) + abs(j - goal_j)
        return distance
    
    @staticmethod
    def euclidean_distance(state):
        """
        Calculate Euclidean distance for all tiles (excluding the blank).
        Euclidean distance is the straight-line distance.
        This is an admissible heuristic.
        """
        distance = 0.0
        for i in range(3):
            for j in range(3):
                value = state[i][j]
                if value != 0:
                    # Calculate goal position for this value
                    goal_i = (value - 1) // 3
                    goal_j = (value - 1) % 3
                    distance += math.sqrt((i - goal_i)**2 + (j - goal_j)**2)
        return distance


def graph_search(problem, heuristic_func=None):
    """
    A* graph search algorithm with support for different heuristics.
    If no heuristic is provided, defaults to uniform cost search.
    
    Returns:
        tuple: (goal_node, nodes_expanded, max_queue_size)
    """
    if heuristic_func is None:
        heuristic_func = Heuristic.uniform_cost
    
    # Initialize
    h_initial = heuristic_func(problem.initial_state)
    initial_node = Node(problem.initial_state, None, None, 0, 0, h_initial)
    frontier = [(initial_node.f, 0, initial_node)]  # (f, counter, node)
    explored = set()
    counter = 1
    nodes_expanded = 0
    max_queue_size = 1
    
    while frontier:
        # Get node with lowest f value
        _, _, node = heapq.heappop(frontier)
        
        # Goal test
        if problem.goal_test(node.state):
            return node, nodes_expanded, max_queue_size
        
        # Add to explored set
        state_tuple = tuple(map(tuple, node.state))
        if state_tuple in explored:
            continue
        explored.add(state_tuple)
        nodes_expanded += 1
        
        # Expand node
        for operator in problem.operators(node.state):
            child_state = problem.result(node.state, operator)
            child_state_tuple = tuple(map(tuple, child_state))
            
            if child_state_tuple not in explored:
                h_cost = heuristic_func(child_state)
                child_node = Node(
                    child_state,
                    node,
                    operator,
                    node.depth + 1,
                    node.path_cost + 1,
                    h_cost
                )
                heapq.heappush(frontier, (child_node.f, counter, child_node))
                counter += 1
        
        # Update max queue size
        max_queue_size = max(max_queue_size, len(frontier))
    
    # No solution found
    return None, nodes_expanded, max_queue_size


def uniform_cost_search(problem):
    """
    Uniform Cost Search (Dijkstra) algorithm.
    This is a special case of A* with h(n) = 0.
    """
    return graph_search(problem, Heuristic.uniform_cost)


def print_state(label, state):
    """
    Print the puzzle state in a readable format.
    
    Args:
        label: Optional label to print before the state (can be empty string)
        state: The puzzle state to print
    """
    if label:
        print(label)
    for row in state:
        print(" ".join("b" if x == 0 else str(x) for x in row))


def print_solution(goal_node):
    """Print the solution path from initial to goal state."""
    if not goal_node:
        print("No solution found!")
        return
    
    # Collect path
    path = []
    node = goal_node
    while node.parent:
        path.append((node.operator, node.state))
        node = node.parent
    path.reverse()
    
    # Print initial state
    print("\nInitial State:")
    print_state("", node.state)
    
    # Print each step
    for i, (operator, state) in enumerate(path, 1):
        print(f"\nStep {i}: Move blank {operator}")
        print_state("", state)
    
    print(f"\nGoal reached in {goal_node.depth} steps!")


def compare_algorithms(initial_state):
    """Compare different heuristic functions on a given puzzle."""
    problem = Problem(initial_state)
    
    # Check solvability first
    if not problem.is_solvable(initial_state):
        print("This puzzle is not solvable!")
        return
    
    algorithms = [
        ("Uniform Cost Search", Heuristic.uniform_cost),
        ("Misplaced Tile", Heuristic.misplaced_tile),
        ("Euclidean Distance", Heuristic.euclidean_distance),
        ("Manhattan Distance", Heuristic.manhattan_distance),
    ]
    
    print("\nAlgorithm Comparison:")
    print("=" * 80)
    print(f"{'Algorithm':<25} {'Depth':>6} {'Nodes':>8} {'Max Queue':>10} {'Time':>8}")
    print("-" * 80)
    
    import time
    for name, heuristic in algorithms:
        start_time = time.time()
        goal, nodes, max_q = graph_search(problem, heuristic)
        elapsed = time.time() - start_time
        
        if goal:
            print(f"{name:<25} {goal.depth:>6} {nodes:>8} {max_q:>10} {elapsed:>7.4f}s")
        else:
            print(f"{name:<25} {'N/A':>6} {nodes:>8} {max_q:>10} {elapsed:>7.4f}s")


def main():
    """Main function for interactive use."""
    print("=" * 80)
    print("8-Puzzle Solver - A* Search with Multiple Heuristics")
    print("=" * 80)
    
    # Example puzzle (Easy difficulty)
    initial_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 0, 8]
    ]
    
    print("\nSolving puzzle:")
    print_state("", initial_state)
    
    # Create problem and check solvability
    problem = Problem(initial_state)
    if not problem.is_solvable(initial_state):
        print("\nThis puzzle is not solvable!")
        return
    
    # Compare all algorithms
    compare_algorithms(initial_state)
    
    # Solve with Manhattan Distance and show solution path
    print("\n" + "=" * 80)
    print("Detailed Solution using Manhattan Distance Heuristic:")
    print("=" * 80)
    goal_node, nodes_expanded, max_queue = graph_search(problem, Heuristic.manhattan_distance)
    
    if goal_node:
        print(f"\nSolution found!")
        print(f"Nodes expanded: {nodes_expanded}")
        print(f"Max queue size: {max_queue}")
        print_solution(goal_node)
    else:
        print("\nNo solution found!")


if __name__ == "__main__":
    main()


