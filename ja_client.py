import socket

# Valid queries expected by the server
VALID_QUERIES = {
    "1": "What is the average moisture inside my kitchen fridge in the past three hours?",
    "2": "What is the average water consumption per cycle in my smart dishwasher?",
    "3": "Which device consumed more electricity among my three IoT devices?"
}

def print_query_options():
    print("\nAvailable Queries:")
    for key, query in VALID_QUERIES.items():
        print(f"{key}. {query}")
    print("Type 'q' to quit.\n")

def start_client():
    try:
        ip = input("Enter the server IP address: ")
        port = int(input("Enter the server port number: "))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((ip, port))
            print(f"Connected to server {ip}:{port}")

            while True:
                print_query_options()
                choice = input("Select a query by number (or type your query): ").strip()

                if choice.lower() == 'q':
                    client_socket.sendall(b'q')
                    break

                # Check if user entered a valid number or full query
                if choice in VALID_QUERIES:
                    message = VALID_QUERIES[choice]
                elif choice in VALID_QUERIES.values():
                    message = choice
                else:
                    print("❌ Invalid query. Please try one of the listed options.")
                    continue

                # Send the valid query to the server
                client_socket.sendall(message.encode())

                # Receive and print the response
                response = client_socket.recv(4096).decode()
                print(f"\n✅ Server reply:\n{response}\n")

    except ValueError:
        print("Invalid port number. Please enter a valid port.")
    except socket.error as e:
        print(f"Socket error: {e}")

if __name__ == "__main__":
    start_client()
