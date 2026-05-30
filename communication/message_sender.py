from protocol.protocol_header import ProtocolHeader
from protocol.protocol_message_builder import ProtocolMessageBuilder


class MessageSender:

    def __init__(self):
        self.protocol_message_builder = ProtocolMessageBuilder()

    def send_message(self, socket_connection, protocol_header: ProtocolHeader, payload: bytes = b""):
        message = self.protocol_message_builder.build_message(protocol_header, payload)
        socket_connection.sendall(message)