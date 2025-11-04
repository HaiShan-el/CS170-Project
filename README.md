CS170 Project 1 — The Eight Puzzle
0) Cover Info

Repository (Private): // 这里记得放仓库的链接和地址

Group members & contribution：

Haishan Cao(// 这里记得你的netID)： Finished most of the code of puzzles, the Search & Heuristics, and came out with the graph.

Qianyu(Rose) Luo（rluo021）： Finished the comparison of Test cases, the report description, and a part of run_test.py to test the puzzle.

1) Project Overview

We implemented an 8-Puzzle graph search solution and compared three algorithms：

Uniform Cost Search（UCS）= A* & h(n)=0;

A* + Misplaced Tile;

A* + Euclidean Distance

2) Design (Objects & Methods)

We kept the design pretty simple and modular so it’s easy to read and test.

Problem is the puzzle wrapper. It stores the initial_state and the fixed goal_state, and gives you the basic operations you need to search:

operators(state) returns which moves are legal from the current blank position;

result(state, op) applies one move and returns the new board;

goal_test(state) checks if we hit the goal;

is_solvable(state) does the standard inversion-count check for 3×3 (even = solvable).
This keeps all puzzle rules in one place.

Node represents one spot in the search tree. It tracks the state, a pointer to the parent, the operator used to get here, and the basic costs: g (we use depth as path cost), h (heuristic), and f = g + h.

graph_search(problem, heuristic) is our generic A* loop. We push the start node into a min-heap frontier, pop the best f, and expand it. While it runs, we track nodes_expanded (time) and max_queue_size (space). Swapping the heuristic function lets us run UCS (h=0) in our project.
Overall, Problem knows the rules, Node knows where we are and how expensive it was to get here, and graph_search does the work of choosing what to try next.

3) Optimizations & Data Structures

Priority Queue (min-heap)： Selects the optimal node from smallest to largest by f to trace stability.

Explored Set： Converts the state into tuples of tuples as hash keys, avoiding redundant expansion.

Parent pointers： Used for backtracking and printing the operation sequence.

Solvability check： Checks the evenness of inversion counts; exits immediately upon encountering an unsolvable instance, saving time.

4) Tree Search vs Graph Search

We implement and use graph search (with explored) by default because states frequently loop in 8-Puzzle; Also, using tree search can increase the number of "nodes created/expanded".

5) Heuristic Functions & Correctness

UCS (h = 0): This is basically A* with h = 0. It explores by path cost only.

Misplaced Tile: Counts how many tiles are not in their goal spots (ignoring the blank). Admissible and consistent.

Euclidean Distance: For each tile, take the straight-line distance to where it should be and sum them up. Admissible.

Manhattan Distance: We used this for extra comparison (not strictly required) because it’s a common baseline.

What we compare: Time = number of nodes expanded, Space = max queue size. Those are the meaningful metrics here.

6) Interface & Trace

The program lets you type any start state, pick an algorithm, and it prints a step-by-step trace. Each step shows the current “best” node with its g(n) and h(n). At the end, we print the total nodes expanded, the peak queue size, and the goal depth.

For the required submission, run_tests.py --trace runs A* with the Euclidean heuristic on the specified puzzle and prints the full trace.

7) Test Cases & Methodology

We ran the built-in set: Trivial, Very Easy, Easy, Doable, Oh Boy, Impossible, plus a few custom medium/hard ones. For every solvable case, we tested UCS / Misplaced / Euclidean / Manhattan.

We recorded:

nodes_expanded (time)

max_queue_size (space)

goal depth

Unsolvable cases (like Impossible) are detected up front and skipped from averages. If needed, we can dump results to results/runs.csv and make quick charts by depth/difficulty.

8) Test Result

// 这里放图片同时你可以增加一点说明。

// 例子↑↓

// 这里记得标注，哪张图是哪个puzzle的，然后简单概括一下得出了什么结果就好。

9) Findings

On shallow puzzles (Trivial / Very Easy), heuristics don’t change much; UCS and A* expand about the same.

As puzzles get harder, heuristics help a lot. Euclidean and Manhattan clearly beat Misplaced and UCS.

With consistent heuristics, A* returns an optimal solution the first time it reaches the goal. We use graph search with an explored set, so we don’t re-expand states.

10) Challenges

Our biggest challenge is tie-breaking when multiple nodes have the same f = g + h. If we just push Node objects with identical f, the pop order can be inconsistent, which makes the trace jumpy and sometimes changes how many nodes we expand.

What we did (in eight_puzzle.py → graph_search)
We store a 3-tuple in the heap: (f, counter, node).

Initialize: frontier = [(initial_node.f, 0, initial_node)]
When pushing children: heapq.heappush(frontier, (child_node.f, counter, child_node)); counter += 1


That counter is a simple increasing number. When two nodes share the same f, Python’s heap uses the second field to break ties, so the queue order becomes stable.
