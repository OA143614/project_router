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

status_router = 'off'
status_protocol = 'stop'

while True:
    try:
        message, address = clientSocket.recvfrom(8192)  # Buffer size is 8192. Change as needed.
        message = message.decode().rstrip()  # Decode the message and strip any trailing whitespace.
        print(status_router)
        print(status_protocol)
        if message == 'on':
            status_router = 'on'
            
        elif message == 'off':
            status_router = 'off'
            
        elif message == 'start':
            status_protocol = 'start'
            
        elif message == 'stop':
            status_protocol = 'stop'
            
    except BlockingIOError:
        # No data available, continue the loop
        pass

    input = getLine()
    if input != False:
        print("input is:", input)
        clientSocket.sendto(input.encode(), remoteAddressAndPort)