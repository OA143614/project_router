import sys, select, socket

# Read a line. Using select for non-blocking reading of sys.stdin
def getLine():
    i, o, e = select.select([sys.stdin], [], [], 0.0001)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return input
    return False

# Ask IP address and port of remote partner
host = '127.0.0.1'  # input("Please Enter Remote IP: ")
port = 65432  # input("Please Enter Remote Port: ")

remoteAddressAndPort = (host, int(port))  # Set the address to send to
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create Datagram Socket (UDP)
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Make Socket Reusable

# s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Allow incoming broadcasts

incomingPort = 12000

clientSocket.setblocking(False)  # Set socket to non-blocking mode
clientSocket.bind(('', incomingPort))  # Accept Connections on port
print("This client is accepting connections on port", incomingPort)

# Add routing algorithm
class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.edges = set()  # Use a set to store edges

    def add_edge(self, u, v, weight):
        self.edges.add((u, v, weight))  # Add the edge (u, v)
        self.edges.add((v, u, weight))  # Add the reverse edge (v, u)

class BellmanFord:
    def __init__(self, graph, source):
        self.graph = graph
        self.source = source
        self.distances = {vertex: float('inf') for vertex in graph.vertices}
        self.distances[source] = 0
        self.predecessors = {vertex: None for vertex in graph.vertices}

    def run(self):
        for _ in range(len(self.graph.vertices) - 1):
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

def update_interface(message):
    try:
        parts = message.split()
        if len(parts) != 3:
            raise ValueError("Invalid message format")
        u, v, weight = parts[0], parts[1], int(parts[2])
        edge_data = (u, v, weight)
        reverse_edge_data = (v, u, weight)
        print("Updating interface with edge:", reverse_edge_data)
        edge_exists = False
        for i, existing_edge in enumerate(data):
            if (existing_edge[0] == edge_data[0] and existing_edge[1] == edge_data[1]) or \
               (existing_edge[0] == reverse_edge_data[0] and existing_edge[1] == reverse_edge_data[1]):
                edge_exists = True
                # If the weight is different, update the edge
                if existing_edge[2] != edge_data[2]:
                    data[i] = edge_data
                    print("Edge updated:", edge_data)
                break
        if not edge_exists:
            data.append(edge_data)  # Add new edge if it doesn't exist
            print("Edge added:", edge_data)
        print("Updated data:", data)
    except Exception as e:
        print("Error updating interface:", e)

def update_recieve_interface(message):
    try:
        # Convert the string representation of the list to an actual list
        import ast
        message_list = ast.literal_eval(message)
        
        for edge in message_list:
            u, v, weight = edge
            edge_data = (u, v, weight)
            reverse_edge_data = (v, u, weight)
            print("Updating interface with edge:", edge_data)
            edge_exists = False
            for i, existing_edge in enumerate(data):
                if (existing_edge[0] == edge_data[0] and existing_edge[1] == edge_data[1]) or \
                   (existing_edge[0] == reverse_edge_data[0] and existing_edge[1] == reverse_edge_data[1]):
                    edge_exists = True
                    # If the weight is different, update the edge
                    if existing_edge[2] != edge_data[2]:
                        data[i] = edge_data
                        print("Edge updated:", edge_data)
                    break
            if not edge_exists:
                data.append(edge_data)  # Add new edge if it doesn't exist
                print("Edge added:", edge_data)
        print("Updated data:", data)
    except Exception as e:
        print("Error updating interface:", e)
        
# Data
vertices = ['10000', '11000', '12000', '13000', '14000']
data = [('12000', '13000', 2) ]

status_router = 'off'
status_protocol = 'stop'

while True:
    try:
        message, address = clientSocket.recvfrom(8192)  # Buffer size is 8192. Change as needed.
        message = message.decode().rstrip()  # Decode the message and strip any trailing whitespace.
        print("Received message:", message)
        if message == 'on':
            status_router = 'on'
        elif message == 'off':
            status_router = 'off'
        elif message == 'start':
            print("Entering add start block")
            while True:
                try:
                    message, address = clientSocket.recvfrom(8192)  # Buffer size is 8192. Change as needed.
                    message = message.decode().rstrip()  # Decode the message and strip any trailing whitespace.
                    print("Received edge to add:", message)
                    parts = message.split()
                    print("access to the port:", parts[1])
                    update_interface(message)
                    print("Data after update:", data)
                    clientSocket.sendto("recieve".encode(), (host, int(parts[1])))
                    data_str = str(data)
                    clientSocket.sendto(data_str.encode(), (host, int(parts[1])))
                    break
                except BlockingIOError:
                    continue  # Continue waiting for the message
        elif message == 'allinterface':
            print('start all interface')
            while True:
                try:
                    print("Data after update:", data)
                    clientSocket.sendto("recieve".encode(), (host, int(parts[1])))
                    data_str = str(data)
                    clientSocket.sendto(data_str.encode(), (host, int(parts[1])))
                    break
                except BlockingIOError:
                    continue  # Continue waiting for the message

        elif message == 'stop':
            status_protocol = 'stop'
        elif message == 'show':
            print('router status: ', status_router)
            print('protocol status: ', status_protocol)
            graph = Graph(vertices)
            add_node_add_edge(graph, vertices, data)
            show_connections(graph, '12000')  # Call the function to show connections for vertex 12000
            bf = BellmanFord(graph, '11000')
            bf.run()
            path, total_distance = bf.get_shortest_path('12000')
            print("Shortest path from 11000 to 12000:", path)
            print("Total distance from 11000 to 12000:", total_distance)
        elif message == 'recieve':
            print("Entering add block")
            while True:
                try:
                    message, address = clientSocket.recvfrom(8192)  # Buffer size is 8192. Change as needed.
                    message = message.decode().rstrip()  # Decode the message and strip any trailing whitespace.
                    
                    print("Received edge to add:", message)
                    update_recieve_interface(message)
                    print("Data after update:", data)
                    clientSocket.sendto("update".encode(), (host, address[1]))
                    data_str = str(data)
                    clientSocket.sendto(data_str.encode(), (host, address[1]))
                    break  # Exit the loop after receiving the message
                except BlockingIOError:
                    continue  # Continue waiting for the message
            
        elif message == 'update':
            print("Entering add block")
            while True:
                try:
                    message, address = clientSocket.recvfrom(8192)  # Buffer size is 8192. Change as needed.
                    message = message.decode().rstrip()  # Decode the message and strip any trailing whitespace.
                    
                    print("Received edge to add:", message)
                    update_recieve_interface(message)
                    print("Data after update:", data) 
                    break  # Exit the loop after receiving the message
                except BlockingIOError:
                    continue  # Continue waiting for the message        
    except BlockingIOError:
        # No data available, continue the loop
        pass

    input = getLine()
    if input != False:
        print("input is:", input)
        clientSocket.sendto(input.encode(), remoteAddressAndPort)