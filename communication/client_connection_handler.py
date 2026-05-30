from communication.message_sender import MessageSender
from communication.message_receiver import MessageReceiver


class ClientConnectionHandler:

    def __init__(self, socket_connection):
        self.socket_connection = socket_connection
        self.emissor = MessageSender()
        self.receptor = MessageReceiver()

    def send_message(self, protocol_header, payload=b""):
        self.emissor.send_message(self.socket_connection, protocol_header, payload)

    def receive_message(self):
        return self.receptor.receive_message(self.socket_connection)

    def close_connection(self):
        self.socket_connection.close()

    def get_socket_connection(self):
        return self.socket_connection
