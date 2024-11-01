import socket
import threading
import queue
import argparse

# Queue untuk menyimpan pesan
messages = queue.Queue()
clients = {}  # Menyimpan alamat IP client dan nama mereka

# Password untuk memasuki chatroom
correct_password = "chatroom123"

def receive(server):
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

                    # Daftarkan client dengan informasi IP, port, dan nama
                    clients[addr] = (True, name)
                    server.sendto(f"Berhasil bergabung dengan chatroom, {name}.".encode(), addr)

                    # Kirim notifikasi ke semua client tentang client baru
                    for client in clients:
                        server.sendto(f"{name} joined!".encode(), client)

                    print(f"Client baru terhubung - IP: {addr[0]}, Port: {addr[1]}, Username: {name}")
                else:
                    server.sendto("Password salah, silakan coba lagi.".encode(), addr)
            else:
                # Periksa apakah pesan adalah perintah keluar
                if decoded_message == "FIN":
                    server.sendto("ACK".encode(), addr)
                    print(f"{clients[addr][1]} telah keluar dari chatroom.")
                    # Kirim FIN ke client setelah semua pesan diproses
                    server.sendto("FIN".encode(), addr)
                    # Hapus client dari daftar clients
                    del clients[addr]
                    # Kirim pemberitahuan ke semua client yang tersisa
                    for client in clients:
                        server.sendto(f"{clients[addr][1]} left the chat.".encode(), client)
                else:
                    # Tambahkan nama pengirim ke pesan sebelum memasukkan ke queue
                    sender_name = clients[addr][1]
                    messages.put((f"{sender_name}: {decoded_message}", addr))
        except Exception as e:
            print(f"Error: {e}")

def broadcast(server):
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

def main():
    parser = argparse.ArgumentParser(description="Server Chatroom")
    parser.add_argument('--port', type=int, required=True, help='Port server')
    args = parser.parse_args()

    # Membuat socket server
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_ip = "0.0.0.0"
    server.bind((server_ip, args.port))

    print(f"Server running on {server_ip}:{args.port}")

    # Mulai thread untuk menerima pesan
    t1 = threading.Thread(target=receive, args=(server,))
    t2 = threading.Thread(target=broadcast, args=(server,))

    t1.start()
    t2.start()

if __name__ == "__main__":
    main()
