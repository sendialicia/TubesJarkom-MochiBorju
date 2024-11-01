import socket
import threading
import argparse
import random
import sys

# Membuat socket client
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Flag untuk menghentikan thread menerima
running = True

def receive(args):
    global running
    while running:
        try:
            message, _ = client.recvfrom(1024)
            decoded_message = message.decode()
            
            if decoded_message == "FIN":
                client.sendto("ACK".encode(), (args.ip, args.port))
                print("Anda telah keluar dari chatroom.")
                break  # Exit the loop when receiving FIN
                
            print(decoded_message)  # Handle other messages
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

    # Set running to False to ensure the main thread can exit
    running = False
    client.close()

def main():
    parser = argparse.ArgumentParser(description="Client Chatroom")
    parser.add_argument('--ip', type=str, required=True, help='IP address of the server')
    parser.add_argument('--port', type=int, required=True, help='Port of the server')
    args = parser.parse_args()

    # Bind client ke IP address acak (berbeda) dengan range port
    client.bind(("", random.randint(8000, 9000)))

    # Memasukkan password
    password = input("Masukkan Password untuk bergabung ke chatroom: ")
    client.sendto(f"{password}".encode(), (args.ip, args.port))

    # Mulai thread untuk menerima pesan
    t = threading.Thread(target=receive, args=(args,), daemon=True)
    t.start()

    # Kirim pesan ke server setelah bergabung
    while True:
        message = input("")
        if message == "!q":
            # Kirim pesan FIN ke server
            client.sendto("FIN".encode(), (args.ip, args.port))
            print("Menunggu konfirmasi dari server...")
            break  # Exit the loop after sending FIN
        else:
            client.sendto(f"{message}".encode(), (args.ip, args.port))

    # Wait for the receive thread to finish
    t.join()
    sys.exit()  # Exit the program

if __name__ == "__main__":
    main()
