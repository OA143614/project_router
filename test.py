class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.edges = []

    def add_edge(self, u, v, weight):
        # Check for duplicates before adding
        if (u, v, weight) not in self.edges:
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

def add_edge(graph, start, end, weight):
    graph.add_edge(start, end, weight)

def add_node_add_edge(graph, vertices, data):
    graph.vertices = vertices
    
    for start, end, weight in data:
        add_edge(graph, start, end, weight)

def show_connections(graph, vertex):
    print(f"Vertices that {vertex} is connected to:")
    seen = set()
    for u, v, weight in graph.edges:
        if u == vertex and (u, v) not in seen:
            print(f"{vertex} <--({weight})--> {v}")
            seen.add((u, v))
            seen.add((v, u))  # Add the reverse direction to avoid duplicates
        elif v == vertex and (v, u) not in seen:
            print(f"{vertex} <--({weight})--> {u}")
            seen.add((u, v))
            seen.add((v, u))  # Add the reverse direction to avoid duplicates
   
       
def main():
    vertices = ['10000', '11000', '12000', '13000', '14000']
    data = [
        ('10000', '11000', 1),
        ('11000', '10000', 1),
        ('10000', '14000', 4),
        ('12000', '10000', 2),
        ('10000', '12000', 2),
        ('11000', '13000', 3),
        ('13000', '11000', 3),
        ('11000', '14000', 6),
        ('14000', '11000', 6),
        ('13000', '14000', 2),
        ('14000', '13000', 2),
        ('12000', '13000', 3),
        ('13000', '14000', 3)
    ]
    
    unique_edges = {}
    for edge in data:
        unique_edges[(edge[0], edge[1])] = edge[2]
        
    filtered_data = [(k[0], k[1], v) for k, v in unique_edges.items()]

    graph = Graph(vertices)
    add_node_add_edge(graph, vertices, filtered_data)
    show_connections(graph, '11000')  # Call the function to show connections for vertex 11000
    
    bf = BellmanFord(graph, '11000')
    bf.run()
    path, total_distance = bf.get_shortest_path('12000')
    print("Shortest path from 11000 to 12000:", path)
    print("Total distance from 11000 to 12000:", total_distance)

if __name__ == "__main__":
    main()