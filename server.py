# import socket
# import psycopg2
# import uuid

# # Dictionary to store session information
# sessions = {}

# def authenticate_user(username, password):
#     try:
#         conn = psycopg2.connect(
#             dbname="postgres",
#             user="postgres",
#             password="2004",
#             host="localhost",
#             port="5432"
#         )
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
#         user = cursor.fetchone()
#         conn.close()
#         return user is not None
#     except psycopg2.Error as e:
#         print("Error connecting to database:", e)
#         return False

# def handle_request(client_socket, request):
#     try:
#         if request.startswith("GET /login"):
#             with open("login.html", "r") as file:
#                 login_page = file.read()
#             response = "HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: {}\n\n{}".format(len(login_page), login_page)
#             client_socket.sendall(response.encode())
#         elif request.startswith("GET /signup"):
#             with open("signup.html", "r") as file:
#                 signup = file.read()
#             response = "HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: {}\n\n{}".format(len(signup), signup)
#             client_socket.sendall(response.encode())

#         elif request.startswith("POST /login"):
#             form_data = request.split("\n")[-1]
#             form_items = form_data.split('&')
#             username = form_items[0].split('=')[1]
#             password = form_items[1].split('=')[1]
#             if authenticate_user(username, password):
#                 # Generate session ID
#                 session_id = str(uuid.uuid4())
#                 # Store session ID in sessions dictionary
#                 sessions[session_id] = username
#                 # Redirect to budget page
#                 with open("budget.html", "r") as file:
#                     other_page = file.read()
#                 response = "HTTP/1.1 302 Found\nLocation: /budget\nSet-Cookie: session_id={}\n\n".format(session_id)
#                 client_socket.sendall(response.encode())
#             else:
#                 client_socket.sendall("HTTP/1.1 401 Unauthorized\n\n".encode())

#         elif request.startswith("GET /budget"):
#             # Check if session ID exists in cookie
#             if "Cookie" in request:
#                 cookies = request.split("Cookie: ")[1]
#                 session_id = cookies.split("=")[1].split("\r\n")[0]
#                 # Check if session ID exists in sessions dictionary
#                 if session_id in sessions:
#                     with open("budget.html", "r") as file:
#                         other_page = file.read()
#                     response = "HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: {}\n\n{}".format(len(other_page), other_page)
#                     client_socket.sendall(response.encode())
#                 else:
#                     client_socket.sendall("HTTP/1.1 401 Unauthorized\n\n".encode())
#             else:
#                 client_socket.sendall("HTTP/1.1 401 Unauthorized\n\n".encode())

#         elif request.startswith("POST /register"):
#             form_data = request.split("\n")[-1]
#             form_items = form_data.split('&')
#             username = form_items[0].split('=')[1]
#             password = form_items[1].split('=')[1]

#             insert_user(username, password)

#             signup_success_page = "<html><body><h1>Signup Successful</h1></body></html>"
#             response = "HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: {}\n\n{}".format(len(signup_success_page), signup_success_page)
#             client_socket.sendall(response.encode())

#     except Exception as e:
#         print("Error handling request:", e)
#         client_socket.sendall("HTTP/1.1 500 Internal Server Error\n\n".encode())

# def create_table():
#     try:
#         conn = psycopg2.connect(
#             dbname="postgres",
#             user="postgres",
#             password="2004",
#             host="localhost",
#             port="5432"
#         )
#         cursor = conn.cursor()
#         cursor.execute('''CREATE TABLE IF NOT EXISTS users
#                         (id SERIAL PRIMARY KEY,
#                         username TEXT,
#                         password TEXT)''')
#         conn.commit()
#         conn.close()
#     except psycopg2.Error as e:
#         print("Error creating table:", e)

# def insert_user(username, password):
#     try:
#         conn = psycopg2.connect(
#             dbname="postgres",
#             user="postgres",
#             password="2004",
#             host="localhost",
#             port="5432"
#         )
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username,  password))
#         conn.commit()
#         print("User inserted successfully.")
#         conn.close()
#     except psycopg2.Error as e:
#         print("Error inserting user:", e)

# def start_server(host, port):
#     try:
#         server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         server_socket.bind((host, port))
#         server_socket.listen(5)

#         print("Server listening on {}:{}".format(host, port))

#         create_table()  # Create database table

#         while True:
#             client_socket, client_address = server_socket.accept()
#             print("Connection from:", client_address)
#             request_data = client_socket.recv(1024).decode()
#             print("Request:", request_data)
#             handle_request(client_socket, request_data)
#             client_socket.close()
#     except Exception as e:
#         print("Error starting server:", e)

# if __name__ == "__main__":
#     start_server('localhost', 8015)
import socket
import psycopg2
import uuid

# Dictionary to store session information
sessions = {}

