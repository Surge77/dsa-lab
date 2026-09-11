from Linear.arrays import MyArray as Array


class DirectedWeightedGraphMatrix:
    """
    Directed Weighted Graph using an adjacency matrix.
    If there is no edge between u and v, the weight is set to float('inf').
    """

    def __init__(self, num_vertices: int):
        """
        Initialize an adjacency matrix for a directed weighted graph.

        Args:
            num_vertices (int): Number of vertices (0-based indexing).
        """
        self.n = num_vertices
        self.adj = Array()

        # Initialize adjacency matrix
        for i in range(num_vertices):
            row = Array()
            for j in range(num_vertices):
                row.append(0 if i == j else float('inf'))  # 0 on diagonal
            self.adj.append(row)

    def _validate_vertex(self, u: int):
        """Raise ValueError if vertex u is invalid."""
        if u < 0 or u >= self.n:
            raise ValueError(f"Vertex {u} out of bounds (0 to {self.n - 1})")

    def add_edge(self, u: int, v: int, weight: float):
        """
        Add a directed edge u -> v with the given weight.

        Time Complexity: O(1)
        """
        self._validate_vertex(u)
        self._validate_vertex(v)
        self.adj.get(u).set(v, weight)

    def remove_edge(self, u: int, v: int):
        """
        Remove the directed edge u -> v.

        Time Complexity: O(1)
        """
        self._validate_vertex(u)
        self._validate_vertex(v)
        self.adj.get(u).set(v, float('inf'))

    def has_edge(self, u: int, v: int) -> bool:
        """
        Check if an edge u -> v exists.

        Time Complexity: O(1)
        """
        self._validate_vertex(u)
        self._validate_vertex(v)
        return self.adj.get(u).get(v) != float('inf')

    def neighbors(self, u: int):
        """
        Return all neighbors of vertex u as (v, weight).

        Time Complexity: O(V)
        """
        self._validate_vertex(u)
        result = []
        row = self.adj.get(u)
        for v in range(self.n):
            weight = row.get(v)
            if weight != float('inf') and u != v:
                result.append((v, weight))
        return result

    def edges(self):
        """
        Return a list of all edges (u, v, weight).

        Time Complexity: O(V²)
        """
        result = []
        for u in range(self.n):
            row = self.adj.get(u)
            for v in range(self.n):
                weight = row.get(v)
                if weight != float('inf') and u != v:
                    result.append((u, v, weight))
        return result

    def vertex_count(self) -> int:
        return self.n

    def edge_count(self) -> int:
        count = 0
        for u in range(self.n):
            row = self.adj.get(u)
            for v in range(self.n):
                if row.get(v) != float('inf') and u != v:
                    count += 1
        return count

    def __len__(self):
        return self.n

    def __str__(self):
        matrix_str = []
        for i in range(self.n):
            row = [str(self.adj.get(i).get(j)) if self.adj.get(i).get(j) != float('inf') else "∞"
                   for j in range(self.n)]
            matrix_str.append(" ".join(row))
        return "\n".join(matrix_str)

    def __repr__(self):
        return f"DirectedWeightedGraphMatrix(num_vertices={self.n})"
