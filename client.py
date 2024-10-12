import socket
import threading
import random

# Meminta pengguna memasukkan IP, Port server, dan password
server_ip = input("Masukkan IP Server: ")
server_port = int(input("Masukkan Port Server: "))
password = input("Masukkan Password: ")

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("localhost", random.randint(8000, 9000)))  # Bind menggunakan localhost
name = input("Nickname: ")

def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except Exception as e:
            print(f"Kesalahan saat menerima pesan: {e}")

t = threading.Thread(target=receive)
t.start()

# Mengirim tanda pendaftaran dengan password
try:
    client.sendto(f"SIGNUP_TAG:{name}:{password}".encode(), (server_ip, server_port))  # Kirim dengan password
except Exception as e:
    print(f"Gagal mengirim tanda pendaftaran: {e}")

while True:
    message = input("")
    if message == "!q":
        exit()
    else:
        try:
            client.sendto(f"{name}: {message}".encode(), (server_ip, server_port))  # Kirim pesan ke server
        except Exception as e:
            print(f"Gagal mengirim pesan: {e}. Pastikan IP dan port server benar.")
