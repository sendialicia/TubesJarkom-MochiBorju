import socket
import threading
import queue

# Queue untuk menyimpan pesan
messages = queue.Queue()
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Mengatur IP dan Port server
server_ip = "172.20.10.2"  # Ubah sesuai dengan IP server
server_port = 9999  # Port server

server.bind((server_ip, server_port))
print(f"Server berjalan di {server_ip}:{server_port}")

# Password untuk masuk ke server
server_password = "password123"

def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
        except:
            pass

def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            decoded_message = message.decode()

            # Menangani signup dengan password
            if decoded_message.startswith("SIGNUP_TAG:"):
                name, password = decoded_message.split(":")[1:]
                if password == server_password:
                    if addr not in clients:
                        clients.append(addr)
                    for client in clients:
                        server.sendto(f"{name} joined!".encode(), client)
                    print(f"{name} berhasil masuk dengan IP {addr}")
                else:
                    server.sendto("Password salah!".encode(), addr)
                    print(f"User gagal masuk karena password salah: {addr}")
            else:
                print(decoded_message)
                for client in clients:
                    if client != addr:
                        server.sendto(message, client)

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()
