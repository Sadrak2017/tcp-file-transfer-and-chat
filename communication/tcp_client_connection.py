import socket


class TcpClientConnection:

    @staticmethod
    def connect_to_server(host: str, port: int):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        return client_socket
