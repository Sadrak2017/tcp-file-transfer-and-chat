from protocol.protocol_message_parser import ProtocolMessageParser
from utils.socket_stream_reader import SocketStreamReader


class MessageReceiver:

    def __init__(self):
        self.socket_stream_reader = SocketStreamReader()
        self.protocol_message_parser = ProtocolMessageParser()

    def receive_message(self, socket_connection):
        header_size_bytes = self.socket_stream_reader.read_exactly(socket_connection, 4)
        header_size = int.from_bytes(header_size_bytes, byteorder="big")
        header_bytes = self.socket_stream_reader.read_exactly(socket_connection, header_size)
        protocol_header = self.protocol_message_parser.parse_header_bytes(header_bytes)
        payload_size = protocol_header.payload_size
        payload = b""
        if payload_size > 0:
            payload = self.socket_stream_reader.read_exactly(socket_connection, payload_size)
        return protocol_header, payload