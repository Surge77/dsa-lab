# Import the base graph class
from collections import deque

# If you need Array and LinkedList (for custom queues or BFS), import them like:
from Non_Linear.graphs.undirected.undirected_graph_base import Graph


def cycle_detection(graph: Graph) -> bool:
    """
    Detects if an undirected graph contains at least one cycle using DFS.

    Args:
        graph (Graph): The undirected graph instance.

    Returns:
        bool: True if a cycle exists, False otherwise.

    Time Complexity: O(V + E), where V = vertices, E = edges.
    Space Complexity: O(V) for the visited array and recursion stack.
    """
    visited = [False] * graph.vertex_count()

    def dfs(u: int, parent: int) -> bool:
        visited[u] = True
        for i in range(len(graph.adj[u])):
            v = graph.adj[u].get(i)
            if not visited[v]:
                if dfs(v, u):
                    return True
            elif v != parent:
                # Found a back-edge indicating a cycle
                return True
        return False

    for u in range(graph.vertex_count()):
        if not visited[u]:
            if dfs(u, -1):
                return True
    return False

def is_bipartite(graph: Graph) -> bool:
    """
    Checks if the given undirected graph is bipartite using BFS coloring.

    A graph is bipartite if we can color its vertices with two colors
    such that no two adjacent vertices share the same color.

    This is a simpler subset of the graph coloring problem.

    Goal: Check if the graph can be colored with just 2 colors (like 0 and 1).

    Args:
        graph (Graph): The undirected graph instance.

    Returns:
        bool: True if the graph is bipartite, False otherwise.

    Time Complexity: O(V + E)
    Space Complexity: O(V) for color tracking
    """
    color = [-1] * graph.vertex_count()  # -1 means uncolored

    def bfs_check(start: int) -> bool:
        from collections import deque
        queue = deque()
        queue.append(start)
        color[start] = 0  # Start coloring with 0

        while queue:
            u = queue.popleft()
            for i in range(len(graph.adj[u])):
                v = graph.adj[u].get(i)
                if color[v] == -1:
                    # Assign opposite color to neighbor
                    color[v] = 1 - color[u]
                    queue.append(v)
                elif color[v] == color[u]:
                    # Neighbor has same color, not bipartite
                    return False
        return True

    # Check for each disconnected component
    for u in range(graph.vertex_count()):
        if color[u] == -1:
            if not bfs_check(u):
                return False
    return True

def get_bipartite_groups(graph: Graph):
    """
    Returns the two sets (groups) of vertices if the graph is bipartite.

    Returns ([], []) if the graph is not bipartite.

    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    n = graph.vertex_count()
    color = [-1] * n
    group_a, group_b = [], []

    def bfs_coloring(start: int) -> bool:
        queue = deque([start])
        color[start] = 0
        group_a.append(start)

        while queue:
            u = queue.popleft()
            for i in range(len(graph.adj[u])):
                v = graph.adj[u].get(i)
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    if color[v] == 0:
                        group_a.append(v)
                    else:
                        group_b.append(v)
                    queue.append(v)
                elif color[v] == color[u]:
                    return False
        return True

    for u in range(n):
        if color[u] == -1:
            # If this component is not bipartite, fail early
            if not bfs_coloring(u):
                return [], []

    return group_a, group_b


def shortest_path_bfs(graph: Graph, start: int):
    """
    Computes the shortest path distances from the start vertex to all other vertices
    in an unweighted graph using BFS.

    Args:
        graph (Graph): The undirected graph instance.
        start (int): The source vertex.

    Returns:
        List[int]: A list where dist[i] is the shortest distance from start to i.
                   If i is unreachable, dist[i] = -1.

    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    graph._validate_vertex(start)
    n = graph.vertex_count()
    dist = [-1] * n   # -1 means unreachable
    dist[start] = 0

    queue = deque([start])

    while queue:
        u = queue.popleft()
        for i in range(len(graph.adj[u])):
            v = graph.adj[u].get(i)
            if dist[v] == -1:  # Not visited
                dist[v] = dist[u] + 1
                queue.append(v)

    return dist


