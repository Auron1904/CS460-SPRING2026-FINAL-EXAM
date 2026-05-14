# The Torchbearer

**Student Name:** AARON TIMBANG
**Student ID:** 133228183
**Course:** CS 460 – Algorithms | Spring 2026

---

## Part 1: Problem Analysis

- **Why a single shortest-path run from S is not enough:**
  _While we can just run Dijkstra from S it will only return the cheapest path from S to every other node; we do not keep track of collection order or consider shortest exit from current vertex to exit node-T._

- **What decision remains after all inter-location costs are known:**
  _The only decision left is what order to visit the relics._

- **Why this requires a search over orders (one sentence):**
  _Total fuel is also reliant on the sequence of inter-location edges taken, so finding the minimum requires comparing across different order traversals rather than computing a single value._

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

| Source Node Type | Why it is a source |
|---|---|
| _startNode_ | _We begin each tour at S; we then calculate shortest paths from S_ |
| _relicNode_ | _We keep track of these as stops, so we need to to calculate shortest path from each relic node until exitNode_ |

### Part 2b: Distance Storage

| Property | Your answer |
|---|---|
| Data structure name | Nested dictionary |
| What the keys represent | Outer key = source node u (entrance or a relic); inner key = destination node v (any node in the graph) |
| What the values represent | Minimum fuel cost of the shortest path from u to v |
| Lookup time complexity | O(1) |
| Why O(1) lookup is possible | Python dicts are hash tables; each key access should be constant time |

### Part 2c: Precomputation Complexity

- **Number of Dijkstra runs:** _1 + k (one from S, one from each relic)_
- **Cost per run:** _O(m log n)_
- **Total complexity:** _O((k + 1) · m log n) = O(k · m log n)_
- **Justification (one line):** _Linear in the number of sources times the per-source cost of one Dijkstra run._

---

## Part 3: Algorithm Correctness

### Part 3a: What the Invariant Means

- **For nodes already finalized (in S):**
  _Their stored distance is the proven shortest-path distance from the source S; other paths have already been provden to be greater than nodes stored in S._

- **For nodes not yet finalized (not in S):**
  _Their stored distance is the cheapest path *yet discovered* from S; a strictly shorter route may still be found once more nodes join S._

### Part 3b: Why Each Phase Holds

- **Initialization : why the invariant holds before iteration 1:**
  _S is empty so the finalized clause is vacuously true; dist[x]=0 and every other dist=infinity correctly shows no path through S has been found yet._

- **Maintenance : why finalizing the min-dist node is always correct:**
  _Any alternative path to u must exit S at some first non-S node y, where dist[y] is at most the cost to reach y. Since u was picked as the minimum, dist[u] ≤ dist[y], and nonnegative edge weights mean the rest of the path can only add cost, so no alternative beats dist[u]._

- **Termination : what the invariant guarantees when the algorithm ends:**
  _Once the priority queue empties, every reachable node is finalized, so dist[v] holds the true shortest distance and unreachable nodes stay at infinity._

### Part 3c: Why This Matters for the Route Planner

_If any dist-table entry is wrong, the order-search compares incorrect tour costs and can pick a suboptimal (or unreachable) ordering as "optimal," wasting the Torchbearer's fuel._

---

## Part 4: Search Design

### Why Greedy Fails

- **The failure mode:** _Greedy picks the cheapest next edge but ignores how that choice forces expensive later edges; a small saving now can lock in a big penalty later._
- **Counter-example setup:** _dist(S→B)=1, dist(S→C)=10, dist(B→C)=100, dist(C→B)=1, dist(B→T)=50, dist(C→T)=1, with relics {B, C}._
- **What greedy picks:** _S→B→C→T = 1 + 100 + 1 = 102_
- **What optimal picks:** _S→C→B→T = 10 + 1 + 50 = 61_
- **Why greedy loses:** _Saving 9 fuel on the first hop locked in a 100-fuel second hop; the optimal tour paid more up front to unlock cheap downstream legs._

### What the Algorithm Must Explore

- _Every possible order in which the relics can be visited, since total fuel depends on which inter-relic legs get chained together and different orders produce different sums._

---

## Part 5: State and Search Space

### Part 5a: State Representation

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | current_loc  | node | The dungeon node the Torchbearer currently stands at; the source for the next leg lookup. |
| Relics already collected | relics_visited_order | list[node] | Ordered list of relics visited so far; companion `relics_remaining` (set) drives the recursion. |
| Fuel cost so far | cost_so_far | float | Sum of edge weights along the current partial tour; compared against `best[0]` for pruning. |

### Part 5b: Data Structure for Visited Relics

| Property | Your answer |
|---|---|
| Data structure chosen | Python-set |
| Operation: check if relic already collected | Time complexity: O(1) |
| Operation: mark a relic as collected | Time complexity: O(1) |
| Operation: unmark a relic (backtrack) | Time complexity: O(1) |
| Why this structure fits | Hash sets give constant-time add/remove/membership, which is exactly what our backtracking implemenation needs at each level. |

### Part 5c: Worst-Case Search Space

- **Worst-case number of orders considered:** _k! where k = |M|_
- **Why:** _At each level we pick one of the remaining relics, giving k · (k−1) · … · 1 = k! complete orderings._

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

- **What is tracked:** _A mutable container `best` holding the cost and order of the cheapest complete S → all-relics → T tour found so far; `best[0]` starts at infinity and updates whenever a cheaper complete tour finishes._
- **When it is used:** _Before recursing deeper, we check if costSoFar plus the lower bound can still beat `best[0]`._
- **What it allows the algorithm to skip:** _Any subtree whose prefix is already too expensive to beat the current best, cutting off every ordering that shares that prefix._

### Part 6b: Lower Bound Estimation

- **What information is available at the current state:** _The current location, the set of relics still to collect, fuel spent so far, and the full precomputed `dist_table`._
- **What the lower bound accounts for:** _The unavoidable cost of eventually reaching the exit, which is at minimum `dist_table[current_loc][exit_node]` since every tour must end at the exit._
- **Why it never overestimates:** _The direct shortest path is the cheapest way to reach the exit, and nonnegative edge weights mean detouring through remaining relics can only add cost, never subtract._

### Part 6c: Pruning Correctness

- _Since the lower bound never overestimates, costSoFar + lowerBound ≤ the true cost of any completion of this branch. So if that sum already meets or exceeds best[0], every completion is at least as bad as the current best and pruning cannot discard a better solution._

---

## References

- _1.https://www.youtube.com/watch?v=GazC3A4OQTE, https://www.youtube.com/watch?v=XB4MIexjvY0_
