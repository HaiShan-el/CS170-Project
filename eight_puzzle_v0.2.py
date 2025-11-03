"""
8-Puzzle Solver 
CS 170 Project 1

This version adds:
- Heuristic functions (Misplaced Tile, Manhattan Distance)
- A* Search implementation
- Basic comparison between algorithms
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
    def manhattan_distance(state):
        """Calculate Manhattan distance for all tiles."""
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


def graph_search(problem, heuristic_func=Heuristic.uniform_cost):
    """A* graph search algorithm."""
    
    # Initialize
    h_initial = heuristic_func(problem.initial_state)
    initial_node = Node(problem.initial_state, None, None, 0, 0, h_initial)
    frontier = [(initial_node.f, 0, initial_node)]
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
        
        # Add to explored
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
        
        max_queue_size = max(max_queue_size, len(frontier))
    
    return None, nodes_expanded, max_queue_size


def print_state(state):
    """Print the puzzle state."""
    for row in state:
        print(" ".join("b" if x == 0 else str(x) for x in row))


def compare_algorithms(initial_state):
    """Compare different heuristic functions."""
    problem = Problem(initial_state)
    
    algorithms = [
        ("Uniform Cost", Heuristic.uniform_cost),
        ("Misplaced Tile", Heuristic.misplaced_tile),
        ("Manhattan Distance", Heuristic.manhattan_distance),
    ]
    
    print("\nAlgorithm Comparison:")
    print("=" * 60)
    
    for name, heuristic in algorithms:
        goal, nodes, max_q = graph_search(problem, heuristic)
        if goal:
            print(f"{name:20} | Depth: {goal.depth:2} | Nodes: {nodes:4} | Max Queue: {max_q:4}")
        else:
            print(f"{name:20} | No solution found")


def main():
    """Main function."""
    print("8-Puzzle Solver v0.2 - A* Search with Heuristics")
    print("=" * 50)
    
    # Test puzzle
    initial_state = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]
    ]
    
    print("\nSolving puzzle:")
    print_state(initial_state)
    
    # Compare algorithms
    compare_algorithms(initial_state)
    
    # Solve with Manhattan Distance
    print("\nSolving with Manhattan Distance heuristic...")
    problem = Problem(initial_state)
    goal, nodes, max_q = graph_search(problem, Heuristic.manhattan_distance)
    
    if goal:
        print(f"\nSolution found in {goal.depth} steps!")
        print(f"Nodes expanded: {nodes}")
        
        # Print solution path
        path = []
        node = goal
        while node.parent:
            path.append(node.operator)
            node = node.parent
        print(f"Path: {' -> '.join(reversed(path))}")


if __name__ == "__main__":
    main()



