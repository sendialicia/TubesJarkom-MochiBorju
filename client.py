import socket
import threading
import argparse
import random

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
running = True

def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            if message.decode() == "ACK":
                print("You have exited the chatroom.")
                break  # Exit if we receive ACK

            print(message.decode())  # This will print received messages
        except Exception as e:
            print(f"Error receiving message: {e}")
            break
    global running
    running = False
    client.close()

def main():
    parser = argparse.ArgumentParser(description="Client Chatroom")
    parser.add_argument('--ip', type=str, required=True, help='IP address of the server')
    parser.add_argument('--port', type=int, required=True, help='Port of the server')
    global args
    args = parser.parse_args()

    client.bind(("", random.randint(8000, 9000)))

    # Prompt for the chatroom's password
    password = input("Enter the chatroom's password to join: ")
    client.sendto(f"{password}".encode(), (args.ip, args.port))

    # Wait for server's response after sending the password
    response, _ = client.recvfrom(1024)
    print(f"{response.decode()}")  # Debug print

    if "Welcome" in response.decode():
        option = input()
        client.sendto(option.encode(), (args.ip, args.port))

        # Start the receive thread
        t = threading.Thread(target=receive, daemon=True)
        t.start()

        while True:
            message = input("")
            if message == "!q":
                client.sendto("FIN".encode(), (args.ip, args.port))
                print("You have left the chatroom, see you back soon :)")
                break
            else:
                client.sendto(f"{message}".encode(), (args.ip, args.port))

if __name__ == "__main__":
    main()