def reconstruct_path(graph: Graph, start: int, end: int):
    """
    Finds and returns the shortest path from the start vertex to the end vertex
    in an unweighted graph using BFS.

    This function computes the shortest path by:
    1. Performing BFS from the start vertex.
    2. Keeping track of parent nodes to reconstruct the path.
    3. Returning the sequence of vertices from start to end.

    Args:
        graph (Graph): The undirected graph instance.
        start (int): The starting vertex.
        end (int): The destination vertex.

    Returns:
        List[int]: A list of vertices representing the shortest path from start
                  to end. Returns an empty list if no path exists.

    Time Complexity: O(V + E), where V = number of vertices, E = number of edges.
    Space Complexity: O(V) for the distance and parent arrays.
    """
    # Validate that both vertices exist
    graph._validate_vertex(start)
    graph._validate_vertex(end)

    n = graph.vertex_count()
    dist = [-1] * n        # Distance array, -1 means 'unvisited'
    parent = [-1] * n      # Parent array to reconstruct path

    # Standard BFS initialization
    queue = deque([start])
    dist[start] = 0

    while queue:
        u = queue.popleft()
        # Visit all neighbors of vertex u
        for i in range(len(graph.adj[u])):
            v = graph.adj[u].get(i)
            if dist[v] == -1:   # If v has not been visited
                dist[v] = dist[u] + 1
                parent[v] = u   # Record parent for path reconstruction
                queue.append(v)

    # If end is unreachable
    if dist[end] == -1:
        return []

    # Reconstruct the path from end to start using the parent array
    path = []
    curr = end
    while curr != -1:
        path.append(curr)
        curr = parent[curr]

    return path[::-1]  # Reverse the path to get start → end order

def has_path(graph: Graph, start: int, end: int) -> bool:
    """
    Checks if there exists a path between two vertices in an unweighted, undirected graph.

    Args:
        graph (Graph): The undirected graph instance.
        start (int): The starting vertex.
        end (int): The destination vertex.

    Returns:
        bool: True if a path exists from start to end, False otherwise.

    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    graph._validate_vertex(start)
    graph._validate_vertex(end)

    if start == end:
        return True

    visited = [False] * graph.vertex_count()
    queue = deque([start])
    visited[start] = True

    while queue:
        u = queue.popleft()
        for i in range(len(graph.adj[u])):
            v = graph.adj[u].get(i)
            if not visited[v]:
                if v == end:
                    return True
                visited[v] = True
                queue.append(v)
    return False


def has_path_dfs(graph: Graph, start: int, end: int) -> bool:
    """
    Checks if there exists a path between two vertices using DFS (recursive).

    Args:
        graph (Graph): The undirected graph instance.
        start (int): The starting vertex.
        end (int): The destination vertex.

    Returns:
        bool: True if a path exists from start to end, False otherwise.

    Time Complexity: O(V + E)
    Space Complexity: O(V) due to recursion stack.
    """
    graph._validate_vertex(start)
    graph._validate_vertex(end)

    visited = [False] * graph.vertex_count()

    def dfs(u: int) -> bool:
        if u == end:
            return True
        visited[u] = True
        for i in range(len(graph.adj[u])):
            v = graph.adj[u].get(i)
            if not visited[v] and dfs(v):
                return True
        return False

    return dfs(start)


def find_bridges(graph: Graph):
    """
    Finds all bridges (critical edges) in an undirected graph using Tarjan's Algorithm.

    Args:
        graph (Graph): The undirected graph instance.

    Returns:
        List[Tuple[int, int]]: List of bridges as (u, v) pairs.

    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    n = graph.vertex_count()
    visited = [False] * n
    disc = [-1] * n    # discovery time
    low = [-1] * n     # lowest discovery time reachable
    parent = [-1] * n
    bridges = []
    time = [0]         # Mutable object to act as counter in recursion

    def dfs(u):
        visited[u] = True
        disc[u] = low[u] = time[0]
        time[0] += 1

        for i in range(len(graph.adj[u])):
            v = graph.adj[u].get(i)
            if not visited[v]:
                parent[v] = u
                dfs(v)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:  # No back edge from v or its subtree
                    bridges.append((u, v))
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])

    for u in range(n):
        if not visited[u]:
            dfs(u)

    return bridges


