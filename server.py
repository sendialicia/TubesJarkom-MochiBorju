import socket
import threading
import queue
import argparse

# Queue for storing messages
messages = queue.Queue()
clients = {}  # Stores IP and name of each client
correct_password = "chatroom123"

def receive(server):
    while True:
        try:
            message, addr = server.recvfrom(1024)
            decoded_message = message.decode()

            # Handshake initiation
            if addr not in clients:
                # Step 1: SYN received from client
                if decoded_message.startswith("SYN"):
                    client_seq = int(decoded_message.split()[1])
                    server_seq = client_seq + 1
                    server.sendto(f"SYN-ACK {server_seq} {client_seq + 1}".encode(), addr)
                    print(f"Received SYN from {addr} with seq {client_seq}. Sent SYN-ACK with seq {server_seq}.")

                # Step 2: ACK received from client, complete handshake
                elif decoded_message.startswith("ACK"):
                    clients[addr] = None  # Temporarily register client without a name
                    print(f"Handshake complete with client {addr}. Awaiting password.")

                    # Prompt for password right after handshake
                    server.sendto("Enter password: ".encode(), addr)
                
                # Step 3: Password verification and username prompt
                elif decoded_message == correct_password and clients[addr] is None:
                    server.sendto("Masukkan nama Anda: ".encode(), addr)
                    name, _ = server.recvfrom(1024)
                    name = name.decode()
                    
                    # Check name uniqueness
                    while name in [client[1] for client in clients.values() if client]:
                        server.sendto("Nama sudah digunakan, silakan masukkan nama lain: ".encode(), addr)
                        name, _ = server.recvfrom(1024)
                        name = name.decode()

                    # Register client with IP, port, and name
                    clients[addr] = name
                    server.sendto(f"Berhasil bergabung dengan chatroom, {name}.".encode(), addr)
                    
                    # Notify all clients about the new joiner
                    for client in clients:
                        server.sendto(f"{name} joined!".encode(), client)
                    print(f"New client connected - IP: {addr[0]}, Port: {addr[1]}, Username: {name}")

                else:
                    server.sendto("Password salah, silakan coba lagi.".encode(), addr)
            else:
                # Process chat messages and FIN command
                if decoded_message == "FIN":
                    server.sendto("ACK".encode(), addr)
                    name = clients.pop(addr)
                    print(f"{name} has left the chatroom.")
                    
                    # Notify remaining clients
                    for client in clients:
                        server.sendto(f"{name} left the chat.".encode(), client)
                else:
                    sender_name = clients[addr]
                    messages.put((f"{sender_name}: {decoded_message}", addr))
        except Exception as e:
            print(f"Error: {e}")

def broadcast(server):
    while True:
        while not messages.empty():
            message, addr = messages.get()
            print(message)  # Print message on server side for debugging

            # Send message to all clients
            for client in clients:
                try:
                    server.sendto(message.encode(), client)
                except Exception as e:
                    print(f"Error sending to client {client}: {e}")
                    clients.pop(client)

def main():
    parser = argparse.ArgumentParser(description="Server Chatroom")
    parser.add_argument('--port', type=int, required=True, help='Server port')
    args = parser.parse_args()

    # Create server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_ip = "0.0.0.0"
    server.bind((server_ip, args.port))

    print(f"Server running on {server_ip}:{args.port}")

    # Start threads for receiving and broadcasting messages
    t1 = threading.Thread(target=receive, args=(server,))
    t2 = threading.Thread(target=broadcast, args=(server,))
    t1.start()
    t2.start()

if __name__ == "__main__":
    main()
