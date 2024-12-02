import sys
import select
import socket

# List to store router addresses
router_address = []

# Read a line using select for non-blocking reading of sys.stdin
def getLine():
    i, o, e = select.select([sys.stdin], [], [], 0.0001)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return input
    return False

print("Number of arguments:", len(sys.argv), "arguments.")
print("Argument List:", str(sys.argv))
print("Second argument", str(sys.argv[1]))

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create Datagram Socket (UDP)
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Make Socket Reusable

incomingPort = int(str(sys.argv[1]))
print("This chat client will listen to incoming port:", incomingPort)

clientSocket.setblocking(False)  # Set socket to non-blocking mode
clientSocket.bind(('', incomingPort))  # Accept Connections on port
print("This client is accepting connections on port", incomingPort)

while True:
    try:
        message, address = clientSocket.recvfrom(8192)  # Buffer size is 8192. Change as needed.
        router_address.append(address)
        
        if message:
            print(address, "> ", message.decode())
    except:
        pass

    user_input = getLine()
    if user_input:
        user_input = input("Enter command: ")
        if user_input == 'ls':
            print(router_address)

        #using start command  start #port enter then source destination weight
        elif user_input.startswith('routing'):
            print("input is:", user_input)
            delimitedInput = user_input.split(' ')
            print(delimitedInput)
            command, remotePort = delimitedInput
            remoteAddressAndPort = ('127.0.0.1', int(remotePort))  # Set the address to send to
            clientSocket.sendto(command.encode(), remoteAddressAndPort)
            start_route_command = input("Enter command: ")
            print("input is:", start_route_command)
            delimitedInput = start_route_command.split(' ')
            print(delimitedInput)
            source, destination, weight = delimitedInput
            print("source:", source)
            print("destination:", destination)
            print("weight:", weight)
            #print("Remote port:", remotePort)
            remoteAddressAndPort = ('127.0.0.1', int(remotePort))  # Set the address to send to
            clientSocket.sendto(start_route_command.encode(), remoteAddressAndPort)

        #using start command  stop #port enter then source destination 1000
        elif user_input.startswith('deactive'):
            print("input is:", user_input)
            delimitedInput = user_input.split(' ')
            print(delimitedInput)
            command, remotePort = delimitedInput
            remoteAddressAndPort = ('127.0.0.1', int(remotePort))  # Set the address to send to
            clientSocket.sendto(command.encode(), remoteAddressAndPort)
            start_route_command = input("Enter command: ")
            print("input is:", start_route_command)
            delimitedInput = start_route_command.split(' ')
            print(delimitedInput)
            source, destination, weight = delimitedInput
            print("source:", source)
            print("destination:", destination)
            print("weight:", weight)
            #print("Remote port:", remotePort)
            remoteAddressAndPort = ('127.0.0.1', int(remotePort))  # Set the address to send to
            clientSocket.sendto(start_route_command.encode(), remoteAddressAndPort)

        elif user_input.startswith('active'):
            print("input is:", user_input)
            delimitedInput = user_input.split(' ')
            print(delimitedInput)
            command, remotePort = delimitedInput
            remoteAddressAndPort = ('127.0.0.1', int(remotePort))  # Set the address to send to
            clientSocket.sendto(command.encode(), remoteAddressAndPort)
            start_route_command = input("Enter command: ")
            print("input is:", start_route_command)
            delimitedInput = start_route_command.split(' ')
            print(delimitedInput)
            source, destination, weight = delimitedInput
            print("source:", source)
            print("destination:", destination)
            print("weight:", weight)
            #print("Remote port:", remotePort)
            remoteAddressAndPort = ('127.0.0.1', int(remotePort))  # Set the address to send to
            clientSocket.sendto(start_route_command.encode(), remoteAddressAndPort)

        elif user_input.startswith('path'):
            print("input is:", user_input)
            delimitedInput = user_input.split(' ')
            print(delimitedInput)
            command, remotePort = delimitedInput
            remoteAddressAndPort = ('127.0.0.1', int(remotePort))  # Set the address to send to
            clientSocket.sendto(command.encode(), remoteAddressAndPort)
            path_route_command = input("Enter command: ")
            print("input is:", path_route_command)
            delimitedInput = path_route_command.split(' ')
            print(delimitedInput)
            source, destination = delimitedInput
            print("source:", source)
            print("destination:", destination)
            #print("Remote port:", remotePort)
            remoteAddressAndPort = ('127.0.0.1', int(remotePort))  # Set the address to send to
            clientSocket.sendto(path_route_command.encode(), remoteAddressAndPort)

        #command for allinterface 
        else:
            print("input is:", user_input)
            delimitedInput = user_input.split(' ')
            print(delimitedInput)
            if len(delimitedInput) == 2:
                command, remotePort = delimitedInput
                print("Command:", command)
                print("Remote port:", remotePort)
                remoteAddressAndPort = ('127.0.0.1', int(remotePort))  # Set the address to send to
                clientSocket.sendto(command.encode(), remoteAddressAndPort)
            else:
                print("Invalid command format. Please use 'command remotePort'.")