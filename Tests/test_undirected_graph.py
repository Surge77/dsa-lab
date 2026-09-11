import unittest

from Non_Linear.graphs.undirected.undirected_graph_base import Graph
from Non_Linear.graphs.undirected.undirected_graph_utils import (
    clear,
    clone,
    degree,
    edges,
    is_connected,
)


class TestGraphMethods(unittest.TestCase):

    def setUp(self):
        # Called before every test case
        self.graph = Graph(5)
        self.graph.add_edge(0, 1)
        self.graph.add_edge(0, 2)
        self.graph.add_edge(1, 3)
        self.graph.add_edge(3, 4)

    def test_add_edge(self):
        self.assertTrue(self.graph.has_edge(0, 1))
        self.assertTrue(self.graph.has_edge(3, 4))
        self.assertFalse(self.graph.has_edge(2, 4))

    def test_remove_edge(self):
        self.graph.remove_edge(0, 1)
        self.assertFalse(self.graph.has_edge(0, 1))
        self.assertTrue(self.graph.has_edge(0, 2))  # other edges remain

    def test_has_edge(self):
        self.assertTrue(self.graph.has_edge(1, 0))  # undirected edge
        self.assertFalse(self.graph.has_edge(2, 4))

    def test_neighbors(self):
        neighbors = [self.graph.adj[0].get(i) for i in range(len(self.graph.adj[0]))]
        self.assertIn(1, neighbors)
        self.assertIn(2, neighbors)

    def test_add_vertex(self):
        old_count = self.graph.vertex_count()
        self.graph.add_vertex()
        self.assertEqual(self.graph.vertex_count(), old_count + 1)

    def test_remove_vertex_static(self):
        self.graph.remove_vertex_static(0)
        self.assertFalse(self.graph.has_edge(0, 1))
        self.assertEqual(len(self.graph.adj[0]), 0)

    def test_edge_count(self):
        self.assertEqual(self.graph.edge_count(), 4)  # 0-1, 0-2, 1-3, 3-4

    def test_bfs(self):
        # Capture BFS output using a list
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.graph.bfs(0)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("BFS Traversal", output)

    def test_dfs(self):
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.graph.dfs(0)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()
        self.assertTrue(output.startswith("0"))  # DFS starts with 0

    def test_connected_components(self):
        components = self.graph.connected_components()
        # Graph is connected initially
        self.assertEqual(len(components), 1)

        # Add a disconnected vertex
        g2 = Graph(3)
        g2.add_edge(0, 1)
        comps = g2.connected_components()
        self.assertEqual(len(comps), 2)  # 0-1 connected, 2 isolated

    def test_is_connected(self):
        self.assertTrue(is_connected(self.graph))
        g = Graph(3)
        g.add_edge(0, 1)
        self.assertFalse(is_connected(g))  # vertex 2 is isolated

    def test_degree(self):
        self.assertEqual(degree(self.graph, 0), 2)  # neighbors: 1, 2
        self.assertEqual(degree(self.graph, 1), 2)  # neighbors: 0, 3

    def test_edges(self):
        all_edges = edges(self.graph)
        self.assertIn((0, 1), all_edges)
        self.assertIn((0, 2), all_edges)
        self.assertIn((1, 3), all_edges)
        self.assertIn((3, 4), all_edges)

    def test_clear(self):
        clear(self.graph)
        self.assertEqual(self.graph.edge_count(), 0)

    def test_clone(self):
        g2 = clone(self.graph)
        self.assertEqual(self.graph.edge_count(), g2.edge_count())
        self.assertTrue(g2.has_edge(0, 1))
        g2.add_edge(1, 4)
        self.assertFalse(self.graph.has_edge(1, 4))  # ensure deep copy


if __name__ == "__main__":
    unittest.main()
