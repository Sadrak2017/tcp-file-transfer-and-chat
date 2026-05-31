import socket
from configuration.network_configuration import NetworkConfiguration


class TcpServerListener:

    @staticmethod
    def create_server_socket():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((NetworkConfiguration.SERVER_HOST, NetworkConfiguration.SERVER_PORT))
        server_socket.listen(NetworkConfiguration.SOCKET_BACKLOG)
        return server_socket
