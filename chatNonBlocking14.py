import sys, select, socket,time

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

incomingPort = 14000

clientSocket.setblocking(False)  # Set socket to non-blocking mode
clientSocket.bind(('', incomingPort))  # Accept Connections on port
print("This client is accepting connections on port", incomingPort)

#stop route information
stop_route = []

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
    output = []
    output.append(f"Vertices that {vertex} is connected to:")
    seen = set()
    for u, v, weight in graph.edges:
        if u == vertex and (u, v) not in seen:
            output.append(f"{vertex} <--({weight})--> {v}")
            seen.add((u, v))
            seen.add((v, u))  # Add the reverse direction to avoid duplicates
        elif v == vertex and (v, u) not in seen:
            output.append(f"{vertex} <--({weight})--> {u}")
            seen.add((u, v))
            seen.add((v, u))  # Add the reverse direction to avoid duplicates
    return "\n".join(output) if output else f"No connections found for vertex {vertex}"

def update_interface(message):
    try:
        parts = message.split()
        if len(parts) != 3:
            raise ValueError("Invalid message format")
        u, v, weight = parts[0], parts[1], int(parts[2])
        edge_data = (u, v, weight)
        reverse_edge_data = (v, u, weight)
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
    except Exception as e:
        print("Error updating interface:", e)

def finding_path(message):
    try:
        parts = message.split()
        if len(parts) != 2:
            raise ValueError("Invalid message format")
        
        source, destination = parts
        graph = Graph(vertices)
        add_node_add_edge(graph, vertices, data)
        
        bf = BellmanFord(graph, source)
        bf.run()
        
        path, total_distance = bf.get_shortest_path(destination)
        
        sent_path = f"Shortest path from {source} to {destination}: {path}"
        clientSocket.sendto(sent_path.encode(), (host, 65432))
        
        sent_total_path = f"Total distance from {source} to {destination}: {total_distance}"
        clientSocket.sendto(sent_total_path.encode(), (host, 65432))
    
    except Exception as e:
        print("Error finding path:", e)

def update_recieve_interface(message):
    try:
        # Convert the string representation of the list to an actual list
        import ast
        message_list = ast.literal_eval(message)
        for edge in message_list:
            u, v, weight = edge
            edge_data = (u, v, weight)
            reverse_edge_data = (v, u, weight)
            edge_exists = False
            for i, existing_edge in enumerate(data):
                if (existing_edge[0] == edge_data[0] and existing_edge[1] == edge_data[1]) or \
                   (existing_edge[0] == reverse_edge_data[0] and existing_edge[1] == reverse_edge_data[1]):
                    edge_exists = True
                    # If the weight is different, update the edge
                    if existing_edge[2] != edge_data[2]:
                        data[i] = edge_data
                    break
            if not edge_exists:
                data.append(edge_data)  # Add new edge if it doesn't exist
    except Exception as e:
        print("Error updating interface:", e)

# Data
vertices = ['10000', '11000', '12000', '13000', '14000']
data = [('10000', '14000', 4),
        ('11000', '14000', 6),
        ('13000', '14000', 2)
        ]

ports = ['10000', '11000', '13000']
    

#log display
def log_routing_advertisement(message, direction, address=None):
    with open("routing_log14.txt", "a") as log_file:
        if address:
            log_file.write(f"{direction}: {message}, Address: {address}\n")
        else:
            log_file.write(f"{direction}: {message}\n")


def display_routing_advertisements():
    with open("routing_log14.txt", "r") as log_file:
        return log_file.read()

# Initialize variables
status_router = 'off'
status_protocol = 'stop'
display_ads = False  # Flag to control display of advertisements
# Clear the routing log file at the start
open("routing_log14.txt", "w").close()

