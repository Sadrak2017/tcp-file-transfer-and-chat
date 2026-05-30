import json
from protocol.protocol_header import ProtocolHeader


class ProtocolMessageBuilder:

    @staticmethod
    def build_header_bytes(protocol_header: ProtocolHeader) -> bytes:
        return json.dumps(protocol_header.to_dictionary()).encode("utf-8")

    @staticmethod
    def build_message(protocol_header: ProtocolHeader, payload: bytes = b"") -> bytes:
        header_bytes = ProtocolMessageBuilder.build_header_bytes(protocol_header)
        header_length = len(header_bytes)
        return (
                header_length.to_bytes(
                    4,
                    byteorder="big"
                )
                + header_bytes
                + payload
        )
