import socket

myTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("client launched")
serverPort = int(input("server port: "))
serverIP = input("server ip: ")
myTCPSocket.connect((serverIP, serverPort))
print("type q to close socket")

while 1:
    clientMessage = input("message: ")
    if clientMessage != 'q' and clientMessage != 'Q':
        myTCPSocket.send(bytearray(str(clientMessage), encoding='utf-8'))
        print("server response:", myTCPSocket.recv(1024).decode())
    else:
        myTCPSocket.send(bytearray(str(clientMessage), encoding='utf-8'))
        break

print("closing socket")
myTCPSocket.close()
