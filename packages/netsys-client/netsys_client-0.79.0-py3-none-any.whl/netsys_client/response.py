import socket

class Response:

    _host = 'localhost'
    _port = 12345
    _message = 0

    def __init__(self):

        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.connect((self._host, self._port))

    def send_message(self, message):

        self._client.sendall(str.encode(message))
        self._message = self._client.recv(4096).decode('utf-8')
        self._client.close()

    def get_message(self):

        return self._message

    