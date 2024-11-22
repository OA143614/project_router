# Based on https://thecodeninja.net/2014/12/udp-chat-in-python/
import sys, select, socket

#data=[] 
# Read a line. Using select for non blocking reading of sys.stdin
def getLine():
    i,o,e = select.select([sys.stdin],[],[],0.0001)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return input
    return False
#ask IP address and port of remote partner
host = '127.0.0.1'    #input("Please Enter Remote IP: ")
port = 65432 #input("Please Enter Remote Port: ")

remoteAddressAndPort = (host, int(port)) # Set the address to send to
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # Create Datagram Socket (UDP)
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Make Socket Reusable

# s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Allow incoming broadcasts

incomingPort = 11000;

clientSocket.setblocking(False) # Set socket to non-blocking mode
clientSocket.bind(('', incomingPort)) #Accept Connections on port
print ("This client is accepting connections on port", incomingPort)
#routing protocol
class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.edges = []

    def add_edge(self, u, v, weight):
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

def router_cal(graph,go_to_distance):
    bf = BellmanFord(graph, '11000')
    bf.run()
    path, total_distance = bf.get_shortest_path(go_to_distance)
    print("Shortest path from 11000 to 12000:", path)
    print("Total distance from 11000 to 12000:", total_distance)


vertices = ['10000', '11000', '12000', '13000', '14000'] 
data = [
        ('10000', '11000', 2),
        ('11000', '10000', 2),
        ('11000', '12000', 8),
        ('12000', '11000', 8)
        

    ]
while 1:
    
    try:
        #print(data)
        
        message, address = clientSocket.recvfrom(20000) # Buffer size is 8192. Change as needed.
        decoded_message = message.decode().rstrip()  # Decode and strip whitespace
        #print(f"Received message: '{decoded_message}'")  # Debugging output
        print(decoded_message=='on')
        # Check the exact length and content of the decoded message

        if decoded_message == 'on' or decoded_message == 'off' and address[1] == 65432:
            print("sending")
           
            for edge_table in data:
                edge_table_str = f"({edge_table[0]}, {edge_table[1]}, {edge_table[2]})"
                clientSocket.sendto(edge_table_str.encode(), (host, 12000))  # send routing table to connect host
            
        else:
            print("recieve")
            print(decoded_message)
            print (address[1], "> ", message.decode())
            # Assuming the message is a string representation of a tuple
            edge = eval(message.decode())
            edge_data = (str(edge[0]), str(edge[1]), edge[2])
            print(edge_data,"1")
            for i, existing_edge in enumerate(data):
                if existing_edge[0] == edge_data[0] and existing_edge[1] == edge_data[1]:
                    edge_exists = True
                    # If the weight is different, update the edge
                    if existing_edge[2] != edge_data[2]:
                        data[i] = edge_data
                        #clientSocket.sendto("edge_data".encode(),(host, 12000))
                    break
           
            graph = Graph(vertices)
            add_node_add_edge(graph, vertices, data)
    
            print(graph.edges)
         
    except:
        pass
 
    
    user_input = getLine()
    if user_input != False:
        if user_input.strip() == 'on':  # Use strip() to remove any extra whitespace
            print("input is: ", user_input)
            clientSocket.sendto(user_input.encode(), remoteAddressAndPort)
        elif user_input.strip() == 'cal':  # Use strip() to remove any extra whitespace
            to_destination = str(input("Enter destination: ").strip())
            #print("enter destination: ", to_destination)
            print(data)
            graph = Graph(vertices)
            add_node_add_edge(graph, vertices, data)
            router_cal(graph, to_destination)
        elif user_input.strip() == 'msg':  # Use strip() to remove any extra whitespace
            msg_to_send = str(input("Enter message: ").strip())
            msg_to_destination = str(input("Enter destination: ").strip())
            graph = Graph(vertices)
            add_node_add_edge(graph, vertices, data)
    
            #print(graph.edges)
            bf = BellmanFord(graph, '11000')
            bf.run()
            path, total_distance = bf.get_shortest_path(msg_to_destination)
            print("Shortest path from 11000 to 12000:", path[1])
            clientSocket.sendto(msg_to_send.encode(),(host, int(path[1])))
            #print("Total distance from 11000 to 12000:", total_distance)

    