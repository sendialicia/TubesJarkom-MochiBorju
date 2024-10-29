import socket
import threading
import queue

# Queue untuk menyimpan pesan
messages = queue.Queue()
clients = {}  # Menyimpan alamat IP client dan nama mereka

# Membuat socket server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_ip = "0.0.0.0"  # IP address server
server_port = 9999  # Port server
server.bind((server_ip, server_port))

# Password untuk memasuki chatroom
correct_password = "chatroom123"  

def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            decoded_message = message.decode()
            
            # Mengecek apakah client sudah terdaftar
            if addr not in clients:
                # Cek apakah client mengirimkan password langsung
                if decoded_message.strip() == correct_password:
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
                    for client in clients:
                        server.sendto(f"{name} joined!".encode(), client)
                    print(f"{name} joined!")
                else:
                    server.sendto("Password salah, silakan coba lagi.".encode(), addr)
            else:
                # Tambahkan nama pengirim ke pesan sebelum memasukkan ke queue
                sender_name = clients[addr][1]
                messages.put((f"{sender_name}: {decoded_message}", addr))
        except Exception as e:
            print(f"Error: {e}")

def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            print(message)  # Debug: Cetak pesan di server agar kita tahu formatnya benar

            # Kirim pesan ke semua client
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
