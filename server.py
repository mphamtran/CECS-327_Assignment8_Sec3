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
    return utc_time.astimezone(pst)

def handle_query(query):
    try:
        conn = conn = psycopg2.connect(**DB_CONFIG, sslmode='require')
        cur = conn.cursor()

        # Query 1: Moisture (past 3 hours)
        if "average moisture" in query.lower():
            cur.execute("""
                SELECT AVG((payload->>'Moisture Meter - Moisture Meter')::float)
                FROM "Data_virtual"
                WHERE payload::jsonb ? 'Moisture Meter - Moisture Meter'
                    AND time > timezone('America/Los_Angeles', now()) - INTERVAL '3 hours';
            """)
            result = cur.fetchone()[0]

            if result is None:
                return "No moisture data available yet."
            else:
                now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
                now_pst = convert_to_pst(now_utc)
                start_pst = now_pst - timedelta(hours=3)

                time_range = f"{start_pst.strftime('%I:%M %p')} to {now_pst.strftime('%I:%M %p')} (PST)"

                return f"Average fridge moisture over past 3 hours: {result:.2f}% RH.\n" \
                       f"Reading from: {time_range}"

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
                SELECT
                    payload->>'parent_asset_uid' AS device,
                    SUM(
                        COALESCE((payload::jsonb->>'Ammeter 1')::float, 0) +
                        COALESCE((payload::jsonb->>'Ammeter 2')::float, 0) +
                        COALESCE((payload::jsonb->>'sensor 2 d84ed403-486c-417d-ae0b-bd73664ff426')::float, 0)
                    ) AS total_amps
                FROM "Data_virtual"
                WHERE
                    payload::jsonb ? 'Ammeter 1'
                    OR payload::jsonb ? 'Ammeter 2'
                    OR payload::jsonb ? 'sensor 2 d84ed403-486c-417d-ae0b-bd73664ff426'
                GROUP BY device
                ORDER BY total_amps DESC
                LIMIT 1;
            """)
            results = cur.fetchall()
            if results:
                device, total_amps = results[0]
                kwh = total_amps * 0.002

                # Step 2: Get human-readable name from metadata
                cur.execute("""
                    SELECT "assetType"
                    FROM "Data_metadata"
                    WHERE "assetUid" = %s;
                """, (device,))
                name_result = cur.fetchone()
                device_name = name_result[0] if name_result else device

                return f"{device_name} used the most electricity: {kwh:.4f} kWh"
            else:
                return "No electricity data available."

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
