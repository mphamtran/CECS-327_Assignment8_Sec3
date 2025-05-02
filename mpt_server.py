import socket
import psycopg2
import pytz
import datetime

database = "postgresql://A8Database_owner:npg_7cnIKPD0Ldpf@ep-dark-wave-a43ghf46-pooler.us-east-1.aws.neon.tech/A8Database?sslmode=require"

conn = psycopg2.connect(database)
cur = conn.cursor()

myTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("server launched")
port = int(input("port: "))
print("server listening...")
myTCPSocket.bind(('', port))
myTCPSocket.listen(5)
incomingSocket, incomingAddress = myTCPSocket.accept()
print("client connected: ", incomingAddress)

query = '''1. "What is the average moisture inside my kitchen fridge in the past three hours?"
2. "What is the average water consumption per cycle in my smart dishwasher?"
3. "Which device consumed more electricity among my three IoT devices?"
q. Exit'''
print(query)


def convert_time(utc_time):
    pst = pytz.timezone("US/Pacific")
    utc = pytz.timezone("UTC")
    utc_time = utc.localize(utc_time)
    return utc_time.astimezone(pst)


while 1:
    clientQuery = str(incomingSocket.recv(512), encoding='utf-8')
    print("clientQuery: ", clientQuery)
    if clientQuery == 'q':
        break
    # 1. "What is the average moisture inside my kitchen fridge in the past three hours?"
    elif int(clientQuery) == 1:
        cur.execute("""SELECT payload FROM "Table_0_virtual;""")
        result = cur.fetchone()[0]
        now_utc = datetime.utcnow()
        now_pst = convert_time(now_utc)
    elif int(clientQuery) == 2:
        print()
    elif int(clientQuery) == 3:
        print()
    elif int(clientQuery) == 4:
        print()
    # serverUpperResponse = clientQuery.upper()
    # incomingSocket.send(bytearray(str(serverUpperResponse), encoding='utf-8'))

print("closing socket")
incomingSocket.close()
