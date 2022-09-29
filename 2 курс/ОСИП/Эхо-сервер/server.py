import socket

HOST = "localhost"
PORT = 33333

with socket.socket() as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello, world!")
    data = s.recv(1024)

print(f">>> Received {data!r}")