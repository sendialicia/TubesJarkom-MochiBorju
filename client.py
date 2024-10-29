import socket
import threading
import random

# Membuat socket client
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Meminta input dari pengguna untuk IP address dan port server
server_ip = input("Masukkan IP address server: ")  # Pengguna memasukkan IP, misal 172.20.10.2
server_port = 9999  # Port yang digunakan tetap sama

# Memasukkan password
password = input("PASSWORD: ")

# Bind client ke IP address acak (berbeda) dengan range port
client.bind(("", random.randint(8000, 9000)))

# Fungsi untuk menerima pesan dari server
def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

# Mulai thread untuk menerima pesan
t = threading.Thread(target=receive)
t.start()

# Kirim password ke server
client.sendto(f"{password}".encode(), (server_ip, server_port))

# Kirim pesan ke server setelah bergabung
while True:
    message = input("")
    if message == "!q":
        exit()
    else:
        client.sendto(f"{message}".encode(), (server_ip, server_port))
