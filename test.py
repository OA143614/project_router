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

def main():
    vertices = ['10000', '11000', '12000', '13000', '14000']
    data = [
        ('10000', '11000', 4),
        ('10000', '11000', 50),
        #('B', 'A', 4),
        ('11000', '12000', 1),
        #('C', 'A', 50),
        ('12000', '11000', 1),
       # ('A', 'B', 60)
        

    ]
    data.append(('11000', '12000', 1))
    data.append(('12000','11000',1))

    
    # Use a dictionary to track unique edges and their values
    unique_edges = {}

    for edge in data:
        print(edge[0], edge[1],edge[2])
        unique_edges[(edge[0], edge[1])] = edge[2]
        
    # Convert the dictionary back to a list of tuples
    filtered_data = [(k[0], k[1], v) for k, v in unique_edges.items()]

    print(filtered_data)
    graph = Graph(vertices)
    add_node_add_edge(graph, vertices, filtered_data)
    
    print(graph.edges)
    bf = BellmanFord(graph, '10000')
    bf.run()
    path, total_distance = bf.get_shortest_path('12000')
    print("Shortest path from 10000 to 12000:", path)
    print("Total distance from 10000 to 12000:", total_distance)

if __name__ == "__main__":
    main()