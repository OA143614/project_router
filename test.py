class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.edges = []

    def add_edge(self, u, v, weight):
        self.edges.append((u, v, weight))


class BellmanFord:
    def __init__(self, graph, source):
        self.graph = graph
        self.source = source
        self.distances = {vertex: float('inf') for vertex in graph.vertices}
        self.distances[source] = 0
        self.predecessors = {vertex: None for vertex in graph.vertices}

    def run(self):
        for i in range(len(self.graph.vertices) - 1):
            for u, v, weight in self.graph.edges:
                if self.distances[u] + weight < self.distances[v]:
                    self.distances[v] = self.distances[u] + weight
                    self.predecessors[v] = u

        for u, v, weight in self.graph.edges:
            if self.distances[u] + weight < self.distances[v]:
                print("Negative cycle detected")
                return

        print("Shortest distances:", self.distances)

    def get_shortest_path(self, destination):
        if self.distances[destination] == float('inf'):
            return None, float('inf')  # Destination is not reachable

        path = []
        total_distance = 0
        while destination is not None:
            path.append(destination)
            next_destination = self.predecessors[destination]
            if next_destination is not None:
                for u, v, weight in self.graph.edges:
                    if u == next_destination and v == destination:
                        total_distance += weight
                        break
            destination = next_destination
        return path[::-1], total_distance


if __name__ == '__main__':
    vertices = ['A', 'B', 'C', 'D', 'E']
    graph = Graph(vertices)
    graph.add_edge('A', 'B', 1)
    graph.add_edge('A', 'C', 2)
    graph.add_edge('A', 'E', 4)
    graph.add_edge('B', 'D', 3)
    graph.add_edge('B', 'E', 6)
    graph.add_edge('B', 'A', 1)
    #graph.add_edge('C', 'B', 1)
    graph.add_edge('C', 'D', 3)
    graph.add_edge('C', 'A', 2)
    graph.add_edge('D', 'E', 2)
    graph.add_edge('D', 'B', 3)
    graph.add_edge('D', 'C', 3)
    graph.add_edge('E', 'A', 4)
    graph.add_edge('E', 'B', 6)
    graph.add_edge('E', 'D', 2)
    print(graph)
    bf = BellmanFord(graph, 'A')
    bf.run()
    path, total_distance = bf.get_shortest_path('E')
    print("Shortest path from A to E:", path)
    print("Total distance from A to E:", total_distance)
