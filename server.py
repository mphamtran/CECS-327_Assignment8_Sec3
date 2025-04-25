import socket

myTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("server launched")
port = int(input("port: "))
print("server listening...")
myTCPSocket.bind(('', port))
myTCPSocket.listen(5)
incomingSocket, incomingAddress = myTCPSocket.accept()
print("client connected: ", incomingAddress)

while 1:
    clientMessage = str(incomingSocket.recv(512), encoding='utf-8')
    print("client message: ", clientMessage)
    serverUpperResponse = clientMessage.upper()
    incomingSocket.send(bytearray(str(serverUpperResponse), encoding='utf-8'))
    if clientMessage == 'q' or clientMessage == 'Q':
        break
    print("server response: ", serverUpperResponse)

print("closing socket")
incomingSocket.close()
