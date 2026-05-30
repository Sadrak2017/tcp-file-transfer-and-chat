class SocketStreamReader:

    @staticmethod
    def read_exactly(socket_connection, total_bytes: int) -> bytes:
        received_data = b""
        while len(received_data) < total_bytes:
            remaining_bytes = (total_bytes - len(received_data))
            chunk = socket_connection.recv(remaining_bytes)
            if not chunk:
                raise ConnectionError("Socket connection closed")
            received_data += chunk
        return received_data
