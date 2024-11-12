# Based on https://thecodeninja.net/2014/12/udp-chat-in-python/
import sys, select, socket
 
# Read a line. Using select for non blocking reading of sys.stdin
def getLine():
    i,o,e = select.select([sys.stdin],[],[],0.0001)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return input
    return False

print ("Number of arguments:", len(sys.argv), "arguments.")
print ("Argument List:", str(sys.argv))
print ("Second argument", str(sys.argv[1]))


 
# host = input("Please Enter Remote IP: ")
# port = input("Please Enter Remote Port: ")


clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # Create Datagram Socket (UDP)
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Make Socket Reusable

# s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Allow incoming broadcasts

incomingPort = int(str(sys.argv[1]));
print ("This chat client will listen to incoming port: ", incomingPort)

clientSocket.setblocking(False) # Set socket to non-blocking mode
clientSocket.bind(('', incomingPort)) #Accept Connections on port
print ("This client is accepting connections on port", incomingPort)
 
while 1:
    try:
        message, address = clientSocket.recvfrom(8192) # Buffer size is 8192. Change as needed.
        if message:
            print (address, "> ", message.decode())
    except:
        pass
 
    input = getLine();
    if(input != False):
        print ("input is: ", input)
        delimitedInput = input.split(' ')
        print (delimitedInput)
        (command, remoteHost, remotePort, message) = delimitedInput
        print ("Command: ", command)
        print ("Remote host address: ", remoteHost)
        print ("Remote port :", remotePort)
        print ("Message: ", message)
        remoteAddressAndPort = (remoteHost, int(remotePort)) # Set the address to send to
        clientSocket.sendto(input.encode(), remoteAddressAndPort)