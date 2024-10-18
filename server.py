import socket
import threading
import queue

# Queue untuk menyimpan pesan
messages = queue.Queue()
clients = {}  # Menyimpan alamat IP client dan nama mereka

# Membuat socket server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_ip = "10.8.107.141"  # IP address server
server_port = 9999         # Port server
server.bind((server_ip, server_port))

PASSWORD = "chatroom123"  # Password untuk memasuki chatroom

def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            decoded_message = message.decode()
            
            # Mengecek password pada pesan pertama
            if addr not in clients:
                if decoded_message.startswith(f"PASSWORD:{PASSWORD}"):
                    # Minta nama client
                    server.sendto("Masukkan nama Anda: ".encode(), addr)
                    name, _ = server.recvfrom(1024)
                    name = name.decode()
                    
                    # Periksa keunikan nama
                    while name in [client[1] for client in clients.values()]:
                        server.sendto("Nama sudah digunakan, silakan masukkan nama lain: ".encode(), addr)
                        name, _ = server.recvfrom(1024)
                        name = name.decode()

                    clients[addr] = (True, name)
                    server.sendto(f"Berhasil bergabung dengan chatroom, {name}.".encode(), addr)
                else:
                    server.sendto(f"Password salah. Koneksi ditolak.".encode(), addr)
                    continue
            else:
                messages.put((decoded_message, addr))
        except Exception as e:
            print(f"Error: {e}")

def broadcast():
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

# Mulai thread untuk menerima pesan
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()

print(f"Server running on {server_ip}:{server_port}")
