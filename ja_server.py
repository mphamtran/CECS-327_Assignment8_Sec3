import socket
import psycopg2
from datetime import datetime, timedelta
import pytz

# PostgreSQL credentials
DB_CONFIG = {
    "dbname": "neondb",
    "user": "neondb_owner",
    "password": "npg_Og01ckSpdDFZ",
    "host": "ep-weathered-cherry-a5udgsuf-pooler.us-east-2.aws.neon.tech",
    "port": "5432"
}

# Convert UTC time to PST
def convert_to_pst(utc_time):
    pst = pytz.timezone("America/Los_Angeles")
    return utc_time.astimezone(pst).strftime("%Y-%m-%d %I:%M %p %Z")

def handle_query(query):
    try:
        conn = conn = psycopg2.connect(**DB_CONFIG, sslmode='require')
        cur = conn.cursor()

        # Query 1: Moisture (past 3 hours)
        if "average moisture" in query.lower():
            cur.execute("""
                SELECT AVG((payload->>'Moisture')::float)
                FROM "Data_virtual"
                WHERE payload::jsonb ? 'Moisture'
                  AND time > NOW() - INTERVAL '3 hours';
            """)
            result = cur.fetchone()[0]
            return f"Average fridge moisture over past 3 hours: {result:.2f}% RH (PST time)."

        # Query 2: Water consumption
        elif "average water consumption" in query.lower():
            cur.execute("""
                SELECT AVG((payload->>'Water Flow')::float)
                FROM "Data_virtual"
                WHERE payload::jsonb ? 'Water Flow';
            """)
            result = cur.fetchone()[0]
            return f"Average water used per cycle: {result:.2f} gallons."

        # Query 3: Electricity comparison
        elif "consumed more electricity" in query.lower():
            cur.execute("""
                SELECT payload->>'asset_uid' AS device,
                       SUM((payload->>'Ammeter 2')::float) AS total_amps
                FROM "Data_virtual"
                WHERE payload::jsonb ? 'Ammeter 2'
                GROUP BY device
                ORDER BY total_amps DESC
                LIMIT 3;
            """)
            results = cur.fetchall()
            reply = "Total electricity usage (by Amps):\n"
            for row in results:
                reply += f"- Device {row[0]}: {row[1]:.2f} A\n"
            return reply

        else:
            return "Unknown query."

    except Exception as e:
        return f"Server error: {e}"
    finally:
        cur.close()
        conn.close()

def start_server():
    try:
        ip = input("Enter the server IP address: ")
        port = int(input("Enter the server port number: "))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((ip, port))
            server_socket.listen(5)
            print(f"Server listening on {ip}:{port}")

            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break

                    message = data.decode().strip()
                    print(f"Received: {message}")

                    if message.lower() == 'q':
                        break

                    response = handle_query(message)
                    conn.sendall(response.encode())

            print("Server is shutting down.")

    except ValueError:
        print("Invalid port number.")
    except socket.error as e:
        print(f"Socket error: {e}")

if __name__ == "__main__":
    start_server()
