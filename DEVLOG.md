# Development Log – The Torchbearer

**Student Name:** AARON TIMBANG
**Student ID:** 133228183

---

## Entry 1 – [11MAY2026]: Initial Plan

_I plan on implementing`run_dijkstra()` function first, that way I get a refresher on core concepts and can test immediatley if my shortest path implementation actually works. From an intial pov I think verifying both `find_optimal_route()` and explore() will be the most challenging. To test I will probably set breakpoints from initial call to each function and step through each line to verify everything is working as intended._
 
---

## Entry 2 – [13MAY2026]: [Wrong Source Set]

_First version of `select_sources` included the exit T as a source, which doesn't break correctness but wastes a full Dijkstra run. Re-read the spec: the exit is only a destination, never a starting point. Fixed it to return only spawn + relics._

---

## Entry 3 – [Date]: [Short description]

_Your entry here._

---

## Entry 4 – [14MAY2026]: Post-Implementation Reflection

_With more time I'd add memoization on `(current_loc, frozenset(relics_remaining))` so the search doesn't re-explore states it's already seen. That alone would make the algorithm scale to way more relics without changing the rest of the code._

---

## Final Entry – [Date]: Time Estimate

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | 1 |
| Part 2: Precomputation Design | 1 |
| Part 3: Algorithm Correctness | 2 |
| Part 4: Search Design | 1 |
| Part 5: State and Search Space | 1 |
| Part 6: Pruning | 2 |
| Part 7: Implementation | 3 |
| README and DEVLOG writing | 2 |
| **Total** | 13 |