def find_articulation_points(graph: Graph):
    """
    Finds all articulation points (cut vertices) in an undirected graph using Tarjan's Algorithm.

    Args:
        graph (Graph): The undirected graph instance.

    Returns:
        List[int]: List of articulation points.

    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    n = graph.vertex_count()
    visited = [False] * n
    disc = [-1] * n
    low = [-1] * n
    parent = [-1] * n
    ap = [False] * n
    time = [0]

    def dfs(u):
        visited[u] = True
        disc[u] = low[u] = time[0]
        time[0] += 1
        children = 0

        for i in range(len(graph.adj[u])):
            v = graph.adj[u].get(i)
            if not visited[v]:
                parent[v] = u
                children += 1
                dfs(v)
                low[u] = min(low[u], low[v])

                # Articulation point conditions
                if parent[u] == -1 and children > 1:
                    ap[u] = True
                if parent[u] != -1 and low[v] >= disc[u]:
                    ap[u] = True
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])

    for u in range(n):
        if not visited[u]:
            dfs(u)

    return [i for i, is_ap in enumerate(ap) if is_ap]



def is_eulerian(graph: Graph) -> str:
    """
    Checks whether the graph has an Eulerian Path or Circuit.

    Args:
        graph (Graph): The undirected graph instance.

    Returns:
        str: "circuit" if an Eulerian circuit exists,
             "path" if an Eulerian path exists,
             "none" otherwise.

    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    odd_degree_count = 0
    for u in range(graph.vertex_count()):
        if len(graph.adj[u]) % 2 != 0:
            odd_degree_count += 1

    # Check if graph is connected (ignoring isolated nodes)
    if not _is_connected_for_euler(graph):
        return "none"

    if odd_degree_count == 0:
        return "circuit"
    if odd_degree_count == 2:
        return "path"
    return "none"


def _is_connected_for_euler(graph: Graph) -> bool:
    """Checks connectivity of the graph ignoring isolated vertices."""
    visited = [False] * graph.vertex_count()

    # Find a vertex with non-zero degree
    start = -1
    for i in range(graph.vertex_count()):
        if len(graph.adj[i]) > 0:
            start = i
            break

    if start == -1:
        return True  # Graph with no edges is trivially Eulerian

    # DFS to check connectivity
    def dfs(u):
        visited[u] = True
        for j in range(len(graph.adj[u])):
            v = graph.adj[u].get(j)
            if not visited[v]:
                dfs(v)

    dfs(start)
    # Check if all non-isolated vertices are visited
    for i in range(graph.vertex_count()):
        if not visited[i] and len(graph.adj[i]) > 0:
            return False
    return True


def find_eulerian_path(graph: Graph):
    """
    Finds and returns an Eulerian path or circuit using Hierholzer's Algorithm.

    Args:
        graph (Graph): The undirected graph instance.

    Returns:
        List[int]: The sequence of vertices in Eulerian path/circuit,
                   or [] if no Eulerian path exists.

    Time Complexity: O(E), where E = number of edges.
    Space Complexity: O(E + V) for path and stack.
    """
    status = is_eulerian(graph)
    if status == "none":
        return []

    # Make a copy of adjacency (to avoid modifying original graph)
    adj_copy = [[graph.adj[u].get(i) for i in range(len(graph.adj[u]))]
                for u in range(graph.vertex_count())]

    # Find starting vertex
    start = 0
    if status == "path":
        for u in range(graph.vertex_count()):
            if len(adj_copy[u]) % 2 != 0:
                start = u
                break

    stack = [start]
    path = []

    while stack:
        u = stack[-1]
        if adj_copy[u]:
            v = adj_copy[u].pop()
            # Remove edge both ways
            adj_copy[v].remove(u)
            stack.append(v)
        else:
            path.append(stack.pop())

    return path[::-1]
