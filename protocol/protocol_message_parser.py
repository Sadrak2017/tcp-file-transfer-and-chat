import json
from protocol.protocol_header import ProtocolHeader


class ProtocolMessageParser:

    @staticmethod
    def parse_header_bytes(header_bytes: bytes) -> ProtocolHeader:
        header_dictionary = json.loads(header_bytes.decode("utf-8"))

        return ProtocolHeader(
            command=header_dictionary.get("command", ""),
            payload_size=header_dictionary.get("payload_size", 0),
            filename=header_dictionary.get("filename", ""),
            filesize=header_dictionary.get("filesize", 0),
            sha256=header_dictionary.get("sha256", "")
        )
