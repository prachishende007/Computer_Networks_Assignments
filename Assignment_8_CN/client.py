import socket
import threading
from config import TCP_IP, TCP_PORT, UDP_IP, UDP_PORT

def receive_tcp(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg:
                print(f"\n[TCP] {msg}")
        except:
            print("[TCP] Connection closed.")
            break

def udp_listener():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind((UDP_IP, UDP_PORT))
    print(f"[UDP] Listening on {UDP_IP}:{UDP_PORT}")
    while True:
        msg, _ = udp_sock.recvfrom(1024)
        print(f"\n[UDP Broadcast] {msg.decode()}")

def tcp_sender(sock):
    while True:
        msg = input()
        try:
            sock.sendall(msg.encode())
        except:
            print("[TCP] Failed to send message.")
            break

def main():
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.connect((TCP_IP, TCP_PORT))
    print(f"[TCP] Connected to server at {TCP_IP}:{TCP_PORT}")

    threading.Thread(target=receive_tcp, args=(tcp_sock,), daemon=True).start()
    threading.Thread(target=udp_listener, daemon=True).start()
    tcp_sender(tcp_sock)

if __name__ == "__main__":
    main()