while True:
    
    #listening and recieving the message from other hosts
    try:
        message, address = clientSocket.recvfrom(8192)  # Buffer size is 8192. Change as needed.
        message = message.decode().rstrip()  # Decode the message and strip any trailing whitespace.
        print("Received message:", message)
        log_routing_advertisement(message, "Incoming",address[1])
        
        #when recieving start command
        if message == 'start':
            print('start')
            status_protocol = 'start'
        elif message == 'stop':
            print('stop')
            status_protocol = 'stop'
            data = [('10000', '14000', 100),
                    ('11000', '14000', 100),
                    ('13000', '14000', 100)
                    ]
            
            while True:
                try:
                    for port in ports:
                        clientSocket.sendto("recieve".encode(), (host, int(port)))
                        log_routing_advertisement("recieve", "Outgoing",int(port))
                        data_str = str(data)
                        clientSocket.sendto(data_str.encode(), (host, int(port)))
                        log_routing_advertisement(data_str, "Outgoing",int(port))
                        
                        break
                except BlockingIOError:
                    continue  # Continue waiting for the message

        elif message == 'routing' and status_protocol == 'start':
            print('routing')
            while True:
                try:
                    message, address = clientSocket.recvfrom(8192)
                    message = message.decode().rstrip()
                    parts = message.split()
                    update_interface(message)
                    clientSocket.sendto("recieve".encode(), (host, int(parts[1])))
                    log_routing_advertisement("recieve", "Outgoing",int(parts[1]))
                    data_str = str(data)
                    clientSocket.sendto(data_str.encode(), (host, int(parts[1])))
                    log_routing_advertisement(data_str, "Outgoing",int(parts[1]))
                    break
                except BlockingIOError:
                    continue  # Continue waiting for the message

        #routing all interfaces command
        elif message == 'allinterface' and status_protocol == 'start':
            print('allinter')
            while True:
                try:
                    for port in ports:
                        if port not in stop_route:
                            clientSocket.sendto("recieve".encode(), (host, int(port)))
                            log_routing_advertisement("recieve", "Outgoing",int(port))
                            data_str = str(data)
                            clientSocket.sendto(data_str.encode(), (host, int(port)))
                            log_routing_advertisement(data_str, "Outgoing",int(port))
                    break
                except BlockingIOError:
                    continue  # Continue waiting for the message

        #stopping protocol 14000 10000 1000
        elif message == 'deactive'and status_protocol == 'start':
            print('deactive')
            while True:
                try:
                    message, address = clientSocket.recvfrom(8192)
                    message = message.decode().rstrip()
                    parts = message.split()
                    stop_route.append(parts[1])
                    update_interface(message)
                    for port in ports:
                        print(port)
                        if port not in stop_route:
                            print(port)
                            clientSocket.sendto("recieve".encode(), (host, int(port)))
                            log_routing_advertisement("recieve", "Outgoing",int(port))
                            data_str = str(data)
                            clientSocket.sendto(data_str.encode(), (host, int(port)))
                            log_routing_advertisement(data_str, "Outgoing",int(port))
                    break
                except BlockingIOError:
                    continue  # Continue waiting for the message
        #active protocol 14000 10000 6
        elif message == 'active'and status_protocol == 'start':
            print('active')
            while True:
                try:
                    message, address = clientSocket.recvfrom(8192)
                    message = message.decode().rstrip()
                    parts = message.split()
                    stop_route.remove(parts[1])
                    update_interface(message)
                    for port in ports:
                        if port not in stop_route:
                            clientSocket.sendto("recieve".encode(), (host, int(port)))
                            log_routing_advertisement("recieve", "Outgoing",int(port))
                            data_str = str(data)
                            clientSocket.sendto(data_str.encode(), (host, int(port)))
                            log_routing_advertisement(data_str, "Outgoing",int(port))
                    break
                except BlockingIOError:
                    continue  # Continue waiting for the message
        #send display when cli send show command
        elif message == 'show':
            # Convert data to string and send to the client
            print('show')
            data_str = str(data)
            clientSocket.sendto(data_str.encode(), (host, address[1]))
            log_routing_advertisement(data_str, "Outgoing", address[1])
    
            # Create the graph and add nodes and edges
            graph = Graph(vertices)
            add_node_add_edge(graph, vertices, data)
    
            # Show connections for vertex 10000 (or 11000 if that's the correct one)
            for vertex in ['14000']:
                connections = show_connections(graph, vertex)
                clientSocket.sendto(connections.encode(), (host, address[1]))
            log_routing_advertisement(connections, "Outgoing", address[1])

            # Show status of the protocol
            sent_status = 'status protocol is '+ status_protocol
            clientSocket.sendto(sent_status.encode(), (host, address[1]))
            log_routing_advertisement(sent_status, "Outgoing", address[1])
            
            
        #recieve new table from routers that it connected and send updated table to outgoing table
        elif message == 'recieve' and status_protocol == 'start':
            print('recieve')
            while True:
                try:
                    message, address = clientSocket.recvfrom(8192)
                    message = message.decode().rstrip()
                    update_recieve_interface(message)
                    for port in ports:
                        clientSocket.sendto("update".encode(), (host,  int(port)))
                        log_routing_advertisement("update", "Outgoing",  int(port))
                        data_str = str(data)
                        clientSocket.sendto(data_str.encode(), (host,  int(port)))
                        log_routing_advertisement(data_str, "Outgoing",  int(port))
                    break  # Exit the loop after receiving the message
                except BlockingIOError:
                    continue  # Continue waiting for the message

        #getting updated table from router that connecting
        elif message == 'update' and status_protocol == 'start':
            print('update')
            while True:
                try:
                    message, address = clientSocket.recvfrom(8192)
                    message = message.decode().rstrip()
                    log_routing_advertisement(message, "Incoming",address[1])
                    update_recieve_interface(message)
                    break  # Exit the loop after receiving the message
                except BlockingIOError:
                    continue  # Continue waiting for the message

        elif message == 'path':
            print('path')
            while True:
                try:
                    message, address = clientSocket.recvfrom(8192)
                    message = message.decode().rstrip()
                    parts = message.split()
                    finding_path(message)
                    break
                except BlockingIOError:
                    continue  # Continue waiting for the message


        #handling log display
        elif message == 'log_start_display':
            print('on')
            display_ads = True
            clientSocket.sendto("Started displaying routing advertisements.".encode(), (host, address[1]))
            print(display_routing_advertisements())
        elif message == 'log_stop_display':
            print('off')
            display_ads = False
            clientSocket.sendto("Stopped displaying routing advertisements.".encode(), (host, address[1]))
        if display_ads:
            print(display_routing_advertisements())
        time.sleep(1)  # Sleep for a short period to avoid busy-waiting
    except BlockingIOError:
        # No data available, continue the loop
        pass
