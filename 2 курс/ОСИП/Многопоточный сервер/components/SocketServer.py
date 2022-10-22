import datetime
import socket


class SocketServer(socket.socket):
    def __init__(self, host: str, port: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._host, self._port = host, port

    def serve_forever(self):
        serve_statement = True

        self.bind((self._host, self._port))
        self.listen()

        while serve_statement:
            connection, address = self.accept()

            with connection:
                print('Connected from %s at %s' % (':'.join(map(str, address)), datetime.datetime.now().strftime(
                    '%H:%M:%S')))

                while 1:
                    data = connection.recv(16)

                    if not data:
                        break

                    if data.decode() == 'exit':
                        serve_statement = False

                    connection.sendall(data)