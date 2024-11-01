import socket
import threading
import argparse
import random
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
running = True

def receive(args):
    while True:
        try:
            message, _ = client.recvfrom(1024)
            if message.decode() == "FIN":
                client.sendto("ACK".encode(), (args.ip, args.port))
                print("You have exited the chatroom.")
                break

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
    args = parser.parse_args()

    client.bind(("", random.randint(8000, 9000)))
    
    # Begin handshake with SYN
    client_seq = random.randint(1000, 9999)
    client.sendto(f"SYN {client_seq}".encode(), (args.ip, args.port))
    print(f"Sent SYN with seq {client_seq}.")
    
    # Wait for SYN-ACK from server
    message, _ = client.recvfrom(1024)
    if message.decode().startswith("SYN-ACK"):
        server_seq, ack = map(int, message.decode().split()[1:])
        print(f"Received SYN-ACK with seq {server_seq}, ack {ack}.")
        
        # Complete handshake with ACK
        client.sendto(f"ACK {server_seq + 1}".encode(), (args.ip, args.port))
        print("Sent ACK to complete the handshake.")

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
    t = threading.Thread(target=receive, args=(args,), daemon=True)
    t.start()

    while True:
        message = input("")
        if message == "!q":
            client.sendto("FIN".encode(), (args.ip, args.port))
            print("You have left the chatroom, see you back soon :)")
            break
        else:
            client.sendto(f"{message}".encode(), (args.ip, args.port))
        sys.exit

if __name__ == "__main__":
    main()
