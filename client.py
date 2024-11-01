import socket
import threading
import argparse
import random
import sys

# Client socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
running = True

def receive(args):
    global running
    while running:
        try:
            message, _ = client.recvfrom(1024)
            decoded_message = message.decode()
            
            if decoded_message == "FIN":
                client.sendto("ACK".encode(), (args.ip, args.port))
                print("You have exited the chatroom.")
                break
                
            print(decoded_message)  # Handle other messages
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

    running = False
    client.close()

def main():
    parser = argparse.ArgumentParser(description="Client Chatroom")
    parser.add_argument('--ip', type=str, required=True, help='Server IP address')
    parser.add_argument('--port', type=int, required=True, help='Server port')
    args = parser.parse_args()

    # Bind client to a random port
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
    
    # Enter password and join chatroom
    password = input("Enter password to join chatroom: ")
    client.sendto(password.encode(), (args.ip, args.port))

    # Start a thread to receive messages
    t = threading.Thread(target=receive, args=(args,), daemon=True)
    t.start()

    # Send messages to server after joining
    while True:
        message = input("")
        if message == "!q":
            client.sendto("FIN".encode(), (args.ip, args.port))
            print("Waiting for confirmation from server...")
            break
        else:
            client.sendto(message.encode(), (args.ip, args.port))

    # Wait for the receive thread to finish
    t.join()
    sys.exit()

if __name__ == "__main__":
    main()
