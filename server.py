from communication.client_connection_handler import ClientConnectionHandler
from communication.tcp_server_listener import TcpServerListener
from services.chat_broadcast_service import ChatBroadcastService
from threads.server_client_thread import ServerClientThread


class ServerApplication:

    def __init__(self):
        self.chat_broadcast_service = ChatBroadcastService()

    def start(self):
        server_socket = TcpServerListener().create_server_socket()
        print("Servidor iniciado")
        while True:
            (client_socket, client_address) = server_socket.accept()
            connection_handler = ClientConnectionHandler(client_socket)
            ServerClientThread(connection_handler, self.chat_broadcast_service).start()


if __name__ == "__main__":
    ServerApplication().start()
