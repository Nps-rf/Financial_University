import socket
from time import sleep


# noinspection Assert
class Receiver:
    def __init__(self, host: str, port: int):
        assert isinstance(host, str)
        assert isinstance(port, int)

        self.host, self.port = host, port

    def receive(self, send_string: str = None, limit: int = 1024) -> bytes:
        assert isinstance(send_string, str)
        assert isinstance(limit, int)

        with socket.socket() as S:
            if send_string:
                S.sendall(send_string.encode())
            S.connect((self.host, self.port))
            return s.recv(limit)


HOST = "localhost"
PORT = 33333

R = Receiver(HOST, PORT)

while True:
    data = R.receive()

    print(f">>> Received {data!r}")
    sleep(2)


