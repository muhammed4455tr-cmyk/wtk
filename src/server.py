import json
import socket
import threading

HOST = "0.0.0.0"
PORT = 5055

clients = []
states = {}
lock = threading.Lock()


def handle_client(conn, addr):
    name = f"player_{addr[1]}"
    with lock:
        clients.append(conn)
    try:
        buf = b""
        while True:
            data = conn.recv(4096)
            if not data:
                break
            buf += data
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                try:
                    msg = json.loads(line.decode("utf-8"))
                    name = msg.get("name", name)
                    with lock:
                        states[name] = {"x": msg.get("x", 100), "y": msg.get("y", 100)}
                        payload = (json.dumps(states) + "\n").encode("utf-8")
                        for c in clients[:]:
                            try:
                                c.sendall(payload)
                            except OSError:
                                clients.remove(c)
                except json.JSONDecodeError:
                    pass
    finally:
        with lock:
            if conn in clients:
                clients.remove(conn)
            if name in states:
                del states[name]
        conn.close()


def main():
    print(f"Server basladi: {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            print("Baglanti:", addr)
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
