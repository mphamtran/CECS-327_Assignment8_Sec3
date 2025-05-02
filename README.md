# CECS 327 Assignment 8: Build an End-to-End IoT System  
### Group 9: Janet Ayala and Michael Pham-Tran  

# IoT Smart Device Query System  

This project demonstrates a Python-based client-server system that queries real-time IoT device data from a PostgreSQL database (hosted on Neon) and returns insights using metadata.  

## Prerequisites  
- Python 3.10+  
- `pip` installed  

## Project Files  
- `server.py` – Runs the TCP server that processes queries and pulls data from Neon PostgreSQL.
- `client.py` – Command-line client that connects to the server and sends queries.  

## Database Details (Neon PostgreSQL)  
All database credentials are defined in the DB_CONFIG section of server.py.  
- Open your project dashboard in Neon and click 'Connect'  
- Find your connection string: postgresql://<user>:<password>@<host>/neondb?sslmode=require  
- Replace `user`, `password`, and `host` in server.py with your own credentials from your connection string  
- dbname: neondb  
- port: 5432  

Tables:  
- Data_virtual: stores incoming JSON payloads from smart devices  
- Data_metadata: stores metadata about devices  

## Step 1: Intall Required Packages  
`pip install psycopg2-binary pytz`  

## Step 2: Set up Server
- Open a terminal on the server machine and navigate to the project folder.  
- Run the server: `python server.py`
- Enter the IP address and port when prompted.  
- The server will start listening for client connections.

## Step 3: Run the Client  
- Open a terminal on the client machine and navigate to the project folder.  
- Run the client: `python client.py`  
- Enter the IP of the server and port number.  
- When prompted, select a query to run:  
  1. What is the average moisture inside my kitchen fridge in the past three hours?  
  2. What is the average water consumption per cycle in my smart dishwasher?  
  3. Which device consumed more electricity among my three IoT devices?
- Type 'q' to quit the program.
