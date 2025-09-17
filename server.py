import socket
import threading
from config import TCP_IP, TCP_PORT, UDP_IP, UDP_PORT

clients = []

def broadcast_tcp(message, conn_to_exclude=None):
    for client in clients:
        if client != conn_to_exclude:
            try:
                client.sendall(message.encode())
            except:
                clients.remove(client)

def handle_client(conn, addr):
    print(f"[TCP] New connection from {addr}")
    while True:
        try:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            print(f"[TCP] Received from {addr}: {msg}")
            broadcast_tcp(f"{addr}: {msg}", conn)
        except:
            break
    print(f"[TCP] {addr} disconnected.")
    clients.remove(conn)
    conn.close()

def tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((TCP_IP, TCP_PORT))
    server.listen()
    print(f"[TCP] Server listening on {TCP_IP}:{TCP_PORT}")

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        threading.Thread(target=handle_client, args=(conn, addr)).start()

def udp_broadcaster():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"[UDP] Broadcasting to {UDP_IP}:{UDP_PORT}")
    while True:
        msg = input("[UDP] Broadcast message: ")
        udp_sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))

if __name__ == "__main__":
    threading.Thread(target=tcp_server).start()
    threading.Thread(target=udp_broadcaster).start()
