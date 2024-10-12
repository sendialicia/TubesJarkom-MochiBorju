import socket
import threading
import random

# Mengganti localhost dengan IP address server
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("192.168.10.231", random.randint(8000, 9000)))  # Sesuaikan IP di sini
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
client.sendto(f"SIGNUP_TAG:{name}".encode(), ("192.168.10.231", 9999))  # Sesuaikan IP di sini

while True:
    message = input("")
    if message == "!q":
        exit()
    else:
        client.sendto(f"{name}: {message}".encode(), ("192.168.10.231", 9999))  # Sesuaikan IP di sini
