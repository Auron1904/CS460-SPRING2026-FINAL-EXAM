"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: AARON TIMBANG
Student ID:   133228183

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    return (
        "1. While we can just run Dijkstra from S it will only return the cheapest path from S to every other node; we do not keep track of collection order or consider shortest exit from current vertex to exit node-T\n"
        "2. The only decision left is what order to visit the relics."
        "3. Total fuel is also reliant on the sequence of inter-location edges taken, so finding the minimum requires comparing across different order traversals rather than computing a single value."

    )


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.

    
    """
    sources = set(relics)
    sources.add(spawn)
    return list(sources)


def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').

    """
    # Source = 0, all other nodes = inf
    dist = {v: float('inf') for v in graph}
    dist[source] = 0

    # minHeap (dist, node)
    pq = [(0, source)]

    while pq:
        d, u = heapq.heappop(pq)

        if d > dist[u]:
            continue

        for v, w in graph[u]:
            new_dist = d + w
            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(pq, (new_dist, v))

    return dist


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.

    """
    sources = select_sources(spawn, relics, exit_node)
    dist_table = {}
    for src in sources:
        dist_table[src] = run_dijkstra(graph, src)
    return dist_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    return (
        "3a-1. Their stored distance is the proven shortest-path distance from the source S; other paths have already been provden to be greater than nodes stored in S."
        "3a-2. Their stored distance is the cheapest path *yet discovered* from S; a strictly shorter route may still be found once more nodes join S."
        "3b-1. S is empty so the finalized clause is vacuously true; dist[x]=0 and every other dist=infinity correctly shows no path through S has been found yet."
        "3b-2. Any alternative path to u must exit S at some first non-S node y, where dist[y] is at most the cost to reach y. Since u was picked as the minimum, dist[u] ≤ dist[y], and nonnegative edge weights mean the rest of the path can only add cost, so no alternative beats dist[u]."
        "3b-3. Once the priority queue empties, every reachable node is finalized, so dist[v] holds the true shortest distance and unreachable nodes stay at infinity."
        "3c. f any dist-table entry is wrong, the order-search compares incorrect tour costs and can pick a suboptimal (or unreachable) ordering as 'optimal' wasting the Torchbearer's fuel."
    )


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    return (
        "4-1. Greedy picks the cheapest next edge but ignores how that choice forces expensive later edges; a small saving now can lock in a big penalty later."
        "4-2. dist(S→B)=1, dist(S→C)=10, dist(B→C)=100, dist(C→B)=1, dist(B→T)=50, dist(C→T)=1, with relics {B, C}."
        "4-3. S→B→C→T = 1 + 100 + 1 = 102"
        "4-4. S→C→B→T = 10 + 1 + 50 = 61"
        "4-5. Saving 9 fuel on the first hop locked in a 100-fuel second hop; the optimal tour paid more up front to unlock cheap downstream legs."
        "4-6. Every possible order in which the relics can be visited, since total fuel depends on which inter-relic legs get chained together and different orders produce different sums."
    )


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    """
    if not relics:
        direct_cost = dist_table[spawn].get(exit_node, float('inf'))
        if direct_cost == float('inf'):
            return (float('inf'), [])
        return (direct_cost, [])
    
    best = [float('inf'), []]

    _explore(dist_table=dist_table, current_loc=spawn, relics_remaining=set(relics),
             relics_visited_order=[], cost_so_far=0.0, exit_node=exit_node, best=best)
    
    if best[0] == float('inf'):
        return (float('inf'), [])
    return (best[0], best[1])


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.

    
    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
    if not relics_remaining:
        finish_cost = dist_table[current_loc].get(exit_node, float('inf'))
        total = cost_so_far + finish_cost
        if total < best[0]:
            best[0] = total
            best[1] = list(relics_visited_order)
        return
    

    # *** REQUIRED COMMENT ***
    # dist_table[current_loc][exit_node] is the cheapest path to the exit, and every
    # tour must end there. Nonnegative weights mean detouring through remaining
    # relics can only add cost, so cost_so_far + lower_bound is at most the true
    # completion cost. If that sum already >= best[0], every completion of this
    # branch is at least as bad as the current best, so pruning is safe.

    lower_bound = dist_table[current_loc].get(exit_node, float('inf'))
    if cost_so_far + lower_bound >= best[0]:
        return
    
    #RECUSRIVE CASE
    for next_relic in list(relics_remaining):
        leg_cost = dist_table[current_loc].get(next_relic, float('inf'))
        if leg_cost == float('inf'):
            continue

        new_cost = cost_so_far + leg_cost
        if new_cost >= best[0]:
            continue

        relics_remaining.discard(next_relic)
        relics_visited_order.append(next_relic)

        _explore(dist_table=dist_table,
                 current_loc=next_relic,
                 relics_remaining=relics_remaining,
                 relics_visited_order=relics_visited_order,
                 cost_so_far=new_cost,
                 exit_node=exit_node,
                 best = best)
        
        relics_visited_order.pop()
        relics_remaining.add(next_relic)
        


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    
    """
    dist_table = precompute_distances(graph, spawn, relics, exit_node)
    return find_optimal_route(dist_table, spawn, relics, exit_node)


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