def authenticate_user(username, password):
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="2004",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        conn.close()
        return user is not None
    except psycopg2.Error as e:
        print("Error connecting to database:", e)
        return False

def insert_transaction(username, transaction_type, name, amount):
    print(username, transaction_type, name, amount)
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="2004",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transactions (username, transaction_type, name, amount) VALUES (%s, %s, %s, %s)", (username, transaction_type, name, amount))
        conn.commit()
        print("Transaction inserted successfully.")
        conn.close()
    except psycopg2.Error as e:
        print("Error inserting transaction:", e)

def handle_request(client_socket, request):
    try:
        if request.startswith("GET /login"):
            with open("login.html", "r") as file:
                login_page = file.read()
            response = "HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: {}\n\n{}".format(len(login_page), login_page)
            client_socket.sendall(response.encode())
        elif request.startswith("GET /signup"):
            with open("signup.html", "r") as file:
                signup = file.read()
            response = "HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: {}\n\n{}".format(len(signup), signup)
            client_socket.sendall(response.encode())

        elif request.startswith("POST /login"):
            form_data = request.split("\n")[-1]
            form_items = form_data.split('&')
            username = form_items[0].split('=')[1]
            password = form_items[1].split('=')[1]
            if authenticate_user(username, password):
                # Generate session ID
                session_id = str(uuid.uuid4())
                # Store session ID in sessions dictionary
                sessions[session_id] = username
                # Redirect to budget page
                with open("budget.html", "r") as file:
                    other_page = file.read()
                response = "HTTP/1.1 302 Found\nLocation: /budget\nSet-Cookie: session_id={}\n\n".format(session_id)
                client_socket.sendall(response.encode())
            else:
                client_socket.sendall("HTTP/1.1 401 Unauthorized\n\n".encode())

        elif request.startswith("GET /budget"):
            # Check if session ID exists in cookie
            if "Cookie" in request:
                cookies = request.split("Cookie: ")[1]
                session_id = cookies.split("=")[1].split("\r\n")[0]
                # Check if session ID exists in sessions dictionary
                if session_id in sessions:
                    with open("budget.html", "r") as file:
                        other_page = file.read()
                    response = "HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: {}\n\n{}".format(len(other_page), other_page)
                    client_socket.sendall(response.encode())
                else:
                    client_socket.sendall("HTTP/1.1 401 Unauthorized\n\n".encode())
            else:
                client_socket.sendall("HTTP/1.1 401 Unauthorized\n\n".encode())

        elif request.startswith("POST /register"):
            form_data = request.split("\n")[-1]
            form_items = form_data.split('&')
            username = form_items[0].split('=')[1]
            password = form_items[1].split('=')[1]

            insert_user(username, password)

            signup_success_page = "<html><body><h1>Signup Successful</h1></body></html>"
            response = "HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: {}\n\n{}".format(len(signup_success_page), signup_success_page)
            client_socket.sendall(response.encode())

        elif request.startswith("POST /transaction"):
            form_data = request.split("\n")[-1]
            form_items = form_data.split('&')
            session_id = form_items[0].split('=')[1]
            transaction_type = form_items[1].split('=')[1]
            name = form_items[2].split('=')[1]
            amount = form_items[3].split('=')[1]
            insert_transaction(username, transaction_type, name, amount)
            if session_id in sessions:
                username = sessions[session_id]
              
               
                response = "HTTP/1.1 200 OK\nContent-Type: text/plain\n\nTransaction completed successfully."
                client_socket.sendall(response.encode())
            else:
                client_socket.sendall("HTTP/1.1 401 Unauthorized\n\n".encode())

    except Exception as e:
        print("Error handling request:", e)
        client_socket.sendall("HTTP/1.1 500 Internal Server Error\n\n".encode())

def create_table():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="2004",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                        (id SERIAL PRIMARY KEY,
                        username TEXT,
                        password TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions
                        (id SERIAL PRIMARY KEY,
                        username TEXT,
                        transaction_type TEXT,
                        name TEXT,
                        amount FLOAT)''')
        conn.commit()
        conn.close()
    except psycopg2.Error as e:
        print("Error creating table:", e)

def insert_user(username, password):
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="2004",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username,  password))
        conn.commit()
        print("User inserted successfully.")
        conn.close()
    except psycopg2.Error as e:
        print("Error inserting user:", e)

def start_server(host, port):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)

        print("Server listening on {}:{}".format(host, port))

        create_table()  # Create database table

        while True:
            client_socket, client_address = server_socket.accept()
            print("Connection from:", client_address)
            request_data = client_socket.recv(1024).decode()
            print("Request:", request_data)
            handle_request(client_socket, request_data)
            client_socket.close()
    except Exception as e:
        print("Error starting server:", e)

if __name__ == "__main__":
    start_server('localhost', 8015)
