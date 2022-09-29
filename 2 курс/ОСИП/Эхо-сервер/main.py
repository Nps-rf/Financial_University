import socket

HOST = "localhost"
PORT = 33333

with socket.socket() as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, ip = s.accept()
    with conn:
        print(f">>> Connected by {':'.join(map(str, ip))}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
