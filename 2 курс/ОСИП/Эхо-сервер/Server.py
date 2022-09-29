import datetime
import socket


class Server(socket.socket):
    def __init__(self, __host: str, __port: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._host, self._port = __host, __port

    def serve_forever(self):
        serve_statement = True

        self.bind((self._host, self._port))
        self.listen()

        while serve_statement:
            connection, address = self.accept()

            with connection:
                print(
                    'Connected from %s at %s' % (
                        ':'.join(map(str, address)),
                        datetime.datetime.now().strftime('%H:%M:%S')
                    )
                )

                while 1:
                    data = connection.recv(16)

                    if not data:
                        break

                    if data.decode() == 'exit':
                        serve_statement = False

                    connection.sendall(data)


if __name__ == '__main__':
    HOST = "localhost"
    PORT = 33333

    server = Server(HOST, PORT)

    server.serve_forever()
