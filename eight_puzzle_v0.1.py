"""
8-Puzzle Solver 
CS 170 Project 1

This version implements:
- Basic Node and Problem classes
- Uniform Cost Search only
- Basic state representation and operations
"""

import heapq
from copy import deepcopy


class Node:
    """Represents a node in the search tree."""
    
    def __init__(self, state, parent=None, operator=None, depth=0, path_cost=0):
        self.state = state
        self.parent = parent
        self.operator = operator
        self.depth = depth
        self.path_cost = path_cost
    
    def __lt__(self, other):
        """Compare nodes based on path cost for priority queue."""
        return self.path_cost < other.path_cost
    
    @property
    def g(self):
        """Return the cost from start to this node."""
        return self.depth
    
    @property
    def f(self):
        """Return the evaluation function f(n) = g(n)."""
        return self.g


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
    
    def _find_blank(self, state):
        """Find the position of the blank (0) in the state."""
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return i, j
        return None, None


def uniform_cost_search(problem):
    """Uniform Cost Search (Dijkstra) algorithm."""
    
    # Initialize
    initial_node = Node(problem.initial_state, None, None, 0, 0)
    frontier = [(initial_node.f, 0, initial_node)]  # (f, counter, node)
    explored = set()
    counter = 1
    nodes_expanded = 0
    max_queue_size = 1
    
    while frontier:
        # Get node with lowest cost
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
                child_node = Node(
                    child_state,
                    node,
                    operator,
                    node.depth + 1,
                    node.path_cost + 1
                )
                heapq.heappush(frontier, (child_node.f, counter, child_node))
                counter += 1
        
        # Update max queue size
        max_queue_size = max(max_queue_size, len(frontier))
    
    # No solution found
    return None, nodes_expanded, max_queue_size


def print_state(state):
    """Print the puzzle state in a readable format."""
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
    print_state(node.state)
    
    # Print each step
    for i, (operator, state) in enumerate(path, 1):
        print(f"\nStep {i}: Move blank {operator}")
        print_state(state)
    
    print(f"\nGoal reached in {goal_node.depth} steps!")


def main():
    """Main function for interactive use."""
    print("8-Puzzle Solver v0.1 - Uniform Cost Search")
    print("=" * 50)
    
    # Example puzzle
    initial_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 0, 8]
    ]
    
    print("\nSolving puzzle:")
    print_state(initial_state)
    
    # Create problem and solve
    problem = Problem(initial_state)
    goal_node, nodes_expanded, max_queue = uniform_cost_search(problem)
    
    # Print results
    print(f"\nNodes expanded: {nodes_expanded}")
    print(f"Max queue size: {max_queue}")
    print_solution(goal_node)


if __name__ == "__main__":
    main()



