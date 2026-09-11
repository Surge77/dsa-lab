# Directed graphs

A directed graph stores edges with a direction: `u -> v` says nothing about
`v -> u`. That asymmetry is the whole point — it is what lets a graph express
dependency rather than mere association.

Implementation: `Non_Linear/graphs/directed/directed_graph.py` (unweighted) and
`Non_Linear/graphs/directed/weighted/` (weighted, split into base / algorithms /
advanced / matrix / utils).

---

## The invariant

```
v in adj[u]   means an edge u -> v exists
              and implies nothing whatsoever about u in adj[v]
```

Every bug in this file family traces back to code that forgot the second line.

---

## Representation: list vs matrix

| | Adjacency list | Adjacency matrix |
|---|---|---|
| Space | O(V + E) | O(V²) regardless of E |
| `has_edge(u, v)` | O(deg u) | O(1) |
| Iterate neighbours of u | O(deg u) | O(V) |
| Best for | sparse graphs (most real ones) | dense graphs, Floyd-Warshall |

This is the first design decision and it is usually decided by E relative to V².
A social graph is sparse; a distance table between every pair of cities is dense.

---

## Cycle detection needs three colours

The single most common mistake. A `visited` set is enough for an **undirected**
graph, but in a directed graph it reports a cycle on any diamond:

```
    a
   / \
  b   c
   \ /
    d        <- d is reached twice, but there is NO cycle
```

You need to distinguish "seen before" from "currently on the stack":

- **white** — not yet visited
- **grey** — visiting, still on the recursion stack
- **black** — fully explored, all descendants done

An edge into a **grey** node is a back edge, and a back edge is a cycle. An edge
into a black node is fine.

```
has_cycle(graph)   ->  Non_Linear/graphs/directed/weighted/
                       directed_weighted_graph_advanced.py
```

---

## Topological sort

A linear ordering where every edge points forward. Exists **if and only if** the
graph is a DAG.

Two ways:

- **DFS post-order, reversed.** Natural if you already wrote the DFS.
- **Kahn's algorithm.** Repeatedly emit a vertex with in-degree 0 and decrement
  its neighbours. Needs **in**-degree specifically, which is the detail people
  get wrong since adjacency lists give you out-degree for free.

The failure mode to guard against: on a cyclic graph, both algorithms return a
partial ordering and **raise nothing**. Always compare the output length against
the vertex count.

```python
order = topological_sort(graph)
if len(order) != graph.vertex_count():
    # the graph has a cycle; the "ordering" is meaningless
```

### Shortest paths on a DAG

Relax edges in topological order and you get single-source shortest paths in
O(V + E) — faster than Dijkstra, and it tolerates negative weights. Dijkstra
cannot. This is `shortest_path_dag`.

---

## Strong connectivity

"Connected" and "strongly connected" are different questions. Two vertices are
strongly connected when each can reach the other.

Kosaraju's algorithm needs the **transpose** graph (every edge reversed), which
is why `transpose()` lives next to the traversals. Tarjan's algorithm computes
the same SCCs in one pass using low-link values.

---

## Weighted directed graphs: which algorithm

| Situation | Use | Why |
|---|---|---|
| Non-negative weights, one source | Dijkstra | O((V+E) log V) |
| Any weights, one source | Bellman-Ford | O(VE), detects negative cycles |
| All pairs | Floyd-Warshall | O(V³), simple triple loop |
| DAG, any weights | relax in topo order | O(V+E), beats all of the above |
| All weights equal | BFS | Dijkstra's heap is pure overhead |

### Bellman-Ford and negative cycles

A negative cycle means no shortest path exists — you can go round it forever and
keep getting cheaper. Bellman-Ford relaxes every edge V-1 times; the **Vth pass**
is the detector. If anything still improves on pass V, there is a negative cycle.

Skipping that pass does not raise — it returns confident nonsense.

### Floyd-Warshall's loop order

```python
for k in range(n):          # intermediate vertex — MUST be outermost
    for i in range(n):
        for j in range(n):
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
```

Any other nesting computes something that is not all-pairs shortest paths. The
`k` loop outermost is what makes the recurrence valid: after iteration k, every
entry is the shortest path using only `{0..k}` as intermediates.

---

## Max flow

`max_flow(graph, source, sink)` implements Ford-Fulkerson with BFS augmenting
paths (Edmonds-Karp).

The detail that makes or breaks it: the search runs on the **residual** graph,
which includes a backward edge for every unit of flow pushed forward. Those
backward edges are what let a later augmenting path *undo* an earlier bad
routing decision. Omit them and the algorithm terminates at a flow that is not
maximal — with no error.

Max-flow equals min-cut, which is why the same function answers "what is the
bottleneck?".

---

## Tests

```
Tests/test_directed_graph.py     unweighted
Tests/test_weighted_graphs.py    weighted: Dijkstra, Bellman-Ford,
                                 Floyd-Warshall, topological sort, max flow
```

Before those existed, eight of these modules could not even be imported: they
began with Python-2 implicit relative imports (`from directed_weighted_graph_base
import ...`), which raise `ModuleNotFoundError` under Python 3. Everything in
this document was unreachable dead code.

---

## Interview problems

- Course Schedule (LC 207) — cycle detection
- Course Schedule II (LC 210) — topological sort
- Alien Dictionary (LC 269)
- Cheapest Flights Within K Stops (LC 787) — Bellman-Ford
- Network Delay Time (LC 743) — Dijkstra
- Find the City With the Smallest Number of Neighbors (LC 1334) — Floyd-Warshall

Drill it: `python drill.py --topic directed_graph`
