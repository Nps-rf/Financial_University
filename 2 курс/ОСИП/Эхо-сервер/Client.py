import socket
from time import sleep

HOST = "localhost"
PORT = 33333

while True:
    with socket.socket() as s:
        s.connect((HOST, PORT))
        s.sendall(b"Hello, world!")
        data = s.recv(1024)

    print(f">>> Received {data!r}")
    sleep(2)


