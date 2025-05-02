import socket

myTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("client launched")
serverPort = int(input("server port: "))
serverIP = input("server ip: ")
myTCPSocket.connect((serverIP, serverPort))

query = '''1. "What is the average moisture inside my kitchen fridge in the past three hours?"
2. "What is the average water consumption per cycle in my smart dishwasher?"
3. "Which device consumed more electricity among my three IoT devices?"
q. Exit'''
print(query)

while 1:
    userQuery = input("Input query number: ")

    if userQuery.lower() == 'q':
        myTCPSocket.send(bytearray(str(userQuery.lower()), encoding='utf-8'))
        break

    try:
        if not (1 <= int(userQuery) <= 4):
            print("Invalid Input")
            print(query)
    except ValueError:
        print("Invalid Input")
        print(query)

    myTCPSocket.send(bytearray(userQuery, encoding='utf-8'))
    print("server response:", myTCPSocket.recv(1024).decode())

print("closing socket")
myTCPSocket.close()
