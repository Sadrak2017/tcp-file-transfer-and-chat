from communication.client_connection_handler import ClientConnectionHandler
from communication.tcp_client_connection import TcpClientConnection
from configuration.network_configuration import NetworkConfiguration
from threads.client_keyboard_thread import ClientKeyboardThread
from threads.client_socket_listener_thread import ClientSocketListenerThread


class ClientApplication:

    @staticmethod
    def start():
        socket_connection = TcpClientConnection().connect_to_server(
            NetworkConfiguration.CLIENT_HOST,
            NetworkConfiguration.SERVER_PORT
        )
        connection_handler = ClientConnectionHandler(socket_connection)
        ClientSocketListenerThread(connection_handler).start()
        keyboard_thread = ClientKeyboardThread(connection_handler)
        keyboard_thread.start()
        keyboard_thread.join()


if __name__ == "__main__":
    ClientApplication().start()
