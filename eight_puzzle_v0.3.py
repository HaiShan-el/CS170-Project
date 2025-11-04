"""
8-Puzzle Solver v0.3
CS 170 Project 1

This version adds:
- Interactive command-line interface
- Step-by-step trace with g(n) and h(n) values
- Comprehensive testing and visualization support
"""

import heapq
import math
from copy import deepcopy

# 请修改为您的学号
STUDENT_ID = "XXX"


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
        
        new_state[blank_row][blank_col] = new_state[new_row][new_col]
        new_state[new_row][new_col] = 0
        
        return new_state
    
    def goal_test(self, state):
        """Check if the state is the goal state."""
        return state == self.goal_state
    
    def is_solvable(self, state):
        """Check if the puzzle is solvable using inversion count."""
        flat = [num for row in state for num in row if num != 0]
        inversions = 0
        for i in range(len(flat)):
            for j in range(i + 1, len(flat)):
                if flat[i] > flat[j]:
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
        """Uniform cost heuristic (always returns 0)."""
        return 0
    
    @staticmethod
    def misplaced_tile(state):
        """Count the number of misplaced tiles."""
        goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        count = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != 0 and state[i][j] != goal[i][j]:
                    count += 1
        return count
    
    @staticmethod
    def euclidean_distance(state):
        """Calculate Euclidean distance for all tiles."""
        distance = 0.0
        for i in range(3):
            for j in range(3):
                value = state[i][j]
                if value != 0:
                    goal_i = (value - 1) // 3
                    goal_j = (value - 1) % 3
                    distance += math.sqrt((i - goal_i)**2 + (j - goal_j)**2)
        return distance
    
    @staticmethod
    def manhattan_distance(state):
        """Calculate Manhattan distance for all tiles."""
        distance = 0
        for i in range(3):
            for j in range(3):
                value = state[i][j]
                if value != 0:
                    goal_i = (value - 1) // 3
                    goal_j = (value - 1) % 3
                    distance += abs(i - goal_i) + abs(j - goal_j)
        return distance


def graph_search_with_trace(problem, heuristic_func, show_trace=True):
    """
    A* graph search algorithm with detailed trace.
    
    Args:
        problem: Problem instance
        heuristic_func: Heuristic function to use
        show_trace: Whether to show detailed trace
    
    Returns:
        Tuple of (goal_node, nodes_expanded, max_queue_size)
    """
    h_initial = heuristic_func(problem.initial_state)
    initial_node = Node(problem.initial_state, None, None, 0, 0, h_initial)
    frontier = [(initial_node.f, 0, initial_node)]
    explored = set()
    counter = 1
    nodes_expanded = 0
    max_queue_size = 1
    
    while frontier:
        _, _, node = heapq.heappop(frontier)
        
        # Goal test
        if problem.goal_test(node.state):
            return node, nodes_expanded, max_queue_size
        
        # Skip if already explored
        state_tuple = tuple(map(tuple, node.state))
        if state_tuple in explored:
            continue
        explored.add(state_tuple)
        
        # Print trace
        if show_trace:
            print(f"\nThe best state to expand with g(n) = {node.g} and h(n) = {node.h:.0f} is...")
            for row in node.state:
                print(" ".join("b" if x == 0 else str(x) for x in row))
            print("     Expanding this node...")
        
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
        
        max_queue_size = max(max_queue_size, len(frontier))
    
    return None, nodes_expanded, max_queue_size


def graph_search(problem, heuristic_func):
    """A* graph search without trace (for testing)."""
    return graph_search_with_trace(problem, heuristic_func, show_trace=False)


def get_default_puzzle():
    """Return a default puzzle."""
    return [[1, 2, 3], [4, 8, 0], [7, 6, 5]]


def get_user_puzzle():
    """Get puzzle from user input."""
    print("\nEnter your puzzle, use a zero to represent the blank")
    
    puzzle = []
    row_names = ["first", "second", "third"]
    
    for i in range(3):
        while True:
            try:
                row_input = input(f"Enter the {row_names[i]} row, use space or tabs between numbers\n")
                row = [int(x) for x in row_input.split()]
                
                if len(row) != 3:
                    print("Error: Please enter exactly 3 numbers")
                    continue
                if any(x < 0 or x > 8 for x in row):
                    print("Error: Numbers must be between 0 and 8")
                    continue
                
                puzzle.append(row)
                break
            except ValueError:
                print("Error: Please enter valid numbers")
    
    return puzzle


def get_algorithm_choice():
    """Get user's algorithm choice."""
    print("\nEnter your choice of algorithm")
    print("  1. Uniform Cost Search")
    print("  2. A* with the Misplaced Tile heuristic.")
    print("  3. A* with the Euclidean distance heuristic.")
    
    while True:
        try:
            choice = input()
            choice = int(choice)
            if choice in [1, 2, 3]:
                return choice
            else:
                print("Invalid choice. Please enter 1, 2, or 3")
        except ValueError:
            print("Invalid input. Please enter a number (1, 2, or 3)")


def main():
    """Interactive main function."""
    print(f"Welcome to {STUDENT_ID} (change this to your student ID) 8 puzzle solver.")
    print('Type "1" to use a default puzzle, or "2" to enter your own puzzle.')
    
    # Step 1: Get puzzle
    while True:
        try:
            choice = input()
            choice = int(choice)
            if choice == 1:
                initial_state = get_default_puzzle()
                print("\nUsing default puzzle:")
                for row in initial_state:
                    print(" ".join(str(x) for x in row))
                break
            elif choice == 2:
                initial_state = get_user_puzzle()
                print("\nYour puzzle:")
                for row in initial_state:
                    print(" ".join(str(x) for x in row))
                break
            else:
                print('Invalid choice. Please enter "1" or "2"')
        except ValueError:
            print('Invalid input. Please enter "1" or "2"')
    
    # Step 2: Get algorithm
    algo_choice = get_algorithm_choice()
    
    algorithms = {
        1: ("Uniform Cost Search", Heuristic.uniform_cost),
        2: ("A* with Misplaced Tile", Heuristic.misplaced_tile),
        3: ("A* with Euclidean Distance", Heuristic.euclidean_distance),
    }
    
    algo_name, heuristic_func = algorithms[algo_choice]
    
    # Check solvability
    problem = Problem(initial_state)
    if not problem.is_solvable(initial_state):
        print("\nThis puzzle is IMPOSSIBLE to solve!")
        return
    
    # Step 3: Run search with trace
    print("\n" + "="*70)
    print(f"Running {algo_name}...")
    print("="*70)
    
    goal_node, nodes_expanded, max_queue_size = graph_search_with_trace(
        problem, heuristic_func, show_trace=True
    )
    
    # Display results
    if goal_node:
        print("\n" + "="*70)
        print("Goal!!!")
        print("="*70)
        print(f"\nTo solve this problem the search algorithm expanded a total of {nodes_expanded} nodes.")
        print(f"The maximum number of nodes in the queue at any one time: {max_queue_size}.")
        print(f"The depth of the goal node was {goal_node.g}.")
    else:
        print("\nNo solution found!")


if __name__ == "__main__":
    main()

