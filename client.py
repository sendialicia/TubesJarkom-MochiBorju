import socket
import threading
import random

# Mengganti localhost dengan IP address server
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("0.0.0.0", random.randint(8000, 9000)))  # Sesuaikan IP di sini
name = input("Nickname: ")

def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except:
            pass

t = threading.Thread(target=receive)
t.start()

# Mengirim data ke server dengan IP address server
client.sendto(f"SIGNUP_TAG:{name}".encode(), ("172.20.10.2", 9999))  # Sesuaikan IP di sini

while True:
    message = input("")
    if message == "!q":
        exit()
    else:
        client.sendto(f"{name}: {message}".encode(), ("172.20.10.2", 9999))  # Sesuaikan IP di sini
