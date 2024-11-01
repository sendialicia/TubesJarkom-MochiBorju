import socket
import threading
import queue
import argparse
import os

# Queue untuk menyimpan pesan
messages = queue.Queue()
clients = {}  # Menyimpan alamat IP client dan nama mereka
user_data_file = "user_data.txt"

# Password untuk memasuki chatroom
correct_password = "1"

# Fungsi untuk memuat data pengguna dari file
def load_user_data():
    if not os.path.exists(user_data_file):
        return {}
    with open(user_data_file, "r") as file:
        users = {}
        for line in file:
            if "," in line:
                username, password = line.strip().split(',', 1)
                users[username] = password
        return users

# Fungsi untuk menyimpan data pengguna ke file
def save_user_data(username, password):
    with open(user_data_file, "a") as file:
        file.write(f"{username},{password}\n")

# Fungsi untuk menerima koneksi dari client
def receive(server):
    user_data = load_user_data()
    while True:
        try:
            message, addr = server.recvfrom(1024)
            decoded_message = message.decode()

            # Memeriksa apakah client sudah terdaftar di chatroom
            if addr not in clients:
                if decoded_message == correct_password:
                    server.sendto("Welcome to the chatroom! Choose option:\n1. Login\n2. Register".encode(), addr)
                    option, _ = server.recvfrom(1024)
                    option = option.decode()

                    if option == '1':  # Login
                        server.sendto("Enter username:".encode(), addr)
                        username, _ = server.recvfrom(1024)
                        username = username.decode()

                        server.sendto("Enter password:".encode(), addr)
                        password, _ = server.recvfrom(1024)
                        password = password.decode()

                        # Validasi login
                        if username in user_data and user_data[username] == password:
                            clients[addr] = (True, username)
                            print(f"User {username} connected from {addr[0]}:{addr[1]}")
                            server.sendto(f"Login succeeded! Welcome to the chatroom, {username}!".encode(), addr)
                            server.sendto(f"If you would like to get out of the chatroom, type '!q'".encode(), addr)
                            for client in clients:
                                server.sendto(f"{username} joined the chatroom!".encode(), client)
                        else:
                            server.sendto("Username or password is wrong! Enter the chatroom password to go back".encode(), addr)

                    elif option == '2':  # Register
                        server.sendto("Enter new username:".encode(), addr)
                        username, _ = server.recvfrom(1024)
                        username = username.decode()

                        server.sendto("Enter password:".encode(), addr)
                        password, _ = server.recvfrom(1024)
                        password = password.decode()

                        # Simpan data pengguna baru
                        if username not in user_data:
                            user_data[username] = password
                            save_user_data(username, password)
                            clients[addr] = (True, username)
                            print(f"User {username} connected from {addr[0]}:{addr[1]} (new registration)")
                            server.sendto(f"Registration succeeded! Welcome to the chatroom, {username}!".encode(), addr)
                            server.sendto(f"If you would like to get out of the chatroom, type '!q'".encode(), addr)
                            for client in clients:
                                server.sendto(f"{username} joined the chatroom!".encode(), client)
                        else:
                            server.sendto("Username is not available :(, Enter the chatroom password to go back".encode(), addr)
                    else:
                        server.sendto("Option is not valid, Enter the chatroom password to go back".encode(), addr)
                else:
                    server.sendto("Password is wrong.".encode(), addr)
            else:
                sender_name = clients[addr][1]
                if decoded_message == "!q":
                    del clients[addr]
                    for client in clients:
                        server.sendto(f"{sender_name} has left the chatroom.".encode(), client)
                    print(f"{sender_name} has left the chatroom.")
                else:
                    messages.put((f"{sender_name}: {decoded_message}", addr))
        except (socket.error, OSError) as e:
            # Handle socket closure gracefully
            print(f"Connection with {addr} has been closed.")
            if addr in clients:
                del clients[addr]  # Remove client from the list
            break  # Exit the loop if an error occurs

# Fungsi untuk menyiarkan pesan ke semua client
def broadcast(server):
    while True:
        while not messages.empty():
            message, addr = messages.get()
            print(message)
            for client in clients:
                try:
                    server.sendto(message.encode(), client)
                except Exception as e:
                    print(f"Error sending to client {client}: {e}")
                    clients.pop(client)

# Fungsi utama server
def main():
    parser = argparse.ArgumentParser(description="Server Chatroom")
    parser.add_argument('--port', type=int, required=True, help='Port server')
    args = parser.parse_args()

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_ip = "0.0.0.0"
    server.bind((server_ip, args.port))

    print(f"Server running on {server_ip}:{args.port}")

    t1 = threading.Thread(target=receive, args=(server,))
    t2 = threading.Thread(target=broadcast, args=(server,))

    t1.start()
    t2.start()

if __name__ == "__main__":
    main()
