import threading


class ChatBroadcastService:

    def __init__(self):
        self.connected_clients = []
        self.lock = threading.Lock()

    def register_connected_client(self, connected_client):
        with self.lock:
            self.connected_clients.append(connected_client)

    def unregister_connected_client(self, connected_client):
        with self.lock:
            if connected_client in self.connected_clients:
                self.connected_clients.remove(connected_client)

    def get_connected_clients(self):
        with self.lock:
            return list(self.connected_clients)

    def broadcast_message(self, protocol_header, payload: bytes):
        disconnected_clients = []
        with self.lock:
            for connected_client in self.connected_clients:
                try:
                    connected_client.send_message(protocol_header, payload)
                except Exception:
                    disconnected_clients.append(connected_client)
            for disconnected_client in disconnected_clients:
                self.connected_clients.remove(disconnected_client)
